import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", 9200))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    """Настройки приложения."""

    kafka_host: str = "broker"
    kafka_port: int = 9092
    clickhouse_host: str = "clickhouse-node1"
    table_name: str = "default.db"
    topic_name: str = "views"

    class Config:
        env_file = ".env"


app_settings = AppSettings()
