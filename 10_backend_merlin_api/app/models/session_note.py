from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import (
    AnalysisNextStepCode,
    DataSensitivityClass,
    RecordStatus,
    RetentionClass,
    RiskLevelCode,
)


class SessionNote(Base):
    __tablename__ = "session_notes"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"), nullable=False, index=True)
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    note_sequence_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    observations_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_actions_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_session_focus_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    coeur_summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    corps_summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    esprit_summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    etre_summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    immediate_context_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    context_factors_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    context_hypotheses_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    identified_tensions_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    vigilance_level_code: Mapped[RiskLevelCode] = mapped_column(
        Enum(RiskLevelCode, native_enum=False),
        nullable=False,
        default=RiskLevelCode.non_urgent,
    )
    next_step_type_code: Mapped[AnalysisNextStepCode | None] = mapped_column(
        Enum(AnalysisNextStepCode, native_enum=False),
        nullable=True,
    )
    client_facing_summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    supervision_summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_notes_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(128), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    complexity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    validated_by_practitioner: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    validated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    practitioner_corrections: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
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

    session = relationship("SessionRecord", back_populates="notes")
    client = relationship("Client")
    derived_documents = relationship("DerivedDocument", back_populates="source_note")
