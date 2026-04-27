from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.derived_document import DerivedDocument
from app.models.session import SessionRecord
from app.models.session_note import SessionNote


def _normalize_text_fragment(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = " ".join(value.split()).strip()
    return normalized or None


def _ensure_terminal_punctuation(value: str | None) -> str | None:
    normalized = _normalize_text_fragment(value)
    if normalized is None:
        return None
    if normalized.endswith((".", "!", "?")):
        return normalized
    return f"{normalized}."


def _build_labeled_sentence(label: str, value: str | None) -> str | None:
    normalized = _ensure_terminal_punctuation(value)
    if normalized is None:
        return None
    return f"{label}: {normalized}"


def build_generated_document_title(session_record: SessionRecord) -> str:
    return f"Synthese de seance {session_record.session_sequence_number}"


def build_document_audience_code(
    client_delivery_requested: bool,
    validated_by_practitioner: bool,
) -> str:
    if not client_delivery_requested:
        return "internal"
    if validated_by_practitioner:
        return "client"
    return "client_pending_review"


def build_document_client_visibility(
    client_delivery_requested: bool,
    validated_by_practitioner: bool,
) -> bool:
    return bool(client_delivery_requested and validated_by_practitioner)


def build_derived_document_text(generated_note: SessionNote) -> str:
    parts = []
    primary_summary = _ensure_terminal_punctuation(
        generated_note.client_facing_summary_text or generated_note.summary_text
    )
    if primary_summary:
        parts.append(primary_summary)

    follow_up_sentence = _build_labeled_sentence(
        "Suites proposees",
        generated_note.follow_up_actions_text,
    )
    if follow_up_sentence:
        parts.append(follow_up_sentence)

    next_focus_sentence = _build_labeled_sentence(
        "Focus prochaine seance",
        generated_note.next_session_focus_text,
    )
    if next_focus_sentence:
        parts.append(next_focus_sentence)

    return " ".join(parts)


def ensure_session_derived_document(
    db: Session,
    session_record: SessionRecord,
    generated_note: SessionNote,
) -> DerivedDocument:
    audience_code = build_document_audience_code(
        client_delivery_requested=generated_note.client_visible,
        validated_by_practitioner=generated_note.validated_by_practitioner,
    )
    client_visible = build_document_client_visibility(
        client_delivery_requested=generated_note.client_visible,
        validated_by_practitioner=generated_note.validated_by_practitioner,
    )
    document = db.scalar(
        select(DerivedDocument).where(DerivedDocument.source_note_id == generated_note.id)
    )
    if document is None:
        document = DerivedDocument(
            client_id=session_record.client_id,
            session_id=session_record.id,
            source_note_id=generated_note.id,
            document_kind_code="session_summary",
            title=build_generated_document_title(session_record),
            body_text=build_derived_document_text(generated_note),
            audience_code=audience_code,
            client_visible=client_visible,
            record_status=session_record.record_status,
            data_sensitivity_class=session_record.data_sensitivity_class,
            retention_class=session_record.retention_class,
        )
    else:
        document.title = build_generated_document_title(session_record)
        document.body_text = build_derived_document_text(generated_note)
        document.audience_code = audience_code
        document.client_visible = client_visible
        document.record_status = session_record.record_status
        document.data_sensitivity_class = session_record.data_sensitivity_class
        document.retention_class = session_record.retention_class

    db.add(document)
    db.flush()
    return document
