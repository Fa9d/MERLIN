from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles, require_operator
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.consent import Consent
from app.models.session import SessionRecord
from app.schemas.consent import ConsentCreate, ConsentRead

router = APIRouter(prefix="/consents", tags=["consents"])


@router.post("", response_model=ConsentRead, status_code=status.HTTP_201_CREATED)
def create_consent(
    payload: ConsentCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_operator()),
) -> Consent:
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
