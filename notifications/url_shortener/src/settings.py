from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """Настройки приложения."""

    gevent_workers: int = 1
    debug: int = 1
    port: int = 5001
    host: str = "127.0.0.1"

    class Config:
        env_prefix = "SHORTENER_APP_"
        env_file = "../.env"


class RedisSettings(BaseSettings):
    """Настройки подключения к Redis."""

    host: str = "127.0.0.1"
    port: int = 6382
    TTL: int = 300
    password: str = "root"

    class Config:
        env_prefix = "SHORTENER_REDIS_"
        env_file = "../.env"


app_settings = AppSettings()
redis_settings = RedisSettings()
