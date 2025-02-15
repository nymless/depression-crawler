from typing import TypedDict


class RequestParam(TypedDict):
    key: str
    value: str


class Error(TypedDict):
    error_code: int
    error_msg: str
    request_params: list[RequestParam]


class ErrorResponse(TypedDict):
    error: Error
