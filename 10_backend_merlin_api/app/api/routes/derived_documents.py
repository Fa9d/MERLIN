from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles, require_operator
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.derived_document import DerivedDocument
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.schemas.derived_document import DerivedDocumentCreate, DerivedDocumentRead

router = APIRouter(prefix="/derived-documents", tags=["derived-documents"])


@router.post("", response_model=DerivedDocumentRead, status_code=status.HTTP_201_CREATED)
def create_derived_document(
    payload: DerivedDocumentCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_operator()),
) -> DerivedDocument:
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

    source_note = db.get(SessionNote, payload.source_note_id)
    if source_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note de seance introuvable.")
    if source_note.session_id != payload.session_id or source_note.client_id != payload.client_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La note source ne correspond pas a la seance ou au client.",
        )

    derived_document = DerivedDocument(**payload.model_dump())
    db.add(derived_document)
    db.commit()
    db.refresh(derived_document)
    return derived_document


@router.get("", response_model=list[DerivedDocumentRead])
def list_derived_documents(
    client_id: str | None = Query(default=None),
    session_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[DerivedDocument]:
    statement = select(DerivedDocument).order_by(DerivedDocument.created_at.desc()).limit(limit)
    if client_id is not None:
        statement = statement.where(DerivedDocument.client_id == client_id)
    if session_id is not None:
        statement = statement.where(DerivedDocument.session_id == session_id)
    return list(db.scalars(statement))


@router.get("/{derived_document_id}", response_model=DerivedDocumentRead)
def get_derived_document(
    derived_document_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> DerivedDocument:
    derived_document = db.get(DerivedDocument, derived_document_id)
    if derived_document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document derive introuvable.")
    return derived_document
