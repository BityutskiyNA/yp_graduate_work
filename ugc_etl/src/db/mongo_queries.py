import random

from db.utils import AbstractBaseDB
from services.logger import logger

from services.config import app_settings


class MongoQueries(AbstractBaseDB):
    def __init__(self, client):
        self.mongo_client = client

    def insert_message(self, data: list) -> None:
        db = self.mongo_client.client[app_settings.mongo_db]
        data_to_mongo = []
        for message in data:
            likes_doc = {
                "user_id": message.key.decode("utf-8").split(" ")[0],
                "movies_id": message.key.decode("utf-8").split(" ")[1],
                "likes": random.randint(0, 10),
            }
            data_to_mongo.append(likes_doc)

        likes_collection = db[app_settings.mongo_collection]

        likes_collection.insert_many(data_to_mongo)
        logger.info("Data has been inserted to mongo")
