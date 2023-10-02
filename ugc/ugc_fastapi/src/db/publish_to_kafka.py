from aiokafka import AIOKafkaProducer
from src.config import config

port = config.kafka.kafka_port
host_name = config.kafka.kafka_host_name
topic_name = config.kafka.kafka_host_name


class KafkaPublisherAsync:
    def __init__(self):
        self.producer = None
        self.config = config

    async def connect(self):
        kafka_bootstrap_servers = [
            f"{self.config.kafka.kafka_host_name}:{self.config.kafka.kafka_port}"
        ]
        self.producer = AIOKafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
        await self.producer.start()

    async def disconnect(self):
        await self.producer.stop()

    async def send_message(self, message):
        await self.producer.send_and_wait(self.config.kafka.TOPIC_NAME, message)
