from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.intake_request import IntakeRequest
from app.schemas.intake_request import IntakeRequestCreate, IntakeRequestRead

router = APIRouter(prefix="/intake-requests", tags=["intake_requests"])


@router.get("", response_model=list[IntakeRequestRead])
def list_intake_requests(
    client_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[IntakeRequest]:
    statement = select(IntakeRequest).order_by(IntakeRequest.created_at.desc()).limit(limit)
    if client_id is not None:
        statement = statement.where(IntakeRequest.client_id == client_id)
    return list(db.scalars(statement))


@router.post("", response_model=IntakeRequestRead, status_code=status.HTTP_201_CREATED)
def create_intake_request(
    payload: IntakeRequestCreate,
    db: Session = Depends(get_db),
) -> IntakeRequest:
    client = db.get(Client, payload.client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    intake_request = IntakeRequest(**payload.model_dump())
    db.add(intake_request)
    db.commit()
    db.refresh(intake_request)
    return intake_request


@router.get("/{intake_request_id}", response_model=IntakeRequestRead)
def get_intake_request(
    intake_request_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> IntakeRequest:
    intake_request = db.get(IntakeRequest, intake_request_id)
    if intake_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demande d'entree introuvable.",
        )
    return intake_request
