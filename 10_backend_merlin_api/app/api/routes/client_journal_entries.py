from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_journal_entry import ClientJournalEntry
from app.models.enums import RecordStatus
from app.schemas.client_journal_entry import (
    ClientJournalEntryCreate,
    ClientJournalEntryRead,
    ClientJournalEntryUpdate,
)

router = APIRouter(prefix="/clients/{client_id}/journal", tags=["journal"])


def _get_client_or_404(client_id: str, db: Session) -> Client:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")
    return client


@router.get("", response_model=list[ClientJournalEntryRead])
def list_journal_entries(
    client_id: str,
    include_archived: bool = Query(default=False),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[ClientJournalEntry]:
    _get_client_or_404(client_id, db)
    stmt = (
        select(ClientJournalEntry)
        .where(ClientJournalEntry.client_id == client_id)
        .order_by(ClientJournalEntry.written_at.desc())
        .limit(limit)
    )
    if not include_archived:
        stmt = stmt.where(ClientJournalEntry.record_status != RecordStatus.archived)
    return list(db.scalars(stmt))


@router.post("", response_model=ClientJournalEntryRead, status_code=status.HTTP_201_CREATED)
def create_journal_entry(
    client_id: str,
    payload: ClientJournalEntryCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> ClientJournalEntry:
    _get_client_or_404(client_id, db)
    data = payload.model_dump()
    data["client_id"] = client_id
    data["id"] = str(uuid4())
    now = datetime.now(timezone.utc)
    if data.get("written_at") is None:
        data["written_at"] = now
    data["created_at"] = now
    entry = ClientJournalEntry(**data)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/{entry_id}", response_model=ClientJournalEntryRead)
def get_journal_entry(
    client_id: str,
    entry_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> ClientJournalEntry:
    _get_client_or_404(client_id, db)
    entry = db.scalar(
        select(ClientJournalEntry).where(
            ClientJournalEntry.id == entry_id,
            ClientJournalEntry.client_id == client_id,
        )
    )
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrée introuvable.")
    return entry


@router.patch("/{entry_id}", response_model=ClientJournalEntryRead)
def update_journal_entry(
    client_id: str,
    entry_id: str,
    payload: ClientJournalEntryUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> ClientJournalEntry:
    _get_client_or_404(client_id, db)
    entry = db.scalar(
        select(ClientJournalEntry).where(
            ClientJournalEntry.id == entry_id,
            ClientJournalEntry.client_id == client_id,
        )
    )
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrée introuvable.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_journal_entry(
    client_id: str,
    entry_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> None:
    _get_client_or_404(client_id, db)
    entry = db.scalar(
        select(ClientJournalEntry).where(
            ClientJournalEntry.id == entry_id,
            ClientJournalEntry.client_id == client_id,
        )
    )
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrée introuvable.")
    entry.record_status = RecordStatus.archived
    db.add(entry)
    db.commit()
