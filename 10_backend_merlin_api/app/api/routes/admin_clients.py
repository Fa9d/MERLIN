"""Dossiers clients (admin) — /admin/clients.

Vue consolidée par personne : enregistrements + transcriptions + analyses,
structurées et accessibles. Réservé à l'administration (require_admin).
"""
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.schemas.common import MerlinSchema

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/clients", tags=["admin-dossiers"])

_FORMULE_LBL = {"solo30": "Solo · 30 min", "solo60": "Solo · 1 h", "libre": "Enregistrement libre", "seance": "Séance live"}


class ClientRow(MerlinSchema):
    client_id: str
    nom: str
    email: str | None
    profile_complete: bool
    nb_enregistrements: int
    nb_transcrits: int
    nb_analyses: int
    derniere_activite: datetime | None


class RecordingItem(MerlinSchema):
    id: str
    date: datetime
    label: str
    duration_minutes: int | None
    statut: str
    transcript_ready: bool
    transcript_text: str | None


class AnalyseItem(MerlinSchema):
    id: str
    date: datetime
    note_sequence_number: int | None
    summary_text: str | None
    observations_text: str | None
    coeur_summary_text: str | None
    corps_summary_text: str | None
    esprit_summary_text: str | None
    etre_summary_text: str | None
    client_facing_summary_text: str | None
    vigilance_level_code: str | None
    validated_by_practitioner: bool


class DossierRead(MerlinSchema):
    client_id: str
    nom: str
    email: str | None
    profile_complete: bool
    enregistrements: list[RecordingItem]
    analyses: list[AnalyseItem]


def _nom(c: Client) -> str:
    return " ".join(p for p in [c.first_name_or_alias, c.last_name] if p).strip() or "(sans nom)"


def _formule(room_name: str | None, channel: str) -> str:
    if room_name and ":" in room_name:
        return _FORMULE_LBL.get(room_name.split(":", 1)[1], room_name.split(":", 1)[1])
    return _FORMULE_LBL.get(channel, channel)


@router.get("", response_model=list[ClientRow])
def list_clients(
    q: str | None = Query(default=None),
    limit: int = Query(default=300, ge=1, le=1000),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> list[ClientRow]:
    stmt = select(Client).order_by(Client.created_at.desc()).limit(limit)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where((Client.first_name_or_alias.ilike(like)) | (Client.last_name.ilike(like)) | (Client.email.ilike(like)))
    clients = list(db.scalars(stmt))
    ids = [c.id for c in clients]
    if not ids:
        return []
    # Comptes agrégés (enregistrements, transcrits, analyses) + dernière activité.
    rec_counts, rec_tr, rec_last = {}, {}, {}
    for cid, total, transcrits, last in db.execute(
        select(
            SessionRecord.client_id,
            func.count(),
            func.count(SessionRecord.transcript_text),
            func.max(SessionRecord.created_at),
        ).where(SessionRecord.client_id.in_(ids)).group_by(SessionRecord.client_id)
    ):
        rec_counts[cid] = total or 0
        rec_tr[cid] = transcrits or 0
        rec_last[cid] = last
    note_counts, note_last = {}, {}
    for cid, total, last in db.execute(
        select(SessionNote.client_id, func.count(), func.max(SessionNote.created_at))
        .where(SessionNote.client_id.in_(ids)).group_by(SessionNote.client_id)
    ):
        note_counts[cid] = total or 0
        note_last[cid] = last

    def _last(cid):
        xs = [d for d in (rec_last.get(cid), note_last.get(cid)) if d]
        return max(xs) if xs else None

    def _depot(cid):
        """Date/heure du dépôt le plus ancien (premier enregistrement déposé)."""
        return rec_last.get(cid) or note_last.get(cid)

    # Ordre de dépôt (traitement FIFO) : dossiers avec dépôt en premier, du plus
    # ancien au plus récent ; comptes sans dépôt rejetés en fin de liste.
    avec_depot = sorted((c for c in clients if _depot(c.id)), key=lambda c: _depot(c.id))
    sans_depot = [c for c in clients if not _depot(c.id)]
    ordered = avec_depot + sans_depot

    return [
        ClientRow(
            client_id=c.id, nom=_nom(c), email=c.email, profile_complete=c.profile_complete,
            nb_enregistrements=rec_counts.get(c.id, 0), nb_transcrits=rec_tr.get(c.id, 0),
            nb_analyses=note_counts.get(c.id, 0), derniere_activite=_last(c.id),
        )
        for c in ordered
    ]


@router.get("/{client_id}/dossier", response_model=DossierRead)
def client_dossier(
    client_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> DossierRead:
    c = db.get(Client, client_id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")
    recs = db.scalars(
        select(SessionRecord).where(SessionRecord.client_id == client_id).order_by(SessionRecord.created_at.desc())
    ).all()
    notes = db.scalars(
        select(SessionNote).where(SessionNote.client_id == client_id).order_by(SessionNote.created_at.desc())
    ).all()
    return DossierRead(
        client_id=c.id, nom=_nom(c), email=c.email, profile_complete=c.profile_complete,
        enregistrements=[
            RecordingItem(
                id=r.id, date=r.created_at, label=_formule(r.room_name, r.session_channel_code.value),
                duration_minutes=r.duration_minutes, statut=r.session_status_code.value,
                transcript_ready=bool(r.transcript_text), transcript_text=r.transcript_text,
            ) for r in recs
        ],
        analyses=[
            AnalyseItem(
                id=n.id, date=n.created_at, note_sequence_number=n.note_sequence_number,
                summary_text=n.summary_text, observations_text=n.observations_text,
                coeur_summary_text=n.coeur_summary_text, corps_summary_text=n.corps_summary_text,
                esprit_summary_text=n.esprit_summary_text, etre_summary_text=n.etre_summary_text,
                client_facing_summary_text=n.client_facing_summary_text,
                vigilance_level_code=n.vigilance_level_code.value if n.vigilance_level_code else None,
                validated_by_practitioner=n.validated_by_practitioner,
            ) for n in notes
        ],
    )
