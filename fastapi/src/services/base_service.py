import abc
from typing import Any, Optional

from db.base_db import AbstractDBGetData
from db.redis import RedisGetDataBase


class BaseService(abc.ABC):
    """
    Абстрактный класс сервиса для получения данных из ElasticSearch
    """

    DataType = Any

    def __init__(self, redis: RedisGetDataBase, search_engine: AbstractDBGetData):
        self.redis = redis
        self.search_engine = search_engine

    @abc.abstractmethod
    async def _get_from_search_engine(
        self, id: Optional[str] = None, *args, **kwargs
    ) -> DataType:
        """
        Абстрактный метод для получения данных из поисковой базы
        :param id: id записи в бд
        :param args:
        :param kwargs:
        :return: данные из бд
        """

        pass

    async def get_data(self, *args, **kwargs) -> DataType:
        """
        Метод для получения данных из поисковой базы
        :return: найденные данные
        """
        data = await self._get_from_search_engine(*args, **kwargs)
        if not data:
            return None
        return data


class BaseCacheService(BaseService, abc.ABC):
    """
    Абстрактный класс сервиса для получения данных из кэша Redis или из ElasticSearch, если в Redis нет данных
    и для записи данных в кэш Redis
    """

    DataType = Any

    def __init__(self, redis: RedisGetDataBase, search_engine: AbstractDBGetData):
        super().__init__(redis, search_engine)

    @abc.abstractmethod
    async def _get_from_redis(self, composite_id: str) -> DataType:
        """
        Абстракнтый метод для получения данных из кэша Redis
        :param composite_id: композитный id записи в Redis
        :return: данные из Redis
        """
        pass

    @abc.abstractmethod
    async def _put_to_redis(self, composite_id: str, data: DataType) -> None:
        """
        Абстракнтый метод для записи данных в кэша Redis
        :param composite_id: композитный id записи в Redis
        :param data: данные для записи в Redis
        :return: None
        """
        pass

    async def get_data(
        self, prefix: str, id: Optional[str] = None, *args, **kwargs
    ) -> DataType:
        """
        Метод для получения данных из кэша Redis или из ElasticSearch, если в Redis нет данных
        с последующей записью в кэш
        :param prefix: префикс для составного индекса для записи в кэш
        :param id: id записи в Elastic
        :return: найденные данные
        """
        data = await self._get_from_redis(f"{prefix}{id}" if id else f"{prefix}")
        if data:
            return data

        if id:
            data = await self._get_from_search_engine(id, *args, **kwargs)
        else:
            data = await self._get_from_search_engine(*args, **kwargs)
        if not data:
            return None

        await self._put_to_redis(f"{prefix}{id}" if id else f"{prefix}", data)

        return data
