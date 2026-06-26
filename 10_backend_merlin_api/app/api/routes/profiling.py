"""Routes du profilage comportemental — câblage interne (NON exposé publiquement).

Garde-fous (cf. SECURITY_REVIEW_PROFILAGE_v1.0) :
- **B2** : la soumission de quiz exige un `consent_id` (refus 403 sinon).
- **B3** : la surface client ne renvoie QUE la triade (ClientFacingProfileView),
  jamais de scores bruts. Le matching/insights (scores) restent réservés aux rôles
  internes (praticien / superviseur / opérateur).
- **B4** : garde d'urgence déterministe sur les champs libres avant tout scoring.
- **B1** : les insights LLM réels restent **désactivés** (flag `insights_enabled`,
  défaut False) — la route prépare l'entrée mais n'appelle pas Anthropic.

Migration `0039` requise avant que ces routes ne touchent réellement la base.
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import (
    require_internal_clinical_roles,
    require_production_roles,
    require_verified_email_user,
)
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import ProfileSource, ProfileSubjectKind
from app.schemas.common import MerlinSchema
from app.services import behavioral_profile_service as svc
from app.services import love_quiz
from app.services.profile_matching import match_profiles

logger = logging.getLogger("merlin.profiling")

router = APIRouter(prefix="/profiling", tags=["profilage"])

_ESCALADE = (
    "Ce que vous partagez est important. Vous pouvez appeler le 1 866 APPELLE "
    "(1 866 277-3553) maintenant, et le 911 en cas de danger immédiat."
)


# ── Schémas de requête ────────────────────────────────────────────────────────
class LoveQuizSubmit(MerlinSchema):
    responses: dict[str, int]
    consent_id: str
    free_text: str | None = None


class MatchingRequest(MerlinSchema):
    client_id: str
    practitioner_user_id: str


class InsightsRequest(MerlinSchema):
    client_id: str


def _my_client(db: Session, user: AppUser) -> Client:
    client = db.scalar(select(Client).where(Client.app_user_id == user.id))
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aucun dossier client pour ce compte.")
    return client


# ── 1) Soumission du quiz (client) — B2 + B3 + B4 ─────────────────────────────
@router.post("/me/quiz/love")
def submit_love_quiz(
    payload: LoveQuizSubmit,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
):
    # B4 — garde d'urgence : on n'établit pas de profil sur un signal de détresse.
    try:
        svc.guard_free_text(payload.free_text)
    except svc.EmergencyDetectedError:
        return {"observation": "", "hypothese": "", "orientation": _ESCALADE, "escalade": True}

    # B2 — consentement obligatoire.
    if not payload.consent_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Consentement requis pour enregistrer un profil.")

    client = _my_client(db, current_user)
    scores = {k: v for k, v in love_quiz.score(payload.responses).items() if v is not None}

    svc.record_layer(
        db,
        layer="love",
        scores=scores,
        subject_kind=ProfileSubjectKind.client,
        client_id=client.id,
        consent_id=payload.consent_id,
        source=ProfileSource.self_report,
        assessed_by_user_id=current_user.id,
        instrument="love_quiz_v1",
    )
    db.commit()

    # B3 — restitution client : triade uniquement, AUCUN score.
    context = love_quiz.build_narrative_context(payload.responses)
    return love_quiz.compose_client_view(context)


# ── 2) Matching (interne) — réservé aux rôles internes ────────────────────────
@router.post("/matching/compute")
def compute_matching(
    payload: MatchingRequest,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_production_roles()),
):
    pa = svc.get_current_profile(db, client_id=payload.client_id)
    pb = svc.get_current_profile(db, practitioner_user_id=payload.practitioner_user_id)
    if not pa or not pb:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Profil courant manquant pour le matching.")
    result = match_profiles(pa, pb)
    logger.info("matching calculé client=%s praticien=%s score=%s",
                payload.client_id, payload.practitioner_user_id, result.score)
    return {
        "score": result.score,
        "per_layer": result.per_layer,
        "dominant_dimensions": result.dominant_dimensions,
        "explanation": result.explanation,
    }


# ── 3) Insights (interne) — Anthropic réel DÉSACTIVÉ par défaut (B1) ──────────
@router.post("/insights/generate")
async def generate_insights(
    payload: InsightsRequest,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
):
    profile = svc.get_current_profile(db, client_id=payload.client_id)
    if not profile:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Aucun profil courant pour ce client.")

    if not settings.insights_enabled:
        # B1 — pas d'appel Anthropic tant que la barrière transfrontalière n'est pas levée.
        from app.services.behavioral_insights import build_insights_input
        logger.info("insights demandés mais DÉSACTIVÉS (flag) client=%s", payload.client_id)
        return {
            "enabled": False,
            "message": "Insights LLM désactivés (barrière B1 — cadre transfrontalier + consentement requis).",
            "prepared_input": build_insights_input(profile),
        }

    from app.services.behavioral_insights import generate_behavioral_insights
    logger.info("insights LLM générés client=%s", payload.client_id)
    return {"enabled": True, "insights": await generate_behavioral_insights(profile)}
