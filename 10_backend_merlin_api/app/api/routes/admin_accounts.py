"""Administration des comptes & accès — /admin/accounts.

Réservé aux admins (require_admin : rôle admin_tech OU courriel en liste blanche).
Voir les inscriptions, renvoyer un lien de confirmation, vérifier manuellement,
changer le rôle, activer/suspendre. Adossé à AppUser + Client (profil complété).
"""
import logging
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import is_admin, require_admin
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import AppRole, RecordStatus
from app.schemas.common import MerlinSchema
from app.services.email import make_verification_email, send_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/accounts", tags=["admin-comptes"])


class AdminAccountRead(MerlinSchema):
    id: str
    email: str
    display_name: str
    role: str
    email_verified: bool
    record_status: str
    is_admin: bool
    profile_complete: bool
    created_at: datetime


class RoleUpdate(MerlinSchema):
    role: AppRole


class StatusUpdate(MerlinSchema):
    suspend: bool  # True → closed (suspendu) ; False → active


class AdminActionAck(MerlinSchema):
    status: str
    account: AdminAccountRead


def _to_read(u: AppUser, profile_complete: bool) -> AdminAccountRead:
    return AdminAccountRead(
        id=u.id,
        email=u.email,
        display_name=u.display_name,
        role=u.role.value,
        email_verified=u.email_verified,
        record_status=u.record_status.value,
        is_admin=is_admin(u),
        profile_complete=profile_complete,
        created_at=u.created_at,
    )


def _profile_map(db: Session, user_ids: list[str]) -> dict[str, bool]:
    """profile_complete par app_user_id (via la fiche Client liée)."""
    rows = db.scalars(select(Client).where(Client.app_user_id.in_(user_ids))).all()
    return {c.app_user_id: c.profile_complete for c in rows if c.app_user_id}


@router.get("", response_model=list[AdminAccountRead])
def list_accounts(
    q: str | None = Query(default=None, description="Filtre courriel ou nom (contient)"),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> list[AdminAccountRead]:
    stmt = select(AppUser).order_by(AppUser.created_at.desc()).limit(limit)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where((AppUser.email.ilike(like)) | (AppUser.display_name.ilike(like)))
    users = list(db.scalars(stmt))
    pmap = _profile_map(db, [u.id for u in users])
    return [_to_read(u, pmap.get(u.id, False)) for u in users]


def _get_user(db: Session, user_id: str) -> AppUser:
    user = db.get(AppUser, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")
    return user


@router.post("/{user_id}/resend-verification", response_model=AdminActionAck)
async def resend_verification(
    user_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Régénère le lien de confirmation et le renvoie au courriel du compte."""
    user = _get_user(db, user_id)
    if user.email_verified:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Courriel déjà vérifié.")
    token = secrets.token_urlsafe(48)
    user.email_verification_token = token
    user.token_expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    db.add(user)
    db.commit()
    db.refresh(user)

    url = f"{settings.frontend_url}/verify-email?{urlencode({'token': token})}"
    html, text = make_verification_email(user.display_name, url)
    sent = await send_email(user.email, "Confirmez votre adresse — IVIA", html, text)
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Le courriel n'a pas pu être envoyé (SMTP).",
        )
    logger.info("Lien de vérification renvoyé (admin) à %s", user.email)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="sent", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/verify", response_model=AdminActionAck)
def verify_manually(
    user_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Marque le courriel comme vérifié sans passer par le lien (dépannage admin)."""
    user = _get_user(db, user_id)
    user.email_verified = True
    user.email_verification_token = None
    user.token_expires_at = None
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="verified", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/role", response_model=AdminActionAck)
def update_role(
    user_id: str,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Change le rôle métier (client/praticien/opérateur/superviseur/admin_tech).

    NB : le droit « admin » par liste blanche (MERLIN_ADMIN_EMAILS) est séparé et
    se règle dans la config, pas ici.
    """
    user = _get_user(db, user_id)
    user.role = payload.role
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="role_updated", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/status", response_model=AdminActionAck)
def update_status(
    user_id: str,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Suspend (closed) ou réactive (active) un compte."""
    user = _get_user(db, user_id)
    user.record_status = RecordStatus.closed if payload.suspend else RecordStatus.active
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="status_updated", account=_to_read(user, pmap.get(user.id, False)))
