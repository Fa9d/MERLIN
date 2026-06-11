import json
from sqlalchemy import select

from app.models.practitioner_profile import PractitionerProfile
from app.models.app_user import AppUser
from app.models.enums import AppRole, RecordStatus

WEIGHTS = {"domaine": 3, "approche": 2, "langue": 3, "dispo": 1}

def _parse(t):
    if not t: return []
    try: return json.loads(t)
    except: return []

def _score(profile, need):
    score = 0
    if not (set(_parse(profile.langues)) & {l.value for l in need.langues}):
        return -1
    score += WEIGHTS["langue"]
    score += len(set(_parse(profile.domaines)) & {d.value for d in need.domaines}) * WEIGHTS["domaine"]
    if need.approches:
        score += len(set(_parse(profile.approches)) & {a.value for a in need.approches}) * WEIGHTS["approche"]
    if need.disponibilites:
        score += len(set(_parse(profile.disponibilites)) & {d.value for d in need.disponibilites}) * WEIGHTS["dispo"]
    return score

def get_ranked_practitioners(db, need, exclude_ids=None):
    stmt = (
        select(PractitionerProfile)
        .join(AppUser, AppUser.id == PractitionerProfile.user_id)
        .where(PractitionerProfile.actif == True)  # noqa: E712
        .where(AppUser.role == AppRole.practitioner)
        .where(AppUser.record_status == RecordStatus.active)
    )
    if exclude_ids:
        stmt = stmt.where(PractitionerProfile.id.not_in(exclude_ids))
    profiles = db.scalars(stmt).all()
    ranked = sorted(
        [(p, _score(p, need)) for p in profiles if _score(p, need) >= 0],
        key=lambda x: x[1], reverse=True,
    )
    return [p for p, _ in ranked]
