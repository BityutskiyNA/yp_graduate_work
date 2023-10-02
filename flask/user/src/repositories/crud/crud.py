from uuid import UUID

from src.databases.db import db_session
from src.models.role import Role
from src.models.session import Session
from src.models.token import Token
from src.models.user import User


class CRUDRepository:
    def __init__(self, model: User | Role | Session | Token) -> None:
        self.model = model
        self.colnames = list(self.model.__dict__["__annotations__"].keys())

    def create(self, data: dict) -> User | Role | Session | Token:
        try:
            model = self.model(**data)
            db_session.add(model)
            db_session.commit()
            return model
        except ValueError:
            print(f"input data:{data}, valid data:{self.colnames}")

    def create_all(
        self, data: list[dict]
    ) -> list[User] | list[Role] | list[Session] | list[Token]:
        models = []
        for row in data:
            try:
                models.append(self.model(**row))
            except ValueError:
                print(f"input data:{data}, valid data:{self.colnames}")
        db_session.add_all(models)
        db_session.commit()

    def get_all(
        self, page: int = 1, per_page: int = 10
    ) -> list[User] | list[Role] | list[Session] | list[Token] | None:
        models = (
            db_session.query(self.model)
            .limit(per_page)
            .offset((page - 1) * per_page)
            .all()
        )
        total = db_session.query(self.model).count()
        return models, total

    def get_by_id(self, id: UUID) -> User | Role | Session | Token | None:
        item = db_session.query(self.model).filter(self.model.id == id).first()
        if item is not None:
            return item
        else:
            raise ValueError("ID does not exist")

    def update_by_id(self, id: UUID, data: dict) -> None:
        item = db_session.query(self.model).filter(self.model.id == id)
        if item.first() is not None:
            try:
                item.update(data)
                db_session.commit()
            except ValueError:
                print(f"input data:{data}, valid data:{self.colnames}")
        else:
            raise ValueError("ID does not exist")

    def delete_by_id(self, id: UUID) -> None:
        item = db_session.query(self.model).filter(self.model.id == id)
        if item.first() is not None:
            item.delete()
            db_session.commit()
        else:
            raise ValueError(f"ID: {id} does not exist")

    def delete_all(self) -> None:
        db_session.query(self.model).delete()
        db_session.commit()
