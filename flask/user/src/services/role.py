from typing import TypedDict
from uuid import UUID

import config
from src.databases import cache
from src.databases.db import db_session
from src.models.role import Role
from src.models.session import Session
from src.models.user import User
from src.repositories.crud.crud_role import RoleCRUDRepository
from src.repositories.crud.crud_session import SessionCRUDRepository
from src.repositories.crud.crud_token import TokenCRUDRepository
from src.repositories.crud.crud_user import UserCRUDRepository
from src.repositories.jwt import JWTRepository


class RoleService:
    def __init__(
        self,
        role_crud_repository: RoleCRUDRepository = RoleCRUDRepository(),
    ) -> None:
        self._role_crud_repository = role_crud_repository

    def create(self, data: dict) -> Role:
        if data is None:
            raise ValueError("data cant be None")
        return self._role_crud_repository.create(data)

    def get_by_id(self, user_id: UUID) -> Role:
        if user_id is None:
            raise ValueError("user_id cant be None")
        return self._role_crud_repository.get_by_id(user_id)

    def get_by_name(self, name: str) -> Role:
        if name is None:
            raise ValueError("name cant be None")
        return self._role_crud_repository.get_by_name(name)

    def get_all(self, page: int = 1, per_page: int = 10) -> list[Role]:
        return self._role_crud_repository.get_all(page=page, per_page=per_page)

    def update_by_id(self, id: UUID, data: dict) -> None:
        if id is None:
            raise ValueError("id cant be None")
        if data is None:
            raise ValueError("data cant be None")
        return self._role_crud_repository.update_by_id(id, data)

    def delete_by_id(self, id: UUID) -> None:
        if id is None:
            raise ValueError("id cant be None")
        return self._role_crud_repository.delete_by_id(id)

    def delete_all(self) -> None:
        return self._role_crud_repository.delete_all()


role_crud_service = RoleService(RoleCRUDRepository())
