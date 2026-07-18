from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_user,
    get_optional_current_user,
    require_internal_clinical_roles,
)
from app.core.config import settings
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import DataSensitivityClass, RecordStatus
from app.schemas.client import ClientCreate, ClientEmailSend, ClientRead, MyClientUpdate
from app.services.email import make_practitioner_direct_email, send_email

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


def _get_or_create_my_client(current_user: AppUser, db: Session) -> Client:
    """Dossier `Client` lié au compte connecté — créé à la demande s'il manque.

    Un compte créé hors du parcours d'intake (inscription directe, magic link)
    peut ne pas avoir de dossier. Le premier accès au profil le crée, pour que
    chacun puisse compléter sa fiche sans erreur 404.
    """
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is not None:
        return client
    display = current_user.display_name or current_user.email or "Client"
    parts = display.split(" ", 1)
    client = Client(
        app_user_id=current_user.id,
        first_name_or_alias=parts[0],
        last_name=parts[1] if len(parts) > 1 else None,
        email=current_user.email,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/me", response_model=ClientRead)
def get_my_client(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> Client:
    """Retourne le dossier `Client` lié au compte connecté (créé à la demande).

    Utilisé par `/mon-espace` pour afficher la fiche du client après activation
    via magic link ou inscription via `/acces-client`.
    """
    return _get_or_create_my_client(current_user, db)


@router.patch("/me", response_model=ClientRead)
def update_my_client(
    payload: MyClientUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> Client:
    """Le client complète/met à jour sa propre fiche (profil de détermination)."""
    client = _get_or_create_my_client(current_user, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.post("/{client_id}/email", status_code=status.HTTP_202_ACCEPTED)
async def send_client_email(
    client_id: str,
    payload: ClientEmailSend,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> dict:
    """Envoie un courriel libre du praticien au client, depuis la fiche client.

    Paramètres : client_id (chemin), payload {subject, message}.
    Sortie : {"sent": true, "to": adresse} en cas de succès ; 404 si client
    introuvable, 422 si le client n'a aucune adresse courriel, 502 si l'envoi
    SMTP échoue.
    Le message part tel que rédigé par le praticien (échappé dans le gabarit) ;
    le gabarit ajoute le lien de connexion à l'espace et le rappel d'urgence.
    """
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    account = db.get(AppUser, client.app_user_id) if client.app_user_id else None
    to_email = (account.email if account else None) or client.email
    if not to_email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ce client n'a aucune adresse courriel au dossier.",
        )

    display = (account.display_name if account else None) or client.first_name_or_alias or "vous"
    practitioner_name = current_user.display_name or "Votre praticien·ne"
    login_url = settings.frontend_url.rstrip("/") + "/connexion.html"

    html, text = make_practitioner_direct_email(
        display_name=display,
        practitioner_name=practitioner_name,
        message=payload.message,
        login_url=login_url,
    )
    sent = await send_email(
        to_email=to_email,
        subject=payload.subject,
        html_body=html,
        text_body=text,
        audience="client",
    )
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="L'envoi du courriel a échoué — réessayez ou vérifiez la configuration SMTP.",
        )
    return {"sent": True, "to": to_email}


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
