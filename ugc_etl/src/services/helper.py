from abc import ABC, abstractmethod
from typing import Optional
from clickhouse_driver import Client

from db.mongo_queries import MongoQueries


class AbstractBaseConsumer(ABC):
    @abstractmethod
    def read_from_storage(self, db_service: Optional[MongoQueries | Client]) -> None:
        pass
