from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.databases.db import db_session
from src.models.session import Session
from src.schemas.token import TokenSchema


class SessionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        include_fk = True
        sqla_session = db_session

    tokens = fields.Nested(TokenSchema, many=True)


session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)
