from abc import ABC, abstractmethod


class AbstractBasePublisher(ABC):
    @abstractmethod
    def add_new_topic(self) -> None:
        pass

    @abstractmethod
    def publish_to_storage(self, data) -> None:
        pass
