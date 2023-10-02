from fastapi.testclient import TestClient
from pytest import fixture

from main import app


@fixture
async def client():
    client = TestClient(app)
    return client
