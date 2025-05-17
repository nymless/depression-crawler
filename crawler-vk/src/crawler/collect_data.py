import logging
import os
from typing import List

from src.crawler.status_manager import CrawlerStatusManager
from vk_data_collector import Collector

log = logging.getLogger(__name__)


def collect_data(
    groups: List[str],
    target_date: str,
    base_dir: str,
    collector: Collector,
    status_manager: CrawlerStatusManager,
) -> None:
    """
    Collect posts and comments from specified VK groups up to target date.

    Args:
        groups: List of VK group names to collect from
        target_date: Target date in YYYY-MM-DD format
        base_dir: Base directory for storing collected data
        collector: VK data collector instance
        status_manager: Status manager for tracking progress and state
    """
    # Create subdirectories
    posts_dir = os.path.join(base_dir, "posts")
    comments_dir = os.path.join(base_dir, "comments")
    # Ensure directories exist
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(comments_dir, exist_ok=True)

    # Reset stop flag at the start
    status_manager.reset_stop_flag()

    total_groups = len(groups)
    for i, group in enumerate(groups, 1):
        # Check if we should stop
        if status_manager.should_stop():
            log.info("Stop requested, finishing current group and stopping")
            break

        status_manager.set_current_group(group)

        # Collect posts
        status_manager.set_state("collecting_posts")
        status_manager.set_progress(int((i - 1) * 100 / total_groups))
        log.info(f"Collecting posts for group: {group}")
        saved_files = collector.collect_posts_to_date(
            [group], target_date, posts_dir
        )
        log.info(f"Collected posts saved to: {saved_files}")

        # Check if we should stop
        if status_manager.should_stop():
            log.info("Stop requested, skipping comments collection")
            break

        # Collect comments
        status_manager.set_state("collecting_comments")
        status_manager.set_progress(int((i - 0.5) * 100 / total_groups))
        log.info(f"Collecting comments for group: {group}")
        collector.collect_comments_for_posts(saved_files, comments_dir)
        log.info("Comments collection completed")
