from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent

cfg = dotenv_values(BASE_DIR / ".env")

dev = bool(int(cfg["DEV"]))
sleep = int(cfg["SLEEP"])

if dev:
    redis = dotenv_values(BASE_DIR / "env/redis/user/.env.dev")
    redis_lb = dotenv_values(BASE_DIR / "env/redis/user/leakybucket/.env.dev")
    postgres = dotenv_values(BASE_DIR / "env/db/user/.env.dev")
    flask = dotenv_values(BASE_DIR / "env/flask/user/.env.dev")
    jwt = dotenv_values(BASE_DIR / "env/jwt/user/.env.dev")
    admin = dotenv_values(BASE_DIR / "env/admin/user/.env.dev")
    docker = dotenv_values(BASE_DIR / "env/docker/user/.env.dev")
    oauth_vk = dotenv_values(BASE_DIR / "env/oauth_vk/.env.dev")
    jaeger = dotenv_values(BASE_DIR / "env/jaeger/.env")
else:
    redis = dotenv_values(BASE_DIR / "env/redis/user/.env.dev")
    redis_lb = dotenv_values(BASE_DIR / "env/redis/user/leakybucket/.env.dev")
    postgres = dotenv_values(BASE_DIR / "env/db/user/.env.dev")
    flask = dotenv_values(BASE_DIR / "env/flask/user/.env.dev")
    jwt = dotenv_values(BASE_DIR / "env/jwt/user/.env.dev")
    admin = dotenv_values(BASE_DIR / "env/admin/user/.env.dev")
    docker = dotenv_values(BASE_DIR / "env/docker/user/.env.dev")
    oauth_vk = dotenv_values(BASE_DIR / "env/oauth_vk/.env.dev")
    jaeger = dotenv_values(BASE_DIR / "env/jaeger/.env")


@dataclass
class Postgres:
    user: str = postgres["POSTGRES_USER"]
    password: str = postgres["POSTGRES_PASSWORD"]
    host: str = postgres["POSTGRES_HOST"]
    port: int = postgres["POSTGRES_PORT"]
    db: str = postgres["POSTGRES_DB"]


@dataclass
class Redis:
    host: str = redis["REDIS_HOST"]
    port: int = redis["REDIS_PORT"]
    db: int = redis["REDIS_DB"]


@dataclass
class RedisLB:
    host: str = redis_lb["REDIS_HOST"]
    port: int = redis_lb["REDIS_PORT"]
    db: int = redis_lb["REDIS_DB"]
    REQUEST_LIMIT_PER_MINUTE: int = int(redis_lb["REQUEST_LIMIT_PER_MINUTE"])


@dataclass
class Flask:
    secret_key: str = flask["SECRET_KEY"]
    sentry_dsn: str = flask["SENTRY_DSN"]


@dataclass
class JWT:
    secret_key: str = jwt["SECRET_KEY"]
    access_token_expires: int = jwt["ACCESS_TOKEN_EXPIRES"]
    refresh_token_expires: int = jwt["REFRESH_TOKEN_EXPIRES"]


@dataclass
class Admin:
    login: str = admin["LOGIN"]
    password: str = admin["PASSWORD"]
    email: str = admin["EMAIL"]
    all_roles: str = admin["ALL_ROLES"]
    admin_role: str = admin["ADMIN_ROLE"]


@dataclass
class Docker:
    postgres_host: str = docker["POSTGRES_HOST"]
    redis_host: str = docker["REDIS_HOST"]


@dataclass
class OAuthVK:
    name: str = (oauth_vk["NAME"],)
    client_id: str = (oauth_vk["CLIENT_ID"],)
    client_secret: str = (oauth_vk["CLIENT_SECRET"],)
    authorize_url: str = (oauth_vk["AUTHORIZE_URL"],)
    access_token_url: str = (oauth_vk["ACCESS_TOKEN_URL"],)
    base_url: str = oauth_vk["BASE_URL"]


@dataclass
class Jaeger:
    agent_host_name: str = (jaeger["AGENT_HOST_NAME"],)
    agent_port: str = (jaeger["AGENT_PORT"],)


class Config:
    postgres: Postgres = Postgres()
    redis: Redis = Redis()
    redisLB: RedisLB = RedisLB()
    flask: Flask = Flask()
    jwt: JWT = JWT()
    admin: Admin = Admin()
    docker: Docker = Docker()
    oauth_vk: OAuthVK = OAuthVK()
    jaeger: Jaeger = Jaeger()


config = Config()
