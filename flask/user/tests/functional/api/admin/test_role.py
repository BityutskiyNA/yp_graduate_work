import json
from http import HTTPStatus

from app import models
from config import config
from src.databases.db import db_session
from src.repositories.cache import CacheRepository


def _load_json_data(role):
    return json.loads(role.get_data())["data"]


def authorization_superuser(client):
    model_user = models["user"]
    admin_user = (
        db_session.query(model_user)
        .filter(model_user.login == config.admin.login)
        .first()
    )
    CacheRepository.block(admin_user.id)
    response = client.post(
        "/auth/login",
        json={
            "login": config.admin.login,
            "password": config.admin.password,
        },
    )
    return response


def create_role(client, token, name):
    response = client.post(
        "/admin/role",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name,
        },
    )
    return response


def test_role_create(client, app):
    response = authorization_superuser(client)

    token = response.json["access_token"]
    response = create_role(client, token, "test_role_create")

    assert response.status_code == HTTPStatus.OK


def test_role_retrieve(client, app):
    response = authorization_superuser(client)

    token = response.json["access_token"]

    role = create_role(client, token, "test_role_retrieve")

    role_id = _load_json_data(role)["id"]

    response = client.get(
        f"/admin/role/{role_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_role_retrieve_all(client, app):
    response = authorization_superuser(client)

    token = response.json["access_token"]

    role = create_role(client, token, "test_role_retrieve_all")

    response = client.get(
        "/admin/roles",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_role_update(client, app):
    response = authorization_superuser(client)
    token = response.json["access_token"]
    role = create_role(client, token, "test_role_update")
    role_id = _load_json_data(role)["id"]
    response = client.put(
        f"/admin/role/{role_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "test_up",
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_role_delete(client, app):
    response = authorization_superuser(client)
    token = response.json["access_token"]
    role = create_role(client, token, "test_role_delete")
    role_id = _load_json_data(role)["id"]
    response = client.delete(
        f"/admin/role/{role_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
