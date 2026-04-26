from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import is_operator_user, require_internal_clinical_roles, require_operator
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.derived_document import DerivedDocument
from app.models.intake_request import IntakeRequest
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.schemas.derived_document import DerivedDocumentCreate, DerivedDocumentRead

router = APIRouter(prefix="/derived-documents", tags=["derived-documents"])


def _resolve_document_publication_state(
    client_delivery_requested: bool,
    source_note_validated: bool,
) -> tuple[str, bool]:
    if not client_delivery_requested:
        return "internal", False
    if source_note_validated:
        return "client", True
    return "client_pending_review", False


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

    audience_code, client_visible = _resolve_document_publication_state(
        client_delivery_requested=payload.client_visible,
        source_note_validated=source_note.validated_by_practitioner,
    )

    derived_document = DerivedDocument(
        **payload.model_dump(exclude={"audience_code", "client_visible"}),
        audience_code=audience_code,
        client_visible=client_visible,
    )
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
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> list[DerivedDocument]:
    statement = select(DerivedDocument).order_by(DerivedDocument.created_at.desc()).limit(limit)
    if is_operator_user(current_user):
        statement = statement.join(SessionRecord, SessionRecord.id == DerivedDocument.session_id).where(
            SessionRecord.operator_user_id == current_user.id
        )
    if client_id is not None:
        statement = statement.where(DerivedDocument.client_id == client_id)
    if session_id is not None:
        statement = statement.where(DerivedDocument.session_id == session_id)
    return list(db.scalars(statement))


@router.get("/public/client/{public_client_code}", response_model=list[DerivedDocumentRead])
def list_public_client_derived_documents(
    public_client_code: str,
    intake_request_id: str = Query(...),
    db: Session = Depends(get_db),
) -> list[DerivedDocument]:
    client = db.scalar(select(Client).where(Client.public_client_code == public_client_code))
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reference client introuvable.")

    intake_request = db.get(IntakeRequest, intake_request_id)
    if intake_request is None or intake_request.client_id != client.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reference d'entree introuvable.")

    statement = (
        select(DerivedDocument)
        .where(DerivedDocument.client_id == client.id)
        .where(DerivedDocument.client_visible.is_(True))
        .join(SessionNote, SessionNote.id == DerivedDocument.source_note_id)
        .where(SessionNote.validated_by_practitioner.is_(True))
        .order_by(DerivedDocument.created_at.desc())
    )
    return list(db.scalars(statement))


@router.get("/{derived_document_id}", response_model=DerivedDocumentRead)
def get_derived_document(
    derived_document_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> DerivedDocument:
    derived_document = db.get(DerivedDocument, derived_document_id)
    if derived_document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document derive introuvable.")
    if is_operator_user(current_user):
        session_record = db.get(SessionRecord, derived_document.session_id)
        if session_record is None or session_record.operator_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document derive introuvable.",
            )
    return derived_document
