# import config
# from src.models import User, Role, Session, Token
from datetime import datetime, timedelta
from uuid import UUID

import config
import jwt
from src.databases.db import db_session
from src.models.role import Role
from src.repositories.crud.crud import CRUDRepository


class RoleCRUDRepository(CRUDRepository):
    def __init__(self, model: Role = Role):
        super().__init__(model)

    def get_by_name(self, name: str) -> Role | None:
        if name is None:
            raise ValueError("name cant be None")
        else:
            item = db_session.query(self.model).filter(self.model.name == name).first()
            if item is not None:
                return item
            else:
                raise ValueError(f"name: {name} does not exist")
