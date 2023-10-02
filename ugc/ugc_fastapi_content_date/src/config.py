from pathlib import Path
from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Mongo(BaseSettings):
    mongo_host_name: str = Field(env="MONGO_HOST")
    mongo_port: int = Field(env="MONGO_PORT")
    TOPIC_NAME: str = Field(env="MONGO_DB")

    class Config:
        env_file = BASE_DIR / "env/mongo/.env.dev"


class JWT(BaseSettings):
    secret_key: str = Field(env="SECRET_KEY")

    class Config:
        env_file = BASE_DIR / "env/jwt/user/.env.dev"


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME")
    jwt = JWT()
    mongo = Mongo()

    class Config:
        env_file = BASE_DIR / "env/ugc/.env.dev"


config = Settings()
