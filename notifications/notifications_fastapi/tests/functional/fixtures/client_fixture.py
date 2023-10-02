from pytest import fixture

from fastapi.testclient import TestClient

from main import app


@fixture
async def client():
    client = TestClient(app)
    return client
