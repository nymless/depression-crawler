import logging
import os
from datetime import date

import psycopg2

log = logging.getLogger(__name__)


def get_db_connection() -> psycopg2.extensions.connection | None:
    """
    Create a connection to the PostgreSQL database.
    Uses environment variables for connection parameters.

    Returns:
        Connection object or None if connection failed
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        return conn
    except psycopg2.Error as e:
        log.exception("Database connection error", exc_info=e)
        return None


def create_tables(conn: psycopg2.extensions.connection) -> None:
    """
    Create all necessary tables if they don't exist.

    Args:
        conn: Database connection
    """
    try:
        with conn.cursor() as cur:
            with open("src/db/create_tables.sql", "r") as f:
                cur.execute(f.read())
        conn.commit()
    except (psycopg2.Error, IOError) as e:
        log.exception("Error creating tables", exc_info=e)
        conn.rollback()
        raise


def create_crawler_run(
    conn: psycopg2.extensions.connection,
    target_date: date,
    group_ids: list[int],
) -> int:
    """
    Create a new crawler run record and link it with groups.

    Args:
        conn: Database connection
        target_date: Target date for the crawler run
        group_ids: List of VK group IDs to analyze

    Returns:
        ID of the created run
    """
    try:
        with conn.cursor() as cur:
            # Create run record
            cur.execute(
                """
                INSERT INTO crawler_runs (target_date)
                VALUES (%s)
                RETURNING id
                """,
                (target_date,),
            )
            run_id = cur.fetchone()[0]

            # Link groups with the run
            for group_id in group_ids:
                try:
                    cur.execute(
                        """
                        INSERT INTO run_groups (run_id, group_id)
                        VALUES (%s, %s)
                        """,
                        (run_id, group_id),
                    )
                except psycopg2.errors.ForeignKeyViolation:
                    log.warning(
                        f"Group {group_id} not found in database, skipping"
                    )
                    continue

            conn.commit()
            return run_id
    except psycopg2.Error as e:
        log.exception("Error creating crawler run", exc_info=e)
        conn.rollback()
        raise


def add_group(
    conn: psycopg2.extensions.connection, group_id: int, name: str
) -> None:
    """
    Add a new group or update existing one.

    Args:
        conn: Database connection
        group_id: VK group ID
        name: Group name
    """
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO groups (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO UPDATE
                SET name = EXCLUDED.name
                """,
                (group_id, name),
            )
            conn.commit()
    except psycopg2.Error as e:
        log.exception(f"Error adding/updating group {group_id}", exc_info=e)
        conn.rollback()
        raise


def save_predictions(
    conn: psycopg2.extensions.connection,
    run_id: int,
    owner_id: int,
    post_id: int,
    vk_id: int,
    depression_prediction: bool,
) -> None:
    """
    Save a single prediction to the database.
    If a post with the same owner_id, post_id and vk_id already exists,
    the prediction will be skipped.

    Args:
        conn: Database connection
        run_id: ID of the crawler run
        owner_id: VK group ID
        post_id: VK post ID
        vk_id: VK comment ID
        depression_prediction: Prediction result (True/False)
    """
    try:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO depression_predictions 
                    (run_id, owner_id, post_id, vk_id, depression_prediction)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (run_id, owner_id, post_id, vk_id, depression_prediction),
                )
                conn.commit()
            except psycopg2.errors.UniqueViolation:
                log.debug(
                    f"Post {post_id} from group {owner_id} already exists, skip"
                )
                conn.rollback()
    except psycopg2.Error as e:
        log.exception("Error saving prediction", exc_info=e)
        conn.rollback()
        raise
