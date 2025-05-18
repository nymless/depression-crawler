import logging
import os
from typing import List

from vk_data_collector import Collector

from src.crawler.collect_data import collect_data
from src.crawler.predict_depression import predict_depression
from src.crawler.preprocess_data import preprocess_data
from src.crawler.status_manager import CrawlerStatusManager

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
        os.makedirs(self.base_dir, exist_ok=True, parents=True)

    def run_pipeline(self, groups: List[str], target_date: str) -> None:
        """
        Run the complete data pipeline:
        1. Collect posts and comments from specified groups
        2. Preprocess collected data (text cleaning, tokenization, embeddings)
        3. Run depression detection inference
        4. Save results (TODO)

        Args:
            groups: List of VK group names to collect from
            target_date: Target date in YYYY-MM-DD format
        """
        try:
            self.status_manager.reset()
            posts_files, comments_files = collect_data(
                groups,
                target_date,
                self.base_dir,
                self.collector,
                self.status_manager,
            )
            self.status_manager.set_state("preprocessing")
            data = preprocess_data(posts_files, comments_files)

            self.status_manager.set_state("inference")
            predict_depression(data)

            # TODO: Add saving results to database
            self.status_manager.reset()

        except Exception as e:
            log.exception("Error during data pipeline processing", exc_info=e)
            self.status_manager.set_state("idle")
            self.status_manager.set_error(
                "Error during data pipeline processing"
            )
            raise
