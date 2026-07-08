"""Dossier de préparation d'entretien — étape 1 du chantier Analyses (cadrage v1.1).

Agrégation LECTURE SEULE de ce que le système sait déjà, au moment où le
praticien s'apprête à recevoir :

- intentions actives du client ;
- entrées de journal depuis la dernière séance — UNIQUEMENT si un
  ``consent_history`` actif et non révoqué existe (sinon le contenu est tu,
  seul le drapeau ``journal_access_granted=false`` est renvoyé) ;
- analyses récentes filtrées par la vanne de capacités (accès journalisés) ;
- dernière note de séance validée par le praticien ;
- ancrages temporels (fragments biographiques évoqués en séance).

Aucune IA nouvelle, aucune écriture métier (seule la journalisation des accès
aux analyses persiste). Accès : praticien ASSIGNÉ à la séance, ou rôle interne
(opérateur/superviseur), ou admin.
"""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.routes.analysis import AnalysisResultRead, _to_read
from app.core.deps import is_admin, require_internal_clinical_roles
from app.db.session import get_db
from app.models.analysis import AnalysisResult
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_intention import ClientIntention
from app.models.client_journal_entry import ClientJournalEntry
from app.models.consent import Consent
from app.models.enums import (
    AppRole,
    ConsentTypeCode,
    IntentionStatusCode,
    RecordStatus,
)
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.models.session_temporal_anchor import SessionTemporalAnchor
from app.schemas.common import MerlinSchema

router = APIRouter(prefix="/sessions", tags=["sessions"])


# ── Schémas de lecture ────────────────────────────────────────────────────────


class PreparationClient(MerlinSchema):
    id: str
    public_client_code: str
    first_name_or_alias: str


class PreparationPreviousSession(MerlinSchema):
    id: str
    session_sequence_number: int
    actual_start_at: datetime | None
    actual_end_at: datetime | None


class PreparationIntention(MerlinSchema):
    id: str
    text: str
    kind: str
    dimension: str | None
    status: str
    created_at: datetime


class PreparationJournalEntry(MerlinSchema):
    id: str
    created_at: datetime
    entry_kind: str
    session_phase: str | None
    emotional_tone: str | None
    dimensions: list | None
    body_text: str


class PreparationNote(MerlinSchema):
    id: str
    session_id: str
    validated_at: datetime | None
    summary_text: str
    next_session_focus_text: str | None
    follow_up_actions_text: str | None
    vigilance_level_code: str
    identified_tensions_json: dict | list | None


class PreparationAnchor(MerlinSchema):
    id: str
    session_id: str
    verbatim_fragment: str | None
    event_year_approx: int | None
    client_age_ref: int | None


class SessionPreparationRead(MerlinSchema):
    session_id: str
    session_sequence_number: int
    scheduled_start_at: datetime | None
    client: PreparationClient
    previous_session: PreparationPreviousSession | None
    intentions: list[PreparationIntention]
    journal_access_granted: bool
    journal_entries: list[PreparationJournalEntry]
    last_validated_note: PreparationNote | None
    anchors: list[PreparationAnchor]
    analyses: list[AnalysisResultRead]


# ── Endpoint ──────────────────────────────────────────────────────────────────


def _journal_consent_active(db: Session, client_id: str) -> bool:
    """Vrai si le client a un consent_history actif, positif et non révoqué."""
    consent = db.scalar(
        select(Consent)
        .where(
            Consent.client_id == client_id,
            Consent.consent_type_code == ConsentTypeCode.consent_history,
            Consent.consent_value.is_(True),
            Consent.revoked_at.is_(None),
            Consent.record_status == RecordStatus.active,
        )
        .order_by(Consent.granted_at.desc())
    )
    return consent is not None


@router.get("/{session_id}/preparation", response_model=SessionPreparationRead)
def get_session_preparation(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionPreparationRead:
    record = db.get(SessionRecord, session_id)
    if record is None or record.record_status != RecordStatus.active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Séance introuvable.")

    # Un praticien ne prépare que SES séances ; opérateur/superviseur/admin passent.
    if (
        current_user.role == AppRole.practitioner
        and not is_admin(current_user)
        and record.praticien_id != current_user.id
    ):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Cette séance n'est pas assignée à ce praticien.",
        )

    client = db.get(Client, record.client_id)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Client introuvable.")

    # Séance précédente du même client (borne temporelle du journal « entre »)
    previous = db.scalar(
        select(SessionRecord)
        .where(
            SessionRecord.client_id == record.client_id,
            SessionRecord.id != record.id,
            SessionRecord.record_status == RecordStatus.active,
            SessionRecord.session_sequence_number < record.session_sequence_number,
        )
        .order_by(SessionRecord.session_sequence_number.desc())
    )
    cutoff = None
    if previous is not None:
        cutoff = previous.actual_end_at or previous.actual_start_at or previous.scheduled_start_at

    # Intentions actives
    intentions = list(
        db.execute(
            select(ClientIntention)
            .where(
                ClientIntention.client_id == record.client_id,
                ClientIntention.record_status == RecordStatus.active,
                ClientIntention.status == IntentionStatusCode.active,
            )
            .order_by(ClientIntention.created_at.desc())
            .limit(20)
        ).scalars()
    )

    # Journal depuis la dernière séance — consentement explicite requis
    journal_ok = _journal_consent_active(db, record.client_id)
    journal_entries: list[ClientJournalEntry] = []
    if journal_ok:
        stmt = (
            select(ClientJournalEntry)
            .where(
                ClientJournalEntry.client_id == record.client_id,
                ClientJournalEntry.record_status == RecordStatus.active,
            )
            .order_by(ClientJournalEntry.created_at.desc())
            .limit(30)
        )
        if cutoff is not None:
            stmt = stmt.where(ClientJournalEntry.created_at >= cutoff)
        journal_entries = list(db.execute(stmt).scalars())

    # Dernière note validée
    note = db.scalar(
        select(SessionNote)
        .where(
            SessionNote.client_id == record.client_id,
            SessionNote.validated_by_practitioner.is_(True),
            SessionNote.record_status == RecordStatus.active,
        )
        .order_by(SessionNote.created_at.desc())
    )

    # Ancrages temporels récents (fragments biographiques)
    anchors = list(
        db.execute(
            select(SessionTemporalAnchor)
            .where(SessionTemporalAnchor.client_id == record.client_id)
            .order_by(SessionTemporalAnchor.created_at.desc())
            .limit(10)
        ).scalars()
    )

    # Analyses récentes, sous vanne (les accès sensibles sont journalisés)
    from app.services import capability_gate  # import tardif : évite un cycle

    analysis_rows = list(
        db.execute(
            select(AnalysisResult)
            .where(AnalysisResult.client_id == record.client_id)
            .order_by(AnalysisResult.created_at.desc())
            .limit(12)
        ).scalars()
    )
    visible_analyses = capability_gate.filter_results(
        db, current_user, analysis_rows, context=f"preparation:{session_id}"
    )
    db.commit()  # persiste les AnalysisAccessLog

    return SessionPreparationRead(
        session_id=record.id,
        session_sequence_number=record.session_sequence_number,
        scheduled_start_at=record.scheduled_start_at,
        client=PreparationClient.model_validate(client),
        previous_session=(
            PreparationPreviousSession.model_validate(previous) if previous else None
        ),
        intentions=[PreparationIntention.model_validate(i) for i in intentions],
        journal_access_granted=journal_ok,
        journal_entries=[
            PreparationJournalEntry.model_validate(e) for e in journal_entries
        ],
        last_validated_note=PreparationNote.model_validate(note) if note else None,
        anchors=[PreparationAnchor.model_validate(a) for a in anchors],
        analyses=[_to_read(r) for r in visible_analyses],
    )
