from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.deps import (
    is_operator_user,
    require_internal_clinical_roles,
    require_operator,
)
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.derived_document import DerivedDocument
from app.models.enums import RecordStatus
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.schemas.session_note import (
    SessionNoteCreate,
    SessionNoteRead,
    SessionNoteValidationPayload,
)

router = APIRouter(prefix="/session-notes", tags=["session-notes"])


def _resolve_document_publication_state(
    client_delivery_requested: bool,
    note_validated: bool,
) -> tuple[str, bool]:
    if not client_delivery_requested:
        return "internal", False
    if note_validated:
        return "client", True
    return "client_pending_review", False


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
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> list[SessionNote]:
    statement = (
        select(SessionNote)
        .join(SessionRecord, SessionRecord.id == SessionNote.session_id)
        .where(
            SessionNote.record_status != RecordStatus.archived,
            SessionRecord.record_status != RecordStatus.archived,
        )
        .order_by(SessionNote.created_at.desc())
    )
    if current_user.role == "practitioner":
        statement = statement.where(SessionRecord.praticien_id == current_user.id)
    elif is_operator_user(current_user):
        statement = statement.where(SessionRecord.operator_user_id == current_user.id)
    if session_id is not None:
        statement = statement.where(SessionNote.session_id == session_id)
    if client_id is not None:
        statement = statement.where(SessionNote.client_id == client_id)
    return list(db.scalars(statement).all())


@router.get("/{session_note_id}", response_model=SessionNoteRead)
def get_session_note(
    session_note_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionNote:
    session_note = db.get(SessionNote, session_note_id)
    if session_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note de seance introuvable.")
    if is_operator_user(current_user):
        session_record = db.get(SessionRecord, session_note.session_id)
        if session_record is None or session_record.operator_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note de seance introuvable.",
            )
    return session_note


@router.patch("/{session_note_id}/validate", response_model=SessionNoteRead)
def validate_session_note(
    session_note_id: str,
    payload: SessionNoteValidationPayload,
    db: Session = Depends(get_db),
    # Validation humaine : le praticien valide sa propre note (constitution MERLIN).
    # Le superviseur reste habilité ; l'opérateur aussi.
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionNote:
    session_note = db.get(SessionNote, session_note_id)
    if session_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note de seance introuvable.")

    session_note.validated_by_practitioner = payload.validated
    session_note.practitioner_corrections = payload.corrections
    session_note.validated_at = datetime.now(timezone.utc)

    audience_code, client_visible = _resolve_document_publication_state(
        client_delivery_requested=session_note.client_visible,
        note_validated=session_note.validated_by_practitioner,
    )
    linked_documents = list(
        db.scalars(select(DerivedDocument).where(DerivedDocument.source_note_id == session_note.id)).all()
    )
    for document in linked_documents:
        document.audience_code = audience_code
        document.client_visible = client_visible
        db.add(document)

    db.add(session_note)
    db.commit()
    db.refresh(session_note)
    return session_note
