"""Restitutions au client — étape 4 du chantier Analyses.

Une restitution (`AnalysisDelivery`) est la version CLIENT d'une analyse :
la triade Observation / Hypothèse / Orientation, RELUE ET ÉDITÉE par le
praticien avant livraison (validation humaine constitutionnelle — rien ne
part automatiquement d'un modèle vers un client).

- Jamais de scores, d'étiquettes ni de contenu brut d'analyse : trois champs
  de texte libre, filtrés Loi 21 à l'écriture.
- Traçabilité complète : l'analyse source, la séance, qui a livré, quand.
- La suppression d'une restitution est un retrait (record_status), pas un
  effacement — le registre reste.
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import RecordStatus


class AnalysisDelivery(Base):
    __tablename__ = "analysis_deliveries"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    analysis_result_id: Mapped[str] = mapped_column(
        ForeignKey("analysis_results.id", ondelete="CASCADE"), nullable=False, index=True
    )
    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True
    )
    delivered_by_user_id: Mapped[str] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"), nullable=False
    )
    # La triade, dans les mots du praticien (relue/éditée avant livraison)
    observation: Mapped[str] = mapped_column(Text, nullable=False)
    hypothese: Mapped[str] = mapped_column(Text, nullable=False)
    orientation: Mapped[str] = mapped_column(Text, nullable=False)
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False),
        nullable=False,
        default=RecordStatus.active,
    )
    delivered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
