import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    """Настройки приложения."""

    kafka_host: str = "broker"
    kafka_port: int = 9092
    clickhouse_host: str = "clickhouse-node1"
    table_name: str = "default.db"
    topic_name: str = "views"
    PROJECT_NAME: str = "movies"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env"


app_settings = AppSettings()
