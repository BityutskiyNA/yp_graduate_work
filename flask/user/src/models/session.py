from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, mapper, relationship
from src.databases.db import Base
from src.models import generate_now, generate_uuid4


class Session(Base):
    __tablename__ = "session"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "user_created_at"], ["user.id", "user.created_at"]
        ),
    )
    # fields
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True))
    user_created_at: Mapped[str] = mapped_column(DateTime)
    user_agent: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    authenticated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, unique=False
    )

    # relations
    user: Mapped["User"] = relationship(back_populates="sessions")
    tokens: Mapped[list["Token"]] = relationship(
        back_populates="session", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, user_id, user_agent, user_created_at):
        self.id = generate_uuid4()
        self.user_created_at = user_created_at
        self.user_id = user_id
        self.user_agent = user_agent
        self.authenticated_at = generate_now()

    def __repr__(self):
        return f"<Session {self.id}>"
