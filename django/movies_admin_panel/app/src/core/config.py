from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent.parent

cfg = dotenv_values(BASE_DIR / ".env")

dev = bool(int(cfg["DEV"]))
sleep = int(cfg["SLEEP"])

env_file = ".env.dev" if dev else ".env"

db = dotenv_values(BASE_DIR / f"env/db/movie/{env_file}")
django = dotenv_values(BASE_DIR / f"env/django/movie/{env_file}")
docker = dotenv_values(BASE_DIR / f"env/docker/movie/{env_file}")


class DB(BaseSettings):
    password: str = db["POSTGRES_PASSWORD"]
    host: str = db["POSTGRES_HOST"]
    port: int = db["POSTGRES_PORT"]
    database: str = db["POSTGRES_DB"]
    user: str = db["POSTGRES_USER"]

    schema_name: str = db["POSTGRES_SCHEMA_NAME"]
    chunk_size: int = db["POSTGRES_CHUNK_SIZE"]


class Django(BaseSettings):
    secret_key: str = django["SECRET_KEY"]
    debug: bool = django["DEBUG"]
    allowed_hosts: str = django["ALLOWED_HOSTS"]
    internal_ips: str = django["INTERNAL_IPS"]


class Docker(BaseSettings):
    db_host: str = docker["DB_HOST"]
    django_host: str = docker["DJANGO_HOST"]


class Config:
    db: DB = DB()
    django: Django = Django()
    docker: Docker = Docker()
    dev: int = 1
    sleep: int = 1


config = Config()
