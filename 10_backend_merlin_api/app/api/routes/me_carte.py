"""Carte de vie — surface CLIENT (Horizon).

GET /me/carte-de-vie : l'HISTORIQUE des analyses `carte_de_vie` du client
connecté (pour la barre de progression : chaque carte est un instantané daté,
la constellation se redessine d'analyse en analyse — corrections fondateur
2026-07-10) + ses MOMENTS FORTS (événements de vie marquants, pas le fil
d'activité).

Gardes :
- vanne capability_gate `ivia_quebec_client` × `carte_de_vie` ;
- SA carte seulement (client_id résolu depuis la session) ;
- filtre Loi 21 EN CODE sur chaque texte exposé — un texte qui échoue est
  OMIS, la structure reste ;
- la TRIADE praticien n'est PAS exposée (lecture professionnelle, voie validée).
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
from app.models.client_life_event import ClientLifeEvent
from app.models.enums import RecordStatus
from app.schemas.common import MerlinSchema
from app.services import capability_gate
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.me_carte")

router = APIRouter(prefix="/me", tags=["carte-de-vie"])


class CarteSnapshot(MerlinSchema):
    id: str
    axes: dict
    tensions: list
    fil: str | None = None
    fil_a_tirer: str | None = None
    constellation_resume: str | None = None
    vigilance: str | None = None
    created_at: datetime


class MomentFort(MerlinSchema):
    titre: str
    annee: int | None = None
    type: str | None = None
    charge: str | None = None
    intergenerationnel: bool = False


class MaCarteRead(MerlinSchema):
    cartes: list[CarteSnapshot]  # du plus ancien au plus récent (barre de progression)
    moments: list[MomentFort]    # moments forts de la vie — pas le fil d'activité


def _texte_sur(t: str | None) -> str | None:
    """Filtre Loi 21 EN CODE : un texte non conforme est omis, jamais réécrit."""
    if not t:
        return None
    try:
        assert_client_safe(str(t))
        return str(t)
    except Loi21ViolationError:
        return None


def _snapshot(result: AnalysisResult) -> CarteSnapshot:
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
    return CarteSnapshot(
        id=result.id,
        axes=axes,
        tensions=tensions,
        fil=_texte_sur(p.get("fil")),
        fil_a_tirer=_texte_sur(p.get("fil_a_tirer")),
        constellation_resume=_texte_sur(p.get("constellation_resume")),
        vigilance=p.get("vigilance"),
        created_at=result.created_at,
    )


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

    results = list(
        db.execute(
            select(AnalysisResult)
            .where(
                AnalysisResult.client_id == client.id,
                AnalysisResult.capability == "carte_de_vie",
            )
            .order_by(AnalysisResult.created_at.asc())
            .limit(20)
        ).scalars()
    )
    cartes = [_snapshot(r) for r in results]

    # Charges par événement, depuis la carte la plus récente qui en porte.
    charges: dict[str, str] = {}
    for r in reversed(results):
        ev = json.loads(r.payload_json).get("evenements") or {}
        if ev:
            charges = {k: (v or {}).get("charge") for k, v in ev.items()}
            break

    events = list(
        db.execute(
            select(ClientLifeEvent)
            .where(
                ClientLifeEvent.client_id == client.id,
                ClientLifeEvent.record_status != RecordStatus.archived,
            )
            .order_by(ClientLifeEvent.event_year_approx.desc().nullslast())
            .limit(30)
        ).scalars()
    )
    moments = []
    for e in events:
        titre = _texte_sur(e.title)
        if not titre:
            continue
        moments.append(MomentFort(
            titre=titre,
            annee=e.event_year_approx,
            type=getattr(e.event_type, "value", None),
            charge=charges.get(e.id),
            intergenerationnel=bool(e.is_intergenerational),
        ))

    return MaCarteRead(cartes=cartes, moments=moments)
