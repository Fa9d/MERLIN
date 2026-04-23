from fastapi import APIRouter, Depends, HTTPException, Query, status
from livekit import api as livekit_api
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_internal_clinical_roles, require_operator
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.audio_session import AudioSession
from app.models.enums import AudioSessionStatusCode, SessionStatusCode
from app.models.session import SessionRecord
from app.schemas.audio_session import AudioSessionJoinRead, AudioSessionProvision, AudioSessionRead

router = APIRouter(prefix="/audio-sessions", tags=["audio-sessions"])


def _build_room_name(session_record: SessionRecord) -> str:
    return f"merlin-session-{session_record.session_sequence_number}-{session_record.id[:8]}"


def _build_client_identity(session_record: SessionRecord) -> str:
    return f"client-{session_record.client_id[:8]}"


def _ensure_livekit_config() -> tuple[str, str, str]:
    if not settings.media_livekit_ws_url:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MERLIN_MEDIA_LIVEKIT_WS_URL est absent.",
        )
    if not settings.media_livekit_api_key:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MERLIN_MEDIA_LIVEKIT_API_KEY est absent.",
        )
    if not settings.media_livekit_api_secret:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MERLIN_MEDIA_LIVEKIT_API_SECRET est absent.",
        )
    return (
        settings.media_livekit_ws_url,
        settings.media_livekit_api_key,
        settings.media_livekit_api_secret,
    )


def _build_operator_join_token(audio_session: AudioSession, current_user: AppUser) -> str:
    return _build_join_token(
        audio_session=audio_session,
        participant_identity=audio_session.operator_participant_identity,
        participant_name=current_user.display_name,
    )


def _build_join_token(
    audio_session: AudioSession,
    participant_identity: str,
    participant_name: str,
) -> str:
    _, api_key, api_secret = _ensure_livekit_config()
    token = (
        livekit_api.AccessToken(api_key=api_key, api_secret=api_secret)
        .with_identity(participant_identity)
        .with_name(participant_name)
        .with_grants(
            livekit_api.VideoGrants(
                room_join=True,
                room=audio_session.room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True,
            )
        )
    )
    return token.to_jwt()


@router.post(
    "/sessions/{session_id}/provision",
    response_model=AudioSessionRead,
    status_code=status.HTTP_201_CREATED,
)
def provision_audio_session(
    session_id: str,
    payload: AudioSessionProvision,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> AudioSession:
    session_record = db.get(SessionRecord, session_id)
    if session_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seance introuvable.")

    if session_record.session_status_code in {
        SessionStatusCode.completed,
        SessionStatusCode.cancelled,
        SessionStatusCode.no_show,
        SessionStatusCode.escalated,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de preparer l'audio pour une seance cloturee.",
        )

    existing_audio_session = db.scalar(
        select(AudioSession).where(AudioSession.session_id == session_id)
    )
    if existing_audio_session is not None:
        if session_record.session_status_code == SessionStatusCode.in_progress:
            existing_audio_session.audio_session_status_code = AudioSessionStatusCode.active
            db.add(existing_audio_session)
            db.commit()
            db.refresh(existing_audio_session)
        return existing_audio_session

    provider_room_url = None
    if settings.media_livekit_ws_url:
        provider_room_url = settings.media_livekit_ws_url

    audio_session = AudioSession(
        session_id=session_record.id,
        audio_session_status_code=(
            AudioSessionStatusCode.active
            if session_record.session_status_code == SessionStatusCode.in_progress
            else AudioSessionStatusCode.provisioned
        ),
        room_name=_build_room_name(session_record),
        provider_room_url=provider_room_url,
        recording_enabled=settings.media_recording_enabled,
        operator_participant_identity=f"operator-{current_user.id[:8]}",
        client_participant_identity=_build_client_identity(session_record),
        practitioner_participant_identity=payload.practitioner_participant_identity,
    )
    db.add(audio_session)
    db.commit()
    db.refresh(audio_session)
    return audio_session


@router.get("", response_model=list[AudioSessionRead])
def list_audio_sessions(
    session_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[AudioSession]:
    statement = select(AudioSession).order_by(AudioSession.created_at.desc())
    if session_id is not None:
        statement = statement.where(AudioSession.session_id == session_id)
    return list(db.scalars(statement).all())


@router.get("/{audio_session_id}", response_model=AudioSessionRead)
def get_audio_session(
    audio_session_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> AudioSession:
    audio_session = db.get(AudioSession, audio_session_id)
    if audio_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session audio introuvable.")
    return audio_session


@router.post("/{audio_session_id}/operator-join", response_model=AudioSessionJoinRead)
def create_operator_join_context(
    audio_session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> AudioSessionJoinRead:
    audio_session = db.get(AudioSession, audio_session_id)
    if audio_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session audio introuvable.")

    ws_url, _, _ = _ensure_livekit_config()
    token = _build_operator_join_token(audio_session, current_user)
    return AudioSessionJoinRead(
        audio_session_id=audio_session.id,
        room_name=audio_session.room_name,
        participant_identity=audio_session.operator_participant_identity,
        provider_code=audio_session.provider_code,
        ws_url=ws_url,
        token=token,
    )


@router.post("/{audio_session_id}/client-join", response_model=AudioSessionJoinRead)
def create_client_join_context(
    audio_session_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_operator()),
) -> AudioSessionJoinRead:
    audio_session = db.get(AudioSession, audio_session_id)
    if audio_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session audio introuvable.")

    ws_url, _, _ = _ensure_livekit_config()
    token = _build_join_token(
        audio_session=audio_session,
        participant_identity=audio_session.client_participant_identity,
        participant_name="Client test",
    )
    return AudioSessionJoinRead(
        audio_session_id=audio_session.id,
        room_name=audio_session.room_name,
        participant_identity=audio_session.client_participant_identity,
        provider_code=audio_session.provider_code,
        ws_url=ws_url,
        token=token,
    )
