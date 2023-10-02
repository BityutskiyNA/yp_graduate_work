import abc
from typing import Any


class AbstractDBGetData(abc.ABC):
    @abc.abstractmethod
    async def get_data(self, *args, **kwargs):
        pass


class AbstractDBSetData(abc.ABC):
    @abc.abstractmethod
    async def set_data(self, *args, **kwargs):
        pass


class AbstractDBBase(abc.ABC):
    @abc.abstractmethod
    def set_db(self, db: Any) -> None:
        pass

    @abc.abstractmethod
    async def close(self):
        pass
