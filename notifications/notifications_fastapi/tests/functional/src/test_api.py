import pytest

from tests.functional.testdata.data_for_test import (
    queue_1_data,
    queue_2_data,
    queue_3_data,
)

pytestmark = pytest.mark.asyncio


async def test_send_to_queue_by_type_of_message(client):
    message = queue_1_data
    response = client.post(
        "/api/v1/notifications/send_to_queue_by_type_of_message", json=message
    )

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


async def test_send_to_queue_by_specific_event(client):
    message = queue_2_data
    response = client.post(
        "/api/v1/notifications/send_to_queue_by_specific_event", json=message
    )

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


async def test_send_to_queue_by_event_type(client):
    message = queue_3_data
    response = client.post(
        "/api/v1/notifications/send_to_queue_by_event_type", json=message
    )

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


async def test_send_to_queue_by_type_of_message_bad_data(client):
    message = {}
    response = client.post(
        "/api/v1/notifications/send_to_queue_by_type_of_message", json=message
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "data"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "message_data"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }
