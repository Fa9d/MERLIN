from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

import httpx
from livekit import api as livekit_api
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai.anthropic_session_note_pipeline import (
    AnthropicSessionNoteError,
    generate_session_note_from_transcript,
)
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.audio_recording import AudioRecording
from app.models.audio_session import AudioSession
from app.models.client import Client
from app.models.derived_document import DerivedDocument
from app.models.enums import (
    AnalysisNextStepCode,
    AudioProviderCode,
    AudioRecordingStatusCode,
    AudioSessionStatusCode,
    RiskLevelCode,
)
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.services.session_documents import ensure_session_derived_document
from app.services.transcription import (
    resolve_provider as resolve_transcription_provider,
    transcribe_with_faster_whisper,
)


logger = logging.getLogger(__name__)

ASSEMBLYAI_UPLOAD_URL = "https://api.assemblyai.com/v2/upload"
ASSEMBLYAI_TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"


class LiveKitAudioError(RuntimeError):
    pass


def normalize_livekit_api_url(ws_url: str) -> str:
    if ws_url.startswith("ws://"):
        return f"http://{ws_url.removeprefix('ws://')}"
    if ws_url.startswith("wss://"):
        return f"https://{ws_url.removeprefix('wss://')}"
    return ws_url


def ensure_livekit_config() -> tuple[str, str, str]:
    if not settings.livekit_url:
        raise LiveKitAudioError("LIVEKIT_URL est absente.")
    if not settings.livekit_api_key:
        raise LiveKitAudioError("LIVEKIT_API_KEY est absente.")
    if not settings.livekit_api_secret:
        raise LiveKitAudioError("LIVEKIT_API_SECRET est absente.")
    return settings.livekit_url, settings.livekit_api_key, settings.livekit_api_secret


def build_room_name(session_record: SessionRecord) -> str:
    return session_record.room_name or f"merlin-session-{session_record.session_sequence_number}-{session_record.id[:8]}"


def build_practitioner_identity(session_record: SessionRecord) -> str:
    return f"practitioner-{session_record.operator_user_id[:8]}"


def build_client_identity(session_record: SessionRecord) -> str:
    return f"client-{session_record.client_id[:8]}"


def build_join_token(
    room_name: str,
    participant_identity: str,
    participant_name: str,
) -> str:
    _, api_key, api_secret = ensure_livekit_config()
    token = (
        livekit_api.AccessToken(api_key=api_key, api_secret=api_secret)
        .with_identity(participant_identity)
        .with_name(participant_name)
        .with_grants(
            livekit_api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True,
            )
        )
    )
    return token.to_jwt()


def ensure_audio_session(
    db: Session,
    session_record: SessionRecord,
) -> AudioSession:
    audio_session = db.scalar(select(AudioSession).where(AudioSession.session_id == session_record.id))
    if audio_session is None:
        audio_session = AudioSession(
            session_id=session_record.id,
            provider_code=AudioProviderCode.livekit,
            audio_session_status_code=AudioSessionStatusCode.provisioned,
            room_name=build_room_name(session_record),
            provider_room_url=settings.livekit_url,
            recording_enabled=settings.media_recording_enabled,
            operator_participant_identity=f"operator-{session_record.operator_user_id[:8]}",
            client_participant_identity=build_client_identity(session_record),
            practitioner_participant_identity=build_practitioner_identity(session_record),
        )
        db.add(audio_session)
    else:
        audio_session.room_name = session_record.room_name or audio_session.room_name
        audio_session.provider_room_url = settings.livekit_url
        audio_session.recording_enabled = settings.media_recording_enabled
        audio_session.practitioner_participant_identity = build_practitioner_identity(session_record)
        audio_session.client_participant_identity = build_client_identity(session_record)
    return audio_session


async def create_livekit_room_for_session(
    db: Session,
    session_record: SessionRecord,
) -> dict[str, str | None]:
    livekit_url, _, _ = ensure_livekit_config()
    room_name = build_room_name(session_record)

    room_sid = session_record.room_sid
    if room_sid is None:
        async with livekit_api.LiveKitAPI(
            url=normalize_livekit_api_url(livekit_url),
            api_key=settings.livekit_api_key,
            api_secret=settings.livekit_api_secret,
        ) as lkapi:
            room = await lkapi.room.create_room(
                livekit_api.CreateRoomRequest(
                    name=room_name,
                    empty_timeout=60 * 15,
                    departure_timeout=60,
                    max_participants=4,
                )
            )
        room_sid = room.sid or None

    session_record.room_name = room_name
    session_record.room_sid = room_sid
    audio_session = ensure_audio_session(db, session_record)
    audio_session.room_name = room_name
    db.add(session_record)
    db.add(audio_session)
    db.commit()
    db.refresh(session_record)
    db.refresh(audio_session)

    practitioner_identity = audio_session.practitioner_participant_identity or build_practitioner_identity(
        session_record
    )
    client_identity = audio_session.client_participant_identity

    client = db.get(Client, session_record.client_id)
    practitioner_token = build_join_token(
        room_name=room_name,
        participant_identity=practitioner_identity,
        participant_name="Praticien IVIA",
    )
    client_token = build_join_token(
        room_name=room_name,
        participant_identity=client_identity,
        participant_name=(client.first_name_or_alias if client else "Client"),
    )

    return {
        "room_name": room_name,
        "room_sid": room_sid,
        "livekit_url": livekit_url,
        "practitioner_identity": practitioner_identity,
        "practitioner_token": practitioner_token,
        "client_identity": client_identity,
        "client_token": client_token,
    }


def _build_local_output_path(room_name: str) -> str:
    recordings_dir = Path(settings.livekit_recording_local_dir).resolve()
    recordings_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{room_name}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.ogg"
    return str(recordings_dir / filename)


def _build_s3_output_key(session_record: SessionRecord) -> str:
    return (
        f"sessions/{session_record.client_id}/{session_record.id}/"
        f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.ogg"
    )


def _build_encoded_output(session_record: SessionRecord) -> tuple[livekit_api.EncodedFileOutput, str]:
    storage_mode = settings.livekit_recording_storage.lower()
    if storage_mode == "s3":
        if not all(
            [
                settings.livekit_s3_bucket,
                settings.livekit_s3_access_key,
                settings.livekit_s3_secret_key,
                settings.livekit_s3_region,
            ]
        ):
            raise LiveKitAudioError("Configuration S3 LiveKit incomplete.")
        output_key = _build_s3_output_key(session_record)
        return (
            livekit_api.EncodedFileOutput(
                file_type=livekit_api.EncodedFileType.OGG,
                filepath=output_key,
                s3=livekit_api.S3Upload(
                    access_key=settings.livekit_s3_access_key,
                    secret=settings.livekit_s3_secret_key,
                    region=settings.livekit_s3_region,
                    endpoint=settings.livekit_s3_endpoint or "",
                    bucket=settings.livekit_s3_bucket,
                    force_path_style=settings.livekit_s3_force_path_style,
                ),
            ),
            output_key,
        )

    output_path = _build_local_output_path(build_room_name(session_record))
    return (
        livekit_api.EncodedFileOutput(
            file_type=livekit_api.EncodedFileType.OGG,
            filepath=output_path,
        ),
        output_path,
    )


def _latest_audio_recording_for_session(db: Session, session_id: str) -> AudioRecording | None:
    audio_session = db.scalar(select(AudioSession).where(AudioSession.session_id == session_id))
    if audio_session is None:
        return None
    return db.scalar(
        select(AudioRecording)
        .where(AudioRecording.audio_session_id == audio_session.id)
        .order_by(AudioRecording.created_at.desc())
    )


async def start_livekit_recording_for_session(
    db: Session,
    session_record: SessionRecord,
    current_user_id: str,
) -> AudioRecording:
    livekit_url, _, _ = ensure_livekit_config()
    if not session_record.room_name:
        await create_livekit_room_for_session(db, session_record)
        db.refresh(session_record)

    if session_record.egress_id:
        raise LiveKitAudioError("Un enregistrement LiveKit est deja actif pour cette seance.")

    audio_session = ensure_audio_session(db, session_record)
    db.add(audio_session)
    db.commit()
    db.refresh(audio_session)

    output_file, output_target = _build_encoded_output(session_record)
    recording = AudioRecording(
        audio_session_id=audio_session.id,
        provider_code=AudioProviderCode.livekit,
        audio_recording_status_code=AudioRecordingStatusCode.starting,
        requested_by_user_id=current_user_id,
        output_location=output_target,
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)

    try:
        async with livekit_api.LiveKitAPI(
            url=normalize_livekit_api_url(livekit_url),
            api_key=settings.livekit_api_key,
            api_secret=settings.livekit_api_secret,
        ) as lkapi:
            # Pragmatic choice: room composite audio-only captures the full room mix reliably.
            egress_info = await lkapi.egress.start_room_composite_egress(
                livekit_api.RoomCompositeEgressRequest(
                    room_name=session_record.room_name,
                    audio_only=True,
                    file_outputs=[output_file],
                )
            )
        session_record.egress_id = egress_info.egress_id or None
        recording.provider_recording_id = egress_info.egress_id or None
        recording.audio_recording_status_code = AudioRecordingStatusCode.recording
        recording.started_at = datetime.now(timezone.utc)
        recording.failure_reason = None
        audio_session.audio_session_status_code = AudioSessionStatusCode.active
        db.add(session_record)
        db.add(audio_session)
    except Exception as exc:
        recording.audio_recording_status_code = AudioRecordingStatusCode.failed
        recording.failure_reason = str(exc)

    db.add(recording)
    db.commit()
    db.refresh(recording)
    return recording


async def stop_livekit_recording_for_session(
    db: Session,
    session_record: SessionRecord,
) -> AudioRecording:
    livekit_url, _, _ = ensure_livekit_config()
    if not session_record.egress_id:
        raise LiveKitAudioError("Aucun egress actif pour cette seance.")

    recording = _latest_audio_recording_for_session(db, session_record.id)
    if recording is None:
        raise LiveKitAudioError("Aucun enregistrement audio associe a cette seance.")

    try:
        async with livekit_api.LiveKitAPI(
            url=normalize_livekit_api_url(livekit_url),
            api_key=settings.livekit_api_key,
            api_secret=settings.livekit_api_secret,
        ) as lkapi:
            egress_info = await lkapi.egress.stop_egress(
                livekit_api.StopEgressRequest(egress_id=session_record.egress_id)
            )
        output_location = recording.output_location
        if egress_info.file_results:
            output_location = egress_info.file_results[0].location or output_location
        recording.output_location = output_location
        recording.audio_recording_status_code = AudioRecordingStatusCode.ready
        recording.ended_at = datetime.now(timezone.utc)
        recording.failure_reason = None
        session_record.audio_file_path = output_location
        session_record.egress_id = None
        audio_session = db.scalar(select(AudioSession).where(AudioSession.session_id == session_record.id))
        if audio_session is not None:
            audio_session.audio_session_status_code = AudioSessionStatusCode.closed
            db.add(audio_session)
    except Exception as exc:
        recording.audio_recording_status_code = AudioRecordingStatusCode.failed
        recording.failure_reason = str(exc)

    db.add(recording)
    db.add(session_record)
    db.commit()
    db.refresh(recording)
    db.refresh(session_record)
    return recording


async def _upload_audio_to_assemblyai(audio_path: str) -> str:
    headers = {"authorization": settings.assemblyai_api_key or ""}
    async with httpx.AsyncClient(timeout=120.0) as client:
        with open(audio_path, "rb") as audio_file:
            upload_response = await client.post(
                ASSEMBLYAI_UPLOAD_URL,
                headers=headers,
                content=audio_file.read(),
            )
        upload_response.raise_for_status()
        return upload_response.json()["upload_url"]


async def _transcribe_audio_with_assemblyai(audio_path: str) -> str:
    if not settings.assemblyai_api_key:
        raise LiveKitAudioError("ASSEMBLYAI_API_KEY est absente.")

    if audio_path.startswith("http://") or audio_path.startswith("https://"):
        audio_url = audio_path
    else:
        audio_url = await _upload_audio_to_assemblyai(audio_path)

    headers = {"authorization": settings.assemblyai_api_key}
    async with httpx.AsyncClient(timeout=120.0) as client:
        transcript_response = await client.post(
            ASSEMBLYAI_TRANSCRIPT_URL,
            headers=headers,
            json={"audio_url": audio_url, "language_code": "fr"},
        )
        transcript_response.raise_for_status()
        transcript_id = transcript_response.json()["id"]

        for _ in range(120):
            poll_response = await client.get(
                f"{ASSEMBLYAI_TRANSCRIPT_URL}/{transcript_id}",
                headers=headers,
            )
            poll_response.raise_for_status()
            payload = poll_response.json()
            if payload["status"] == "completed":
                return payload.get("text", "")
            if payload["status"] == "error":
                raise LiveKitAudioError(
                    f"Transcription AssemblyAI en echec: {payload.get('error', 'erreur inconnue')}"
                )
            await asyncio.sleep(2)

    raise LiveKitAudioError("Timeout AssemblyAI durant la transcription.")


def _coerce_vigilance_level(value: str | None) -> RiskLevelCode:
    try:
        return RiskLevelCode(value or RiskLevelCode.non_urgent.value)
    except ValueError:
        return RiskLevelCode.non_urgent


def _coerce_next_step_type(value: str | None) -> AnalysisNextStepCode | None:
    if value is None:
        return None
    try:
        return AnalysisNextStepCode(value)
    except ValueError:
        return None


async def run_post_recording_pipeline(session_id: str, audio_file_path: str) -> None:
    provider = resolve_transcription_provider()
    if provider == "assemblyai" and not settings.assemblyai_api_key:
        logger.info(
            "Pipeline post-enregistrement ignore pour %s: aucun provider de transcription "
            "(faster-whisper non installe, ASSEMBLYAI_API_KEY absente).",
            session_id,
        )
        return

    try:
        if provider == "faster_whisper":
            transcript_text = await transcribe_with_faster_whisper(audio_file_path)
        else:
            transcript_text = await _transcribe_audio_with_assemblyai(audio_file_path)
        if not transcript_text.strip():
            logger.warning("Transcription vide pour la seance %s.", session_id)
            return
    except Exception as exc:
        logger.exception(
            "Echec transcription (%s) pour %s: %s", provider, session_id, exc
        )
        return

    with SessionLocal() as db:
        session_record = db.get(SessionRecord, session_id)
        if session_record is None:
            logger.warning("Seance introuvable pour pipeline post-enregistrement: %s", session_id)
            return

        existing_note = db.scalar(
            select(SessionNote).where(SessionNote.session_id == session_id).order_by(
                SessionNote.created_at.desc()
            )
        )
        if existing_note is not None:
            existing_document = db.scalar(
                select(DerivedDocument).where(DerivedDocument.source_note_id == existing_note.id)
            )
            if existing_document is None:
                ensure_session_derived_document(db, session_record, existing_note)
                db.commit()
            logger.info(
                "Note deja presente pour la seance %s, pipeline audio ignore pour eviter un doublon.",
                session_id,
            )
            return

        try:
            ai_payload = await generate_session_note_from_transcript(
                transcript_text,
                session_context={
                    "session_id": session_record.id,
                    "client_id": session_record.client_id,
                    "session_sequence_number": session_record.session_sequence_number,
                    "session_mode_code": session_record.session_mode_code.value,
                    "session_channel_code": session_record.session_channel_code.value,
                    "audio_file_path": audio_file_path,
                    "source": "livekit_recording",
                },
            )
        except AnthropicSessionNoteError as exc:
            logger.exception("Echec generation Claude post-enregistrement pour %s: %s", session_id, exc)
            return

        production_note = ai_payload.get("production_note", {})
        client_delivery = ai_payload.get("client_delivery", {})
        supervision_block = ai_payload.get("supervision", {})
        research_block = ai_payload.get("research", {})
        metadata = ai_payload.get("metadata", {})
        latest_note_sequence_number = db.scalar(
            select(func.max(SessionNote.note_sequence_number)).where(SessionNote.session_id == session_id)
        )

        generated_note = SessionNote(
            session_id=session_record.id,
            client_id=session_record.client_id,
            note_sequence_number=(latest_note_sequence_number or 0) + 1,
            summary_text=production_note.get("summary_text")
            or f"Note generee automatiquement a partir de l'enregistrement de la seance {session_record.session_sequence_number}.",
            observations_text=production_note.get("observations_text"),
            follow_up_actions_text=production_note.get("follow_up_actions_text"),
            next_session_focus_text=production_note.get("next_session_focus_text"),
            coeur_summary_text=production_note.get("coeur_summary_text"),
            corps_summary_text=production_note.get("corps_summary_text"),
            esprit_summary_text=production_note.get("esprit_summary_text"),
            etre_summary_text=production_note.get("etre_summary_text"),
            immediate_context_text=production_note.get("immediate_context_text"),
            context_factors_json=production_note.get("context_factors_json"),
            context_hypotheses_json=production_note.get("context_hypotheses_json"),
            identified_tensions_json=production_note.get("identified_tensions_json"),
            vigilance_level_code=_coerce_vigilance_level(production_note.get("vigilance_level_code")),
            next_step_type_code=_coerce_next_step_type(production_note.get("next_step_type_code")),
            client_facing_summary_text=client_delivery.get("client_facing_summary_text"),
            supervision_summary_text=supervision_block.get("supervision_summary_text"),
            research_notes_text=research_block.get("research_notes_text"),
            model_used=metadata.get("model_used"),
            prompt_version=metadata.get("prompt_version"),
            complexity_score=metadata.get("complexity_score"),
            validated_by_practitioner=bool(metadata.get("validated_by_practitioner", False)),
            practitioner_corrections=metadata.get("practitioner_corrections"),
            client_visible=False,
            record_status=session_record.record_status,
            data_sensitivity_class=session_record.data_sensitivity_class,
            retention_class=session_record.retention_class,
        )
        db.add(generated_note)
        db.flush()
        ensure_session_derived_document(db, session_record, generated_note)
        db.commit()
        logger.info("Pipeline post-enregistrement complete pour la seance %s.", session_id)
