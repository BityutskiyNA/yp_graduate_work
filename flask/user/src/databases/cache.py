import redis
from config import config

cache = redis.Redis(
    host=config.docker.redis_host,
    port=config.redis.port,
    db=config.redis.db,
)
