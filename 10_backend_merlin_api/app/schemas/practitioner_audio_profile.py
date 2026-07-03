"""Schémas pour profils audio praticiens."""
from datetime import datetime

from pydantic import BaseModel


class PractitionerAudioProfileOut(BaseModel):
    """Métadonnées profil audio praticien (visible client)."""
    id: str
    practitioner_id: str
    duration_seconds: int | None
    file_size_kb: int | None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class PractitionerAudioProfileMeta(BaseModel):
    """Métadonnées pour édition praticien."""
    duration_seconds: int | None = None
    file_size_kb: int | None = None
