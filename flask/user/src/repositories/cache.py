from config import config
from src.databases.cache import cache


class CacheRepository:
    @staticmethod
    def set(user_id, access_token):
        cache.set(str(user_id), access_token, ex=config.jwt.access_token_expires)

    @staticmethod
    def get(user_id):
        return cache.get(str(user_id))

    @staticmethod
    def block(user_id):
        return cache.set(str(user_id), "", ex=config.jwt.access_token_expires)

    @staticmethod
    def check(user_id):
        if cache.get(str(user_id)) is not None:
            if cache.get(str(user_id)) != b"":
                raise ValueError("Already logged in")


cache_repository = CacheRepository()
