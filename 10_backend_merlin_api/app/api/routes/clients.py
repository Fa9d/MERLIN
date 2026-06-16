from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_user,
    get_optional_current_user,
    require_internal_clinical_roles,
)
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import DataSensitivityClass, RecordStatus
from app.schemas.client import ClientCreate, ClientRead, MyClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


def _validate_create_access(payload: ClientCreate, current_user: AppUser | None) -> None:
    if current_user is not None:
        return

    if not payload.is_adult_confirmed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="L'entree publique est reservee aux adultes confirmes.",
        )

    if payload.record_status != RecordStatus.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce niveau de creation client.",
        )

    if payload.data_sensitivity_class != DataSensitivityClass.high:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce niveau de creation client.",
        )

    if not (payload.email or payload.phone):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Un courriel ou un telephone est requis pour l'entree publique.",
        )


@router.get("", response_model=list[ClientRead])
def list_clients(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[Client]:
    statement = select(Client).order_by(Client.created_at.desc()).limit(limit)
    return list(db.scalars(statement))


@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    current_user: AppUser | None = Depends(get_optional_current_user),
) -> Client:
    _validate_create_access(payload, current_user)

    payload_data = payload.model_dump()
    if current_user is not None:
        existing = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
        payload_data["app_user_id"] = current_user.id
        if not payload_data.get("email"):
            payload_data["email"] = current_user.email

        if existing is not None:
            for key, value in payload_data.items():
                setattr(existing, key, value)
            db.add(existing)
            db.commit()
            db.refresh(existing)
            return existing

    client = Client(**payload_data)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/me", response_model=ClientRead)
def get_my_client(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> Client:
    """Retourne le dossier `Client` durablement lié au compte connecté.

    Utilisé par `/mon-espace` pour afficher la fiche du client après activation
    via magic link ou inscription via `/acces-client`.
    """
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun dossier client n'est rattaché à ce compte.",
        )
    return client


@router.patch("/me", response_model=ClientRead)
def update_my_client(
    payload: MyClientUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> Client:
    """Le client complète/met à jour sa propre fiche (profil de détermination)."""
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun dossier client n'est rattaché à ce compte.",
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/{client_id}", response_model=ClientRead)
def get_client(
    client_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> Client:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")
    return client
