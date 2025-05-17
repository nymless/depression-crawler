import logging
import os
from typing import List

from vk_data_collector import Collector

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
        # Create subdirectories
        self.posts_dir = os.path.join(self.base_dir, "posts")
        self.comments_dir = os.path.join(self.base_dir, "comments")
        # Ensure directories exist
        os.makedirs(self.posts_dir, exist_ok=True)
        os.makedirs(self.comments_dir, exist_ok=True)

    def collect_data(self, groups: List[str], target_date: str) -> None:
        """
        Collects posts and comments from specified groups up to target date.

        Args:
            groups: List of VK group names to collect from
            target_date: Target date in YYYY-MM-DD format
        """
        try:
            # Reset stop flag at the start
            self.status_manager.reset_stop_flag()

            total_groups = len(groups)
            for i, group in enumerate(groups, 1):
                # Check if we should stop
                if self.status_manager.should_stop():
                    log.info(
                        "Stop requested, finishing current group and stopping"
                    )
                    break

                self.status_manager.set_current_group(group)

                # Collect posts
                self.status_manager.set_state("collecting_posts")
                self.status_manager.set_progress(
                    int((i - 1) * 100 / total_groups)
                )
                log.info(f"Collecting posts for group: {group}")
                saved_files = self.collector.collect_posts_to_date(
                    [group], target_date, self.posts_dir
                )
                log.info(f"Collected posts saved to: {saved_files}")

                # Check if we should stop
                if self.status_manager.should_stop():
                    log.info("Stop requested, skipping comments collection")
                    break

                # Collect comments
                self.status_manager.set_state("collecting_comments")
                self.status_manager.set_progress(
                    int((i - 0.5) * 100 / total_groups)
                )
                log.info(f"Collecting comments for group: {group}")
                self.collector.collect_comments_for_posts(
                    saved_files, self.comments_dir
                )
                log.info("Comments collection completed")

            # TODO: Add preprocessing, inference and saving results
            # For now, just set to idle when done
            self.status_manager.set_state("idle")
            self.status_manager.set_current_group(None)
            self.status_manager.set_progress(100)
            self.status_manager.reset()  # Complete reset of all status fields

        except Exception as e:
            log.exception("Error during data collection")
            self.status_manager.set_error(str(e))
            self.status_manager.set_state("idle")
            self.status_manager.reset()  # Reset state even in case of error
            raise
