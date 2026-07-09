"""Journal de pratique — routes du praticien, pour lui-même.

POST /pratique/retours : déposer un retour (optionnel, ADN IVIA).
GET  /pratique/retours : ses retours (fenêtre récente).
POST /pratique/reflet  : demander le reflet de sa pratique.
GET  /pratique/reflets : ses reflets passés.

STRICTEMENT PERSONNEL : chaque route ne voit que la matière du praticien
connecté — pas d'exception admin (l'intimité du praticien vaut celle du
client ; l'admin n'y a pas accès).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_practitioner_or_operator
from app.db.session import get_db
from app.models.analysis import AnalysisResult, AnalysisSensitivity
from app.models.app_user import AppUser
from app.models.enums import RecordStatus
from app.models.practitioner_journal import PractitionerJournalEntry
from app.models.session import SessionRecord
from app.schemas.common import MerlinSchema
from app.services import capability_gate, practice_reflection

logger = logging.getLogger("merlin.pratique")

router = APIRouter(prefix="/pratique", tags=["pratique"])


class RetourCreate(MerlinSchema):
    body_text: str
    session_id: str | None = None


class RetourRead(MerlinSchema):
    id: str
    body_text: str
    session_id: str | None
    created_at: datetime


class PratiqueRefletRead(MerlinSchema):
    id: str
    reflet: str
    constats: list
    pistes: list
    vigilance: dict
    ressources: str | None
    created_at: datetime


@router.post("/retours", response_model=RetourRead, status_code=status.HTTP_201_CREATED)
def create_retour(
    payload: RetourCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> PractitionerJournalEntry:
    texte = payload.body_text.strip()
    if not (5 <= len(texte) <= 4000):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Retour invalide (5 à 4000 caractères)."
        )
    if payload.session_id is not None:
        record = db.get(SessionRecord, payload.session_id)
        # Le retour ne se lie qu'à SA propre séance — sans exception admin :
        # cet espace est le sien, personne d'autre n'y écrit ni n'y lit.
        if record is None or record.praticien_id != current_user.id:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Séance introuvable dans ta pratique."
            )
    entry = PractitionerJournalEntry(
        praticien_id=current_user.id,
        session_id=payload.session_id,
        body_text=texte,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/retours", response_model=list[RetourRead])
def list_retours(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> list[PractitionerJournalEntry]:
    return list(
        db.execute(
            select(PractitionerJournalEntry)
            .where(
                PractitionerJournalEntry.praticien_id == current_user.id,
                PractitionerJournalEntry.record_status == RecordStatus.active,
            )
            .order_by(PractitionerJournalEntry.created_at.desc())
            .limit(50)
        ).scalars()
    )


def _reflet_to_read(r: AnalysisResult) -> PratiqueRefletRead:
    p = json.loads(r.payload_json)
    return PratiqueRefletRead(
        id=r.id,
        reflet=p.get("reflet", ""),
        constats=p.get("constats") or [],
        pistes=p.get("pistes") or [],
        vigilance=p.get("vigilance") or {"niveau": "aucun"},
        ressources=p.get("ressources"),
        created_at=r.created_at,
    )


@router.post("/reflet", response_model=PratiqueRefletRead, status_code=status.HTTP_201_CREATED)
async def create_reflet(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> PratiqueRefletRead:
    if not settings.insights_enabled:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Les reflets sont momentanément indisponibles."
        )
    profile = capability_gate.profile_for_user(db, current_user)
    if not capability_gate.is_capability_enabled(db, profile, "praticien_reflet"):
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Les reflets de pratique sont désactivés."
        )

    try:
        payload = await practice_reflection.generate_practice_reflet(db, current_user.id)
    except practice_reflection.PratiqueCooldownError as exc:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(exc)) from exc
    except practice_reflection.PratiqueRefletError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except practice_reflection.BehavioralInsightsError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc

    result = AnalysisResult(
        capability="praticien_reflet",
        sensitivity=AnalysisSensitivity.hypothese,
        client_id=None,          # matière du praticien — AUCUN client concerné
        session_id=None,
        engine_version=practice_reflection.ENGINE_VERSION,
        payload_json=json.dumps(payload, ensure_ascii=False),
        created_by_user_id=current_user.id,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return _reflet_to_read(result)


@router.get("/reflets", response_model=list[PratiqueRefletRead])
def list_reflets(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> list[PratiqueRefletRead]:
    rows = db.execute(
        select(AnalysisResult)
        .where(
            AnalysisResult.capability == "praticien_reflet",
            AnalysisResult.created_by_user_id == current_user.id,
        )
        .order_by(AnalysisResult.created_at.desc())
        .limit(20)
    ).scalars()
    return [_reflet_to_read(r) for r in rows]
