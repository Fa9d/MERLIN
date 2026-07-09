"""Reflets de journal — surface CLIENT du mode autonome.

POST /me/journal/reflet : le client demande un reflet de sa période d'écriture
(avec ou sans praticien — c'est SON journal, SA lecture).
GET /me/reflets : ses reflets passés.

Décision fondateur 2026-07-09 : seule sortie IA→client sans relecture
praticien, sous triple verrou (safety suite passée + filtre Loi 21 en code +
protocole d'urgence avec ressources injectées en code). Voir
`app/services/journal_reflection.py` et `00_GOUVERNANCE/`.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.analysis import AnalysisResult, AnalysisSensitivity
from app.models.app_user import AppUser
from app.models.client import Client
from app.schemas.common import MerlinSchema
from app.services import capability_gate, journal_reflection

logger = logging.getLogger("merlin.me_reflets")

router = APIRouter(prefix="/me", tags=["reflets"])


class RefletRead(MerlinSchema):
    id: str
    reflet: str
    fils: list
    question_ouverte: str
    piste: str
    vigilance: dict
    ressources: str | None
    created_at: datetime


def _get_my_client(current_user: AppUser, db: Session) -> Client:
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier introuvable. Complète ton inscription.",
        )
    return client


def _to_read(r: AnalysisResult) -> RefletRead:
    p = json.loads(r.payload_json)
    return RefletRead(
        id=r.id,
        reflet=p.get("reflet", ""),
        fils=p.get("fils") or [],
        question_ouverte=p.get("question_ouverte", ""),
        piste=p.get("piste", ""),
        vigilance=p.get("vigilance") or {"niveau": "aucun"},
        ressources=p.get("ressources"),
        created_at=r.created_at,
    )


@router.post("/journal/reflet", response_model=RefletRead, status_code=status.HTTP_201_CREATED)
async def create_my_reflet(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> RefletRead:
    if not settings.insights_enabled:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Les reflets sont momentanément indisponibles.",
        )
    if not capability_gate.is_capability_enabled(
        db, "ivia_quebec_client", "journal_reflet_client"
    ):
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Les reflets sont désactivés pour le moment.",
        )
    client = _get_my_client(current_user, db)

    try:
        payload = await journal_reflection.generate_reflet(db, client)
    except journal_reflection.RefletCooldownError as exc:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(exc)) from exc
    except journal_reflection.JournalRefletError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except journal_reflection.Loi21ViolationError as exc:
        logger.warning("journal_reflet bloqué par le filtre Loi 21 (client %s).", client.id)
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            "Le reflet n'a pas passé nos vérifications — réessaie dans un moment.",
        ) from exc
    except journal_reflection.BehavioralInsightsError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc

    result = AnalysisResult(
        capability="journal_reflet_client",
        sensitivity=AnalysisSensitivity.hypothese,
        client_id=client.id,
        session_id=None,  # mode autonome : aucun rattachement de séance requis
        engine_version=journal_reflection.ENGINE_VERSION,
        payload_json=json.dumps(payload, ensure_ascii=False),
        created_by_user_id=current_user.id,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return _to_read(result)


@router.get("/reflets", response_model=list[RefletRead])
def list_my_reflets(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> list[RefletRead]:
    client = _get_my_client(current_user, db)
    rows = db.execute(
        select(AnalysisResult)
        .where(
            AnalysisResult.client_id == client.id,
            AnalysisResult.capability == "journal_reflet_client",
        )
        .order_by(AnalysisResult.created_at.desc())
        .limit(20)
    ).scalars()
    return [_to_read(r) for r in rows]
