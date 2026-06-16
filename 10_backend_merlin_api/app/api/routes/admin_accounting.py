"""Grand livre & comptabilité — /admin/accounting (réservé admin).

Ventile chaque encaissement via billing.revenue_breakdown : HT, TPS, TVQ, frais
Stripe, coût IA, part praticien, marge. Sépare le RÉEL des paiements de TEST
(parcours gratuit ou paiement simulé), exclus des totaux réels.
"""
import json
import logging
from datetime import date, datetime, time, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import PaymentOrderStatusCode
from app.models.payment_order import PaymentOrder
from app.schemas.common import MerlinSchema
from app.services import billing

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/accounting", tags=["admin-comptabilite"])


class LedgerRow(MerlinSchema):
    order_id: str
    date: datetime | None
    product_label: str
    product_code: str
    currency: str
    is_test: bool
    ttc: int
    ht: int
    tps: int
    tvq: int
    frais_stripe: int
    cout_ia: int
    part_praticien: int
    marge_ivia: int


class AccountingSummary(MerlinSchema):
    date_from: date
    date_to: date
    tax_registered: bool
    # Totaux RÉELS (hors paiements de test), en cents
    nb_reel: int
    ttc: int
    ht: int
    tps: int
    tvq: int
    frais_stripe: int
    cout_ia: int
    part_praticien: int
    marge_ivia: int
    # Test (pour info)
    nb_test: int
    ttc_test: int


def _is_test(order: PaymentOrder) -> bool:
    raw = order.metadata_json or ""
    if not raw:
        return order.amount_cents == 0
    try:
        meta = json.loads(raw)
    except Exception:
        return order.amount_cents == 0
    return bool(meta.get("free_test_grant") or meta.get("test_payment")) or order.amount_cents == 0


def _paid_orders(db: Session, date_from: date, date_to: date) -> list[PaymentOrder]:
    start = datetime.combine(date_from, time.min, tzinfo=timezone.utc)
    end = datetime.combine(date_to, time.max, tzinfo=timezone.utc)
    stmt = (
        select(PaymentOrder)
        .where(PaymentOrder.status_code == PaymentOrderStatusCode.paid)
        .where(PaymentOrder.paid_at.isnot(None))
        .where(PaymentOrder.paid_at >= start)
        .where(PaymentOrder.paid_at <= end)
        .order_by(PaymentOrder.paid_at.desc())
    )
    return list(db.scalars(stmt))


@router.get("/ledger", response_model=list[LedgerRow])
def ledger(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> list[LedgerRow]:
    rows: list[LedgerRow] = []
    for o in _paid_orders(db, date_from, date_to):
        test = _is_test(o)
        # En test, aucun frais réel ; sinon estimation (le réel viendra du webhook Stripe).
        b = billing.revenue_breakdown(
            o.amount_cents,
            stripe_fee_cents=0 if test else None,
            ai_cost_cents=None,
        )
        rows.append(LedgerRow(
            order_id=o.id, date=o.paid_at, product_label=o.product_label,
            product_code=o.product_code, currency=o.currency, is_test=test, **b,
        ))
    return rows


@router.get("/summary", response_model=AccountingSummary)
def summary(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AccountingSummary:
    from app.core.config import settings

    agg = {k: 0 for k in ("ttc", "ht", "tps", "tvq", "frais_stripe", "cout_ia", "part_praticien", "marge_ivia")}
    nb_reel = nb_test = ttc_test = 0
    for o in _paid_orders(db, date_from, date_to):
        if _is_test(o):
            nb_test += 1
            ttc_test += o.amount_cents
            continue
        nb_reel += 1
        b = billing.revenue_breakdown(o.amount_cents)
        for k in agg:
            agg[k] += b[k]
    return AccountingSummary(
        date_from=date_from, date_to=date_to,
        tax_registered=settings.tax_registered,
        nb_reel=nb_reel, nb_test=nb_test, ttc_test=ttc_test, **agg,
    )
