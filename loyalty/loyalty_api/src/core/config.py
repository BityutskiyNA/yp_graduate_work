import os
from logging import config as logging_config

from pydantic_settings import BaseSettings

from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    """Настройки приложения."""

    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    name: str = "postgres"
    url: str = f"postgresql://{user}:{password}@{host}:{port}/{name}"

    class Config:
        env_prefix = "LOYALTY_DB_"
        env_file = ".env"


class RedisSettings(BaseSettings):
    """Настройки редиса."""

    host: str = "localhost"
    port: int = 6379

    class Config:
        env_prefix = "LOYALTY_REDIS_"
        env_file = ".env"


app_settings = AppSettings()
redis_settings = RedisSettings()
