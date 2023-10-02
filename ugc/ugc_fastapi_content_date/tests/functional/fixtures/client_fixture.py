from pytest import fixture
from jose import jwt
from fastapi.testclient import TestClient
from src.main import app
from src.config import config


@fixture
async def mock_jwt_token():
    payload = {"user_id": "4dd40b60-d4de-4990-845a-ec0deb18e979"}
    secret_key = config.jwt.secret_key
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


@fixture
async def client():
    config.kafka.TOPIC_NAME = "test_database"
    client = TestClient(app)
    return client
