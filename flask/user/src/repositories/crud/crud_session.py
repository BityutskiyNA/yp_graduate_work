from uuid import UUID

from src.databases.db import db_session
from src.models.session import Session
from src.repositories.crud.crud import CRUDRepository


class SessionCRUDRepository(CRUDRepository):
    def __init__(self, model: Session = Session):
        super().__init__(model)

    def get_by_user_id(self, user_id: UUID) -> Session:
        if user_id is None:
            raise ValueError("user_id cant be None")
        else:
            data = db_session.query(Session).filter(Session.user_id == user_id).all()
            if len(data) == 0:
                raise ValueError("No records")
            else:
                return data

    def delete_by_user_id(self, user_id: UUID) -> None:
        if user_id is None:
            raise ValueError("user_id cant be None")
        else:
            sessions = db_session.query(self.model).filter(
                self.model.user_id == user_id
            )
            if sessions.count() == 0:
                raise ValueError("No records")
            else:
                sessions.delete()
                db_session.commit()
