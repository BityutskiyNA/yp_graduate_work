from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text, UniqueConstraint, or_, text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, mapper, relationship
from src.databases.db import Base
from src.models import generate_now, generate_uuid4, user_role, user_message_type
from werkzeug.security import check_password_hash, generate_password_hash


def create_partition(target, connection, **kw) -> None:
    table_quarter = create_table_quarter()
    for x in table_quarter:
        text_sql = f"""
                    CREATE TABLE IF NOT EXISTS "{x}"
                    PARTITION OF "user" FOR VALUES FROM ('{table_quarter[x][0]}') TO ('{table_quarter[x][1]}')"""
        text_sql = text(text_sql)
        connection.execute(text_sql)


def create_table_quarter() -> dict:
    return {
        "user_2023_1_kv": ["2023-01-01", "2023-03-31"],
        "user_2023_2_kv": ["2023-04-01", "2023-06-30"],
        "user_2023_3_kv": ["2023-07-01", "2023-10-30"],
        "user_2023_4_kv": ["2023-11-01", "2023-12-31"],
        "user_2024_1_kv": ["2024-04-01", "2024-06-30"],
        "user_2024_2_kv": ["2024-07-01", "2024-10-30"],
        "user_2024_3_kv": ["2024-11-01", "2024-12-31"],
        "user_2024_4_kv": ["2024-01-01", "2024-03-31"],
    }


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("id", "created_at"),
        {
            "postgresql_partition_by": "RANGE (created_at)",
            "listeners": [("after_create", create_partition)],
        },
    )
    # fields
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    login: Mapped[str] = mapped_column(String, nullable=False, primary_key=False)
    password: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, primary_key=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, primary_key=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=False)
    social_id: Mapped[str] = mapped_column(String, nullable=True)
    fio: Mapped[str] = mapped_column(String, nullable=True)
    time_zone: Mapped[int] = mapped_column(Integer, nullable=True)
    email_confirmed: Mapped[str] = mapped_column(Boolean, nullable=True)
    # relations
    sessions: Mapped[list["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete", passive_deletes=True
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary=user_role,
        back_populates="users",
        cascade="all, delete",
        passive_deletes=True,
    )
    message_type: Mapped[list["Message_type"]] = relationship(
        secondary=user_message_type,
        back_populates="users",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(self, login, password, email, social_id=None):
        dt_now = generate_now()
        self.id = generate_uuid4()
        self.login = login
        self.password = generate_password_hash(password, "scrypt")
        self.email = email
        self.social_id = social_id
        self.created_at = dt_now
        self.updated_at = dt_now

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None, email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first()

    def is_password_valid(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.login}>"
