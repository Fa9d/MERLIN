from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import DataSensitivityClass, RecordStatus


def _public_client_code() -> str:
    return f"CLI-{uuid4().hex[:10].upper()}"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    public_client_code: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False,
        default=_public_client_code,
    )
    first_name_or_alias: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    language_code: Mapped[str] = mapped_column(String(16), nullable=False, default="fr-CA")
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="America/Toronto")
    territory_code: Mapped[str] = mapped_column(String(16), nullable=False, default="QC")
    is_adult_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
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

    intake_requests = relationship("IntakeRequest", back_populates="client")
    consents = relationship("Consent", back_populates="client")
    sessions = relationship("SessionRecord", back_populates="client")
