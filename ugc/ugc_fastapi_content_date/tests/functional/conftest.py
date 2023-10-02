from pytest import fixture
from jose import jwt
from fastapi.testclient import TestClient

from src.config import config
from src.main import app


@fixture
async def mock_jwt_token():
    payload = {"user_id": "4dd40b60-d4de-4990-845a-ec0deb18e979"}
    secret_key = "jwt_secret"
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


@fixture
async def incorrect_mock_jwt_token():
    payload = {"no_user_id": "4dd40b60-d4de-4990-845a-ec0deb18e979"}
    secret_key = "jwt_secret"
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


@fixture
def client():
    config.mongo.TOPIC_NAME = "test_database"
    client = TestClient(app)
    return client


# def pytest_sessionfinish(session, exitstatus):
#     port = config.kafka.kafka_port
#     host_name = config.kafka.kafka_host_name
#     client =  KafkaAdminClient(bootstrap_servers=f'{host_name}:{port}', )
#     topic = [NewTopic(name=config.kafka.TOPIC_NAME, num_partitions=1, replication_factor=1)]
#     client.delete_topics(topic)
#
#     client.close()
