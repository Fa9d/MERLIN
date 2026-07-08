"""Routes client autonome pour les intentions (/api/v1/me/intentions).

Une intention est un cap court que le client se donne et suit entre les séances.
Repère d'autonomie, jamais une prescription (constitution §6.4).
Le client_id est résolu depuis la session JWT ; le client n'accède qu'à ses intentions.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_intention import ClientIntention
from app.models.enums import IntentionStatusCode, RecordStatus
from app.models.session import SessionRecord
from app.schemas.client_intention import IntentionRead, MyIntentionCreate, MyIntentionUpdate

router = APIRouter(prefix="/me/intentions", tags=["intentions-client"])

_MAX_ACTIVES = 5  # garder le cap simple : pas plus de 5 intentions actives à la fois


def _get_my_client(current_user: AppUser, db: Session) -> Client:
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier client introuvable. Complétez votre inscription.",
        )
    return client


@router.get("", response_model=list[IntentionRead])
def list_my_intentions(
    include_closed: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> list[ClientIntention]:
    client = _get_my_client(current_user, db)
    stmt = (
        select(ClientIntention)
        .where(
            ClientIntention.client_id == client.id,
            ClientIntention.record_status != RecordStatus.archived,
        )
        .order_by(ClientIntention.created_at.desc())
        .limit(limit)
    )
    if not include_closed:
        stmt = stmt.where(ClientIntention.status == IntentionStatusCode.active)
    return list(db.scalars(stmt))


@router.post("", response_model=IntentionRead, status_code=status.HTTP_201_CREATED)
def create_my_intention(
    payload: MyIntentionCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> ClientIntention:
    client = _get_my_client(current_user, db)
    actives = db.scalars(
        select(ClientIntention.id).where(
            ClientIntention.client_id == client.id,
            ClientIntention.status == IntentionStatusCode.active,
            ClientIntention.record_status != RecordStatus.archived,
        )
    ).all()
    if len(actives) >= _MAX_ACTIVES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Vous avez déjà {_MAX_ACTIVES} intentions actives. "
            "Réalisez ou laissez aller une intention avant d'en ajouter une nouvelle.",
        )
    if payload.session_id is not None:
        owned = db.scalar(
            select(SessionRecord.id).where(
                SessionRecord.id == payload.session_id,
                SessionRecord.client_id == client.id,
            )
        )
        if owned is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Séance introuvable.")
    intention = ClientIntention(
        client_id=client.id,
        session_id=payload.session_id,
        text=payload.text,
        kind=payload.kind,
        dimension=payload.dimension,
        created_by="client",
    )
    db.add(intention)
    db.commit()
    db.refresh(intention)
    return intention


@router.patch("/{intention_id}", response_model=IntentionRead)
def update_my_intention(
    intention_id: str,
    payload: MyIntentionUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> ClientIntention:
    client = _get_my_client(current_user, db)
    intention = db.scalar(
        select(ClientIntention).where(
            ClientIntention.id == intention_id,
            ClientIntention.client_id == client.id,
        )
    )
    if intention is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intention introuvable.")
    updates = payload.model_dump(exclude_unset=True)
    if "text" in updates:
        text = (updates["text"] or "").strip()
        if not text:
            raise HTTPException(status_code=422, detail="L'intention ne peut pas être vide.")
        intention.text = text[:500]
    if "status" in updates and updates["status"] is not None:
        intention.status = updates["status"]
        intention.realized_at = (
            datetime.now(timezone.utc)
            if updates["status"] == IntentionStatusCode.realisee
            else None
        )
    db.commit()
    db.refresh(intention)
    return intention
