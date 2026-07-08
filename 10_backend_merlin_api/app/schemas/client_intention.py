from datetime import datetime

from pydantic import field_validator

from app.models.enums import IntentionKindCode, IntentionStatusCode
from app.schemas.client_journal_entry import CANONICAL_AXES
from app.schemas.common import MerlinSchema


class MyIntentionCreate(MerlinSchema):
    """Créée par le client depuis son espace — client_id injecté depuis la session."""

    text: str
    kind: IntentionKindCode = IntentionKindCode.intention
    dimension: str | None = None
    session_id: str | None = None

    @field_validator("text")
    @classmethod
    def _texte_non_vide(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("L'intention ne peut pas être vide.")
        if len(v) > 500:
            raise ValueError("L'intention doit tenir en 500 caractères.")
        return v

    @field_validator("dimension")
    @classmethod
    def _valider_axe(cls, v: str | None) -> str | None:
        if v is not None and v not in CANONICAL_AXES:
            raise ValueError(f"Axe inconnu : {v}. Axes valides : {sorted(CANONICAL_AXES)}")
        return v


class MyIntentionUpdate(MerlinSchema):
    status: IntentionStatusCode | None = None
    text: str | None = None


class IntentionRead(MerlinSchema):
    id: str
    client_id: str
    session_id: str | None = None
    text: str
    kind: IntentionKindCode
    dimension: str | None = None
    status: IntentionStatusCode
    created_by: str
    realized_at: datetime | None = None
    created_at: datetime
