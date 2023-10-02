from src.databases.db import db_session
from src.models.user import User
from src.repositories.crud.crud import CRUDRepository


class UserCRUDRepository(CRUDRepository):
    def __init__(self, model: User = User):
        super().__init__(model)

    def get_by_login(self, login: str) -> User | None:
        if login is None:
            raise ValueError("login cant be None")
        else:
            item = (
                db_session.query(self.model).filter(self.model.login == login).first()
            )
            if item is not None:
                return item
            else:
                raise ValueError(f"login: {login} does not exist")

    def get_by_id(self, id: str) -> User | None:
        if id is None:
            raise ValueError("id cant be None")
        else:
            item = db_session.query(self.model).filter(self.model.id == id).first()
            if item is not None:
                return item
            else:
                raise ValueError(f"User: {id} does not exist")

    def get_by_type(self, typeid: str) -> User | None:
        if typeid is None:
            raise ValueError("id cant be None")
        else:
            item = (
                db_session.query(self.model)
                .filter(self.model.message_type == typeid)
                .all()
            )
            if item is not None:
                return item
            else:
                raise ValueError(f"User: {typeid} does not exist")
