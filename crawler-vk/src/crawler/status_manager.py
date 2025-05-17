import threading
from typing import Literal, TypedDict

CrawlerState = Literal[
    "idle",  # crawler is idle
    "collecting_posts",  # collecting posts
    "collecting_comments",  # collecting comments
    "preprocessing",  # preprocessing data
    "inference",  # inference
    "saving_results",  # saving results
]


class CrawlerStatus(TypedDict):
    state: CrawlerState
    current_group: str | None  # current group being processed
    progress: int  # progress in percent
    error: str | None  # error, if any
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
            "progress": 0,
            "error": None,
            "should_stop": False,
        }

    def set_state(self, new_state: CrawlerState) -> None:
        """Set the current state of the crawler."""
        with self._lock:
            self._status["state"] = new_state
            # Reset progress when changing state
            self._status["progress"] = 0
            # Clear error when changing state
            self._status["error"] = None

    def set_current_group(self, group: str | None) -> None:
        """Set the current group being processed."""
        with self._lock:
            self._status["current_group"] = group

    def set_progress(self, progress: int) -> None:
        """Set the progress percentage (0-100)."""
        with self._lock:
            self._status["progress"] = max(0, min(100, progress))

    def set_error(self, error: str | None) -> None:
        """Set an error message or clear it."""
        with self._lock:
            self._status["error"] = error

    def request_stop(self) -> None:
        """Request the crawler to stop."""
        with self._lock:
            self._status["should_stop"] = True

    def should_stop(self) -> bool:
        """Check if crawler should stop."""
        with self._lock:
            return self._status["should_stop"]

    def reset_stop_flag(self) -> None:
        """Reset the stop flag."""
        with self._lock:
            self._status["should_stop"] = False

    def get_status(self) -> CrawlerStatus:
        """Get the current status of the crawler."""
        with self._lock:
            return self._status.copy()

    def reset(self) -> None:
        """Reset all status fields to their initial values."""
        with self._lock:
            self._status = {
                "state": "idle",
                "current_group": None,
                "progress": 0,
                "error": None,
                "should_stop": False,
            }
