"""Documents livrés au client connecté — /me/documents.

Le client retrouve ici les reformulations de séance déposées dans son espace par
le praticien : documents dérivés `client_visible` dont la note source est validée
(relecture humaine obligatoire — constitution MERLIN). Lecture seule.
"""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_verified_email_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.derived_document import DerivedDocument
from app.models.session_note import SessionNote
from app.schemas.derived_document import DerivedDocumentRead

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/me/documents", tags=["documents-client"])


@router.get("", response_model=list[DerivedDocumentRead])
def list_my_documents(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> list[DerivedDocument]:
    """Reformulations livrées au compte connecté (plus récentes d'abord)."""
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        return []
    statement = (
        select(DerivedDocument)
        .where(DerivedDocument.client_id == client.id)
        .where(DerivedDocument.client_visible.is_(True))
        .join(SessionNote, SessionNote.id == DerivedDocument.source_note_id)
        .where(SessionNote.validated_by_practitioner.is_(True))
        .order_by(DerivedDocument.created_at.desc())
    )
    return list(db.scalars(statement))
