"""Schémas /me/recordings — enregistrements solo du client connecté.

Le client enregistre sa voix dans le navigateur (MediaRecorder), l'envoie en
base64, et la transcription (faster-whisper local — données Québec) tourne en
tâche de fond. Le client relit ensuite ses propres mots ; la note praticien
générée reste côté praticien, soumise à validation humaine.
"""

from datetime import datetime

from pydantic import Field

from app.schemas.common import MerlinSchema


class MyRecordingCreate(MerlinSchema):
    """Payload d'upload — client_id résolu depuis la session, jamais envoyé."""

    audio_data: str = Field(description="Contenu audio encodé en base64.")
    filename: str = "enregistrement.webm"
    formule: str = "solo30"
    duration_seconds: int | None = Field(default=None, ge=1)


class MyRecordingRead(MerlinSchema):
    id: str
    formule: str | None = None
    created_at: datetime
    actual_end_at: datetime | None = None
    duration_minutes: int | None = None
    status: str
    transcript_ready: bool
    transcript_text: str | None = None
