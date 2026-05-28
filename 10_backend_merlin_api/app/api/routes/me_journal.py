"""Routes client autonome pour le journal personnel (/api/v1/me/journal).

N'exige pas de rôle clinique — seul un compte client authentifié est requis.
Le client_id est résolu depuis la session JWT; le client ne peut accéder qu'à ses propres entrées.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_journal_entry import ClientJournalEntry
from app.models.enums import AuthoredByCode, RecordStatus
from app.schemas.client_journal_entry import (
    ClientJournalEntryRead,
    ClientJournalEntryUpdate,
    MyJournalEntryCreate,
)

router = APIRouter(prefix="/me/journal", tags=["journal-client"])


def _get_my_client(current_user: AppUser, db: Session) -> Client:
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier client introuvable. Complétez votre inscription pour accéder au journal.",
        )
    return client


@router.get("", response_model=list[ClientJournalEntryRead])
def list_my_journal(
    include_archived: bool = Query(default=False),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> list[ClientJournalEntry]:
    client = _get_my_client(current_user, db)
    stmt = (
        select(ClientJournalEntry)
        .where(ClientJournalEntry.client_id == client.id)
        .order_by(ClientJournalEntry.written_at.desc())
        .limit(limit)
    )
    if not include_archived:
        stmt = stmt.where(ClientJournalEntry.record_status != RecordStatus.archived)
    return list(db.scalars(stmt))


@router.post("", response_model=ClientJournalEntryRead, status_code=status.HTTP_201_CREATED)
def create_my_journal_entry(
    payload: MyJournalEntryCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> ClientJournalEntry:
    client = _get_my_client(current_user, db)
    data = payload.model_dump()
    data["client_id"] = client.id
    data["id"] = str(uuid4())
    data["authored_by"] = AuthoredByCode.client
    now = datetime.now(timezone.utc)
    if data.get("written_at") is None:
        data["written_at"] = now
    data["created_at"] = now
    entry = ClientJournalEntry(**data)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.patch("/{entry_id}", response_model=ClientJournalEntryRead)
def update_my_journal_entry(
    entry_id: str,
    payload: ClientJournalEntryUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> ClientJournalEntry:
    client = _get_my_client(current_user, db)
    entry = db.scalar(
        select(ClientJournalEntry).where(
            ClientJournalEntry.id == entry_id,
            ClientJournalEntry.client_id == client.id,
        )
    )
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrée introuvable.")
    updates = payload.model_dump(exclude_unset=True)
    updates.pop("authored_by", None)  # authored_by ne peut être modifié
    for field, value in updates.items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_my_journal_entry(
    entry_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> None:
    client = _get_my_client(current_user, db)
    entry = db.scalar(
        select(ClientJournalEntry).where(
            ClientJournalEntry.id == entry_id,
            ClientJournalEntry.client_id == client.id,
        )
    )
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrée introuvable.")
    entry.record_status = RecordStatus.archived
    db.commit()
