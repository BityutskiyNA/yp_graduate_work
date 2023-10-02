import json

import pika
from aio_pika import Message, connect

from src.core.config import app_settings
from src.models.notification import (
    NotificationByEventType,
    NotificationBySpecificEvent,
    NotificationByTypeOfMessage,
    NotificationRegisteredUser,
)


class RabbitPublisherAsync:
    @staticmethod
    async def create_queues(self):
        connection = await connect(
            f"amqp://{app_settings.rabbit_user}:"
            f"{app_settings.rabbit_password}"
            f"@{app_settings.rabbit_host}:{app_settings.rabbit_port}/"
        )
        async with connection:
            # Creating a channel
            channel = await connection.channel()

            # Declaring queue
            await channel.declare_queue("queue_by_type_of_message")
            await channel.declare_queue("queue_by_specific_event")
            await channel.declare_queue("queue_by_type_of_message")
            await channel.declare_queue("queue_by_event_type")

    @staticmethod
    async def send_to_queue_by_type_of_message(
        self, message: NotificationByTypeOfMessage, queue
    ):
        connection = await connect(
            f"amqp://{app_settings.rabbit_user}:"
            f"{app_settings.rabbit_password}"
            f"@{app_settings.rabbit_host}:{app_settings.rabbit_port}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(json.dumps(message.dict()).encode("utf-8")),
                routing_key=queue,
            )

    @staticmethod
    async def send_to_queue_by_specific_event(
        self, message: NotificationBySpecificEvent, queue
    ):
        connection = await connect(
            f"amqp://{app_settings.rabbit_user}:"
            f"{app_settings.rabbit_password}"
            f"@{app_settings.rabbit_host}:{app_settings.rabbit_port}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(json.dumps(message.dict()).encode("utf-8")),
                routing_key=queue,
            )

    @staticmethod
    async def send_to_queue_by_event_type(
        self, message: NotificationByEventType, queue
    ):
        connection = await connect(
            f"amqp://{app_settings.rabbit_user}:"
            f"{app_settings.rabbit_password}"
            f"@{app_settings.rabbit_host}:{app_settings.rabbit_port}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(json.dumps(message.dict()).encode("utf-8")),
                routing_key=queue,
            )

    @staticmethod
    async def send_to_queue_registration_event(
        self, message: NotificationRegisteredUser, queue
    ):
        connection = await connect(
            f"amqp://{app_settings.rabbit_user}:"
            f"{app_settings.rabbit_password}"
            f"@{app_settings.rabbit_host}:{app_settings.rabbit_port}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(json.dumps(message.dict()).encode("utf-8")),
                routing_key=queue,
            )

    @staticmethod
    async def send_to_queue_for_a_specific_event_urgent(
        message: NotificationBySpecificEvent, queue
    ):
        connection = await connect(
            f"amqp://{app_settings.rabbit_user}:"
            f"{app_settings.rabbit_password}"
            f"@{app_settings.rabbit_host}:{app_settings.rabbit_port}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(json.dumps(message.dict()).encode("utf-8")),
                routing_key=queue,
            )

    @staticmethod
    async def send_to_queue_by_event_type_urgent(
        message: NotificationByEventType, queue
    ):
        connection = await connect(
            f"amqp://{app_settings.rabbit_user}:"
            f"{app_settings.rabbit_password}"
            f"@{app_settings.rabbit_host}:{app_settings.rabbit_port}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(json.dumps(message.dict()).encode("utf-8")),
                routing_key=queue,
            )


class RabbitPublisher:
    def __init__(self):
        self.credentials = pika.PlainCredentials(
            username=app_settings.rabbit_user, password=app_settings.rabbit_password
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=app_settings.rabbit_host,
                port=app_settings.rabbit_port,
                credentials=self.credentials,
            )
        )
        self.channel = self.connection.channel()
        self.queue_by_type_of_message = self.channel.queue_declare(
            queue="queue_by_type_of_message"
        )
        self.queue_by_specific_event = self.channel.queue_declare(
            queue="queue_by_specific_event"
        )
        self.queue_by_event_type = self.channel.queue_declare(
            queue="queue_by_event_type"
        )
        self.queue_by_event_type = self.channel.queue_declare(
            queue="queue_registration_event"
        )

    def connect_to_rabbit(self):
        self.credentials = pika.PlainCredentials(
            username=app_settings.rabbit_user, password=app_settings.rabbit_password
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=app_settings.rabbit_host,
                port=app_settings.rabbit_port,
                credentials=self.credentials,
            )
        )
        self.channel = self.connection.channel()

    def send_to_queue_by_type_of_message(
        self, message: NotificationByTypeOfMessage, queue: str
    ):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message.dict()).encode("utf-8"),
        )

    def send_to_queue_by_specific_event(
        self, message: NotificationBySpecificEvent, queue: str
    ):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message.dict()).encode("utf-8"),
        )

    def send_to_queue_by_event_type(self, message: NotificationByEventType, queue: str):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message.dict()).encode("utf-8"),
        )

    def send_to_queue_registration_event(
        self, message: NotificationRegisteredUser, queue: str
    ):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message.dict()).encode("utf-8"),
        )

    def send_to_queue_for_a_specific_event_urgent(
        self, message: NotificationBySpecificEvent, queue: str
    ):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message.dict()).encode("utf-8"),
        )

    def send_to_queue_by_event_type_urgent(
        self, message: NotificationByEventType, queue: str
    ):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message.dict()).encode("utf-8"),
        )
