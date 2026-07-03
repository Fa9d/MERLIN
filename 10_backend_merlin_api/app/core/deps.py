from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import AppRole, RecordStatus

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AppUser:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise.",
        )

    try:
        payload = decode_access_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide.",
        ) from exc

    user = db.get(AppUser, payload.get("sub"))
    if user is None or user.record_status != RecordStatus.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable ou inactif.",
        )
    return user


async def require_verified_email_user(
    current_user: AppUser = Depends(get_current_user),
) -> AppUser:
    if not current_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email non vérifié. Consultez votre boîte mail.",
        )
    return current_user


def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AppUser | None:
    if credentials is None:
        return None

    try:
        payload = decode_access_token(credentials.credentials)
    except Exception:
        return None

    user = db.get(AppUser, payload.get("sub"))
    if user is None or user.record_status != RecordStatus.active:
        return None
    return user


def require_roles(*allowed_roles: AppRole):
    allowed: set[AppRole] = set(allowed_roles)

    def _dependency(current_user: AppUser = Depends(get_current_user)) -> AppUser:
        if current_user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role insuffisant pour cette operation.",
            )
        return current_user

    return _dependency


def require_operator():
    return require_roles(AppRole.operator)


def require_practitioner():
    return require_roles(AppRole.practitioner)


def require_practitioner_or_operator():
    return require_roles(AppRole.practitioner, AppRole.operator)


def require_client():
    """Alias de compatibilité pour les routes client historiques.

    Plusieurs surfaces client utilisent déjà `get_current_user` sans contrainte
    de rôle stricte (ex. /me/*). On garde ce comportement ici pour éviter de
    casser les imports et le démarrage API.
    """
    return get_current_user


def require_supervisor():
    """Guard réservé au rôle `supervisor` uniquement.

    Renommé depuis `require_supervision_roles` (BACK-DEPS-001) pour cohérence
    avec `require_operator` / `require_practitioner` (singulier = un seul rôle).
    """
    return require_roles(AppRole.supervisor)


# Alias rétroactif — à supprimer après migration complète des appels.
require_supervision_roles = require_supervisor


def require_production_roles():
    return require_roles(AppRole.practitioner, AppRole.operator)


def require_internal_clinical_roles():
    return require_roles(AppRole.practitioner, AppRole.operator, AppRole.supervisor)


def require_admin_tech():
    return require_roles(AppRole.admin_tech)


def is_admin(user: AppUser) -> bool:
    """Vrai si l'utilisateur a des droits admin : rôle admin_tech OU courriel en liste blanche.

    Permet à un praticien d'être aussi admin sans changer son rôle
    (voir settings.admin_emails / MERLIN_ADMIN_EMAILS).
    """
    from app.core.config import settings

    if user.role == AppRole.admin_tech:
        return True
    if getattr(user, "is_platform_admin", False):
        return True
    return bool(user.email and user.email.strip().lower() in settings.admin_emails)


def require_admin():
    """Guard admin : rôle admin_tech ou courriel en liste blanche."""

    def _dependency(current_user: AppUser = Depends(get_current_user)) -> AppUser:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acces reserve a l'administration.",
            )
        return current_user

    return _dependency


def is_operator_user(user: AppUser) -> bool:
    return user.role in (AppRole.operator, AppRole.practitioner)
