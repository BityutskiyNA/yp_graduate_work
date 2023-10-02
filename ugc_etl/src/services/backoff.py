import time
from functools import wraps

from services.logger import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """Декоратор для подключения к БД."""

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            retries = 0
            sleep_time = start_sleep_time
            while True:
                try:
                    conn = func(*args, **kwargs)
                    retries += 1
                    logger.info(f"Successful connection (attempt {retries})")
                    return conn
                except Exception:
                    if sleep_time >= border_sleep_time:
                        logger.warning(
                            f"Wait time exceeded ({border_sleep_time} seconds)"
                        )
                        raise
                    retries += 1
                    logger.warning(f"Connection error (attempt {retries})")
                    time.sleep(sleep_time)
                    sleep_time = min(
                        start_sleep_time * (factor**retries), border_sleep_time
                    )

        return inner

    return func_wrapper
