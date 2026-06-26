import logging
from datetime import datetime, timezone

import base64
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status

logger = logging.getLogger(__name__)
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai.anthropic_session_note_pipeline import (
    AnthropicSessionNoteError,
    generate_session_note_from_transcript,
)
from app.core.deps import is_operator_user, require_internal_clinical_roles, require_operator, require_production_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.audio_recording import AudioRecording
from app.models.audio_session import AudioSession
from app.models.client import Client
from app.models.enums import (
    AnalysisNextStepCode,
    AudioSessionStatusCode,
    RiskLevelCode,
    SessionChannelCode,
    SessionStatusCode,
)
from app.models.intake_request import IntakeRequest
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.services.livekit_audio import (
    LiveKitAudioError,
    create_livekit_room_for_session,
    run_post_recording_pipeline,
    start_livekit_recording_for_session,
    stop_livekit_recording_for_session,
)
from app.services.session_documents import ensure_session_derived_document
from app.schemas.session import (
    SessionAssign,
    SessionClose,
    SessionCloseResult,
    SessionCreate,
    SessionDeliver,
    SessionRecordingRead,
    SessionRoomRead,
    SessionRead,
    SessionStart,
)

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _get_owned_session_or_404(
    session_id: str,
    db: Session,
    current_user: AppUser,
) -> SessionRecord:
    session_record = db.get(SessionRecord, session_id)
    if session_record is None or session_record.operator_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seance introuvable.")
    return session_record


def _compute_duration_minutes(
    actual_start_at,
    actual_end_at,
    current_duration_minutes: int | None,
) -> int | None:
    if actual_start_at and actual_end_at:
        normalized_start = _normalize_datetime(actual_start_at)
        normalized_end = _normalize_datetime(actual_end_at)
        seconds = (normalized_end - normalized_start).total_seconds()
        return int(seconds // 60)
    return current_duration_minutes


def _normalize_datetime(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _build_generated_summary(session_record: SessionRecord, payload: SessionClose) -> str:
    return (
        f"Seance {session_record.session_sequence_number} cloturee avec statut "
        f"{payload.session_status_code.value}. "
        f"Sujet principal: {payload.presenting_topic_text}. "
        f"Points saillants: {payload.session_highlights_text}."
    )


def _build_generated_observations(payload: SessionClose) -> str:
    parts = [f"Niveau de vigilance: {payload.vigilance_level_code.value}."]
    if payload.operator_assessment_text:
        parts.append(f"Evaluation operateur: {payload.operator_assessment_text}.")
    return " ".join(parts)


def _infer_next_step_type_code(payload: SessionClose) -> AnalysisNextStepCode:
    if payload.session_status_code == SessionStatusCode.escalated:
        return AnalysisNextStepCode.escalate_immediate_relay
    if payload.follow_up_actions_text or payload.next_session_focus_text:
        return AnalysisNextStepCode.propose_follow_up
    if payload.vigilance_level_code in {
        RiskLevelCode.priority,
        RiskLevelCode.urgent,
    }:
        return AnalysisNextStepCode.orient_to_appropriate_service
    return AnalysisNextStepCode.clarify_major_point


def _build_client_facing_summary(
    session_record: SessionRecord,
    payload: SessionClose,
) -> str | None:
    if not payload.client_visible:
        return None

    next_step = payload.follow_up_actions_text or payload.next_session_focus_text
    parts = [
        f"Resume de seance {session_record.session_sequence_number}: {payload.session_highlights_text}."
    ]
    if next_step:
        parts.append(f"Prochaine etape: {next_step}.")
    return " ".join(parts)


def _normalize_tensions_json(value):
    if value is None:
        return None
    return value


def _coerce_vigilance_level(value) -> RiskLevelCode | None:
    if value is None or isinstance(value, RiskLevelCode):
        return value
    try:
        return RiskLevelCode(value)
    except ValueError:
        return None


def _coerce_next_step_type(value) -> AnalysisNextStepCode | None:
    if value is None or isinstance(value, AnalysisNextStepCode):
        return value
    try:
        return AnalysisNextStepCode(value)
    except ValueError:
        return None


async def _build_ai_note_payload(
    session_record: SessionRecord,
    payload: SessionClose,
) -> dict:
    ai_payload = await generate_session_note_from_transcript(
        payload.transcript_text or "",
        session_context={
            "session_id": session_record.id,
            "client_id": session_record.client_id,
            "session_sequence_number": session_record.session_sequence_number,
            "session_mode_code": session_record.session_mode_code.value,
            "session_channel_code": session_record.session_channel_code.value,
            "session_status_code": payload.session_status_code.value,
            "manual_presenting_topic_text": payload.presenting_topic_text,
            "manual_session_highlights_text": payload.session_highlights_text,
            "manual_operator_assessment_text": payload.operator_assessment_text,
        },
    )
    if "production_note" not in ai_payload:
        raise AnthropicSessionNoteError("Reponse Claude invalide: bloc production_note absent.")
    return ai_payload


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: SessionCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_production_roles()),
) -> SessionRecord:
    client = db.get(Client, payload.client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    if payload.intake_request_id is not None:
        intake_request = db.get(IntakeRequest, payload.intake_request_id)
        if intake_request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Demande d'entree introuvable.",
            )
        if intake_request.client_id != payload.client_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le client et la demande d'entree ne correspondent pas.",
            )

    duration_minutes = payload.duration_minutes
    if payload.actual_start_at and payload.actual_end_at:
        if payload.actual_end_at < payload.actual_start_at:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La fin de seance ne peut pas preceder le debut.",
            )
        if duration_minutes is None:
            duration_minutes = _compute_duration_minutes(
                payload.actual_start_at,
                payload.actual_end_at,
                duration_minutes,
            )

    session_sequence_number = payload.session_sequence_number
    if session_sequence_number is None:
        latest_sequence_number = db.scalar(
            select(func.max(SessionRecord.session_sequence_number)).where(
                SessionRecord.client_id == payload.client_id
            )
        )
        session_sequence_number = (latest_sequence_number or 0) + 1

    initial_status = payload.session_status_code
    if payload.session_channel_code == SessionChannelCode.audio_async:
        initial_status = SessionStatusCode.pending_review

    session_payload = payload.model_dump(exclude={"duration_minutes", "session_sequence_number"})
    session_payload["session_status_code"] = initial_status

    session_record = SessionRecord(
        **session_payload,
        duration_minutes=duration_minutes,
        session_sequence_number=session_sequence_number,
        operator_user_id=current_user.id,
    )
    db.add(session_record)
    db.commit()
    db.refresh(session_record)
    return session_record


@router.post("/{session_id}/close", response_model=SessionCloseResult)
async def close_session(
    session_id: str,
    payload: SessionClose,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_production_roles()),
) -> SessionCloseResult:
    session_record = _get_owned_session_or_404(session_id, db, current_user)

    if session_record.session_status_code in {
        SessionStatusCode.completed,
        SessionStatusCode.cancelled,
        SessionStatusCode.no_show,
        SessionStatusCode.escalated,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cette seance est deja cloturee.",
        )

    if payload.session_status_code not in {
        SessionStatusCode.completed,
        SessionStatusCode.cancelled,
        SessionStatusCode.no_show,
        SessionStatusCode.escalated,
    }:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Le statut final doit etre un statut de cloture.",
        )

    if payload.actual_start_at and payload.actual_end_at and payload.actual_end_at < payload.actual_start_at:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La fin de seance ne peut pas preceder le debut.",
        )

    session_record.actual_start_at = payload.actual_start_at or session_record.actual_start_at
    session_record.actual_end_at = payload.actual_end_at or session_record.actual_end_at

    if payload.session_status_code in {SessionStatusCode.completed, SessionStatusCode.escalated}:
        if session_record.actual_start_at is None or session_record.actual_end_at is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Une seance realisee doit contenir un debut et une fin reels.",
            )

    session_record.duration_minutes = _compute_duration_minutes(
        session_record.actual_start_at,
        session_record.actual_end_at,
        session_record.duration_minutes,
    )
    session_record.session_status_code = payload.session_status_code

    linked_audio_session = db.scalar(
        select(AudioSession).where(AudioSession.session_id == session_id)
    )
    if linked_audio_session is not None:
        linked_audio_session.audio_session_status_code = AudioSessionStatusCode.closed
        db.add(linked_audio_session)

    existing_generated_note = db.scalar(
        select(SessionNote)
        .where(SessionNote.session_id == session_id)
        .order_by(SessionNote.created_at.desc())
    )
    if existing_generated_note is not None and not payload.transcript_text:
        generated_document = ensure_session_derived_document(db, session_record, existing_generated_note)
        db.add(session_record)
        db.commit()
        db.refresh(session_record)
        db.refresh(existing_generated_note)
        db.refresh(generated_document)
        return SessionCloseResult(
            session=session_record,
            generated_note=existing_generated_note,
            generated_document=generated_document,
        )

    latest_note_sequence_number = db.scalar(
        select(func.max(SessionNote.note_sequence_number)).where(SessionNote.session_id == session_id)
    )
    ai_payload: dict | None = None
    if payload.transcript_text:
        try:
            ai_payload = await _build_ai_note_payload(session_record, payload)
        except AnthropicSessionNoteError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Generation IA de la note impossible: {exc}",
            ) from exc

    production_note = ai_payload.get("production_note", {}) if ai_payload else {}
    client_delivery = ai_payload.get("client_delivery", {}) if ai_payload else {}
    supervision_block = ai_payload.get("supervision", {}) if ai_payload else {}
    research_block = ai_payload.get("research", {}) if ai_payload else {}
    metadata = ai_payload.get("metadata", {}) if ai_payload else {}

    generated_note = SessionNote(
        session_id=session_record.id,
        client_id=session_record.client_id,
        note_sequence_number=(latest_note_sequence_number or 0) + 1,
        summary_text=production_note.get("summary_text")
        or _build_generated_summary(session_record, payload),
        observations_text=production_note.get("observations_text")
        or _build_generated_observations(payload),
        follow_up_actions_text=production_note.get("follow_up_actions_text")
        or payload.follow_up_actions_text,
        next_session_focus_text=production_note.get("next_session_focus_text")
        or payload.next_session_focus_text,
        coeur_summary_text=production_note.get("coeur_summary_text") or payload.coeur_summary_text,
        corps_summary_text=production_note.get("corps_summary_text") or payload.corps_summary_text,
        esprit_summary_text=production_note.get("esprit_summary_text") or payload.esprit_summary_text,
        etre_summary_text=production_note.get("etre_summary_text") or payload.etre_summary_text,
        immediate_context_text=production_note.get("immediate_context_text")
        or payload.immediate_context_text,
        context_factors_json=production_note.get("context_factors_json")
        or payload.context_factors_json,
        context_hypotheses_json=production_note.get("context_hypotheses_json"),
        identified_tensions_json=_normalize_tensions_json(
            production_note.get("identified_tensions_json") or payload.identified_tensions_json
        ),
        vigilance_level_code=_coerce_vigilance_level(production_note.get("vigilance_level_code"))
        or payload.vigilance_level_code,
        next_step_type_code=payload.next_step_type_code
        or _coerce_next_step_type(production_note.get("next_step_type_code"))
        or _infer_next_step_type_code(payload),
        client_facing_summary_text=client_delivery.get("client_facing_summary_text")
        or payload.client_facing_summary_text
        or _build_client_facing_summary(session_record, payload),
        supervision_summary_text=supervision_block.get("supervision_summary_text")
        or payload.supervision_summary_text
        or payload.operator_assessment_text,
        research_notes_text=research_block.get("research_notes_text") or payload.research_notes_text,
        model_used=metadata.get("model_used"),
        prompt_version=metadata.get("prompt_version")
        if ai_payload
        else None,
        complexity_score=metadata.get("complexity_score"),
        validated_by_practitioner=bool(metadata.get("validated_by_practitioner", False)),
        practitioner_corrections=metadata.get("practitioner_corrections"),
        client_visible=bool(payload.client_visible and client_delivery.get("client_visible_recommended", True)),
        record_status=session_record.record_status,
        data_sensitivity_class=session_record.data_sensitivity_class,
        retention_class=session_record.retention_class,
    )

    db.add(generated_note)
    db.flush()

    generated_document = ensure_session_derived_document(db, session_record, generated_note)
    db.add(session_record)
    db.commit()
    db.refresh(session_record)
    db.refresh(generated_note)
    db.refresh(generated_document)
    return SessionCloseResult(
        session=session_record,
        generated_note=generated_note,
        generated_document=generated_document,
    )


@router.post("/{session_id}/deliver", response_model=SessionCloseResult)
async def deliver_audio_async_session(
    session_id: str,
    payload: SessionDeliver,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> SessionCloseResult:
    session_record = _get_owned_session_or_404(session_id, db, current_user)

    if session_record.session_channel_code != SessionChannelCode.audio_async:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La livraison est reservee aux seances audio_async.",
        )

    if session_record.session_status_code != SessionStatusCode.pending_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La seance doit etre en statut pending_review pour etre livree.",
        )

    session_record.actual_end_at = datetime.now(timezone.utc)
    session_record.session_status_code = SessionStatusCode.completed

    linked_audio_session = db.scalar(
        select(AudioSession).where(AudioSession.session_id == session_id)
    )
    if linked_audio_session is not None:
        linked_audio_session.audio_session_status_code = AudioSessionStatusCode.closed
        db.add(linked_audio_session)

    latest_note_sequence_number = db.scalar(
        select(func.max(SessionNote.note_sequence_number)).where(SessionNote.session_id == session_id)
    )

    try:
        ai_payload = await generate_session_note_from_transcript(
            payload.response_text,
            session_context={
                "session_id": session_record.id,
                "client_id": session_record.client_id,
                "session_sequence_number": session_record.session_sequence_number,
                "session_mode_code": session_record.session_mode_code.value,
                "session_channel_code": session_record.session_channel_code.value,
                "session_status_code": SessionStatusCode.completed.value,
                "deliver_flow": True,
            },
        )
    except AnthropicSessionNoteError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Generation IA de la note impossible: {exc}",
        ) from exc

    production_note = ai_payload.get("production_note", {}) if ai_payload else {}
    supervision_block = ai_payload.get("supervision", {}) if ai_payload else {}
    research_block = ai_payload.get("research", {}) if ai_payload else {}
    metadata = ai_payload.get("metadata", {}) if ai_payload else {}

    generated_note = SessionNote(
        session_id=session_record.id,
        client_id=session_record.client_id,
        note_sequence_number=(latest_note_sequence_number or 0) + 1,
        summary_text=production_note.get("summary_text") or payload.response_text,
        observations_text=production_note.get("observations_text") or payload.response_text,
        follow_up_actions_text=production_note.get("follow_up_actions_text")
        or payload.follow_up_actions_text,
        next_session_focus_text=production_note.get("next_session_focus_text")
        or payload.next_session_focus_text,
        coeur_summary_text=production_note.get("coeur_summary_text"),
        corps_summary_text=production_note.get("corps_summary_text"),
        esprit_summary_text=production_note.get("esprit_summary_text"),
        etre_summary_text=production_note.get("etre_summary_text"),
        immediate_context_text=production_note.get("immediate_context_text"),
        context_factors_json=production_note.get("context_factors_json"),
        context_hypotheses_json=production_note.get("context_hypotheses_json"),
        identified_tensions_json=_normalize_tensions_json(
            production_note.get("identified_tensions_json")
        ),
        vigilance_level_code=_coerce_vigilance_level(production_note.get("vigilance_level_code"))
        or payload.vigilance_level_code,
        next_step_type_code=_coerce_next_step_type(production_note.get("next_step_type_code")),
        client_facing_summary_text=payload.client_visible_summary
        or production_note.get("summary_text")
        or payload.response_text,
        supervision_summary_text=supervision_block.get("supervision_summary_text"),
        research_notes_text=research_block.get("research_notes_text"),
        model_used=metadata.get("model_used"),
        prompt_version=metadata.get("prompt_version"),
        complexity_score=metadata.get("complexity_score"),
        validated_by_practitioner=True,
        practitioner_corrections=metadata.get("practitioner_corrections"),
        client_visible=True,
        record_status=session_record.record_status,
        data_sensitivity_class=session_record.data_sensitivity_class,
        retention_class=session_record.retention_class,
    )

    db.add(generated_note)
    db.flush()

    generated_document = ensure_session_derived_document(db, session_record, generated_note)
    db.add(session_record)
    db.commit()
    db.refresh(session_record)
    db.refresh(generated_note)
    db.refresh(generated_document)
    return SessionCloseResult(
        session=session_record,
        generated_note=generated_note,
        generated_document=generated_document,
    )


@router.post("/{session_id}/start", response_model=SessionRead)
def start_session(
    session_id: str,
    payload: SessionStart,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_production_roles()),
) -> SessionRecord:
    session_record = _get_owned_session_or_404(session_id, db, current_user)

    if session_record.session_status_code in {
        SessionStatusCode.completed,
        SessionStatusCode.cancelled,
        SessionStatusCode.no_show,
        SessionStatusCode.escalated,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de demarrer une seance deja cloturee.",
        )

    if session_record.session_status_code == SessionStatusCode.in_progress:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cette seance est deja en cours.",
        )

    session_record.actual_start_at = payload.actual_start_at or datetime.now(timezone.utc)
    session_record.session_status_code = SessionStatusCode.in_progress
    linked_audio_session = db.scalar(
        select(AudioSession).where(AudioSession.session_id == session_id)
    )
    if linked_audio_session is not None:
        linked_audio_session.audio_session_status_code = AudioSessionStatusCode.active
        db.add(linked_audio_session)
    db.add(session_record)
    db.commit()
    db.refresh(session_record)
    return session_record


@router.get("", response_model=list[SessionRead])
def list_sessions(
    client_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> list[SessionRecord]:
    statement = select(SessionRecord).order_by(SessionRecord.created_at.desc())
    if current_user.role == "practitioner":
        statement = statement.where(SessionRecord.praticien_id == current_user.id)
    elif is_operator_user(current_user):
        statement = statement.where(SessionRecord.operator_user_id == current_user.id)
    if client_id is not None:
        statement = statement.where(SessionRecord.client_id == client_id)
    return list(db.scalars(statement).all())


@router.get("/{session_id}", response_model=SessionRead)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionRecord:
    session_record = db.get(SessionRecord, session_id)
    if session_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seance introuvable.")
    if is_operator_user(current_user) and session_record.operator_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seance introuvable.")
    return session_record


@router.patch("/{session_id}/assign", response_model=SessionRead)
def assign_praticien(
    session_id: str,
    payload: SessionAssign,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> SessionRecord:
    session_record = _get_owned_session_or_404(session_id, db, current_user)
    if payload.praticien_id is not None:
        praticien = db.get(AppUser, payload.praticien_id)
        if praticien is None or praticien.role != "practitioner":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Praticien introuvable.",
            )
    session_record.praticien_id = payload.praticien_id
    db.add(session_record)
    db.commit()
    db.refresh(session_record)
    return session_record


@router.post(
    "/{session_id}/room",
    deprecated=True,
    summary="[DEPRECATED] Creer une salle LiveKit via sessions — utiliser /audio-sessions",
)
async def create_session_room(
    session_id: str,
) -> None:
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Cette route est dépréciée. Utilisez /api/v1/audio-sessions à la place.",
    )


@router.post(
    "/{session_id}/recording/start",
    response_model=SessionRecordingRead,
    deprecated=True,
    summary="[DEPRECATED] Demarrer enregistrement via sessions — utiliser /audio-recordings",
)
async def start_session_recording(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> SessionRecordingRead:
    logger.warning(
        "Route legacy POST /sessions/%s/recording/start appelee. Utiliser POST /audio-recordings/audio-sessions/{audio_session_id}/start.",
        session_id,
    )
    session_record = _get_owned_session_or_404(session_id, db, current_user)

    try:
        recording: AudioRecording = await start_livekit_recording_for_session(
            db,
            session_record,
            current_user.id,
        )
        db.refresh(session_record)
    except LiveKitAudioError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return SessionRecordingRead(
        session_id=session_record.id,
        room_name=session_record.room_name or "",
        room_sid=session_record.room_sid,
        egress_id=session_record.egress_id,
        audio_file_path=session_record.audio_file_path,
        audio_recording_id=recording.id,
        status=recording.audio_recording_status_code.value,
    )


@router.post(
    "/{session_id}/recording/stop",
    response_model=SessionRecordingRead,
    deprecated=True,
    summary="[DEPRECATED] Arreter enregistrement via sessions — utiliser /audio-recordings",
)
async def stop_session_recording(
    session_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> SessionRecordingRead:
    logger.warning(
        "Route legacy POST /sessions/%s/recording/stop appelee. Utiliser POST /audio-recordings/{audio_recording_id}/stop.",
        session_id,
    )
    session_record = _get_owned_session_or_404(session_id, db, current_user)

    try:
        recording: AudioRecording = await stop_livekit_recording_for_session(db, session_record)
        db.refresh(session_record)
    except LiveKitAudioError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    if session_record.audio_file_path:
        background_tasks.add_task(
            run_post_recording_pipeline,
            session_record.id,
            session_record.audio_file_path,
        )

    return SessionRecordingRead(
        session_id=session_record.id,
        room_name=session_record.room_name or "",
        room_sid=session_record.room_sid,
        egress_id=session_record.egress_id,
        audio_file_path=session_record.audio_file_path,
        audio_recording_id=recording.id,
        status=recording.audio_recording_status_code.value,
    )


# ---------------------------------------------------------------------------
# POST /sessions/{session_id}/upload-audio
# Flux pilote : upload d'un fichier audio WebM depuis le navigateur.
# Pipeline transcription + analyse AI déclenché en tâche de fond.
# ---------------------------------------------------------------------------

from pydantic import BaseModel as _UploadBaseModel


class AudioUploadIn(_UploadBaseModel):
    """Payload JSON pour upload audio pilote (base64)."""
    audio_data: str  # base64-encoded audio bytes
    filename: str = "recording.webm"


class UploadAudioResult(_UploadBaseModel):
    session_id: str
    audio_file_path: str
    pipeline_queued: bool


@router.post(
    "/{session_id}/upload-audio",
    response_model=UploadAudioResult,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload audio pilote (base64 JSON) — transcription + analyse AI en tâche de fond",
)
async def upload_session_audio(
    session_id: str,
    payload: AudioUploadIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_production_roles()),
) -> UploadAudioResult:
    import os

    session_record = _get_owned_session_or_404(session_id, db, current_user)

    if session_record.session_status_code not in {
        SessionStatusCode.scheduled,
        SessionStatusCode.in_progress,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de soumettre un audio pour une seance deja cloturee.",
        )

    try:
        audio_bytes = base64.b64decode(payload.audio_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="audio_data invalide : base64 attendu.",
        )

    storage_dir = "/app/storage/recordings"
    os.makedirs(storage_dir, exist_ok=True)
    safe_ext = os.path.splitext(payload.filename)[1].lstrip(".") or "webm"
    file_path = os.path.join(storage_dir, f"session_{session_id}_pilot.{safe_ext}")

    with open(file_path, "wb") as out:
        out.write(audio_bytes)

    session_record.audio_file_path = file_path
    if session_record.session_status_code == SessionStatusCode.scheduled:
        session_record.session_status_code = SessionStatusCode.in_progress
    db.add(session_record)
    db.commit()

    background_tasks.add_task(run_post_recording_pipeline, session_id, file_path)

    return UploadAudioResult(
        session_id=session_id,
        audio_file_path=file_path,
        pipeline_queued=True,
    )
