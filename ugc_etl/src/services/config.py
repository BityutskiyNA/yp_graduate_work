from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """Настройки приложения."""

    kafka_host: str = "broker"
    kafka_port: int = 9092
    clickhouse_host: str = "clickhouse-node1"
    clickhouse_table: str = "default.db"
    topic_name: str = "views"
    mongo_host: str = "mongos1"
    mongo_port: int = 27017
    mongo_db: str = "someDb"
    mongo_collection: str = "someCollection"

    class Config:
        env_file = ".env"


app_settings = AppSettings()
