from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import DataSensitivityClass, RecordStatus, RetentionClass


class DerivedDocument(Base):
    __tablename__ = "derived_documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"), nullable=False, index=True)
    source_note_id: Mapped[str] = mapped_column(
        ForeignKey("session_notes.id"),
        nullable=False,
        index=True,
    )
    document_kind_code: Mapped[str] = mapped_column(String(64), nullable=False, default="session_summary")
    audience_code: Mapped[str] = mapped_column(String(32), nullable=False, default="client")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    client_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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

    client = relationship("Client", back_populates="derived_documents")
    session = relationship("SessionRecord", back_populates="derived_documents")
    source_note = relationship("SessionNote", back_populates="derived_documents")
