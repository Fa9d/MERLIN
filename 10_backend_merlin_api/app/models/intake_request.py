from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import NeedCode, RecordStatus, RequestForCode, RiskLevelCode


class IntakeRequest(Base):
    __tablename__ = "intake_requests"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    request_channel_code: Mapped[str] = mapped_column(String(32), nullable=False)
    request_for_code: Mapped[RequestForCode] = mapped_column(
        Enum(RequestForCode, native_enum=False),
        nullable=False,
    )
    primary_need_code: Mapped[NeedCode] = mapped_column(
        Enum(NeedCode, native_enum=False),
        nullable=False,
    )
    perceived_urgency_code: Mapped[RiskLevelCode] = mapped_column(
        Enum(RiskLevelCode, native_enum=False),
        nullable=False,
        default=RiskLevelCode.non_urgent,
    )
    support_already_in_place: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    requested_outcome_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    entry_summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    referential_version: Mapped[str] = mapped_column(String(32), nullable=False, default="v1")
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

    client = relationship("Client", back_populates="intake_requests")
    sessions = relationship("SessionRecord", back_populates="intake_request")
