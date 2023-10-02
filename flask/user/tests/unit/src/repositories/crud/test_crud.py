import uuid
from http import HTTPStatus
from uuid import UUID

import pytest
from src.databases.db import db_session
from src.models.role import Role
from src.models.session import Session
from src.models.token import Token
from src.models.user import User
from src.repositories.crud.crud import CRUDRepository

role_repository = CRUDRepository(Role)
role = {"name": "test"}
many_roles = [{"name": "test2"}, {"name": "test3"}]


def test_role_crud_create():
    role_repository.create(role)


def test_role_crud_create_all():
    role_repository.create_all(many_roles)


def test_role_crud_get_all():
    t_many_roles = role_repository.get_all()
    assert len(t_many_roles) >= len(many_roles)


def test_role_crud_get_by_id():
    t_all_roles = role_repository.get_all()
    id = t_all_roles[-1].id
    t_role = role_repository.get_by_id(id)
    assert t_role.name == many_roles[-1]["name"]


def test_role_crud_get_by_id_wrong():
    id = uuid.uuid4()
    try:
        role_repository.get_by_id(id)
    except ValueError as exc:
        assert "ID does not exist"


def test_role_crud_update_by_id():
    t_all_roles = role_repository.get_all()
    id = t_all_roles[-1].id
    role_repository.update_by_id(id=id, data={"name": "changed_name"})
    changed_role = role_repository.get_by_id(id)
    assert changed_role.name == "changed_name"


def test_role_crud_delete_by_id():
    t_all_roles = role_repository.get_all()
    count_before = len(t_all_roles)
    id = t_all_roles[-1].id
    role_repository.delete_by_id(id=id)
    count_after = len(role_repository.get_all())
    assert count_after == count_before - 1


def test_role_crud_delete_all():
    role_repository.delete_all()
    count_after = len(role_repository.get_all())
    assert count_after == 0


def test_user_crud_create_all():
    pass


def test_user_crud_get_all():
    pass


def test_user_crud_get_by_id():
    pass


def test_user_crud_update_by_id():
    pass


def test_user_crud_delete_by_id():
    pass


def test_user_crud_delete_all():
    pass


def test_session_crud_create_all():
    pass


def test_session_crud_get_all():
    pass


def test_session_crud_get_by_id():
    pass


def test_session_crud_update_by_id():
    pass


def test_session_crud_delete_by_id():
    pass


def test_session_crud_delete_all():
    pass


def test_token_crud_create_all():
    pass


def test_token_crud_get_all():
    pass


def test_token_crud_get_by_id():
    pass


def test_token_crud_update_by_id():
    pass


def test_token_crud_delete_by_id():
    pass


def test_token_crud_delete_all():
    pass
