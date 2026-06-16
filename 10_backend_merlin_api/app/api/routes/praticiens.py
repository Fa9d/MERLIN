from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_practitioner
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import AppRole, RecordStatus
from app.schemas.auth import PraticienPublic
from app.schemas.common import MerlinSchema

router = APIRouter(prefix="/praticiens", tags=["praticiens"])


@router.get("", response_model=list[PraticienPublic])
def list_praticiens(db: Session = Depends(get_db)) -> list[AppUser]:
    users = db.scalars(
        select(AppUser)
        .where(AppUser.is_publicly_listed == True)  # noqa: E712
        .where(AppUser.role == AppRole.practitioner)
        .where(AppUser.record_status == RecordStatus.active)
        .order_by(AppUser.display_name)
    ).all()
    return list(users)


class TarifsRead(MerlinSchema):
    # Prix appliqués (tarif praticien si défini, sinon défaut serveur).
    session_price_30min_cents: int
    session_price_60min_cents: int
    is_default_30: bool
    is_default_60: bool


class TarifsUpdate(MerlinSchema):
    session_price_30min_cents: int | None = None
    session_price_60min_cents: int | None = None


def _tarifs_read(user: AppUser) -> TarifsRead:
    p30 = user.session_price_30min_cents
    p60 = user.session_price_60min_cents
    return TarifsRead(
        session_price_30min_cents=p30 if p30 is not None else settings.stripe_seance_30min_amount_cents,
        session_price_60min_cents=p60 if p60 is not None else settings.stripe_seance_amount_cents,
        is_default_30=p30 is None,
        is_default_60=p60 is None,
    )


@router.get("/me/tarifs", response_model=TarifsRead)
def get_my_tarifs(
    current_user: AppUser = Depends(require_practitioner()),
) -> TarifsRead:
    """Tarifs de séance du praticien connecté (défaut serveur si non fixés)."""
    return _tarifs_read(current_user)


@router.patch("/me/tarifs", response_model=TarifsRead)
def set_my_tarifs(
    payload: TarifsUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner()),
) -> TarifsRead:
    """Le praticien fixe ses prix (cents). Null/absent → revient au défaut serveur."""
    data = payload.model_dump(exclude_unset=True)
    if "session_price_30min_cents" in data:
        current_user.session_price_30min_cents = data["session_price_30min_cents"]
    if "session_price_60min_cents" in data:
        current_user.session_price_60min_cents = data["session_price_60min_cents"]
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return _tarifs_read(current_user)
