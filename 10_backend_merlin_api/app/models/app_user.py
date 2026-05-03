from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.db.base import Base
from app.models.enums import AppRole, RecordStatus


class AppUser(Base):
    __tablename__ = "app_users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    legal_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_line: Mapped[str | None] = mapped_column(String(255), nullable=True)
    intro_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    presentation_audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    spoken_languages: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array
    available_channels: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array
    is_publicly_listed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    role: Mapped[AppRole] = mapped_column(
        Enum(AppRole, native_enum=False),
        nullable=False,
        default=AppRole.operator,
    )
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False),
        nullable=False,
        default=RecordStatus.active,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    email_verification_token: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

