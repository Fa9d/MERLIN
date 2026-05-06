from typing import Optional
from pydantic import BaseModel, field_validator
from enum import Enum


class Domaine(str, Enum):
    travail="travail"; relation="relation"; famille="famille"; deuil="deuil"
    anxiete="anxiete"; identite="identite"; sante="sante"; trauma="trauma"
    transition="transition"; autre="autre"

class Approche(str, Enum):
    ecoute_active="ecoute_active"; outils_concrets="outils_concrets"
    approche_systemique="approche_systemique"; psychocorporel="psychocorporel"
    spirituel="spirituel"; cognitif_comportemental="cognitif_comportemental"
    narratif="narratif"; autochtone="autochtone"

class LangueMatching(str, Enum):
    fr="fr"; en="en"; bil="bil"

class DispoSlot(str, Enum):
    matin="matin"; apres_midi="apres_midi"; soir="soir"; fin_semaine="fin_semaine"


class ClientNeedProfile(BaseModel):
    domaines:       list[Domaine]
    approches:      Optional[list[Approche]] = None
    langues:        list[LangueMatching] = [LangueMatching.fr]
    disponibilites: Optional[list[DispoSlot]] = None

    @field_validator("domaines")
    @classmethod
    def min_1_max_3(cls, v):
        if not v: raise ValueError("Au moins 1 domaine requis")
        if len(v) > 3: raise ValueError("Maximum 3 domaines")
        return v


class PractitionerCard(BaseModel):
    user_id: str; display_name: str; title_line: Optional[str]
    intro_text: Optional[str]; presentation_audio_url: Optional[str]
    domaines: list[str]; approches: list[str]; langues: list[str]
    disponibilites: list[str]; tarif_horaire_cents: Optional[int]
    model_config = {"from_attributes": True}


class MatchingSuggestRequest(BaseModel):
    need: ClientNeedProfile
    exclude_ids: list[int] = []

class MatchingSuggestResponse(BaseModel):
    suggestion: Optional[PractitionerCard]
    remaining_count: int
    waitlist_mode: bool
