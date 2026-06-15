"""Séance express — création praticien + accès client par lien (token).

Flux MVP :
1. Le praticien crée une séance express (`POST /sessions/express`) : client ad hoc
   (alias, sans compte), statut de paiement, notes privées. Renvoie un token.
2. Le frontend praticien compose un lien partageable contenant le token.
3. Le client ouvre le lien → `GET /public/express/{token}` (infos d'accueil), puis
   dépose un enregistrement → `POST /public/express/{token}/recording`, qui réutilise
   le pipeline de transcription (faster-whisper, données Québec).

Sécurité : le token est une capacité (hashé SHA-256 au repos). Les endpoints publics
n'exposent jamais d'identifiants internes ni les notes privées du praticien.
Posture non clinique : aucune sortie diagnostic ; validation humaine côté praticien.
"""

import base64
import logging
import os
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_practitioner_or_operator
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
from app.schemas.express import (
    ExpressRecordingResult,
    ExpressRecordingUpload,
    ExpressSessionCreate,
    ExpressSessionCreated,
    ExpressSessionPublic,
)
from app.services.client_activation import generate_activation_token, hash_activation_token
from app.services.livekit_audio import run_post_recording_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(tags=["seance-express"])

_MAX_UPLOAD_BYTES = 60 * 1024 * 1024  # nginx plafonne à 64m — marge de sécurité
_STORAGE_DIR = "/app/storage/recordings"


def _session_by_token_or_404(token: str, db: Session) -> SessionRecord:
    token_hash = hash_activation_token(token)
    session = db.scalar(
        select(SessionRecord).where(SessionRecord.express_token_hash == token_hash)
    )
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lien de séance introuvable ou expiré.")
    return session


# ---------------------------------------------------------------------------
# POST /sessions/express — le praticien crée une séance express
# ---------------------------------------------------------------------------
@router.post("/sessions/express", response_model=ExpressSessionCreated, status_code=status.HTTP_201_CREATED)
def create_express_session(
    payload: ExpressSessionCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> ExpressSessionCreated:
    # Client ad hoc (alias, sans compte) — le lien sert d'accès, pas un compte.
    alias = (payload.client_name or "").strip() or "Invité·e"
    client = Client(first_name_or_alias=alias)
    db.add(client)
    db.flush()

    token = generate_activation_token()
    session = SessionRecord(
        id=str(uuid4()),
        client_id=client.id,
        session_sequence_number=1,
        session_mode_code=SessionModeCode.standard,
        session_channel_code=SessionChannelCode.audio_async,
        operator_user_id=current_user.id,
        praticien_id=current_user.id,
        session_status_code=SessionStatusCode.scheduled,
        duration_minutes=payload.duration_minutes,
        express_token_hash=hash_activation_token(token),
        payment_status=payload.payment_status,
        private_notes=(payload.private_notes or None),
        room_name=f"express:{client.id}",
    )
    db.add(session)
    db.commit()

    logger.info("Séance express créée par %s (session=%s, paiement=%s).",
                current_user.id, session.id, payload.payment_status.value)
    return ExpressSessionCreated(
        session_id=session.id,
        token=token,
        duration_minutes=payload.duration_minutes,
        payment_status=payload.payment_status,
    )


# ---------------------------------------------------------------------------
# GET /public/express/{token} — accueil du client (public)
# ---------------------------------------------------------------------------
@router.get("/public/express/{token}", response_model=ExpressSessionPublic)
def get_express_session_public(token: str, db: Session = Depends(get_db)) -> ExpressSessionPublic:
    session = _session_by_token_or_404(token, db)
    praticien = db.get(AppUser, session.praticien_id) if session.praticien_id else None
    client = db.get(Client, session.client_id)
    return ExpressSessionPublic(
        praticien_display=(praticien.display_name if praticien else None),
        client_display=(client.first_name_or_alias if client else None),
        duration_minutes=session.duration_minutes,
        payment_status=session.payment_status,
        already_recorded=bool(session.audio_file_path),
    )


# ---------------------------------------------------------------------------
# POST /public/express/{token}/recording — le client dépose son enregistrement
# ---------------------------------------------------------------------------
@router.post(
    "/public/express/{token}/recording",
    response_model=ExpressRecordingResult,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_express_recording(
    token: str,
    payload: ExpressRecordingUpload,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ExpressRecordingResult:
    session = _session_by_token_or_404(token, db)

    if session.audio_file_path:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un enregistrement a déjà été déposé pour cette séance.",
        )

    try:
        audio_bytes = base64.b64decode(payload.audio_data, validate=True)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="audio_data invalide : base64 attendu.")
    if not audio_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Audio vide.")
    if len(audio_bytes) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Fichier audio trop volumineux.")

    now = datetime.now(timezone.utc)
    os.makedirs(_STORAGE_DIR, exist_ok=True)
    safe_ext = os.path.splitext(payload.filename)[1].lstrip(".") or "webm"
    file_path = os.path.join(_STORAGE_DIR, f"session_{session.id}_express.{safe_ext}")
    with open(file_path, "wb") as out:
        out.write(audio_bytes)

    session.audio_file_path = file_path
    session.actual_start_at = session.actual_start_at or now
    session.actual_end_at = now
    if payload.duration_seconds:
        session.duration_minutes = max(1, round(payload.duration_seconds / 60))
    session.session_status_code = SessionStatusCode.pending_review

    # Consentements captés au moment du dépôt (Loi 25), rattachés à la séance.
    for consent_type in (ConsentTypeCode.consent_recording, ConsentTypeCode.consent_transcription):
        db.add(
            Consent(
                client_id=session.client_id,
                session_id=session.id,
                consent_type_code=consent_type,
                consent_value=True,
                granted_by_actor_code=GrantedByActorCode.client,
            )
        )

    db.add(session)
    db.commit()

    background_tasks.add_task(run_post_recording_pipeline, session.id, file_path)
    logger.info("Enregistrement express déposé (session=%s, %d octets) — transcription en file.",
                session.id, len(audio_bytes))
    return ExpressRecordingResult(ok=True, transcript_pending=True, recorded_at=now)
