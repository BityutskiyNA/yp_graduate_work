import pytest
from http import HTTPStatus

pytestmark = pytest.mark.asyncio


async def test_addlikefilm(mock_jwt_token, client):
    headers = {"Authorization": f"Bearer {await mock_jwt_token}"}
    message = {
        "movies_id": "421412412412",
        "review_id": "34324234",
        "review_text": "3ffsdfasfasfsafsafs",
    }
    response = client.post("/api/v1/reviews/addreviews", headers=headers, json=message)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "ok"}
