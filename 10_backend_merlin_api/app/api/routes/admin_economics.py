"""Économie des analyses — /admin/economics (réservé admin).

Croise le grand livre des coûts LLM réels (`llm_usage_events`) avec les
encaissements (`payment_orders`) pour donner :
- le sommaire de période : revenus réels, coûts IA réels (par finalité, par
  modèle), bénéfice net ;
- la ventilation PAR SÉANCE : revenu rattaché (via appointments), coût IA de
  la séance (note + analyses), bénéfice.

Les coûts sont mesurés en USD (facturation Anthropic) et convertis en CAD au
taux `MERLIN_USD_CAD_RATE` — approximation d'affichage, le réel vient du
relevé. Les paiements de TEST sont exclus des revenus (même règle que le
grand livre comptable).
"""
import logging
from datetime import date, datetime, time, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.routes.admin_accounting import _breakdown_for, _is_test
from app.core.deps import require_admin
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.appointment import Appointment
from app.models.enums import PaymentOrderStatusCode
from app.models.llm_usage import LlmUsageEvent
from app.models.payment_order import PaymentOrder
from app.models.session import SessionRecord
from app.schemas.common import MerlinSchema
from app.services import llm_ledger

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/economics", tags=["admin-economie"])


class CostBucket(MerlinSchema):
    nb_appels: int
    input_tokens: int
    output_tokens: int
    cost_usd: float
    cost_cad_cents: int


class EconomicsSummary(MerlinSchema):
    date_from: date
    date_to: date
    usd_cad_rate: float
    # Revenus RÉELS (hors test), cents CAD — même ventilation que la comptabilité
    nb_encaissements: int
    revenus_ttc: int
    revenus_ht: int
    marge_ivia_avant_ia: int
    # Coûts IA réels mesurés
    couts: CostBucket
    par_finalite: dict[str, CostBucket]
    par_modele: dict[str, CostBucket]
    # Bénéfice net = marge IVIA (HT − Stripe − part praticien) − coûts IA réels
    benefice_net_cad_cents: int


class SessionEconomics(MerlinSchema):
    session_id: str
    date: datetime | None
    praticien: str | None
    session_type_code: str | None
    statut: str | None
    nb_appels_ia: int
    cout_ia_usd: float
    cout_ia_cad_cents: int
    revenu_ttc_cents: int | None
    revenu_ivia_cents: int | None  # frais plateforme si ventilé, sinon marge estimée
    is_test: bool | None
    benefice_cad_cents: int | None  # revenu_ivia − coût IA (None si aucun paiement)


def _bucket(rows) -> CostBucket:
    nb = len(rows)
    tin = sum(r.input_tokens for r in rows)
    tout = sum(r.output_tokens for r in rows)
    usd = sum(r.cost_usd for r in rows)
    return CostBucket(
        nb_appels=nb, input_tokens=tin, output_tokens=tout,
        cost_usd=round(usd, 6), cost_cad_cents=llm_ledger.usd_to_cad_cents(usd),
    )


@router.get("/summary", response_model=EconomicsSummary)
def economics_summary(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _admin: AppUser = Depends(require_admin()),
) -> EconomicsSummary:
    today = datetime.now(timezone.utc).date()
    dfrom = date_from or today.replace(day=1)
    dto = date_to or today
    start = datetime.combine(dfrom, time.min, tzinfo=timezone.utc)
    end = datetime.combine(dto, time.max, tzinfo=timezone.utc)

    events = list(
        db.execute(
            select(LlmUsageEvent).where(
                LlmUsageEvent.occurred_at >= start, LlmUsageEvent.occurred_at <= end
            )
        ).scalars()
    )
    par_finalite: dict[str, list] = {}
    par_modele: dict[str, list] = {}
    for e in events:
        par_finalite.setdefault(e.purpose, []).append(e)
        par_modele.setdefault(e.model, []).append(e)

    orders = list(
        db.execute(
            select(PaymentOrder).where(
                PaymentOrder.status_code == PaymentOrderStatusCode.paid,
                PaymentOrder.paid_at >= start,
                PaymentOrder.paid_at <= end,
            )
        ).scalars()
    )
    nb = ttc = ht = marge = 0
    for o in orders:
        if _is_test(o):
            continue
        # coût IA réel mesuré séparément → on neutralise le forfait estimé ici
        bd = _breakdown_for(o, False)
        nb += 1
        ttc += bd["ttc"]
        ht += bd["ht"]
        marge += bd["marge_ivia"] + bd["cout_ia"]  # marge AVANT IA (forfait ré-ajouté)

    couts = _bucket(events)
    return EconomicsSummary(
        date_from=dfrom,
        date_to=dto,
        usd_cad_rate=llm_ledger.usd_to_cad_cents(1.0) / 100,
        nb_encaissements=nb,
        revenus_ttc=ttc,
        revenus_ht=ht,
        marge_ivia_avant_ia=marge,
        couts=couts,
        par_finalite={k: _bucket(v) for k, v in sorted(par_finalite.items())},
        par_modele={k: _bucket(v) for k, v in sorted(par_modele.items())},
        benefice_net_cad_cents=marge - couts.cost_cad_cents,
    )


@router.get("/sessions", response_model=list[SessionEconomics])
def economics_by_session(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    _admin: AppUser = Depends(require_admin()),
) -> list[SessionEconomics]:
    """Les séances récentes qui ont généré au moins un appel IA, avec revenu et bénéfice."""
    session_ids = [
        row[0]
        for row in db.execute(
            select(LlmUsageEvent.session_id, func.max(LlmUsageEvent.occurred_at).label("last"))
            .where(LlmUsageEvent.session_id.is_not(None))
            .group_by(LlmUsageEvent.session_id)
            .order_by(func.max(LlmUsageEvent.occurred_at).desc())
            .limit(limit)
        )
    ]
    if not session_ids:
        return []

    events_by_session: dict[str, list] = {}
    for e in db.execute(
        select(LlmUsageEvent).where(LlmUsageEvent.session_id.in_(session_ids))
    ).scalars():
        events_by_session.setdefault(e.session_id, []).append(e)

    records = {
        r.id: r
        for r in db.execute(
            select(SessionRecord).where(SessionRecord.id.in_(session_ids))
        ).scalars()
    }
    praticien_ids = {r.praticien_id for r in records.values() if r.praticien_id}
    praticiens = {
        u.id: u.display_name
        for u in db.execute(select(AppUser).where(AppUser.id.in_(praticien_ids))).scalars()
    } if praticien_ids else {}

    # Revenu par séance : appointment lié → payment_order payé
    appts = list(
        db.execute(
            select(Appointment).where(
                Appointment.session_id.in_(session_ids),
                Appointment.payment_order_id.is_not(None),
            )
        ).scalars()
    )
    order_by_session: dict[str, PaymentOrder] = {}
    if appts:
        orders = {
            o.id: o
            for o in db.execute(
                select(PaymentOrder).where(
                    PaymentOrder.id.in_([a.payment_order_id for a in appts]),
                    PaymentOrder.status_code == PaymentOrderStatusCode.paid,
                )
            ).scalars()
        }
        for a in appts:
            if a.session_id and a.payment_order_id in orders:
                order_by_session[a.session_id] = orders[a.payment_order_id]

    out: list[SessionEconomics] = []
    for sid in session_ids:
        rec = records.get(sid)
        evs = events_by_session.get(sid, [])
        usd = sum(e.cost_usd for e in evs)
        cad = llm_ledger.usd_to_cad_cents(usd)
        order = order_by_session.get(sid)
        revenu_ttc = revenu_ivia = benefice = None
        is_test = None
        if order is not None:
            is_test = _is_test(order)
            bd = _breakdown_for(order, is_test)
            revenu_ttc = bd["ttc"]
            # revenu IVIA = marge avant IA (frais plateforme nets de Stripe)
            revenu_ivia = bd["marge_ivia"] + bd["cout_ia"]
            benefice = revenu_ivia - cad
        out.append(
            SessionEconomics(
                session_id=sid,
                date=rec.created_at if rec is not None else None,
                praticien=praticiens.get(rec.praticien_id) if rec is not None else None,
                session_type_code=getattr(rec, "session_type_code", None) if rec is not None else None,
                statut=rec.session_status_code.value if rec is not None and rec.session_status_code else None,
                nb_appels_ia=len(evs),
                cout_ia_usd=round(usd, 6),
                cout_ia_cad_cents=cad,
                revenu_ttc_cents=revenu_ttc,
                revenu_ivia_cents=revenu_ivia,
                is_test=is_test,
                benefice_cad_cents=benefice,
            )
        )
    return out
