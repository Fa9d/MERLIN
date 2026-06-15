from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import (
    DataSensitivityClass,
    PaymentStatusCode,
    RecordStatus,
    RetentionClass,
    SessionChannelCode,
    SessionModeCode,
    SessionStatusCode,
)


class SessionRecord(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    intake_request_id: Mapped[str | None] = mapped_column(
        ForeignKey("intake_requests.id"),
        nullable=True,
        index=True,
    )
    session_sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    session_mode_code: Mapped[SessionModeCode] = mapped_column(
        Enum(SessionModeCode, native_enum=False),
        nullable=False,
        default=SessionModeCode.standard,
    )
    session_channel_code: Mapped[SessionChannelCode] = mapped_column(
        Enum(SessionChannelCode, native_enum=False),
        nullable=False,
        default=SessionChannelCode.audio_live,
    )
    scheduled_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    room_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    room_sid: Mapped[str | None] = mapped_column(String(160), nullable=True)
    egress_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    audio_file_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # Transcription persistée (faster-whisper / AssemblyAI) — relisible par le client.
    transcript_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Séance express : lien partageable (token hashé), statut de paiement, notes privées praticien.
    express_token_hash: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    payment_status: Mapped[PaymentStatusCode | None] = mapped_column(
        Enum(PaymentStatusCode, native_enum=False),
        nullable=True,
    )
    private_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    operator_user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    praticien_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id"), nullable=True, index=True
    )
    session_status_code: Mapped[SessionStatusCode] = mapped_column(
        Enum(SessionStatusCode, native_enum=False),
        nullable=False,
        default=SessionStatusCode.scheduled,
    )
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False),
        nullable=False,
        default=RecordStatus.active,
    )
    data_sensitivity_class: Mapped[DataSensitivityClass] = mapped_column(
        Enum(DataSensitivityClass, native_enum=False),
        nullable=False,
        default=DataSensitivityClass.high,
    )
    retention_class: Mapped[RetentionClass] = mapped_column(
        Enum(RetentionClass, native_enum=False),
        nullable=False,
        default=RetentionClass.standard,
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

    client = relationship("Client", back_populates="sessions")
    intake_request = relationship("IntakeRequest", back_populates="sessions")
    consents = relationship("Consent", back_populates="session")
    notes = relationship("SessionNote", back_populates="session")
    audio_session = relationship("AudioSession", back_populates="session", uselist=False)
    derived_documents = relationship("DerivedDocument", back_populates="session")
    temporal_anchors = relationship("SessionTemporalAnchor", back_populates="session")
