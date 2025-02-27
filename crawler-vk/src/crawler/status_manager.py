import threading
from typing import TypedDict


class CrawlerStatus(TypedDict):
    running: bool
    requests_count: int
    saved_posts_count: int


class CrawlerStatusManager:
    """
    A class to manage the crawler's state.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._status: CrawlerStatus = {
            "running": False,
            "requests_count": 0,
            "saved_posts_count": 0,
        }

    def start(self) -> None:
        with self._lock:
            self._status["running"] = True

    def stop(self) -> None:
        with self._lock:
            self._status["running"] = False

    def reset(self) -> None:
        with self._lock:
            self._status["requests_count"] = 0
            self._status["saved_posts_count"] = 0

    def increment_requests(self) -> None:
        with self._lock:
            self._status["requests_count"] += 1

    def increment_saved_posts(self) -> None:
        with self._lock:
            self._status["saved_posts_count"] += 1

    def get_status(self) -> CrawlerStatus:
        with self._lock:
            return self._status.copy()
