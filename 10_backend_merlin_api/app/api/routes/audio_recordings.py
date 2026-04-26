from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, status
from livekit import api as livekit_api
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import is_operator_user, require_internal_clinical_roles, require_operator
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.audio_recording import AudioRecording
from app.models.audio_session import AudioSession
from app.models.enums import AudioRecordingStatusCode, AudioSessionStatusCode
from app.models.session import SessionRecord
from app.schemas.audio_recording import AudioRecordingRead

router = APIRouter(prefix="/audio-recordings", tags=["audio-recordings"])


def _normalize_livekit_api_url(ws_url: str) -> str:
    if ws_url.startswith("ws://"):
        return f"http://{ws_url.removeprefix('ws://')}"
    if ws_url.startswith("wss://"):
        return f"https://{ws_url.removeprefix('wss://')}"
    return ws_url


def _build_placeholder_output_location(recording: AudioRecording) -> str:
    return f"pending://audio-recordings/{recording.id}"


async def _start_provider_recording(
    audio_session: AudioSession,
    recording: AudioRecording,
) -> tuple[str | None, str | None]:
    if settings.media_recording_strategy == "metadata_only":
        return None, _build_placeholder_output_location(recording)

    if settings.media_recording_strategy != "livekit_egress":
        raise RuntimeError(
            f"Strategie d'enregistrement inconnue: {settings.media_recording_strategy}."
        )

    if not settings.media_livekit_ws_url:
        raise RuntimeError("MERLIN_MEDIA_LIVEKIT_WS_URL est absent.")
    if not settings.media_livekit_api_key:
        raise RuntimeError("MERLIN_MEDIA_LIVEKIT_API_KEY est absent.")
    if not settings.media_livekit_api_secret:
        raise RuntimeError("MERLIN_MEDIA_LIVEKIT_API_SECRET est absent.")

    recordings_dir = Path(settings.media_recordings_dir).resolve()
    recordings_dir.mkdir(parents=True, exist_ok=True)
    output_path = recordings_dir / f"{audio_session.room_name}-{recording.id}.ogg"

    async with livekit_api.LiveKitAPI(
        url=_normalize_livekit_api_url(settings.media_livekit_ws_url),
        api_key=settings.media_livekit_api_key,
        api_secret=settings.media_livekit_api_secret,
    ) as lkapi:
        egress_info = await lkapi.egress.start_room_composite_egress(
            livekit_api.RoomCompositeEgressRequest(
                room_name=audio_session.room_name,
                audio_only=True,
                file_outputs=[
                    livekit_api.EncodedFileOutput(
                        filepath=str(output_path),
                        file_type=livekit_api.EncodedFileType.OGG,
                    )
                ],
            )
        )

    return egress_info.egress_id or None, str(output_path)


async def _stop_provider_recording(recording: AudioRecording) -> str | None:
    if settings.media_recording_strategy == "metadata_only":
        return recording.output_location or _build_placeholder_output_location(recording)

    if settings.media_recording_strategy != "livekit_egress":
        raise RuntimeError(
            f"Strategie d'enregistrement inconnue: {settings.media_recording_strategy}."
        )

    if not recording.provider_recording_id:
        return recording.output_location
    if not settings.media_livekit_ws_url:
        raise RuntimeError("MERLIN_MEDIA_LIVEKIT_WS_URL est absent.")
    if not settings.media_livekit_api_key:
        raise RuntimeError("MERLIN_MEDIA_LIVEKIT_API_KEY est absent.")
    if not settings.media_livekit_api_secret:
        raise RuntimeError("MERLIN_MEDIA_LIVEKIT_API_SECRET est absent.")

    async with livekit_api.LiveKitAPI(
        url=_normalize_livekit_api_url(settings.media_livekit_ws_url),
        api_key=settings.media_livekit_api_key,
        api_secret=settings.media_livekit_api_secret,
    ) as lkapi:
        egress_info = await lkapi.egress.stop_egress(
            livekit_api.StopEgressRequest(egress_id=recording.provider_recording_id)
        )

    if egress_info.file_results:
        return egress_info.file_results[0].location or recording.output_location
    return recording.output_location


@router.get("", response_model=list[AudioRecordingRead])
def list_audio_recordings(
    audio_session_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> list[AudioRecording]:
    statement = select(AudioRecording).order_by(AudioRecording.created_at.desc())
    if is_operator_user(current_user):
        statement = (
            statement.join(AudioSession, AudioSession.id == AudioRecording.audio_session_id)
            .join(SessionRecord, SessionRecord.id == AudioSession.session_id)
            .where(SessionRecord.operator_user_id == current_user.id)
        )
    if audio_session_id is not None:
        statement = statement.where(AudioRecording.audio_session_id == audio_session_id)
    return list(db.scalars(statement).all())


@router.get("/{audio_recording_id}", response_model=AudioRecordingRead)
def get_audio_recording(
    audio_recording_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> AudioRecording:
    audio_recording = db.get(AudioRecording, audio_recording_id)
    if audio_recording is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enregistrement audio introuvable.",
        )
    if is_operator_user(current_user):
        audio_session = db.get(AudioSession, audio_recording.audio_session_id)
        session_record = db.get(SessionRecord, audio_session.session_id) if audio_session else None
        if session_record is None or session_record.operator_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enregistrement audio introuvable.",
            )
    return audio_recording


@router.post("/audio-sessions/{audio_session_id}/start", response_model=AudioRecordingRead, status_code=status.HTTP_201_CREATED)
async def start_audio_recording(
    audio_session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> AudioRecording:
    audio_session = db.get(AudioSession, audio_session_id)
    if audio_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session audio introuvable.")
    if not audio_session.recording_enabled:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="L'enregistrement est desactive pour cette session audio.",
        )
    if audio_session.audio_session_status_code == AudioSessionStatusCode.closed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de lancer un enregistrement sur une session audio cloturee.",
        )

    active_recording = db.scalar(
        select(AudioRecording).where(
            AudioRecording.audio_session_id == audio_session_id,
            AudioRecording.audio_recording_status_code.in_(
                [AudioRecordingStatusCode.starting, AudioRecordingStatusCode.recording]
            ),
        )
    )
    if active_recording is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un enregistrement est deja en cours pour cette session audio.",
        )

    recording = AudioRecording(
        audio_session_id=audio_session.id,
        provider_code=audio_session.provider_code,
        audio_recording_status_code=AudioRecordingStatusCode.starting,
        requested_by_user_id=current_user.id,
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)

    try:
        provider_recording_id, output_location = await _start_provider_recording(audio_session, recording)
        recording.provider_recording_id = provider_recording_id
        recording.output_location = output_location
        recording.audio_recording_status_code = AudioRecordingStatusCode.recording
        recording.started_at = datetime.now(timezone.utc)
        recording.failure_reason = None
    except Exception as exc:
        recording.audio_recording_status_code = AudioRecordingStatusCode.failed
        recording.failure_reason = str(exc)

    db.add(recording)
    db.commit()
    db.refresh(recording)
    return recording


@router.post("/{audio_recording_id}/stop", response_model=AudioRecordingRead)
async def stop_audio_recording(
    audio_recording_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_operator()),
) -> AudioRecording:
    recording = db.get(AudioRecording, audio_recording_id)
    if recording is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enregistrement audio introuvable.",
        )
    if recording.audio_recording_status_code not in {
        AudioRecordingStatusCode.starting,
        AudioRecordingStatusCode.recording,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cet enregistrement n'est pas actif.",
        )

    try:
        recording.output_location = await _stop_provider_recording(recording)
        recording.audio_recording_status_code = AudioRecordingStatusCode.ready
        recording.ended_at = datetime.now(timezone.utc)
        recording.failure_reason = None
    except Exception as exc:
        recording.audio_recording_status_code = AudioRecordingStatusCode.failed
        recording.failure_reason = str(exc)

    db.add(recording)
    db.commit()
    db.refresh(recording)
    return recording
