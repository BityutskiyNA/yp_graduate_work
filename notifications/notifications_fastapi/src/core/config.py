import os
from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    """Настройки приложения."""

    rabbit_host: str = "localhost"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_password: str = "guest"

    shortener_link: str = "http://url_shortener:5001/shorten-url"

    class Config:
        env_file = ".env"


app_settings = AppSettings()
