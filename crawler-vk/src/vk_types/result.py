import logging
from collections.abc import Mapping
from typing import Any, Callable, Generic, TypeVar, cast

from src.vk_types.response.error import ErrorResponse

T = TypeVar("T", bound=Mapping[str, Any])


class APIResponse(Generic[T]):
    def _log_response(self) -> None:
        if self.is_empty:
            logging.warning(
                f"Response object is empty. Request ID: {self.request_id}"
            )
        if self.is_error:
            error_code = self.data["error"]["error_code"]
            error_msg = self.data["error"]["error_msg"]
            logging.warning(
                f"VK API Error received. API Request ID: {self.request_id} "
                f"Error code: {error_code}. Error message: {error_msg}"
            )
        if not (self.is_success or self.is_error or self.is_empty):
            logging.warning(f"Unknown response object: {self.data}")

    def __init__(
        self,
        response: tuple[int, T | ErrorResponse],
        check_empty_fn: Callable[[T], bool],
    ) -> None:
        self.request_id = response[0]
        self.data = response[1]
        self.is_success = "response" in self.data
        self.is_error = "error" in self.data
        if self.is_success:
            self.data = cast(T, self.data)
            self.is_empty = check_empty_fn(self.data)
        elif self.is_error:
            self.data = cast(ErrorResponse, self.data)
        self.is_success = self.is_success and not self.is_empty
        self._log_response()
