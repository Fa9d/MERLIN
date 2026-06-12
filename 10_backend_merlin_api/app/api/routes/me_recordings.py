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

from app.core.deps import require_verified_email_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.consent import Consent
from app.models.enums import (
    ConsentTypeCode,
    GrantedByActorCode,
    SessionChannelCode,
    SessionModeCode,
    SessionStatusCode,
)
from app.models.session import SessionRecord
from app.schemas.me_recording import MyRecordingCreate, MyRecordingRead
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
}

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


def _to_read(record: SessionRecord) -> MyRecordingRead:
    return MyRecordingRead(
        id=record.id,
        formule=_formule_from_room_name(record.room_name),
        created_at=record.created_at,
        actual_end_at=record.actual_end_at,
        duration_minutes=record.duration_minutes,
        status=record.session_status_code.value,
        transcript_ready=bool(record.transcript_text),
        transcript_text=record.transcript_text,
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
        operator_user_id=current_user.id,  # solo : le client est l'initiateur
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
    return _to_read(record)


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
    return [_to_read(r) for r in records]
