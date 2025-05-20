"""Exceptions for crawler operations."""


class CrawlerStopRequested(Exception):
    """Exception raised when crawler stop is requested."""

    def __init__(
        self, message: str = "Crawler stop was requested by user"
    ) -> None:
        super().__init__(message)
