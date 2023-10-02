from pytest import fixture

from fastapi.testclient import TestClient

from src.core.config import app_settings
from src.main import app


@fixture
def client():
    app_settings.rabbit_user = "guest"
    app_settings.rabbit_password = "guest"
    app_settings.rabbit_host = "localhost"
    client = TestClient(app)
    return client
