from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, mapper, relationship
from src.databases.db import Base
from src.models import generate_uuid4


class Token(Base):
    __tablename__ = "token"

    # fields
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        ForeignKey("session.id", ondelete="CASCADE")
    )
    value: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False)
    deactivated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, unique=False
    )

    # relations
    session: Mapped["Session"] = relationship(back_populates="tokens")

    def __init__(self, session_id, value):
        self.id = generate_uuid4()
        self.session_id = session_id
        self.value = value
        self.is_active = True

    def __repr__(self):
        return f"<Session {self.id}>"
