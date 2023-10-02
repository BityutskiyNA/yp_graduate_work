import uuid
from http import HTTPStatus

import pytest
from config import config
from src.dataclasses.auth import AuthDataclass
from tests.unit.test_data.dataclasses.test_auth import (
    generate_blank_login_data,
    generate_blank_password_data,
    generate_none_login_data,
    generate_none_password_data,
    generate_valid_data,
)

valid_data = generate_valid_data()
none_login_data = generate_none_login_data()
none_password_data = generate_none_password_data()
blank_password_data = generate_blank_password_data()
blank_login_data = generate_blank_login_data()


def test_auth_dataclass_valid():
    model = AuthDataclass(**valid_data)
    assert model.login == valid_data["login"]
    assert model.password == valid_data["password"]


def test_auth_dataclass_none_login():
    try:
        model = AuthDataclass(**none_login_data)
    except AssertionError as exc:
        assert "Login required"


def test_auth_dataclass_none_password():
    try:
        model = AuthDataclass(**none_password_data)
    except AssertionError as exc:
        assert "Password required"


def test_auth_dataclass_blank_password():
    try:
        model = AuthDataclass(**blank_password_data)
    except AssertionError as exc:
        assert "Password cant be blank"


def test_auth_dataclass_login_password():
    try:
        model = AuthDataclass(**blank_login_data)
    except AssertionError as exc:
        assert "Login cant be blank"
