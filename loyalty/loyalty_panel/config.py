import os
from pathlib import Path
from pydantic import BaseSettings
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent

cfg = dotenv_values(BASE_DIR / ".env")

dev = bool(int(cfg["DEV"]))
sleep = int(cfg["SLEEP"])


class AppSettings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    debug: str
    allowed_host: dict
    secret_key: str

    class Config:
        env_file = os.path.join(BASE_DIR, "env/db/loyalty/.env.dev")


app_settings = AppSettings()
