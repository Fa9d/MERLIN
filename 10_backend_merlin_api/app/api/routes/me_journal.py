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
from app.models.enums import RecordStatus
from app.models.session import SessionRecord
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


def _verifier_session_du_client(session_id: str | None, client_id: str, db: Session) -> None:
    """Une trace ne peut être rattachée qu'à une séance appartenant au client."""
    if session_id is None:
        return
    owned = db.scalar(
        select(SessionRecord.id).where(
            SessionRecord.id == session_id,
            SessionRecord.client_id == client_id,
        )
    )
    if owned is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Séance introuvable.",
        )


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
    # Première écriture = création du dossier client au vol (cohérent avec bookings/checkout) :
    # le journal ne doit jamais être bloqué par l'absence de fiche.
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        display = current_user.display_name or current_user.email or "Client"
        parts = display.split(" ", 1)
        client = Client(
            app_user_id=current_user.id,
            first_name_or_alias=parts[0],
            last_name=parts[1] if len(parts) > 1 else None,
            email=current_user.email,
        )
        db.add(client)
        db.flush()
    _verifier_session_du_client(payload.session_id, client.id, db)
    data = payload.model_dump()
    data["client_id"] = client.id
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
    if "session_id" in updates:
        _verifier_session_du_client(updates["session_id"], client.id, db)
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
