from typing import Optional

import pymongo

from kafka import KafkaConsumer

from db.mongo_queries import MongoQueries
from services.backoff import backoff
from services.config import app_settings
from services.helper import AbstractBaseConsumer
from services.logger import logger

# from clickhouse_driver import Client
# from db.clickhouse_queries import ClickhouseQueries

BATCH_SIZE = 3


class KafkaClickhouseConsumer(AbstractBaseConsumer):
    @backoff()
    def connect_to_storage(self) -> KafkaConsumer:
        return KafkaConsumer(
            app_settings.topic_name,
            bootstrap_servers=[f"{app_settings.kafka_host}:{app_settings.kafka_port}"],
            auto_offset_reset="earliest",
            group_id="echo-messages-to-stdout",
            enable_auto_commit=False,
        )

    def read_from_storage(self, db_service: Optional[MongoQueries]) -> None:
        consumer = self.connect_to_storage()
        if not consumer:
            logger.info("Can't connect to Storage")
            return None
        data = []
        logger.info("Connected to Storage")
        for message in consumer:
            logger.info("message read from kafka: %s %s", message.value, message.key)
            data.append(message)
            if len(data) >= BATCH_SIZE:
                db_service.insert_message(data=data)  # nomypy
                data.clear()

                consumer.commit()


if __name__ == "__main__":
    consumer_service = KafkaClickhouseConsumer()
    # consumer_service.read_from_storage(ClickhouseQueries(Client(host=app_settings.clickhouse_host)))
    consumer_service.read_from_storage(
        MongoQueries(
            pymongo.MongoClient(
                f"mongodb://{app_settings.mongo_host}:{app_settings.mongo_port}/"
            )
        )
    )
