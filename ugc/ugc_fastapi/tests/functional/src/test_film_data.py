import pytest

pytestmark = pytest.mark.asyncio


async def test_addtorepository(mock_jwt_token, client):
    headers = {"Authorization": f"Bearer {await mock_jwt_token}"}
    message = {"id": "Nezhdanova_NA", "event_time": "Nezhdanova_NA"}
    response = client.post(
        "/api/v1/film_data/addtorepository", headers=headers, json=message
    )

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


async def test_incorrect_jwt(incorrect_mock_jwt_token, client):
    headers = {"Authorization": f"Bearer {await incorrect_mock_jwt_token}"}
    message = {"id": "Nezhdanova_NA", "event_time": "Nezhdanova_NA"}
    response = client.post(
        "/api/v1/film_data/addtorepository", headers=headers, json=message
    )

    assert response.status_code == 401


async def test_addtorepository_bad_data(mock_jwt_token, client):
    headers = {"Authorization": f"Bearer {await mock_jwt_token}"}
    message = {}
    response = client.post(
        "/api/v1/film_data/addtorepository", headers=headers, json=message
    )

    assert response.status_code == 400
    assert response.json() == {"message": "not ok"}
