from typing import TypedDict
from uuid import UUID

from config import config
from src.databases.cache import cache
from src.databases.db import db_session
from src.dataclasses.payload import PayloadDataclass
from src.dataclasses.session import SessionDataclass
from src.models.role import Role
from src.models.session import Session
from src.models.user import User
from src.repositories.crud.crud_role import RoleCRUDRepository
from src.repositories.crud.crud_session import SessionCRUDRepository
from src.repositories.crud.crud_token import TokenCRUDRepository
from src.repositories.crud.crud_user import UserCRUDRepository
from src.repositories.jwt import JWTRepository


class ConstructedPayload(TypedDict):
    access: PayloadDataclass
    refresh: PayloadDataclass


class SessionService:
    def __init__(
        self,
        user_crud_repository: UserCRUDRepository = UserCRUDRepository(),
        session_crud_repository: SessionCRUDRepository = SessionCRUDRepository(),
        token_crud_repository: TokenCRUDRepository = TokenCRUDRepository(),
        jwt_repository: JWTRepository = JWTRepository(),
    ) -> None:
        self._user_crud_repository = user_crud_repository
        self._session_crud_repository = session_crud_repository
        self._token_crud_repository = token_crud_repository
        self._jwt_repository = jwt_repository

    def create(self, data: SessionDataclass) -> tuple[Session, str, str]:
        if data is None:
            raise ValueError("data cant be None")
        user_id = self.__get_user_id(data)
        user = self._user_crud_repository.get_by_id(id=user_id)
        data["user_created_at"] = user.created_at
        is_admin = self.__check_admin(user)
        session = self._session_crud_repository.create(data)
        session_id = self.__get_session_id(session)
        d_payloads = self.__construct_payloads(user_id, is_admin, session_id)
        access_token = self._jwt_repository.encode(payload=d_payloads["access"])
        refresh_token = self._jwt_repository.encode(payload=d_payloads["refresh"])
        refresh_token_model = self._token_crud_repository.create(
            {"session_id": session_id, "value": refresh_token}
        )
        session.tokens.append(refresh_token_model)
        user.sessions.append(session)
        db_session.commit()
        cache.setex(str(user_id), config.jwt.access_token_expires, access_token)
        token_id = refresh_token_model.id
        return access_token, refresh_token

    def get_by_id(self, id: UUID) -> Session:
        if id is None:
            raise ValueError("id cant be None")
        return self._session_crud_repository.get_by_id(id)

    def get_by_user_id(self, user_id: UUID) -> Session:
        if user_id is None:
            raise ValueError("user_id cant be None")
        return self._session_crud_repository.get_by_user_id(user_id)

    def get_all(self, page: int = 1, per_page: int = 10) -> list[Session]:
        return self._session_crud_repository.get_all(page=page, per_page=per_page)

    def update_by_id(self, id: UUID, data: dict) -> None:
        if id is None:
            raise ValueError("id cant be None")
        if data is None:
            raise ValueError("data cant be None")
        return self._session_crud_repository.update_by_id(id, data)

    def delete_by_id(self, id: UUID) -> None:
        if id is None:
            raise ValueError("id cant be None")
        return self._session_crud_repository.delete_by_id(id)

    def delete_by_user_id(self, user_id: UUID) -> None:
        if id is None:
            raise ValueError("id cant be None")
        return self._session_repository.delete_by_user_id(user_id)

    def delete_all(self) -> None:
        return self._session_repository.delete_all()

    def deactivate_refresh(self, session_id: str):
        if session_id is None:
            raise ValueError("session_id cant be None")
        self._token_crud_repository.deactivate_refresh(session_id)

    def is_active_refresh(self, value: str):
        if value is None:
            raise ValueError("value cant be None")
        return self._token_crud_repository.is_active(value)

    def refresh_token(self, token: str) -> tuple[str]:
        if token is None:
            raise ValueError("token cant be None")
        payload = self._token_process_repository.decode(token)
        del payload["exp"]
        del payload["is_refresh"]
        d_payloads = self.__construct_payloads(
            payload["user_id"], payload["is_admin"], payload["session_id"]
        )
        access_token = self._token_process_repository.encode(
            payload=d_payloads["access"]
        )
        refresh_token = self._token_process_repository.encode(
            payload=d_payloads["refresh"]
        )
        refresh_token_model = self._token_crud_repository.create(
            {"session_id": payload["session_id"], "value": refresh_token}
        )
        return access_token, refresh_token

    def __construct_payloads(self, user_id, is_admin, session_id) -> ConstructedPayload:
        if user_id is None:
            raise ValueError("user_id cant be None")
        if is_admin is None:
            raise ValueError("is_admin cant be None")
        if session_id is None:
            raise ValueError("session_id cant be None")
        d_payloads = {}
        for key, flag in zip(("refresh", "access"), (True, False)):
            payload = {
                "user_id": str(user_id),
                "is_admin": is_admin,
                "session_id": str(session_id),
                "is_refresh": flag,
            }
            d_payloads[key] = payload
        return d_payloads

    def __check_admin(self, user: User):
        if user is None:
            raise ValueError("user cant be None")
        return config.admin.admin_role in [r.name for r in user.roles]

    def __get_user_id(self, data: dict):
        if data is None:
            raise ValueError("data cant be None")
        return data["user_id"]

    def __get_session_id(self, session: SessionDataclass):
        if session is None:
            raise ValueError("session cant be None")
        return session.id


session_service = SessionService(
    UserCRUDRepository(),
    SessionCRUDRepository(),
    TokenCRUDRepository(),
    JWTRepository(),
)
