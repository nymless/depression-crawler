import logging
import os
from typing import List

from vk_data_collector import Collector

from src.crawler.status_manager.status_manager import CrawlerStatusManager

log = logging.getLogger(__name__)


def collect_groups(
    groups: List[str],
    target_date: str,
    base_dir: str,
    collector: Collector,
    status_manager: CrawlerStatusManager,
) -> List[str]:
    """
    Collect groups information from specified VK groups.

    Args:
        groups: List of VK group names to collect from
        target_date: Target date in YYYY-MM-DD format
        base_dir: Base directory for storing collected data
        collector: VK data collector instance
        status_manager: Status manager for tracking progress and state
    """
    # Create subdirectories
    group_dir = os.path.join(base_dir, "groups")
    # Ensure directories exist
    os.makedirs(group_dir, exist_ok=True)

    # Reset stop flag at the start
    status_manager.reset_stop_flag()

    groups_files = []

    total_groups = len(groups)
    for i, group in enumerate(groups):
        # Check if we should stop
        if status_manager.should_stop():
            log.info("Stop requested, finishing current group and stopping")
            break

        status_manager.set_current_group(group)
        status_manager.set_progress(int(i * 100 / total_groups))

        # Collect groups information
        log.info(f"Collecting group information: {group}")
        saved_files = collector.collect_groups([group], group_dir)
        log.info(f"Collected group information saved to: {saved_files}")
        groups_files.extend(saved_files)

    if not status_manager.should_stop():
        status_manager.set_current_group(None)
        status_manager.set_progress(None)

    return groups_files
