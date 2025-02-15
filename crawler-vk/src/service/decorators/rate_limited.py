import time
from collections import deque
from functools import wraps
from typing import Callable


def rate_limited(limit: int):
    """Decorator factory for rate limiting with a given limit per second."""

    requests: deque[float] = deque(maxlen=limit)

    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            if len(requests) == limit:
                earliest = requests[0]
                if now - earliest < 1:
                    sleep_time = 1 - (now - earliest)
                    time.sleep(max(0, sleep_time))

            requests.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator
