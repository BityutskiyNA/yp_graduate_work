from abc import ABC, abstractmethod


class AbstractBaseDB(ABC):
    @abstractmethod
    def insert_message(self, data: list) -> None:
        pass
