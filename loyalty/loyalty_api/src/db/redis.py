from typing import Optional

from redis.asyncio import Redis
from src.db.base_db import AbstractDBBase, AbstractDBGetData, AbstractDBSetData


class RedisBase(AbstractDBBase):
    def __init__(self):
        self.db: Optional[Redis] = None

    def set_db(self, db: Redis) -> None:
        self.db = db

    async def close(self):
        await self.db.close()


class RedisGetDataBase(RedisBase, AbstractDBGetData, AbstractDBSetData):
    def __init__(self, redis_instance: RedisBase):
        super().__init__()
        self.db = redis_instance.db

    async def get_data(self, *args, **kwargs):
        pass

    async def set_data(self, *args, **kwargs):
        pass

    async def delete_data(self, *args, **kwargs):
        pass


class RedisManageData(RedisGetDataBase):
    async def get_data(self, key: str) -> Optional[str]:
        promocode = await self.db.get(key)

        return promocode

    async def set_data(self, key: str, value: str) -> bool | None:
        result = await self.db.set(name=key, value=value)

        return result

    async def delete_data(self, key: str) -> None:
        keys_to_delete = await self.db.scan(match=key)
        for key in keys_to_delete[1]:
            await self.db.delete(key)


def get_redis_data() -> RedisManageData:
    return RedisManageData(red)


red = RedisBase()
