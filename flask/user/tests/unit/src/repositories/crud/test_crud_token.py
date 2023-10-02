from src.databases.db import db_session
from src.models.token import Token
from src.repositories.crud.crud import CRUDRepository


class TokenCRUDRepository(CRUDRepository):
    def __init__(self, model: Token = Token):
        super().__init__(model)

    def get_by_value(self, value: str) -> Token | None:
        if value is None:
            raise ValueError("value cant be None")
        else:
            token = (
                db_session.query(self.model).filter(self.model.value == value).first()
            )
            if token is None:
                raise ValueError("value does not exist")
            else:
                return token

    def check_is_active(self, value: str) -> Token | None:
        if value is None:
            raise ValueError("value cant be None")
        else:
            return self.get_by_value(value).is_active

    def deactivate_refresh(self, session_id: str) -> None:
        if session_id is None:
            raise ValueError("value cant be None")
        else:
            all_tokens = (
                db_session.query(self.model)
                .filter(self.model.session_id == session_id)
                .all()
            )
            if all_tokens is None:
                raise ValueError("session does not exist")
            else:
                all_tokens[-1].is_active = False
                db_session.commit()
