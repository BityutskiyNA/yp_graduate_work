import pytest

from tests.functional.testdata.data_for_test import (
    test_message,
    test_campaign_data,
    test_promocode,
    test_history,
)


pytestmark = pytest.mark.asyncio


async def test_get_all_promocodes(client):
    message = test_message
    response = client.get("/api/v1/loyalty/get_all_promocodes", params=message)
    data = response.json()

    assert data["status"] == "success"
    assert response.status_code == 200


async def test_get_all_promocodes_by_campaign(client):
    message = test_campaign_data
    response = client.get(
        "/api/v1/loyalty/get_all_promocodes_by_campaign", params=message
    )
    data = response.json()

    assert data["status"] == "success"
    assert response.status_code == 200


async def test_get_campaign_info_by_promocode(client):
    message = test_promocode
    response = client.get("/api/v1/loyalty/get_campaign_info", params=message)
    data = response.json()

    assert data["status"] == "success"
    assert response.status_code == 200


async def test_add_promocode_history(client):
    message = test_history
    response = client.post("/api/v1/loyalty/add_promocode_history", json=message)
    data = response.json()

    assert data["status"] == "success"
    assert response.status_code == 200
