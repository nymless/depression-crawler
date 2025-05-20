import logging
import os
from typing import List, Tuple

from vk_data_collector import Collector

from src.crawler.status_manager.status_manager import CrawlerStatusManager

log = logging.getLogger(__name__)


def collect_data(
    group_names: List[str],
    target_date: str,
    base_dir: str,
    collector: Collector,
    status_manager: CrawlerStatusManager,
) -> Tuple[List[str], List[str]]:
    """
    Collect posts and comments from specified VK groups up to target date.

    Args:
        group_names: List of VK group names to collect from
        target_date: Target date in YYYY-MM-DD format
        base_dir: Base directory for storing collected data
        collector: VK data collector instance
        status_manager: Status manager for tracking progress and state
    """
    try:
        # Create subdirectories
        posts_dir = os.path.join(base_dir, "posts")
        comments_dir = os.path.join(base_dir, "comments")
        # Ensure directories exist
        os.makedirs(posts_dir, exist_ok=True)
        os.makedirs(comments_dir, exist_ok=True)

        # Reset stop flag at the start
        status_manager.reset_stop_flag()

        posts_files = []
        comments_files = []

        total_groups = len(group_names)
        for i, group in enumerate(group_names):
            # Check if we should stop
            if status_manager.should_stop():
                log.info("Stop requested, finishing current group and stopping")
                break

            status_manager.set_current_group(group)
            status_manager.set_progress(int(i * 100 / total_groups))

            # Collect posts
            log.info(f"Collecting posts for group: {group}")
            saved_files = collector.collect_posts_to_date(
                [group], target_date, posts_dir
            )
            log.info(f"Collected posts saved to: {saved_files}")
            posts_files.extend(saved_files)

            # Check if we should stop
            if status_manager.should_stop():
                log.info("Stop requested, skipping comments collection")
                break

            # Collect comments
            log.info(f"Collecting comments for group: {group}")
            saved_files = collector.collect_comments_for_posts(
                saved_files, comments_dir
            )
            log.info(f"Collected comments saved to: {saved_files}")
            comments_files.extend(saved_files)

        return posts_files, comments_files
    except Exception as e:
        log.exception(
            "Error collecting posts and comments data",
            exc_info=e,
        )
        raise
