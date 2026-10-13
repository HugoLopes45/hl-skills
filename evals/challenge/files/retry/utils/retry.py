import functools
import random
import time


def retry(attempts=3, base_delay=0.2, retry_on=(OSError,)):
    """Retry with exponential backoff and full jitter."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except retry_on:
                    if attempt == attempts - 1:
                        raise
                    time.sleep(random.uniform(0, base_delay * 2 ** attempt))
        return wrapper
    return decorator
