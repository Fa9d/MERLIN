from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AudioProviderCode, AudioSessionStatusCode


class AudioSession(Base):
    __tablename__ = "audio_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    session_id: Mapped[str] = mapped_column(
        ForeignKey("sessions.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    provider_code: Mapped[AudioProviderCode] = mapped_column(
        Enum(AudioProviderCode, native_enum=False),
        nullable=False,
        default=AudioProviderCode.livekit,
    )
    audio_session_status_code: Mapped[AudioSessionStatusCode] = mapped_column(
        Enum(AudioSessionStatusCode, native_enum=False),
        nullable=False,
        default=AudioSessionStatusCode.provisioned,
    )
    room_name: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    provider_room_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recording_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    operator_participant_identity: Mapped[str] = mapped_column(String(120), nullable=False)
    client_participant_identity: Mapped[str] = mapped_column(String(120), nullable=False)
    practitioner_participant_identity: Mapped[str | None] = mapped_column(String(120), nullable=True)
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

    session = relationship("SessionRecord", back_populates="audio_session")
    recordings = relationship("AudioRecording", back_populates="audio_session")
