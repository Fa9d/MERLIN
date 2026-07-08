"""Modèles pour profils audio praticiens."""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PractitionerAudioProfile(Base):
    """Profil audio praticien : enregistrement vocal introductif."""
    __tablename__ = "practitioner_audio_profiles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    practitioner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    s3_key: Mapped[str | None] = mapped_column(
        String(255), nullable=True, unique=True
    )
    s3_presigned_url: Mapped[str | None] = mapped_column(
        String(2048), nullable=True  # Presigned URL (max 2000 chars)
    )
    presigned_url_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_size_kb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relations
    practitioner: Mapped["app.models.app_user.AppUser"] = relationship(  # type: ignore[name-defined]
        "AppUser", foreign_keys=[practitioner_id]
    )
