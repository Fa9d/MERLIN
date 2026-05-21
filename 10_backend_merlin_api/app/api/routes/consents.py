from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_optional_current_user, require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.consent import Consent
from app.models.enums import AppRole, ConsentTypeCode, GrantedByActorCode
from app.models.session import SessionRecord
from app.schemas.consent import ConsentCreate, ConsentRead

router = APIRouter(prefix="/consents", tags=["consents"])

PUBLIC_INTAKE_CONSENT_TYPES = {
    ConsentTypeCode.consent_session,
    ConsentTypeCode.consent_session_note,
    ConsentTypeCode.consent_history,
}


def _validate_create_access(payload: ConsentCreate, current_user: AppUser | None) -> None:
    if current_user is not None:
        if current_user.role != AppRole.operator:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role insuffisant pour cette operation.",
            )
        return

    if payload.session_id is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour lier un consentement a une seance.",
        )

    if payload.granted_by_actor_code != GrantedByActorCode.client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce type de consentement.",
        )

    if payload.consent_type_code not in PUBLIC_INTAKE_CONSENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce type de consentement.",
        )


@router.get("", response_model=list[ConsentRead])
def list_consents(
    client_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[Consent]:
    statement = select(Consent).order_by(Consent.granted_at.desc(), Consent.created_at.desc()).limit(limit)
    if client_id is not None:
        statement = statement.where(Consent.client_id == client_id)
    return list(db.scalars(statement))


@router.post("", response_model=ConsentRead, status_code=status.HTTP_201_CREATED)
def create_consent(
    payload: ConsentCreate,
    db: Session = Depends(get_db),
    current_user: AppUser | None = Depends(get_optional_current_user),
) -> Consent:
    _validate_create_access(payload, current_user)

    client = db.get(Client, payload.client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    if payload.session_id is not None:
        session = db.get(SessionRecord, payload.session_id)
        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seance introuvable.")
        if session.client_id != payload.client_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le client et la seance ne correspondent pas.",
            )

    consent = Consent(**payload.model_dump())
    db.add(consent)
    db.commit()
    db.refresh(consent)
    return consent


@router.get("/{consent_id}", response_model=ConsentRead)
def get_consent(
    consent_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> Consent:
    consent = db.get(Consent, consent_id)
    if consent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consentement introuvable.")
    return consent
