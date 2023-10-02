import uuid
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, ForeignKeyConstraint, Table
from sqlalchemy.dialects.postgresql import UUID
from src.databases.db import Base


def generate_now():
    return datetime.now()


def generate_uuid4():
    return uuid4()


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("user_created_at", DateTime, primary_key=True),
    Column("role_id", ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
    ForeignKeyConstraint(
        ("user_created_at", "user_id"), ("user.created_at", "user.id")
    ),
)

user_message_type = Table(
    "user_message_type",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("user_created_at", DateTime, primary_key=True),
    Column("message_type", ForeignKey("message_type.id", ondelete="CASCADE"), primary_key=True),
    ForeignKeyConstraint(
        ("user_created_at", "user_id"), ("user.created_at", "user.id")
    ),
)