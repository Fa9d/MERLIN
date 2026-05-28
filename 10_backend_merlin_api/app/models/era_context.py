"""
era_context — référentiel des contextes sociétaux par période et territoire.
Alimenté par IVIA, utilisé pour ancrer les événements biographiques dans
leur époque (normes, économie, structure familiale, droits).
"""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EraContext(Base):
    __tablename__ = "era_contexts"

    # tag court unique : ex "QC_recession_1980", "QC_loi_101_1977"
    tag: Mapped[str] = mapped_column(String(80), primary_key=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    period_start: Mapped[int] = mapped_column(Integer, nullable=False)
    period_end: Mapped[int | None] = mapped_column(Integer, nullable=True)
    territory_code: Mapped[str] = mapped_column(String(16), nullable=False, default="QC")

    # Données structurées libres :
    # { economic, gender_norms, family_structure, rights, key_events[], notes }
    data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    life_events = relationship("ClientLifeEvent", back_populates="era")
