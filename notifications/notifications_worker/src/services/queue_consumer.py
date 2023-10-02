import asyncio

import aio_pika

from notifications.notifications_worker.config import app_settings


class QueueConsumer:
    def __init__(self, queue_name, callback):
        self.queue_name = queue_name
        self.callback = callback
        self.connection = None
        self.channel = None
        self.queue = None
        self.stop_event = asyncio.Event()

    async def on_message(self, message):
        async with message.process():
            await self.callback(message.body)

    async def setup(self):
        self.connection = await aio_pika.connect_robust(app_settings.aio_pika_connect_robust)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.consume(self.on_message)

    async def run(self):
        await self.setup()
        await self.stop_event.wait()

    async def stop(self):
        self.stop_event.set()
        if self.connection:
            await self.connection.close()