import json
from typing import Optional

from db.base_db import AbstractDBBase, AbstractDBGetData, AbstractDBSetData
from redis.asyncio import Redis


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

    async def get_dataset(self, *args, **kwargs):
        pass

    async def delete_and_push_list(self, *args, **kwargs):
        pass

    async def delete_and_push_dict(self, *args, **kwargs):
        pass


class RedisManageData(RedisGetDataBase):
    async def get_data(self, key: str) -> Optional[str]:
        doc = await self.db.get(key)

        return doc

    async def set_data(self, key: str, value: dict, expires: int) -> bool:
        result = await self.db.set(name=key, value=value, ex=expires)

        return result

    async def get_dataset(self, composite_id: str) -> list:
        length = await self.db.llen(composite_id)
        dataset = await self.db.lrange(composite_id, 1, length)
        return dataset

    async def delete_and_push_list(self, composite_id, data_list, match) -> None:
        keys_to_delete = await self.db.scan(match=match)
        for key in keys_to_delete[1]:
            await self.db.delete(key)
        await self.db.lpush(
            composite_id,
            *[item.json() for item in data_list],
        )

    async def delete_and_push_dict(self, composite_id, data_dict, match, field) -> None:
        keys_to_delete = await self.db.scan(match=match)
        for key in keys_to_delete[1]:
            await self.db.delete(key)

        items = data_dict.get(field)
        await self.db.lpush(
            composite_id,
            *[json.dumps(item, indent=4) for item in items],
        )


def get_redis_data() -> RedisManageData:
    return RedisManageData(red)


red = RedisBase()
