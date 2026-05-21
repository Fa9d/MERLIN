from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_entitlement import ClientEntitlement
from app.schemas.client_entitlement import ClientEntitlementRead

router = APIRouter(prefix="/client-entitlements", tags=["client-entitlements"])


def _resolve_client_for_current_user(db: Session, current_user: AppUser) -> Client:
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun dossier client rattache a ce compte.",
        )
    return client


@router.get("", response_model=list[ClientEntitlementRead])
def list_client_entitlements(
    client_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[ClientEntitlement]:
    statement = (
        select(ClientEntitlement)
        .order_by(ClientEntitlement.created_at.desc())
        .limit(limit)
    )
    if client_id is not None:
        statement = statement.where(ClientEntitlement.client_id == client_id)
    return list(db.scalars(statement))


@router.get("/me", response_model=list[ClientEntitlementRead])
def list_my_entitlements(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> list[ClientEntitlement]:
    client = _resolve_client_for_current_user(db, current_user)
    statement = (
        select(ClientEntitlement)
        .where(ClientEntitlement.client_id == client.id)
        .order_by(ClientEntitlement.created_at.desc())
    )
    return list(db.scalars(statement))