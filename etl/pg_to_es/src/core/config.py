from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

cfg = dotenv_values(BASE_DIR / ".env")

dev = bool(int(cfg["DEV"]))
sleep = int(cfg["SLEEP"])

env_file = ".env.dev" if dev else ".env"

cache = dotenv_values(BASE_DIR / f"env/cache/movie/{env_file}")
db = dotenv_values(BASE_DIR / f"env/db/movie/{env_file}")
es = dotenv_values(BASE_DIR / f"env/es/movie/{env_file}")
docker = dotenv_values(BASE_DIR / f"env/docker/movie/{env_file}")


@dataclass
class DB:
    password: str = db["POSTGRES_PASSWORD"]
    host: str = db["POSTGRES_HOST"]
    port: int = db["POSTGRES_PORT"]
    database: str = db["POSTGRES_DB"]
    user: str = db["POSTGRES_USER"]

    schema_name: str = db["POSTGRES_SCHEMA_NAME"]
    chunk_size: int = db["POSTGRES_CHUNK_SIZE"]


@dataclass
class Cache:
    host: str = cache["REDIS_HOST"]
    port: int = cache["REDIS_PORT"]


@dataclass
class ES:
    host: str = es["HOST"]
    port: str = es["PORT"]
    url: str = "http://{host}:{port}".format(host=docker["ES_HOST"], port=es["PORT"])

    filmwork_mapping: str = es["FILMWORK_MAPPING"]
    genre_mapping: str = es["GENRE_MAPPING"]
    actor_mapping: str = es["ACTOR_MAPPING"]
    writer_mapping: str = es["WRITER_MAPPING"]
    director_mapping: str = es["DIRECTOR_MAPPING"]

    filmwork_index: str = es["FILMWORK_INDEX"]
    genre_index: str = es["GENRE_INDEX"]
    actor_index: str = es["ACTOR_INDEX"]
    writer_index: str = es["WRITER_INDEX"]
    director_index: str = es["DIRECTOR_INDEX"]


@dataclass
class Docker:
    db_host: str = docker["DB_HOST"]
    cache_host: str = docker["CACHE_HOST"]
    es_host: str = docker["ES_HOST"]


class Config:
    db: DB = DB()
    cache: Cache = Cache()
    es: ES = ES()
    docker: Docker = Docker()
    backoff_max_tries: int = 5
    dev: int = 1
    sleep: int = 1


config = Config()
