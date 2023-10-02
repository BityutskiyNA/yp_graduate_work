from http import HTTPStatus

from app import models
from config import config
from src.databases.db import db_session
from src.repositories.cache import CacheRepository


def test_ok(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_sing_up(client):
    response = client.post(
        "/auth/register",
        json={
            "login": "test_sing_up",
            "password": "test_sing_up",
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_login(client):
    response = client.post(
        "/auth/login",
        json={
            "login": config.admin.login,
            "password": config.admin.password,
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_logout_AUTHORIZED(client, app):
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
    token = response.json["access_token"]
    response = client.delete(
        "/auth/logout", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
