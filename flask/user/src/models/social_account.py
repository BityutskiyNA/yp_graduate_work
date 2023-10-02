from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, or_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, backref, mapped_column, mapper, relationship
from src.databases.db import Base
from src.models import generate_now, generate_uuid4, user_role
from werkzeug.security import check_password_hash, generate_password_hash


class SocialAccount(Base):
    __tablename__ = "social_account"
    __table_args__ = (UniqueConstraint("social_id", "social_name", name="social_pk"),)

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(backref=backref("social_accounts", lazy=True))

    social_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True
    )
    social_name: Mapped[str] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=False
    )

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
