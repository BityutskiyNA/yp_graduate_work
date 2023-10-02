import datetime

import pandas as pd
from services.logger import logger

from db.utils import AbstractBaseDB

from services.config import app_settings


class ClickhouseQueries(AbstractBaseDB):
    def __init__(self, client):
        self.clickhouse_client = client

    def insert_message(self, data: list) -> None:
        data_to_sql = []
        for message in data:
            data_to_sql.append(
                [
                    message.key.decode("utf-8").split(" ")[0],
                    message.key.decode("utf-8").split(" ")[1],
                    message.value.decode("utf-8"),
                    datetime.datetime.now(),
                ],
            )

        dataframe = pd.DataFrame(
            data_to_sql, columns=["film_id", "user_id", "user_time", "event_time"]
        )

        self.clickhouse_client.insert_dataframe(
            f"""INSERT INTO {app_settings.clickhouse_table} (film_id, user_id, user_time, event_time) VALUES """,
            dataframe,
            settings=dict(use_numpy=True),
        )
