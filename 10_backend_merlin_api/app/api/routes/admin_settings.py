"""Réglages admin — interrupteurs de facturation par offre (mode test).

Coché (payant=true) → l'offre est facturée. Décoché → gratuite (pour tester).

Accès réservé à l'administration via `require_admin` (rôle admin_tech OU courriel en
liste blanche `MERLIN_ADMIN_EMAILS`). Un praticien ordinaire ne peut donc pas rendre
les offres gratuites globalement — seul un admin déclaré le peut.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.app_user import AppUser
from app.schemas.common import MerlinSchema
from app.services import app_settings, billing

router = APIRouter(prefix="/admin/billing-flags", tags=["admin-facturation"])


class BillingFlags(MerlinSchema):
    flags: dict[str, bool]   # { offre_code: payant }


def _read_flags(db: Session) -> dict[str, bool]:
    return {code: billing.is_offer_payant(db, code) for code in billing.OFFERS}


@router.get("", response_model=BillingFlags)
def get_billing_flags(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> BillingFlags:
    return BillingFlags(flags=_read_flags(db))


@router.patch("", response_model=BillingFlags)
def update_billing_flags(
    payload: BillingFlags,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> BillingFlags:
    for code, payant in payload.flags.items():
        if code in billing.OFFERS:
            app_settings.set_value(db, billing.offer_payant_key(code), "true" if payant else "false")
    db.commit()
    return BillingFlags(flags=_read_flags(db))
