from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.databases.db import db_session
from src.models.user import User
from src.schemas.role import RoleSchema
from src.schemas.session import SessionSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        sqla_session = db_session

    roles = fields.Nested("RoleSchema", many=True)
    sessions = fields.Nested("SessionSchema", many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
