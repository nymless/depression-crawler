import logging
from datetime import date
from typing import List

from vk_data_collector import Collector

from src.config import settings
from src.crawler.collect_data import collect_data
from src.crawler.collect_groups import collect_groups
from src.crawler.database_handler.database_handler import DatabaseHandler
from src.crawler.exceptions.crawler_exceptions import CrawlerStopRequested
from src.crawler.predict_depression import predict_depression
from src.crawler.preprocess_data import preprocess_data
from src.crawler.preprocess_groups import preprocess_groups
from src.crawler.status_manager.status_manager import CrawlerStatusManager
from src.db.db import create_tables, get_db_connection

log = logging.getLogger(__name__)


class Crawler:
    """
    Crawler for collecting posts from VK.
    """

    def __init__(self, collector: Collector) -> None:
        self.collector = collector
        self.status_manager = CrawlerStatusManager()
        # Get base data directory from environment
        self.data_dir = settings.data_dir

        # Initialize database connection
        self.db_conn = get_db_connection()
        if not self.db_conn:
            log.exception("Crawler failed to connect to database")
            raise ValueError("Crawler failed to connect to database")

        # Create database tables if they don't exist
        try:
            create_tables(self.db_conn)
            log.info("Database tables checked/created successfully.")
        except Exception as e:
            log.exception(
                (
                    "Failed to create database tables "
                    "during Crawler initialization."
                ),
                exc_info=e,
            )
            raise

    def run_pipeline(self, group_names: List[str], target_date: str) -> None:
        """
        Run the complete data pipeline:
        1. Collect groups
        2. Preprocess groups
        3. Collect posts and comments
        4. Preprocess data
        5. Run inference
        6. Save all results to database

        Args:
            groups_names: List of VK group names to collect from
            target_date: Target date in YYYY-MM-DD format
        """
        try:
            self.status_manager.reset()

            # ------ STEP 1: Collect groups --------------------
            self.status_manager.set_state("collecting_groups")
            groups_files = collect_groups(
                group_names,
                target_date,
                self.data_dir,
                self.collector,
                self.status_manager,
            )

            # ------ STEP 2: Preprocess groups -----------------
            self.status_manager.set_state("preprocessing_groups")
            groups_data = preprocess_groups(groups_files)

            # ------ STEP 3: Collect posts and comments ------
            self.status_manager.set_state("collecting_data")
            posts_files, comments_files = collect_data(
                group_names,
                target_date,
                self.data_dir,
                self.collector,
                self.status_manager,
            )

            # ------ STEP 4: Preprocess data -------------------
            self.status_manager.set_state("preprocessing")
            data = preprocess_data(posts_files, comments_files)
            if data is None or data.empty:
                log.info(
                    (
                        "No data to process after preprocessing. "
                        "Stopping pipeline."
                    )
                )
                self.status_manager.set_state("idle")
                self.status_manager.set_error("No data to process.")
                return None

            # ------ STEP 5: Run inference ---------------------
            self.status_manager.set_state("inference")
            predict_depression(data)

            # ------ STEP 6: Save all results to database ------
            self.status_manager.set_state("saving_results")

            # Initialize database handler
            db_handler = DatabaseHandler(
                conn=self.db_conn,
                group_ids=groups_data["id"].tolist(),
                target_date=date.fromisoformat(target_date),
            )

            # Start transaction
            try:
                # Save groups
                for _, row in groups_data.iterrows():
                    db_handler.add_group(
                        group_id=row["id"],
                        name=row["name"],
                        screen_name=row["screen_name"],
                        is_closed=row["is_closed"],
                        type=row["type"],
                    )

                # Create run record
                run_id = db_handler.save_run()

                # Save predictions
                for _, row in data.iterrows():
                    db_handler.save_prediction(
                        run_id=run_id,
                        owner_id=abs(row["owner_id"]),
                        post_id=row["post_id"],
                        vk_id=row["id"],
                        depression_prediction=bool(
                            row["depression_prediction"]
                        ),
                    )

                # Commit transaction
                self.db_conn.commit()
                log.info("Successfully saved all results to database")

            except Exception as e:
                # Rollback transaction on any error
                self.db_conn.rollback()
                log.error(
                    "Failed to save results to database, rolling back changes",
                    exc_info=e,
                )
                raise

            self.status_manager.reset()

        except CrawlerStopRequested as sr:
            log.exception("Crawler was stopped by user request", exc_info=sr)
            self.status_manager.set_state("idle")
            self.status_manager.set_error("Crawler was stopped by user request")

        except Exception as e:
            log.exception("Error during data pipeline processing", exc_info=e)
            self.status_manager.set_state("idle")
            self.status_manager.set_error(
                "Error during data pipeline processing"
            )
