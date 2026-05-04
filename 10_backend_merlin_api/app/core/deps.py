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


def require_supervision_roles():
    return require_roles(AppRole.supervisor)


def require_production_roles():
    return require_roles(AppRole.practitioner, AppRole.operator)


def require_internal_clinical_roles():
    return require_roles(AppRole.practitioner, AppRole.operator, AppRole.supervisor)


def require_admin_tech():
    return require_roles(AppRole.admin_tech)


def is_operator_user(user: AppUser) -> bool:
    return user.role in (AppRole.operator, AppRole.practitioner)
