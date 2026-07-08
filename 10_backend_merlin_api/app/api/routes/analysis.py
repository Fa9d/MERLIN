"""Analyses de séance — exécution et consultation, sous vanne de capacités.

- ``POST /analysis/sessions/{id}/prosody`` : lance l'analyse prosodique locale
  sur l'audio d'une séance (praticien/opérateur). La sortie brute est stockée
  à pleine capacité ; l'exposition dépend du profil du lecteur.
- ``GET /analysis/sessions/{id}`` : sorties visibles pour l'utilisateur courant,
  filtrées par ``capability_gate`` (profil, interrupteurs, niveau de sensibilité)
  avec journalisation des accès sensibles.
- ``GET /analysis/transmission-rights`` : indique si le praticien courant peut
  transmettre des contenus inference_clinique à ses clients
  (credential vérifié + ``recognized_by_order``).
"""
from __future__ import annotations

import json
import logging
import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_practitioner_or_operator
from app.db.session import get_db
from app.models.analysis import AnalysisResult, AnalysisSensitivity
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.session import SessionRecord
from app.schemas.common import MerlinSchema
from app.services import capability_gate, prosody

logger = logging.getLogger("merlin.analysis")

router = APIRouter(prefix="/analysis", tags=["analyses"])


class AnalysisResultRead(MerlinSchema):
    id: str
    capability: str
    sensitivity: AnalysisSensitivity
    client_id: str | None
    session_id: str | None
    engine_version: str | None
    payload: dict
    created_at: str


def _to_read(r: AnalysisResult) -> AnalysisResultRead:
    return AnalysisResultRead(
        id=r.id,
        capability=r.capability,
        sensitivity=r.sensitivity,
        client_id=r.client_id,
        session_id=r.session_id,
        engine_version=r.engine_version,
        payload=json.loads(r.payload_json),
        created_at=r.created_at.isoformat(),
    )


@router.post("/sessions/{session_id}/prosody", response_model=AnalysisResultRead)
def run_prosody(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> AnalysisResultRead:
    profile = capability_gate.profile_for_user(db, current_user)
    if not capability_gate.is_capability_enabled(db, profile, "prosody_local"):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Capacité prosody_local désactivée pour votre profil.",
        )
    record = db.get(SessionRecord, session_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Séance introuvable.")
    if not record.audio_file_path or not os.path.exists(record.audio_file_path):
        raise HTTPException(status.HTTP_409_CONFLICT, "Aucun fichier audio pour cette séance.")

    try:
        features = prosody.analyse_fichier_audio(record.audio_file_path)
    except prosody.ProsodyError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc

    result = AnalysisResult(
        capability="prosody_local",
        sensitivity=AnalysisSensitivity.observation,  # descripteurs bruts, non interprétés
        client_id=record.client_id,
        session_id=record.id,
        engine_version=features.get("engine_version"),
        payload_json=json.dumps(features, ensure_ascii=False),
        created_by_user_id=current_user.id,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    logger.info("Analyse prosodique produite (séance %s, par %s).", session_id, current_user.id)
    return _to_read(result)


@router.get("/sessions/{session_id}", response_model=list[AnalysisResultRead])
def list_session_analyses(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> list[AnalysisResultRead]:
    record = db.get(SessionRecord, session_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Séance introuvable.")
    rows = list(
        db.execute(
            select(AnalysisResult)
            .where(AnalysisResult.session_id == session_id)
            .order_by(AnalysisResult.created_at.desc())
        ).scalars()
    )
    visible = capability_gate.filter_results(
        db, current_user, rows, context=f"session:{session_id}"
    )
    db.commit()  # persiste les AnalysisAccessLog créés par filter_results
    return [_to_read(r) for r in visible]


@router.get("/clients/{client_id}", response_model=list[AnalysisResultRead])
def list_client_analyses(
    client_id: str,
    capability: str | None = None,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> list[AnalysisResultRead]:
    """Sorties d'analyse rattachées à un client (toutes séances confondues),
    filtrées par la vanne de capacités. Filtre optionnel par capacité
    (ex. ``carte_de_vie``)."""
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Client introuvable.")
    stmt = (
        select(AnalysisResult)
        .where(AnalysisResult.client_id == client_id)
        .order_by(AnalysisResult.created_at.desc())
    )
    if capability:
        stmt = stmt.where(AnalysisResult.capability == capability)
    rows = list(db.execute(stmt).scalars())
    visible = capability_gate.filter_results(
        db, current_user, rows, context=f"client:{client_id}"
    )
    db.commit()
    return [_to_read(r) for r in visible]


class CarteDeVieWrite(MerlinSchema):
    """Lecture Carte de Vie rédigée par le praticien — structure libre versionnée.

    Payload attendu (miroir de la page praticien) :
    axes (résonances + notes), tensions actives, sol (territoire/époque),
    triade observation/hypothese/orientation, fil_a_tirer, synthese.
    """

    payload: dict


@router.put("/clients/{client_id}/carte-de-vie", response_model=AnalysisResultRead)
def upsert_carte_de_vie(
    client_id: str,
    body: CarteDeVieWrite,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> AnalysisResultRead:
    """Enregistre (ou actualise) la lecture Carte de Vie du client.

    Une seule lecture active par client : l'écriture remplace la précédente
    (l'historique reste en base, seule la plus récente est servie en premier).
    Sensibilité ``hypothese`` — jamais de vocabulaire de diagnostic (Loi 21).
    """
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Client introuvable.")
    profile = capability_gate.profile_for_user(db, current_user)
    if not capability_gate.is_capability_enabled(db, profile, "carte_de_vie"):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Capacité carte_de_vie désactivée pour votre profil.",
        )
    result = AnalysisResult(
        capability="carte_de_vie",
        sensitivity=AnalysisSensitivity.hypothese,
        client_id=client_id,
        engine_version="carte-de-vie-v1",
        payload_json=json.dumps(body.payload, ensure_ascii=False),
        created_by_user_id=current_user.id,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    logger.info("Carte de Vie enregistrée (client %s, par %s).", client_id, current_user.id)
    return _to_read(result)


@router.get("/transmission-rights")
def transmission_rights(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> dict:
    """Droits de transmission du praticien courant (inference_clinique → client)."""
    cred = capability_gate.active_credential(db, current_user.id)
    return {
        "profile": capability_gate.profile_for_user(db, current_user),
        "has_verified_credential": cred is not None,
        "can_transmit_inference_to_client": capability_gate.can_transmit_to_client(
            db, current_user.id
        ),
        "order_body": cred.order_body if cred else None,
    }
