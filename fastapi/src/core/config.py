import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = "movies"

    # Настройки Redis
    redis_film_host: str
    redis_film_port: int

    # Настройки Elasticsearch
    elastic_host: str
    elastic_port: int

    # Настройки логирования
    logging_level: str = "INFO"
    loggers_logging_level: str = "INFO"

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
