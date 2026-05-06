import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.matching import MatchingSuggestRequest, MatchingSuggestResponse, PractitionerCard
from app.services.matching import get_ranked_practitioners

router = APIRouter(prefix="/matching", tags=["matching"])

def _build_card(profile, user):
    def _p(t): return json.loads(t) if t else []
    return PractitionerCard(
        user_id=user.id, display_name=user.display_name,
        title_line=user.title_line, intro_text=user.intro_text,
        presentation_audio_url=user.presentation_audio_url,
        domaines=_p(profile.domaines), approches=_p(profile.approches),
        langues=_p(profile.langues), disponibilites=_p(profile.disponibilites),
        tarif_horaire_cents=profile.tarif_horaire_cents,
    )

@router.post("/suggest", response_model=MatchingSuggestResponse)
def suggest_practitioner(payload: MatchingSuggestRequest, db: Session = Depends(get_db)):
    ranked = get_ranked_practitioners(db=db, need=payload.need, exclude_ids=payload.exclude_ids)
    if not ranked:
        return MatchingSuggestResponse(suggestion=None, remaining_count=0, waitlist_mode=True)
    best = ranked[0]
    return MatchingSuggestResponse(
        suggestion=_build_card(best, best.user),
        remaining_count=len(ranked) - 1,
        waitlist_mode=False,
    )
