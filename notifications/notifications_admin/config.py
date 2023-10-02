from dataclasses import dataclass
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

    fastapi_url: str = "http://localhost:/endpoint"

    class Config:
        env_file =  dotenv_values(BASE_DIR / "env/postgres/notifications_admin/.env.dev")


app_settings = AppSettings()

