import uuid
from http import HTTPStatus

import pytest
from config import config
from src.dataclasses.session import SessionDataclass
from tests.unit.test_data.dataclasses.test_session import (
    generate_none_user_agent_data,
    generate_none_user_id_data,
    generate_valid_data,
)

valid_data = generate_valid_data()
none_user_id_data = generate_none_user_id_data()
none_user_agent_data = generate_none_user_agent_data()


def test_payload_dataclass_valid():
    model = SessionDataclass(**valid_data)
    assert model.user_id == valid_data["user_id"]


def test_payload_dataclass_none_id():
    try:
        model = SessionDataclass(**none_user_id_data)
    except AssertionError as exc:
        assert "user_id cant be None"


def test_payload_dataclass_none_session_id():
    try:
        model = SessionDataclass(**none_user_agent_data)
    except AssertionError as exc:
        assert "user_agent cant be None"
