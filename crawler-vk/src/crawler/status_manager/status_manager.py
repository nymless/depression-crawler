import threading
from typing import Literal, TypedDict

from src.crawler.exceptions.crawler_exceptions import CrawlerStopRequested

CrawlerState = Literal[
    "idle",  # crawler is idle
    "collecting_groups",  # collecting groups info
    "preprocessing_groups",  # preprocessing groups info
    "collecting_data",  # collecting posts and comments
    "preprocessing",  # preprocessing data
    "inference",  # inference
    "saving_results",  # saving results
]


class CrawlerStatus(TypedDict):
    state: CrawlerState
    current_group: str | None  # current group data collection
    progress: int | None  # data collection progress in percent, None if not
    error: str | None  # error message, None if no error
    should_stop: bool  # flag to stop


class CrawlerStatusManager:
    """
    A class to manage the crawler's state.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._status: CrawlerStatus = {
            "state": "idle",
            "current_group": None,
            "progress": None,
            "error": None,
            "should_stop": False,
        }

    def get_status(self) -> CrawlerStatus:
        """Get current status."""
        with self._lock:
            return self._status.copy()

    def set_state(self, state: CrawlerState) -> None:
        """Set current state."""
        with self._lock:
            # Don't check stop flag when setting idle state
            if state != "idle" and self._status["should_stop"]:
                raise CrawlerStopRequested()
            self._status["state"] = state
            # Reset progress for non-collecting states
            if state not in ["collecting_data", "collecting_groups"]:
                self._status["current_group"] = None
                self._status["progress"] = None

    def set_current_group(self, group: str | None) -> None:
        """Set current group being processed."""
        with self._lock:
            # Don't check stop flag when resetting group to None
            if group is not None and self._status["should_stop"]:
                raise CrawlerStopRequested()
            self._status["current_group"] = group

    def set_progress(self, progress: int) -> None:
        """Set progress in percent."""
        with self._lock:
            self._status["progress"] = progress

    def set_error(self, error: str) -> None:
        """Set error message."""
        with self._lock:
            self._status["error"] = error

    def set_stop_flag(self) -> None:
        """Set stop flag."""
        with self._lock:
            self._status["should_stop"] = True

    def reset_stop_flag(self) -> None:
        """Reset stop flag."""
        with self._lock:
            self._status["should_stop"] = False

    def should_stop(self) -> bool:
        """Check if should stop."""
        with self._lock:
            return self._status["should_stop"]

    def reset(self) -> None:
        """Reset status to initial state."""
        with self._lock:
            self._status = {
                "state": "idle",
                "current_group": None,
                "progress": None,
                "error": None,
                "should_stop": False,
            }
