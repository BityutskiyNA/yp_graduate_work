from pydantic import BaseSettings


class TestSettings(BaseSettings):
    test_service_url: str = "http://localhost:8006"

    class Config:
        env_file = ".env"


test_settings = TestSettings()
