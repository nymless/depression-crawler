import json
import logging
import os
from datetime import UTC, datetime
from typing import cast

import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

log = logging.getLogger(__name__)


class DAL:
    """Handles storing API requests and сollected posts in the database."""

    def __init__(self) -> None:
        self.conn = psycopg2.connect(DATABASE_URL)
        self.curr = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create tables for storing API requests and posts with a foreign
        key."""

        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                request_id  serial PRIMARY KEY,
                timestamp   text,
                endpoint    text,
                params      text,
                status_code integer
            );
            """
        )
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                post_id     serial PRIMARY KEY,
                request_id  integer,
                owner_type  text,
                owner_id    integer,
                post_vk_id  integer,
                text        text,
                likes       integer,
                reposts     integer,
                comments    integer,
                timestamp   timestamp,
                CONSTRAINT fk_request_id FOREIGN KEY (request_id)
                    REFERENCES requests(request_id)
                    ON DELETE SET NULL,
                CONSTRAINT unique_owner_post_id UNIQUE (owner_id, post_vk_id)
            );
            """
        )
        self.conn.commit()

    def save_request(
        self,
        endpoint: str,
        params: dict,
        status_code: int,
    ) -> int:
        """Log API request details in the requests table and return its ID."""
        self.curr.execute(
            """
            INSERT INTO requests (timestamp, endpoint, params, status_code) 
            VALUES (%s, %s, %s, %s)
            RETURNING request_id;
            """,
            (
                datetime.now(UTC).isoformat(),
                endpoint,
                json.dumps(params),
                status_code,
            ),
        )
        request_id = self.curr.fetchone()[0]
        self.conn.commit()
        return cast(int, request_id)

    def save_post(
        self,
        request_id: int,
        owner_type: str,
        owner_id: int,
        post_id: int,
        text: str,
        likes: int,
        reposts: int,
        comments: int,
        timestamp: str,
    ):
        """Save a collected post in the posts table, linking it to the
        request."""
        try:
            self.curr.execute(
                """
                INSERT INTO posts (
                    request_id,
                    owner_type,
                    owner_id,
                    post_vk_id,
                    text,
                    likes,
                    reposts,
                    comments,
                    timestamp) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    request_id,
                    owner_type,
                    owner_id,
                    post_id,
                    text,
                    likes,
                    reposts,
                    comments,
                    timestamp,
                ),
            )
        except psycopg2.errors.UniqueViolation:
            log.exception("Save post unique violation error")
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
