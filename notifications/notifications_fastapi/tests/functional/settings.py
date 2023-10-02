from pydantic import BaseSettings


class TestSettings(BaseSettings):
    rabbit_host: str = "localhost"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_password: str = "guest"

    test_service_url: str = "http://localhost:8004"

    class Config:
        env_file = ".env"


test_settings = TestSettings()
