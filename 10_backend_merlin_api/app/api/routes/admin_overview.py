"""Vue d'ensemble admin — /admin/overview (réservé admin).

Chiffres clés du jour + alertes de vigilance (demandes et analyses en priorité/urgence
— escalade humaine, Loi 21). Agrège en une réponse pour le tableau de bord admin.
"""
import json
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import (
    IntakeHandlingStatusCode,
    PaymentOrderStatusCode,
    RiskLevelCode,
)
from app.models.intake_request import IntakeRequest
from app.models.payment_order import PaymentOrder
from app.models.session_note import SessionNote
from app.schemas.common import MerlinSchema

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/overview", tags=["admin-vue"])

_VIGILANCE = (RiskLevelCode.priority, RiskLevelCode.urgent)


class Alerte(MerlinSchema):
    type: str           # "demande" | "analyse"
    niveau: str
    label: str
    ref_id: str
    date: datetime | None


class Overview(MerlinSchema):
    comptes_total: int
    comptes_non_verifies: int
    comptes_recents_7j: int
    demandes_total: int
    demandes_nouvelles: int
    demandes_vigilance: int
    notes_vigilance: int
    encaisse_mois_cents: int
    alertes: list[Alerte]


def _is_test(order: PaymentOrder) -> bool:
    raw = order.metadata_json or ""
    if not raw:
        return order.amount_cents == 0
    try:
        meta = json.loads(raw)
    except Exception:
        return order.amount_cents == 0
    return bool(meta.get("free_test_grant") or meta.get("test_payment")) or order.amount_cents == 0


@router.get("", response_model=Overview)
def overview(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> Overview:
    now = datetime.now(timezone.utc)
    since_7j = now - timedelta(days=7)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    comptes_total = db.scalar(select(func.count()).select_from(AppUser)) or 0
    comptes_non_verifies = db.scalar(
        select(func.count()).select_from(AppUser).where(AppUser.email_verified.is_(False))
    ) or 0
    comptes_recents = db.scalar(
        select(func.count()).select_from(AppUser).where(AppUser.created_at >= since_7j)
    ) or 0

    demandes_total = db.scalar(select(func.count()).select_from(IntakeRequest)) or 0
    demandes_nouvelles = db.scalar(
        select(func.count()).select_from(IntakeRequest)
        .where(IntakeRequest.handling_status_code == IntakeHandlingStatusCode.new)
    ) or 0
    demandes_vigilance = db.scalar(
        select(func.count()).select_from(IntakeRequest)
        .where(
            (IntakeRequest.perceived_urgency_code.in_(_VIGILANCE))
            | (IntakeRequest.handling_status_code == IntakeHandlingStatusCode.vigilance)
        )
    ) or 0
    notes_vigilance = db.scalar(
        select(func.count()).select_from(SessionNote)
        .where(SessionNote.vigilance_level_code.in_(_VIGILANCE))
    ) or 0

    # Encaissé du mois (réel, hors paiements de test)
    paid = db.scalars(
        select(PaymentOrder)
        .where(PaymentOrder.status_code == PaymentOrderStatusCode.paid)
        .where(PaymentOrder.paid_at.isnot(None))
        .where(PaymentOrder.paid_at >= month_start)
    ).all()
    encaisse = sum(o.amount_cents for o in paid if not _is_test(o))

    # Alertes de vigilance (les plus récentes d'abord)
    alertes: list[Alerte] = []
    for d in db.scalars(
        select(IntakeRequest)
        .where(
            (IntakeRequest.perceived_urgency_code.in_(_VIGILANCE))
            | (IntakeRequest.handling_status_code == IntakeHandlingStatusCode.vigilance)
        )
        .order_by(IntakeRequest.created_at.desc()).limit(20)
    ):
        alertes.append(Alerte(
            type="demande", niveau=d.perceived_urgency_code.value,
            label=(d.entry_summary_text or d.primary_need_code.value)[:140],
            ref_id=d.id, date=d.created_at,
        ))
    for n in db.scalars(
        select(SessionNote).where(SessionNote.vigilance_level_code.in_(_VIGILANCE))
        .order_by(SessionNote.created_at.desc()).limit(20)
    ):
        alertes.append(Alerte(
            type="analyse", niveau=n.vigilance_level_code.value,
            label=(n.summary_text or "Analyse en vigilance")[:140],
            ref_id=n.id, date=n.created_at,
        ))
    alertes.sort(key=lambda a: a.date or now, reverse=True)

    return Overview(
        comptes_total=comptes_total, comptes_non_verifies=comptes_non_verifies,
        comptes_recents_7j=comptes_recents, demandes_total=demandes_total,
        demandes_nouvelles=demandes_nouvelles, demandes_vigilance=demandes_vigilance,
        notes_vigilance=notes_vigilance, encaisse_mois_cents=encaisse, alertes=alertes[:25],
    )
