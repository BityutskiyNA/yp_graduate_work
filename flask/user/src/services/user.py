from typing import TypedDict
from uuid import UUID

from config import config
from src.databases.cache import cache
from src.databases.db import db_session
from src.models.role import Role
from src.models.session import Session
from src.models.user import User
from src.repositories.crud.crud_role import RoleCRUDRepository
from src.repositories.crud.crud_session import SessionCRUDRepository
from src.repositories.crud.crud_token import TokenCRUDRepository
from src.repositories.crud.crud_user import UserCRUDRepository
from src.repositories.jwt import JWTRepository


class UserService:
    def __init__(
        self,
        user_crud_repository: UserCRUDRepository = UserCRUDRepository(),
        role_crud_repository: RoleCRUDRepository = RoleCRUDRepository(),
    ) -> None:
        self._user_crud_repository = user_crud_repository
        self._role_crud_repository = role_crud_repository

    def create(self, data: dict, roles: list[str]) -> User:
        if data is None:
            raise ValueError("data cant be None")
        if roles is None:
            raise ValueError("roles cant be None")
        user = self._user_crud_repository.create(data)
        user.roles = [self._role_crud_repository.get_by_name(role) for role in roles]
        db_session.commit()
        return user

    def get_by_id(self, user_id: UUID) -> User:
        if user_id is None:
            raise ValueError("user_id cant be None")
        return self._user_crud_repository.get_by_id(user_id)

    def get_by_login(self, login: str) -> User:
        if login is None:
            raise ValueError("login cant be None")
        return self._user_crud_repository.get_by_login(login)

    def get_all(self, page: int = 1, per_page: int = 10) -> list[User]:
        return self._user_crud_repository.get_all(page=page, per_page=per_page)

    def update_by_id(self, id: UUID, data: dict) -> None:
        if id is None:
            raise ValueError("id cant be None")
        if data is None:
            raise ValueError("data cant be None")
        self._user_crud_repository.update_by_id(id, data)

    def delete_by_id(self, id: UUID) -> None:
        if id is None:
            raise ValueError("id cant be None")
        return self._user_crud_repository.delete_by_id(id)

    def delete_all(self) -> None:
        return self._user_crud_repository.delete_all()


user_crud_service = UserService(UserCRUDRepository(), RoleCRUDRepository())
