"""Réglages admin — interrupteurs de facturation par offre (mode test).

Coché (payant=true) → l'offre est facturée. Décoché → gratuite (pour tester).

⚠️ Gardé pour l'instant aux rôles cliniques internes (praticien/opérateur/superviseur)
afin que le fondateur puisse tester en phase solo. À RESSERRER à `require_admin_tech`
avant l'arrivée de praticiens externes — un praticien ne doit pas pouvoir rendre les
offres gratuites globalement.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles
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
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> BillingFlags:
    return BillingFlags(flags=_read_flags(db))


@router.patch("", response_model=BillingFlags)
def update_billing_flags(
    payload: BillingFlags,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> BillingFlags:
    for code, payant in payload.flags.items():
        if code in billing.OFFERS:
            app_settings.set_value(db, billing.offer_payant_key(code), "true" if payant else "false")
    db.commit()
    return BillingFlags(flags=_read_flags(db))
