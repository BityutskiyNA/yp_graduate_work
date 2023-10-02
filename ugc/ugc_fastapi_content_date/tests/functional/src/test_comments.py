import pytest
from http import HTTPStatus

pytestmark = pytest.mark.asyncio


async def test_addcomment(mock_jwt_token, client):
    headers = {"Authorization": f"Bearer {await mock_jwt_token}"}
    message = {
        "movies_id": "421412412412",
        "comment_id": "421412412412",
        "comment_text": "421412412412",
    }
    response = client.post("/api/v1/comments/addcomment", headers=headers, json=message)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "ok"}
