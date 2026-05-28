from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_life_event import ClientLifeEvent
from app.models.enums import RecordStatus
from app.schemas.client_life_event import (
    ClientLifeEventCreate,
    ClientLifeEventRead,
    ClientLifeEventUpdate,
)

router = APIRouter(prefix="/clients/{client_id}/life-events", tags=["life-events"])


def _get_client_or_404(client_id: str, db: Session) -> Client:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")
    return client


@router.get("", response_model=list[ClientLifeEventRead])
def list_life_events(
    client_id: str,
    include_archived: bool = Query(default=False),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[ClientLifeEvent]:
    _get_client_or_404(client_id, db)
    stmt = (
        select(ClientLifeEvent)
        .where(ClientLifeEvent.client_id == client_id)
        .order_by(ClientLifeEvent.event_year_approx.asc().nullslast())
    )
    if not include_archived:
        stmt = stmt.where(ClientLifeEvent.record_status != RecordStatus.archived)
    return list(db.scalars(stmt))


@router.post("", response_model=ClientLifeEventRead, status_code=status.HTTP_201_CREATED)
def create_life_event(
    client_id: str,
    payload: ClientLifeEventCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> ClientLifeEvent:
    _get_client_or_404(client_id, db)
    data = payload.model_dump()
    data["client_id"] = client_id
    data["id"] = str(uuid4())
    now = datetime.now(timezone.utc)
    data.setdefault("created_at", now)
    data["updated_at"] = now
    event = ClientLifeEvent(**data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/{event_id}", response_model=ClientLifeEventRead)
def get_life_event(
    client_id: str,
    event_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> ClientLifeEvent:
    _get_client_or_404(client_id, db)
    event = db.scalar(
        select(ClientLifeEvent).where(
            ClientLifeEvent.id == event_id,
            ClientLifeEvent.client_id == client_id,
        )
    )
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Événement introuvable.")
    return event


@router.patch("/{event_id}", response_model=ClientLifeEventRead)
def update_life_event(
    client_id: str,
    event_id: str,
    payload: ClientLifeEventUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> ClientLifeEvent:
    _get_client_or_404(client_id, db)
    event = db.scalar(
        select(ClientLifeEvent).where(
            ClientLifeEvent.id == event_id,
            ClientLifeEvent.client_id == client_id,
        )
    )
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Événement introuvable.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    event.updated_at = datetime.now(timezone.utc)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_life_event(
    client_id: str,
    event_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> None:
    _get_client_or_404(client_id, db)
    event = db.scalar(
        select(ClientLifeEvent).where(
            ClientLifeEvent.id == event_id,
            ClientLifeEvent.client_id == client_id,
        )
    )
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Événement introuvable.")
    event.record_status = RecordStatus.archived
    event.updated_at = datetime.now(timezone.utc)
    db.add(event)
    db.commit()
