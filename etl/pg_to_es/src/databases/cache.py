import logging

import backoff
import redis
from src.core.config import config


@backoff.on_exception(
    backoff.expo, redis.exceptions.ConnectionError, max_tries=config.backoff_max_tries
)
def get_cache_client(logger: logging.Logger) -> redis.Redis.client:
    """Get redis instance."""
    params = {
        "host": config.docker.cache_host,
        "port": config.cache.port,
    }
    try:
        cache = redis.Redis(**params)
        return cache
    except redis.exceptions.ConnectionError as e:
        logger.error(e)
