"""Carte de vie — surface CLIENT (Horizon).

GET /me/carte-de-vie : la dernière analyse `carte_de_vie` du client connecté,
pour la constellation des onze axes AVEC champs de tension (décision fondateur
2026-07-10, session client #1 : même représentation que côté praticien).

Gardes :
- vanne capability_gate `ivia_quebec_client` × `carte_de_vie` ;
- SA carte seulement (client_id résolu depuis la session) ;
- filtre Loi 21 EN CODE sur chaque texte exposé (note d'axe, desc de tension,
  fil, résumé) — un texte qui échoue est OMIS, la structure reste ;
- la TRIADE praticien (observation/hypothèse/orientation) n'est PAS exposée
  ici : c'est la lecture professionnelle, elle passe par la voie validée.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.analysis import AnalysisResult
from app.models.app_user import AppUser
from app.models.client import Client
from app.schemas.common import MerlinSchema
from app.services import capability_gate
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.me_carte")

router = APIRouter(prefix="/me", tags=["carte-de-vie"])


class MaCarteRead(MerlinSchema):
    axes: dict
    tensions: list
    fil: str | None = None
    constellation_resume: str | None = None
    vigilance: str | None = None
    created_at: datetime


def _texte_sur(t: str | None) -> str | None:
    """Filtre Loi 21 EN CODE : un texte non conforme est omis, jamais réécrit."""
    if not t:
        return None
    try:
        assert_client_safe(str(t))
        return str(t)
    except Loi21ViolationError:
        return None


@router.get("/carte-de-vie", response_model=MaCarteRead)
def ma_carte_de_vie(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> MaCarteRead:
    if not capability_gate.is_capability_enabled(db, "ivia_quebec_client", "carte_de_vie"):
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "La carte de vie est désactivée pour le moment."
        )
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Dossier introuvable.")
    result = db.scalar(
        select(AnalysisResult)
        .where(
            AnalysisResult.client_id == client.id,
            AnalysisResult.capability == "carte_de_vie",
        )
        .order_by(AnalysisResult.created_at.desc())
    )
    if result is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Aucune carte de vie pour l'instant — elle se dessinera avec tes séances.",
        )
    p = json.loads(result.payload_json)

    axes = {}
    for code, ax in (p.get("axes") or {}).items():
        axes[code] = {
            "resonance": ax.get("resonance", "sourdine"),
            "note": _texte_sur(ax.get("note")),
        }
    tensions = []
    for t in p.get("tensions") or []:
        tensions.append({
            "code": t.get("code"),
            "entre": t.get("entre") or [],
            "intensite": t.get("intensite"),
            "label": _texte_sur(t.get("label")) or "Champ de tension",
            "desc": _texte_sur(t.get("desc")),
        })
    return MaCarteRead(
        axes=axes,
        tensions=tensions,
        fil=_texte_sur(p.get("fil")),
        constellation_resume=_texte_sur(p.get("constellation_resume")),
        vigilance=p.get("vigilance"),
        created_at=result.created_at,
    )
