from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AudioProviderCode, AudioRecordingStatusCode


class AudioRecording(Base):
    __tablename__ = "audio_recordings"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    audio_session_id: Mapped[str] = mapped_column(
        ForeignKey("audio_sessions.id"),
        nullable=False,
        index=True,
    )
    provider_code: Mapped[AudioProviderCode] = mapped_column(
        Enum(AudioProviderCode, native_enum=False),
        nullable=False,
    )
    audio_recording_status_code: Mapped[AudioRecordingStatusCode] = mapped_column(
        Enum(AudioRecordingStatusCode, native_enum=False),
        nullable=False,
        default=AudioRecordingStatusCode.starting,
    )
    provider_recording_id: Mapped[str | None] = mapped_column(String(160), nullable=True, index=True)
    output_location: Mapped[str | None] = mapped_column(String(512), nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    requested_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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

    audio_session = relationship("AudioSession", back_populates="recordings")
