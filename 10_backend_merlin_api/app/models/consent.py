from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import (
    ConsentTypeCode,
    GrantedByActorCode,
    RecordStatus,
    RevocationScopeCode,
)


class Consent(Base):
    __tablename__ = "consents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    session_id: Mapped[str | None] = mapped_column(ForeignKey("sessions.id"), nullable=True, index=True)
    consent_type_code: Mapped[ConsentTypeCode] = mapped_column(
        Enum(ConsentTypeCode, native_enum=False),
        nullable=False,
    )
    consent_value: Mapped[bool] = mapped_column(Boolean, nullable=False)
    consent_version_code: Mapped[str] = mapped_column(String(32), nullable=False, default="v1")
    granted_by_actor_code: Mapped[GrantedByActorCode] = mapped_column(
        Enum(GrantedByActorCode, native_enum=False),
        nullable=False,
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_scope_code: Mapped[RevocationScopeCode | None] = mapped_column(
        Enum(RevocationScopeCode, native_enum=False),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    client = relationship("Client", back_populates="consents")
    session = relationship("SessionRecord", back_populates="consents")
