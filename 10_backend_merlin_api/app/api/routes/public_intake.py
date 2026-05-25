"""Parcours public d'entrée IVIA : un seul appel orchestre intake + magic link.

Le formulaire `/rendez-vous` côté frontend appelle `POST /public/intake/start` :
- crée le `Client` (avec email/téléphone optionnels) ;
- crée l'`IntakeRequest` ;
- enregistre les 3 consentements publics autorisés ;
- si un courriel est fourni, crée l'`AppUser` lié, génère un magic link et l'envoie par mail.

L'utilisateur reçoit ensuite un lien qui ouvre `/activer?token=...`.
La route `POST /public/activate/{token}` consomme le token, marque l'email vérifié,
et retourne un JWT pour que le frontend ouvre directement `/mon-espace`.
"""
from __future__ import annotations

import logging
import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, text as sql_text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.consent import Consent
from app.models.enums import (
    AppRole,
    ConsentTypeCode,
    DataSensitivityClass,
    GrantedByActorCode,
    NeedCode,
    RecordStatus,
    RequestChannelCode,
    RequestForCode,
    RiskLevelCode,
)
from app.models.intake_request import IntakeRequest
from app.services.client_activation import (
    activation_is_expired,
    clear_activation_token,
    generate_activation_token,
    hash_activation_token,
    set_activation_token,
    utc_now,
)
from app.services.email import make_magic_link_email, send_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/public", tags=["public_intake"])


# ---------------------------------------------------------------------------
# Schémas
# ---------------------------------------------------------------------------


class PublicIntakeStartIn(BaseModel):
    """Charge utile soumise par `/rendez-vous` (utilisateur non authentifié).

    Le consentement est omnibus : une seule case « J'accepte les CGU et la politique
    de confidentialité » couvre toutes les finalités énumérées dans ces documents
    (Loi 25 art. 14 — consentement présenté distinctement, fins spécifiques nommées
    explicitement dans le document accepté). Le backend en dérive les entrées
    individuelles dans la table `Consent` pour la tenue du registre légal.

    Le consentement biométrique (enregistrement + transcription) reste en dehors
    de cet omnibus : il sera demandé séparément au moment de la première séance,
    conformément à Loi 25 art. 8.1.
    """

    first_name_or_alias: str = Field(min_length=1, max_length=120)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=40)
    is_adult_confirmed: bool

    primary_need_code: NeedCode = NeedCode.support
    perceived_urgency_code: RiskLevelCode = RiskLevelCode.non_urgent
    support_already_in_place: bool = False
    requested_outcome_text: str | None = Field(default=None, max_length=6000)
    entry_summary_text: str | None = None

    consent_terms_accepted: bool
    consent_terms_version: str = Field(default="v1.2", max_length=16)


class PublicIntakeStartOut(BaseModel):
    client_id: str
    public_client_code: str
    intake_request_id: str
    magic_link_sent: bool
    email_used: str | None
    message: str


class PublicActivateOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    display_name: str
    role: str
    client_id: str
    public_client_code: str
    password_needed: bool
    message: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ensure_adult(payload: PublicIntakeStartIn) -> None:
    if not payload.is_adult_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La demande est réservée aux adultes de 18 ans et plus.",
        )


def _ensure_terms_accepted(payload: PublicIntakeStartIn) -> None:
    if not payload.consent_terms_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous devez accepter les CGU et la politique de confidentialité pour continuer.",
        )


def _build_magic_link_url(token: str) -> str:
    base = settings.frontend_url.rstrip("/")
    return f"{base}/activer?token={token}"


# Marqueur stocké dans `password_hash` pour les comptes créés via magic link
# qui n'ont pas encore défini de mot de passe utilisateur. Ce hash est techniquement
# valide mais le mot de passe sous-jacent est aléatoire et jamais communiqué :
# le compte ne peut donc pas être loggé via /auth/login tant que l'utilisateur
# n'a pas défini un vrai mot de passe depuis /mon-espace.
def _generate_placeholder_password_hash() -> str:
    return hash_password(secrets.token_urlsafe(48))


def _attach_or_create_app_user(
    db: Session,
    *,
    email: str,
    display_name: str,
    client: Client,
) -> tuple[AppUser, bool]:
    """Retourne (user, password_needed). Lie le client à l'AppUser au passage."""
    normalized_email = email.lower()

    existing = db.scalar(select(AppUser).where(AppUser.email == normalized_email))
    if existing is not None:
        if client.app_user_id is None:
            # Vérification défensive : ne pas lier si l'AppUser est déjà lié à un autre client
            already_linked = db.scalar(
                select(Client).where(Client.app_user_id == existing.id)
            )
            if already_linked is None:
                client.app_user_id = existing.id
        password_needed = not existing.email_verified
        return existing, password_needed

    new_user = AppUser(
        email=normalized_email,
        password_hash=_generate_placeholder_password_hash(),
        display_name=display_name,
        role=AppRole.public_client,
        email_verified=False,
        record_status=RecordStatus.active,
    )
    db.add(new_user)
    db.flush()  # pour obtenir new_user.id avant d'attacher au client
    client.app_user_id = new_user.id
    return new_user, True


# ---------------------------------------------------------------------------
# POST /public/intake/start
# ---------------------------------------------------------------------------


@router.post(
    "/intake/start",
    response_model=PublicIntakeStartOut,
    status_code=status.HTTP_201_CREATED,
    summary="Orchestrateur public : crée client + intake + consentements + magic link",
)
async def start_public_intake(
    payload: PublicIntakeStartIn,
    db: Session = Depends(get_db),
) -> PublicIntakeStartOut:
    _ensure_adult(payload)
    _ensure_terms_accepted(payload)

    # 1) Trouver ou créer le Client
    # Double-check avec SQL brut pour éviter tout problème de cache ORM.
    client: Client | None = None
    if payload.email:
        normalized_email = payload.email.lower()
        # ORM lookup
        client = db.scalar(
            select(Client).where(Client.email == normalized_email)
        )
        # Si l'ORM ne trouve pas, fallback sur SQL direct (contourne les bugs de cache)
        if client is None:
            row = db.execute(
                sql_text("SELECT id FROM clients WHERE email = :e"),
                {"e": normalized_email},
            ).first()
            if row:
                client = db.get(Client, row[0])
                logger.warning(
                    "find_client ORM miss but SQL found id=%s for email=%s",
                    row[0], normalized_email,
                )
        logger.warning("find_client email=%s found=%s", normalized_email, client.id if client else None)
    if client is None:
        client = Client(
            first_name_or_alias=payload.first_name_or_alias.strip(),
            email=(payload.email.lower() if payload.email else None),
            phone=payload.phone,
            is_adult_confirmed=True,
            record_status=RecordStatus.active,
            data_sensitivity_class=DataSensitivityClass.high,
        )
        db.add(client)
        db.flush()  # obtenir client.id

    # 2) IntakeRequest
    intake = IntakeRequest(
        client_id=client.id,
        request_channel_code=RequestChannelCode.web_form,
        request_for_code=RequestForCode.self,
        primary_need_code=payload.primary_need_code,
        perceived_urgency_code=payload.perceived_urgency_code,
        support_already_in_place=payload.support_already_in_place,
        requested_outcome_text=(payload.requested_outcome_text or None),
        entry_summary_text=(payload.entry_summary_text or None),
        referential_version="v1",
        record_status=RecordStatus.active,
    )
    db.add(intake)

    # 3) Registre légal : un seul opt-in omnibus côté UX est décomposé en trois
    #    entrées `Consent` pour la tenue de registre Loi 25 (art. 14 + politique
    #    gouvernance §5). L'utilisateur n'a jamais vu trois cases : il a accepté
    #    les CGU + politique de confidentialité qui nomment ces trois finalités.
    for type_code in (
        ConsentTypeCode.consent_session,
        ConsentTypeCode.consent_session_note,
        ConsentTypeCode.consent_history,
    ):
        db.add(
            Consent(
                client_id=client.id,
                consent_type_code=type_code,
                consent_value=True,
                consent_version_code=payload.consent_terms_version,
                granted_by_actor_code=GrantedByActorCode.client,
                record_status=RecordStatus.active,
                notes=f"Dérivé de l'acceptation omnibus CGU/Confidentialité {payload.consent_terms_version}",
            )
        )

    # 4) Magic link (uniquement si un email est fourni)
    magic_link_sent = False
    email_used: str | None = None

    if payload.email:
        email_used = payload.email
        app_user, _password_needed = _attach_or_create_app_user(
            db,
            email=payload.email,
            display_name=payload.first_name_or_alias.strip(),
            client=client,
        )

        raw_token = generate_activation_token()
        set_activation_token(client, raw_token)

        db.commit()
        db.refresh(client)
        db.refresh(intake)

        magic_link_url = _build_magic_link_url(raw_token)
        html, text = make_magic_link_email(
            display_name=app_user.display_name,
            magic_link_url=magic_link_url,
        )
        # send_email retourne False en cas de SMTP non configuré ou erreur
        try:
            magic_link_sent = await send_email(
                to_email=app_user.email,
                subject="Votre espace IVIA est prêt — un clic pour ouvrir",
                html_body=html,
                text_body=text,
                audience="client",
            )
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Magic link non envoyé pour %s: %s", app_user.email, exc)
            magic_link_sent = False
    else:
        db.commit()
        db.refresh(client)
        db.refresh(intake)

    if email_used and magic_link_sent:
        message = (
            f"Demande reçue. Un lien d'activation vient d'être envoyé à {email_used}. "
            "Ouvrez votre boîte mail pour accéder à votre espace IVIA."
        )
    elif email_used and not magic_link_sent:
        message = (
            "Demande reçue. L'envoi du lien d'activation a échoué temporairement — "
            "vous pourrez réessayer depuis la page d'accès, ou un membre de l'équipe IVIA vous contactera."
        )
    else:
        message = (
            "Demande reçue. Pour ouvrir un espace personnel et suivre votre démarche, "
            "ajoutez un courriel à votre dossier — un lien d'activation vous sera envoyé."
        )

    return PublicIntakeStartOut(
        client_id=client.id,
        public_client_code=client.public_client_code,
        intake_request_id=intake.id,
        magic_link_sent=magic_link_sent,
        email_used=email_used,
        message=message,
    )


# ---------------------------------------------------------------------------
# POST /public/activate/{token}
# ---------------------------------------------------------------------------


@router.post(
    "/activate/{token}",
    response_model=PublicActivateOut,
    summary="Consomme le magic link et ouvre une session client",
)
def consume_magic_link(token: str, db: Session = Depends(get_db)) -> PublicActivateOut:
    token_hash = hash_activation_token(token)
    client: Client | None = db.scalar(
        select(Client).where(Client.activation_token_hash == token_hash)
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lien d'activation invalide ou déjà utilisé.",
        )

    if activation_is_expired(client):
        clear_activation_token(client)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Ce lien d'activation a expiré. Renouvelez votre demande pour recevoir un nouveau lien.",
        )

    if client.app_user_id is None:
        # Cas dégénéré : un client a un token mais pas d'AppUser lié.
        # Ne devrait pas arriver via le flow normal. Nettoyer le token.
        clear_activation_token(client)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Aucun compte n'est associé à ce lien. Contactez l'équipe IVIA.",
        )

    app_user: AppUser | None = db.get(AppUser, client.app_user_id)
    if app_user is None:
        clear_activation_token(client)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Le compte associé à ce lien est introuvable.",
        )

    # Active le compte et consomme le token
    app_user.email_verified = True
    client.activation_accepted_at = utc_now()
    clear_activation_token(client)

    db.commit()
    db.refresh(app_user)
    db.refresh(client)

    access_token = create_access_token(subject=app_user.id, role=app_user.role.value)

    # `password_needed` indique au frontend s'il doit proposer à l'utilisateur
    # de définir un vrai mot de passe (cas magic-link first sans password).
    # Heuristique : on considère qu'un mot de passe a été défini si l'utilisateur
    # s'est déjà connecté avec un password (cas /acces-client → email_verified
    # passe à true plus tard via verify-email). Comme le magic link force
    # email_verified=True en sortie, on s'appuie sur un marqueur dérivé :
    # si activation_accepted_at vient d'être posé pour la première fois,
    # l'utilisateur n'a probablement pas encore défini de mot de passe.
    # On expose `password_needed = True` par défaut sur magic-link, à charge
    # au frontend de masquer le CTA si l'utilisateur a déjà défini un mdp.
    password_needed = True

    return PublicActivateOut(
        access_token=access_token,
        token_type="bearer",
        user_id=app_user.id,
        email=app_user.email,
        display_name=app_user.display_name,
        role=app_user.role.value,
        client_id=client.id,
        public_client_code=client.public_client_code,
        password_needed=password_needed,
        message="Bienvenue. Votre espace IVIA est ouvert.",
    )


# ---------------------------------------------------------------------------
# GET /public/activate/preview/{token}
# Permet au frontend de prévalider le token avant de l'utiliser (UX douce)
# ---------------------------------------------------------------------------


class PublicActivatePreviewOut(BaseModel):
    valid: bool
    expires_at: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None


@router.get(
    "/activate/preview/{token}",
    response_model=PublicActivatePreviewOut,
    summary="Prévalide un magic link sans le consommer",
)
def preview_magic_link(token: str, db: Session = Depends(get_db)) -> PublicActivatePreviewOut:
    token_hash = hash_activation_token(token)
    client: Client | None = db.scalar(
        select(Client).where(Client.activation_token_hash == token_hash)
    )
    if client is None or activation_is_expired(client):
        return PublicActivatePreviewOut(valid=False)

    app_user: AppUser | None = (
        db.get(AppUser, client.app_user_id) if client.app_user_id else None
    )
    return PublicActivatePreviewOut(
        valid=True,
        expires_at=(
            client.activation_token_expires_at.isoformat()
            if client.activation_token_expires_at
            else None
        ),
        display_name=(app_user.display_name if app_user else client.first_name_or_alias),
        email=(app_user.email if app_user else client.email),
    )
