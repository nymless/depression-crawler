import logging
import os
from datetime import date
from typing import List

from vk_data_collector import Collector

from src.crawler.collect_data import collect_data
from src.crawler.collect_groups import collect_groups
from src.crawler.database_handler.database_handler import DatabaseHandler
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
        # Get base directory from environment
        self.base_dir = os.getenv("CRAWLER_DATA_DIR")
        if not self.base_dir:
            raise ValueError("CRAWLER_DATA_DIR environment variable is not set")
        # Ensure base_dir exist
        os.makedirs(self.base_dir, exist_ok=True)

        # Initialize database connection
        self.db_conn = get_db_connection()
        if not self.db_conn:
            raise ValueError("Failed to connect to database")

        # Create database tables if they don't exist
        try:
            create_tables(self.db_conn)
            log.info("Database tables checked/created successfully.")
        except Exception as e:
            log.exception(
                "Failed to create database tables during Crawler initialization.",
                exc_info=e,
            )
            raise

    def run_pipeline(self, group_names: List[str], target_date: str) -> None:
        """
        Run the complete data pipeline:
        1. Collect groups
        2. Preprocess groups
        3. Initialize run
        4. Collect posts
        5. Collect comments
        6. Preprocess data
        7. Run inference
        8. Save predictions

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
                self.base_dir,
                self.collector,
                self.status_manager,
            )

            # ------ STEP 2: Preprocess groups -----------------
            self.status_manager.set_state("preprocessing_groups")
            groups_data = preprocess_groups(groups_files)

            # ------ STEP 3: Initialize run --------------------
            self.status_manager.set_state("initializing")
            db_handler = DatabaseHandler(
                conn=self.db_conn,
                group_ids=groups_data["id"].tolist(),
                target_date=date.fromisoformat(target_date),
            )
            for _, row in groups_data.iterrows():  # Save groups
                db_handler.add_group(
                    group_id=row["id"],
                    name=row["name"],
                    screen_name=row["screen_name"],
                    is_closed=row["is_closed"],
                    type=row["type"],
                )
            run_id = db_handler.start_run()  # Create run record

            # ------ STEP 4-5: Collect posts and comments ------
            posts_files, comments_files = collect_data(
                group_names,
                target_date,
                self.base_dir,
                self.collector,
                self.status_manager,
            )

            # ------ STEP 6: Preprocess data -------------------
            self.status_manager.set_state("preprocessing")
            data = preprocess_data(posts_files, comments_files)

            # ------ STEP 7: Run inference ---------------------
            self.status_manager.set_state("inference")
            predict_depression(data)

            # ------ STEP 8: Save predictions ------------------
            self.status_manager.set_state("saving_results")
            for _, row in data.iterrows():
                db_handler.save_prediction(
                    run_id=run_id,
                    owner_id=abs(row["owner_id"]),
                    post_id=row["post_id"],
                    vk_id=row["id"],
                    depression_prediction=bool(row["depression_prediction"]),
                )

            self.status_manager.reset()

        except Exception as e:
            log.exception("Error during data pipeline processing", exc_info=e)
            self.status_manager.set_state("idle")
            self.status_manager.set_error(
                "Error during data pipeline processing"
            )
            raise
