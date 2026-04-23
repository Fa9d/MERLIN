from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles, require_operator
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.schemas.session_note import (
    SessionNoteCreate,
    SessionNoteRead,
    SessionNoteValidationPayload,
)

router = APIRouter(prefix="/session-notes", tags=["session-notes"])


@router.post("", response_model=SessionNoteRead, status_code=status.HTTP_201_CREATED)
def create_session_note(
    payload: SessionNoteCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_operator()),
) -> SessionNote:
    client = db.get(Client, payload.client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    session_record = db.get(SessionRecord, payload.session_id)
    if session_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seance introuvable.")
    if session_record.client_id != payload.client_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Le client et la seance ne correspondent pas.",
        )

    note_sequence_number = payload.note_sequence_number
    if note_sequence_number is None:
        latest_sequence_number = db.scalar(
            select(func.max(SessionNote.note_sequence_number)).where(
                SessionNote.session_id == payload.session_id
            )
        )
        note_sequence_number = (latest_sequence_number or 0) + 1

    session_note = SessionNote(
        **payload.model_dump(exclude={"note_sequence_number"}),
        note_sequence_number=note_sequence_number,
    )
    db.add(session_note)
    db.commit()
    db.refresh(session_note)
    return session_note


@router.get("", response_model=list[SessionNoteRead])
def list_session_notes(
    session_id: str | None = Query(default=None),
    client_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[SessionNote]:
    statement = select(SessionNote).order_by(SessionNote.created_at.desc())
    if session_id is not None:
        statement = statement.where(SessionNote.session_id == session_id)
    if client_id is not None:
        statement = statement.where(SessionNote.client_id == client_id)
    return list(db.scalars(statement).all())


@router.get("/{session_note_id}", response_model=SessionNoteRead)
def get_session_note(
    session_note_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionNote:
    session_note = db.get(SessionNote, session_note_id)
    if session_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note de seance introuvable.")
    return session_note


@router.patch("/{session_note_id}/validate", response_model=SessionNoteRead)
def validate_session_note(
    session_note_id: str,
    payload: SessionNoteValidationPayload,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_operator()),
) -> SessionNote:
    session_note = db.get(SessionNote, session_note_id)
    if session_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note de seance introuvable.")

    session_note.validated_by_practitioner = payload.validated
    session_note.practitioner_corrections = payload.corrections
    session_note.validated_at = datetime.now(timezone.utc)
    db.add(session_note)
    db.commit()
    db.refresh(session_note)
    return session_note
