import logging
import os
from typing import List

from vk_data_collector import Collector

from src.crawler.collect_data import collect_data
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
        os.makedirs(self.base_dir, exist_ok=True)

    def process_data(self, groups: List[str], target_date: str) -> None:
        """
        Collects posts and comments from specified groups up to target date.

        Args:
            groups: List of VK group names to collect from
            target_date: Target date in YYYY-MM-DD format
        """
        try:
            posts_files, comments_files = collect_data(
                groups,
                target_date,
                self.base_dir,
                self.collector,
                self.status_manager,
            )

            # TODO: Add preprocessing, inference and saving results
            # For now, just reset status manager
            self.status_manager.reset()

        except Exception as e:
            log.exception("Error during data processing", exc_info=e)
            self.status_manager.reset()
            raise
