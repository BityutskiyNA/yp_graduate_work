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
