import uuid
from http import HTTPStatus

import pytest
from config import config
from src.dataclasses.payload import PayloadDataclass
from tests.unit.test_data.dataclasses.test_payload import (
    generate_none_exp_data,
    generate_none_id_data,
    generate_none_is_admin_data,
    generate_none_is_refresh_data,
    generate_none_session_id_data,
    generate_none_token_data,
    generate_valid_data,
)

valid_data = generate_valid_data()
none_id_data = generate_none_id_data()
none_session_id = generate_none_session_id_data()
none_is_admin_data = generate_none_is_admin_data()
none_is_refresh_data = generate_none_is_refresh_data()
none_exp_data = generate_none_exp_data()
none_token_data = generate_none_token_data()


def test_payload_dataclass_valid():
    model = PayloadDataclass(**valid_data)
    assert model.id == valid_data["id"]


def test_payload_dataclass_none_id():
    try:
        model = PayloadDataclass(**none_id_data)
    except AssertionError as exc:
        assert "id cant be None"


def test_payload_dataclass_none_session_id():
    try:
        model = PayloadDataclass(**none_session_id)
    except AssertionError as exc:
        assert "session_id cant be None"


def test_payload_dataclass_none_is_admin():
    try:
        model = PayloadDataclass(**none_is_admin_data)
    except AssertionError as exc:
        assert "is_admin cant be None"


def test_payload_dataclass_none_is_refresh():
    try:
        model = PayloadDataclass(**none_is_refresh_data)
    except AssertionError as exc:
        assert "is_refresh cant be None"


def test_payload_dataclass_none_exp():
    try:
        model = PayloadDataclass(**none_exp_data)
    except AssertionError as exc:
        assert "exp cant be None"


def test_payload_dataclass_none_token():
    try:
        model = PayloadDataclass(**none_token_data)
    except AssertionError as exc:
        assert "token cant be None"
