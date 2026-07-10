"""Enregistrements solo du client connecté — /me/recordings.

Flux : le client enregistre sa voix dans le navigateur (MediaRecorder), envoie
le fichier en base64 avec sa formule, et la transcription tourne en tâche de
fond (faster-whisper local — données Québec, Loi 25). Le client peut ensuite
relire ses propres mots ; la note praticien générée par le pipeline reste côté
praticien, soumise à validation humaine (constitution MERLIN).

Les consentements consent_recording + consent_transcription sont capturés au
moment de l'envoi, rattachés à la séance créée (granted_by = client).
"""

import base64
import logging
import os
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_verified_email_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_entitlement import ClientEntitlement
from app.models.consent import Consent
from app.models.enums import (
    AppRole,
    ClientEntitlementTypeCode,
    ConsentTypeCode,
    GrantedByActorCode,
    RecordStatus,
    SessionChannelCode,
    SessionModeCode,
    SessionStatusCode,
)
from app.models.session import SessionRecord
from app.schemas.me_recording import MyRecordingCreate, MyRecordingRead
from app.services import billing
from app.services.livekit_audio import run_post_recording_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/me/recordings", tags=["enregistrements-client"])

# ---------------------------------------------------------------------------
# Formules — source de vérité serveur. Ajouter une formule = une entrée ici
# (le frontend lit la même clé via ?formule=). Durées en secondes, avec marge.
# ---------------------------------------------------------------------------
FORMULES: dict[str, dict] = {
    "solo30": {"label": "Séance solo · 30 minutes", "max_seconds": 30 * 60 + 90},
    "solo60": {"label": "Séance solo · 1 heure", "max_seconds": 60 * 60 + 90},
    "libre": {"label": "Enregistrement libre", "max_seconds": 40 * 60 + 90},
    # Séance live (déjà payée à la réservation) : pas de frais ici, plafond large.
    "seance": {"label": "Séance live", "max_seconds": 90 * 60 + 90},
}

# Formule payante → offre du catalogue (interrupteur admin is_offer_payant).
# Le solo30 correspond à l'offre vendue « enr_rappel » (35 $ — enregistrement + rappel
# 10 min) ; libre/solo60 restent gratuits (démo / hors catalogue public).
FORMULE_OFFER: dict[str, str] = {"solo30": "enr_rappel"}


def _solo_credit(db: Session, client_id: str) -> ClientEntitlement | None:
    """Crédit d'enregistrement solo disponible (quantity_remaining > 0)."""
    return db.scalar(
        select(ClientEntitlement)
        .where(ClientEntitlement.client_id == client_id)
        .where(
            ClientEntitlement.entitlement_type_code
            == ClientEntitlementTypeCode.solo_recording_credit
        )
        .where(ClientEntitlement.quantity_remaining > 0)
        .order_by(ClientEntitlement.created_at.asc())
    )

_MAX_UPLOAD_BYTES = 60 * 1024 * 1024  # nginx plafonne à 64m — garder une marge
_STORAGE_DIR = "/app/storage/recordings"
_ROOM_PREFIX = "solo"  # room_name = "solo:<formule>" — marqueur d'enregistrement solo


def _get_or_create_my_client(current_user: AppUser, db: Session) -> Client:
    """Même logique que /me/journal : le premier geste crée le dossier client."""
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
    db.flush()
    return client


def _formule_from_room_name(room_name: str | None) -> str | None:
    if room_name and room_name.startswith(f"{_ROOM_PREFIX}:"):
        return room_name.split(":", 1)[1]
    return None


def _default_practitioner(db: Session) -> AppUser | None:
    """Praticien·ne attribué·e par défaut à une séance solo.

    Tant qu'il n'y a qu'un·e seul·e praticien·ne publié·e et active, on l'attribue
    automatiquement (« votre praticien IVIA ») pour que la séance arrive dans son
    espace. Avec plusieurs praticien·nes, l'attribution automatique est désactivée
    (None) — une page de sélection devra précéder l'envoi.
    """
    prats = db.scalars(
        select(AppUser).where(
            AppUser.role == AppRole.practitioner,
            AppUser.record_status == RecordStatus.active,
            AppUser.is_publicly_listed == True,  # noqa: E712
        )
    ).all()
    return prats[0] if len(prats) == 1 else None


def _resolve_practitioner(praticien_id: str | None, db: Session) -> AppUser | None:
    """Résout un praticien_id fourni par le client.

    Valide que la cible est bien un·e praticien·ne actif·ve — refuse silencieusement
    si l'id est inconnu ou n'est pas un praticien (repli sur défaut serveur).
    """
    if not praticien_id:
        return None
    user = db.get(AppUser, praticien_id)
    if user and user.role == AppRole.practitioner and user.record_status == RecordStatus.active:
        return user
    return None


def _to_read(record: SessionRecord, db: Session | None = None) -> MyRecordingRead:
    praticien_name = None
    if db is not None and record.operator_user_id:
        op = db.get(AppUser, record.operator_user_id)
        # Le destinataire n'est un praticien que si c'en est un — le client
        # attribué à lui-même (mode autonome pur) reste sans destinataire.
        if op is not None and op.role == AppRole.practitioner:
            praticien_name = op.display_name
    return MyRecordingRead(
        id=record.id,
        formule=_formule_from_room_name(record.room_name),
        created_at=record.created_at,
        actual_end_at=record.actual_end_at,
        duration_minutes=record.duration_minutes,
        status=record.session_status_code.value,
        transcript_ready=bool(record.transcript_text),
        praticien_name=praticien_name,
    )


@router.post("", response_model=MyRecordingRead, status_code=status.HTTP_202_ACCEPTED)
async def upload_my_recording(
    payload: MyRecordingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> MyRecordingRead:
    """Reçoit l'audio solo du client et lance la transcription en tâche de fond."""
    formule = FORMULES.get(payload.formule)
    if formule is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Formule inconnue : {payload.formule}. Disponibles : {', '.join(FORMULES)}.",
        )
    if payload.duration_seconds and payload.duration_seconds > formule["max_seconds"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Durée au-delà de la formule « {formule['label']} ».",
        )

    try:
        audio_bytes = base64.b64decode(payload.audio_data, validate=True)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="audio_data invalide : base64 attendu.",
        )
    if not audio_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Audio vide.")
    if len(audio_bytes) > _MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Fichier audio trop volumineux.",
        )

    client = _get_or_create_my_client(current_user, db)

    # Interrupteur de facturation : si l'offre liée à la formule est payante, exiger
    # un crédit (acheté via /payments/stripe/public-checkout, produit solo_recording)
    # et le consommer. Offre décochée côté admin → gratuit (mode test).
    offer_code = FORMULE_OFFER.get(payload.formule)
    solo_credit: ClientEntitlement | None = None
    if offer_code is not None and billing.is_offer_payant(db, offer_code):
        solo_credit = _solo_credit(db, client.id)
        if solo_credit is None:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Paiement requis pour cet enregistrement.",
            )

    next_seq = (
        db.scalar(
            select(func.max(SessionRecord.session_sequence_number)).where(
                SessionRecord.client_id == client.id
            )
        )
        or 0
    ) + 1

    now = datetime.now(timezone.utc)
    duration_minutes = (
        max(1, round(payload.duration_seconds / 60)) if payload.duration_seconds else None
    )
    record = SessionRecord(
        id=str(uuid4()),
        client_id=client.id,
        session_sequence_number=next_seq,
        session_mode_code=SessionModeCode.standard,
        session_channel_code=SessionChannelCode.audio_async,
        actual_start_at=now,
        duration_minutes=duration_minutes,
        room_name=f"{_ROOM_PREFIX}:{payload.formule}",
        # Attribution : praticien choisi par le client > défaut serveur > client lui-même.
        operator_user_id=(
            _resolve_practitioner(payload.praticien_id, db)
            or _default_practitioner(db)
            or current_user
        ).id,
        session_status_code=SessionStatusCode.in_progress,
    )
    db.add(record)
    db.flush()

    # Consentements capturés au moment du geste (Loi 25) — rattachés à la séance.
    for consent_type in (ConsentTypeCode.consent_recording, ConsentTypeCode.consent_transcription):
        db.add(
            Consent(
                client_id=client.id,
                session_id=record.id,
                consent_type_code=consent_type,
                consent_value=True,
                granted_by_actor_code=GrantedByActorCode.client,
            )
        )

    os.makedirs(_STORAGE_DIR, exist_ok=True)
    safe_ext = os.path.splitext(payload.filename)[1].lstrip(".") or "webm"
    file_path = os.path.join(_STORAGE_DIR, f"session_{record.id}_solo.{safe_ext}")
    with open(file_path, "wb") as out:
        out.write(audio_bytes)
    record.audio_file_path = file_path

    # Consommation du crédit (après écriture réussie du fichier).
    if solo_credit is not None:
        solo_credit.quantity_remaining -= 1
        db.add(solo_credit)

    db.add(record)
    db.commit()
    db.refresh(record)

    background_tasks.add_task(run_post_recording_pipeline, record.id, file_path)
    logger.info(
        "Enregistrement solo recu (%s, formule=%s, %d octets) — transcription en file.",
        record.id,
        payload.formule,
        len(audio_bytes),
    )
    return _to_read(record, db)


@router.get("/access")
def solo_recording_access(
    formule: str = "solo30",
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> dict:
    """Indique si la formule exige un paiement et si le client a déjà un crédit.

    `needs_payment` True → le frontend affiche « Payer » avant l'enregistrement.
    """
    offer_code = FORMULE_OFFER.get(formule)
    payant = offer_code is not None and billing.is_offer_payant(db, offer_code)
    has_credit = False
    if payant:
        client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
        has_credit = client is not None and _solo_credit(db, client.id) is not None
    return {
        "formule": formule,
        "offer_code": offer_code,
        "payant": payant,
        "has_credit": has_credit,
        "needs_payment": bool(payant and not has_credit),
        "amount_cents": settings.stripe_solo_amount_cents if payant else 0,
    }


@router.get("", response_model=list[MyRecordingRead])
def list_my_recordings(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> list[MyRecordingRead]:
    """Liste les enregistrements solo du client connecté (plus récents d'abord)."""
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        return []
    records = db.scalars(
        select(SessionRecord)
        .where(
            SessionRecord.client_id == client.id,
            SessionRecord.session_channel_code == SessionChannelCode.audio_async,
        )
        .order_by(SessionRecord.created_at.desc())
    ).all()
    return [_to_read(r, db) for r in records]
