from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

cfg = dotenv_values(BASE_DIR / ".env")

dev = bool(int(cfg["DEV"]))
sleep = int(cfg["SLEEP"])

class AppSettingsPostgres(BaseSettings):

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    class Config:
        env_file =  dotenv_values(BASE_DIR / "env/postgres/notification/.env.dev")

app_settings_ps = AppSettingsPostgres()


class AppSettingsRabbit(BaseSettings):
    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_virtual_host: str

    class Config:
        env_file = dotenv_values(BASE_DIR / "env/postgres/rabbitmq/.env.dev")

app_settings_rabbit = AppSettingsRabbit()


class AppSettings(BaseSettings):
    mailgun_url: str
    aio_pika_connect_robust: str  = "amqp://guest:guest@localhost/"
    mailing_system_events: str  = "http://localhost:5000/mailing/system_events/"
    notification_getbyid: str = "http://localhost:5000/notification/getbyid/"
    notification_getbytype: str = "http://localhost:5000/notification/getbytype/"
    mailing_mailing_type: str = "http://localhost:5000/mailing/mailing_type/"

    class Config:
        env_file = dotenv_values(BASE_DIR / "env/notification/.env.dev")

app_settings = AppSettings()





