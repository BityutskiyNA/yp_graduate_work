import motor.motor_asyncio
from config import config


class Mongo_db:
    def __init__(self):
        self.client = None
        self.db_name = None
        self.config = config

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            self.config.mongo.mongo_host_name, self.config.mongo.mongo_port
        )
        self.db_name = self.client[self.config.mongo.TOPIC_NAME]

    async def disconnect(self):
        self.client.close()

    async def send_document(self, document, collection):
        await self.connect()
        try:
            await self.db_name[collection].insert_one(document)
        finally:
            await self.disconnect()

    async def get_aggregate_document_by_user(self, user_id, collection):
        s_filter = {"user_id": user_id}
        await self.connect()
        try:
            collection = self.db_name[collection]
            cursor = collection.find(s_filter)
            records = await cursor.to_list(length=None)
        finally:
            await self.disconnect()
        return records

    async def get_aggregate_document_by_movie(self, movies_id, collection):
        s_filter = {"movies_id": movies_id}
        await self.connect()
        try:
            collection = self.db_name[collection]
            cursor = collection.find(s_filter)
            records = await cursor.to_list(length=None)
        finally:
            await self.disconnect()
        return records

    async def del_document(self, user_id, movies_id, collection):
        d_filter = {
            "$and": [
                {"user_id": user_id},
                {"movies_id": movies_id},
            ]
        }
        await self.connect()
        try:
            collection = self.db_name[collection]
            result = await collection.delete_many(d_filter)
            records = result.deleted_count
        finally:
            await self.disconnect()

        return records


def get_mongo_data():
    return Mongo_db()
