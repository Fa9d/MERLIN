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


class ProfilRead(MerlinSchema):
    display_name: str
    title_line: str | None = None
    intro_text: str | None = None
    is_publicly_listed: bool
    themes: list[str] = []
    formats: list[str] = []


class ProfilUpdate(MerlinSchema):
    display_name: str | None = None
    title_line: str | None = None
    intro_text: str | None = None
    is_publicly_listed: bool | None = None
    themes: list[str] | None = None
    formats: list[str] | None = None


def _json_list(raw: str | None) -> list[str]:
    import json
    if not raw:
        return []
    try:
        v = json.loads(raw)
        return v if isinstance(v, list) else []
    except Exception:
        return []


def _profil_read(u: AppUser) -> ProfilRead:
    return ProfilRead(
        display_name=u.display_name,
        title_line=u.title_line,
        intro_text=u.intro_text,
        is_publicly_listed=u.is_publicly_listed,
        themes=_json_list(u.themes),
        formats=_json_list(u.available_channels),
    )


@router.get("/me/profil", response_model=ProfilRead)
def get_my_profil(current_user: AppUser = Depends(require_practitioner())) -> ProfilRead:
    """Profil public du praticien connecté."""
    return _profil_read(current_user)


@router.patch("/me/profil", response_model=ProfilRead)
def update_my_profil(
    payload: ProfilUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner()),
) -> ProfilRead:
    """Le praticien met à jour son profil public (identité, bio, thèmes, formats, visibilité)."""
    import json
    data = payload.model_dump(exclude_unset=True)
    if "display_name" in data and data["display_name"]:
        current_user.display_name = data["display_name"].strip()
    if "title_line" in data:
        current_user.title_line = data["title_line"]
    if "intro_text" in data:
        current_user.intro_text = data["intro_text"]
    if "is_publicly_listed" in data and data["is_publicly_listed"] is not None:
        current_user.is_publicly_listed = data["is_publicly_listed"]
    if "themes" in data and data["themes"] is not None:
        current_user.themes = json.dumps(data["themes"], ensure_ascii=False)
    if "formats" in data and data["formats"] is not None:
        current_user.available_channels = json.dumps(data["formats"], ensure_ascii=False)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return _profil_read(current_user)


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
