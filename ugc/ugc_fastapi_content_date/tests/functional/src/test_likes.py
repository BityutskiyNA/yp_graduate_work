import pytest
from http import HTTPStatus

pytestmark = pytest.mark.asyncio


async def test_addlikefilm(mock_jwt_token, client):
    headers = {"Authorization": f"Bearer {await mock_jwt_token}"}
    message = {"movies_id": "421412412412", "like": 10}
    response = client.post("/api/v1/likes/addlikefilm", headers=headers, json=message)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "ok"}
