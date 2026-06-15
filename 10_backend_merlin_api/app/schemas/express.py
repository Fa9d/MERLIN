"""Schémas séance express — création praticien + accès public par token.

Le praticien crée une séance express et reçoit un token ; il en compose un lien
partageable côté frontend. Le client ouvre le lien, voit les infos publiques de
la séance, puis dépose un enregistrement (réutilise le pipeline transcription).
Posture non clinique : aucune donnée sensible exposée publiquement.
"""

from datetime import datetime

from pydantic import Field

from app.models.enums import PaymentStatusCode
from app.schemas.common import MerlinSchema


class ExpressSessionCreate(MerlinSchema):
    client_name: str | None = Field(default=None, max_length=120)
    duration_minutes: int = Field(ge=5, le=240)
    payment_status: PaymentStatusCode = PaymentStatusCode.gratuit
    private_notes: str | None = Field(default=None, max_length=2000)


class ExpressSessionCreated(MerlinSchema):
    session_id: str
    token: str
    duration_minutes: int
    payment_status: PaymentStatusCode


class ExpressSessionPublic(MerlinSchema):
    """Vue publique (token) — strictement ce qu'il faut pour accueillir le client."""
    praticien_display: str | None = None
    client_display: str | None = None
    duration_minutes: int | None = None
    payment_status: PaymentStatusCode | None = None
    already_recorded: bool = False


class ExpressRecordingUpload(MerlinSchema):
    audio_data: str = Field(description="Contenu audio encodé en base64.")
    filename: str = "enregistrement.webm"
    duration_seconds: int | None = Field(default=None, ge=1)


class ExpressRecordingResult(MerlinSchema):
    ok: bool
    transcript_pending: bool
    recorded_at: datetime
