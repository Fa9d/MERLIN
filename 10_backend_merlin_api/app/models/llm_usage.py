"""Grand livre des coûts LLM — un événement par appel à l'API Anthropic.

Chaque appel (note de séance, synthèses, croisement, reflets, insights) laisse
une trace économique : modèle, tokens réels, coût calculé au tarif du modèle
au moment de l'appel. C'est la source de vérité des coûts d'analyse — fin des
forfaits estimés. AUCUN contenu n'est stocké ici : uniquement des compteurs.

Rattachements optionnels (séance, client, praticien, résultat d'analyse) pour
ventiler les bénéfices par séance et au général (console admin — Économie).
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LlmUsageEvent(Base):
    __tablename__ = "llm_usage_events"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    # Finalité de l'appel : session_note, journal_semantic, semantic_llm,
    # croisement, journal_reflet_client, praticien_reflet, behavioral_insights…
    purpose: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Coût en dollars US, calculé au tarif du modèle au moment de l'appel.
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    client_id: Mapped[str | None] = mapped_column(
        ForeignKey("clients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    praticien_user_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True
    )
    analysis_result_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True
    )
    created_by_user_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
