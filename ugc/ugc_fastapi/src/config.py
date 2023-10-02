from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Kafka(BaseSettings):
    kafka_host_name: str = Field(env="KAFKA_HOST")
    kafka_port: str = Field(env="KAFKA_PORT")
    TOPIC_NAME: str = Field(env="KAFKA_DB")

    class Config:
        env_file = BASE_DIR / "env/kafka/.env.dev"


class JWT(BaseSettings):
    secret_key: str = Field(env="SECRET_KEY")

    class Config:
        env_file = BASE_DIR / "env/jwt/user/.env.dev"


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME")
    jwt = JWT()
    kafka = Kafka()

    class Config:
        env_file = BASE_DIR / "env/ugc/.env.dev"


config = Settings()
