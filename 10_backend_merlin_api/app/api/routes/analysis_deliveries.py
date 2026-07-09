"""Restitutions au client — étape 4 : validation humaine avant toute livraison.

Le praticien assigné relit l'analyse, ÉDITE la triade dans ses mots, et livre.
Le client la retrouve dans son espace (« Mes repères »).

Verrous à la livraison :
- praticien assigné à la séance de l'analyse (opérateur/admin : passe) ;
- capacité source dont la safety suite est PASSED (registre §8.3) —
  `journal_semantic` et `semantic_llm` aujourd'hui ;
- `croisement_prosodie_semantique` : exige EN PLUS le droit
  `recognized_by_order` (transmission d'inference_clinique) ;
- triade bornée + filtre Loi 21 sur chaque champ (surface client) ;
- retrait possible par le praticien (record_status → archived).
"""
from __future__ import annotations

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_user,
    is_admin,
    require_practitioner_or_operator,
)
from app.db.session import get_db
from app.models.analysis import AnalysisResult
from app.models.analysis_delivery import AnalysisDelivery
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import AppRole, RecordStatus
from app.models.session import SessionRecord
from app.schemas.common import MerlinSchema
from app.services import capability_gate
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.deliveries")

router = APIRouter(tags=["restitutions"])

# Capacités livrables : safety suite PASSED au registre (§8.3). Étendre cette
# liste UNIQUEMENT après un run passé de la suite correspondante.
DELIVERABLE_CAPABILITIES = {"journal_semantic", "semantic_llm"}
# Livrable seulement avec le droit de transmission (inference_clinique)
TRANSMISSION_CAPABILITIES = {"croisement_prosodie_semantique"}


class DeliveryCreate(MerlinSchema):
    analysis_result_id: str
    observation: str
    hypothese: str
    orientation: str


class DeliveryRead(MerlinSchema):
    id: str
    analysis_result_id: str
    session_id: str | None
    observation: str
    hypothese: str
    orientation: str
    delivered_at: datetime


def _validate_triade(observation: str, hypothese: str, orientation: str) -> None:
    for nom, texte in (("observation", observation), ("hypothese", hypothese),
                       ("orientation", orientation)):
        if not (10 <= len(texte.strip()) <= 1200):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Champ '{nom}' invalide (10 à 1200 caractères).",
            )
    try:
        assert_client_safe(observation)
        assert_client_safe(hypothese)
        assert_client_safe(orientation)
    except Loi21ViolationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Vocabulaire non conforme (Loi 21) : {exc}",
        ) from exc


@router.post("/analysis/deliveries", response_model=DeliveryRead, status_code=status.HTTP_201_CREATED)
def deliver_to_client(
    payload: DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> AnalysisDelivery:
    result = db.get(AnalysisResult, payload.analysis_result_id)
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Analyse introuvable.")

    # Le gate §8.3 : seule une capacité dont la suite est passée se livre.
    if result.capability in TRANSMISSION_CAPABILITIES:
        if not capability_gate.can_transmit_to_client(db, current_user.id):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "La transmission de cette lecture exige la reconnaissance par "
                "l'instance professionnelle (recognized_by_order).",
            )
    elif result.capability not in DELIVERABLE_CAPABILITIES:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"La capacité '{result.capability}' n'est pas livrable au client "
            "(safety suite non passée ou surface praticien uniquement).",
        )

    # Praticien assigné à la séance de l'analyse (si l'analyse est liée à une séance)
    if result.session_id:
        record = db.get(SessionRecord, result.session_id)
        if (
            record is not None
            and current_user.role == AppRole.practitioner
            and not is_admin(current_user)
            and record.praticien_id != current_user.id
        ):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Cette analyse appartient à une séance qui n'est pas assignée à ce praticien.",
            )

    _validate_triade(payload.observation, payload.hypothese, payload.orientation)

    delivery = AnalysisDelivery(
        analysis_result_id=result.id,
        client_id=result.client_id,
        session_id=result.session_id,
        delivered_by_user_id=current_user.id,
        observation=payload.observation.strip(),
        hypothese=payload.hypothese.strip(),
        orientation=payload.orientation.strip(),
    )
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    logger.info(
        "Restitution livrée (analyse %s, capacité %s, par %s).",
        result.id, result.capability, current_user.id,
    )
    return delivery


@router.get("/analysis/deliveries/session/{session_id}", response_model=list[DeliveryRead])
def list_session_deliveries(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> list[AnalysisDelivery]:
    record = db.get(SessionRecord, session_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Séance introuvable.")
    # Modele IVIA reel : clients + praticiens choisis + admin. Aucun role
    # intermediaire (operateur = vestige) ne contourne l'assignation.
    if not is_admin(current_user) and record.praticien_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Cette séance n'est pas assignée à ce praticien."
        )
    return list(
        db.execute(
            select(AnalysisDelivery)
            .where(
                AnalysisDelivery.client_id == record.client_id,
                AnalysisDelivery.record_status == RecordStatus.active,
            )
            .order_by(AnalysisDelivery.delivered_at.desc())
        ).scalars()
    )


@router.delete(
    "/analysis/deliveries/{delivery_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def withdraw_delivery(
    delivery_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> None:
    """Retrait d'une restitution (record_status → archived, jamais d'effacement)."""
    delivery = db.get(AnalysisDelivery, delivery_id)
    if delivery is None or delivery.record_status != RecordStatus.active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Restitution introuvable.")
    if not is_admin(current_user) and delivery.delivered_by_user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Seul le praticien qui a livré peut retirer."
        )
    delivery.record_status = RecordStatus.archived
    db.add(delivery)
    db.commit()


# ── Client : mes repères ──────────────────────────────────────────────────────


@router.get("/me/reperes", response_model=list[DeliveryRead])
def list_my_reperes(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> list[AnalysisDelivery]:
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Dossier client introuvable. Complétez votre inscription.",
        )
    return list(
        db.execute(
            select(AnalysisDelivery)
            .where(
                AnalysisDelivery.client_id == client.id,
                AnalysisDelivery.record_status == RecordStatus.active,
            )
            .order_by(AnalysisDelivery.delivered_at.desc())
        ).scalars()
    )
