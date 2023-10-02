from pydantic import BaseSettings


class TestSettings(BaseSettings):
    elastic_host: str
    elastic_port: str = "9200"

    es_id_field: str = "id"

    redis_film_host: str
    redis_film_port: str

    service_url: str
    service_port: str = "8001"

    class Config:
        env_file = ".env"


test_settings = TestSettings()
