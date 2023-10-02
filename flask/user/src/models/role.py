from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, mapper, relationship
from src.databases.db import Base
from src.models import generate_now, generate_uuid4, user_role


class Role(Base):
    __tablename__ = "role"

    # fields
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=False)

    # relations
    users: Mapped[list["User"]] = relationship(
        secondary=user_role, back_populates="roles", passive_deletes=True
    )

    def __init__(self, name):
        dt_now = generate_now()
        self.id = generate_uuid4()
        self.name = name
        self.created_at = dt_now
        self.updated_at = dt_now

    def __repr__(self):
        return f"<Role {self.name}>"
