from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PractitionerProfile(Base):
    __tablename__ = "practitioner_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("app_users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    display_name:             Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    bio:                      Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    modalites:                Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    langues:                  Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    approches:                Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    public_visible:           Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepting_clients:        Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Legacy fields kept for compatibility with existing matching endpoints.
    title_line:               Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    intro_text:               Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    presentation_audio_url:   Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    domaines:            Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disponibilites:      Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tarif_horaire_cents: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    actif: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user: Mapped["AppUser"] = relationship("AppUser", back_populates="practitioner_profile")
