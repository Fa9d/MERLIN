from datetime import datetime

from app.models.enums import AudioProviderCode, AudioSessionStatusCode
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class AudioSessionProvision(MerlinSchema):
    practitioner_participant_identity: str | None = None


class AudioSessionRead(TimestampedReadSchema):
    id: str
    session_id: str
    provider_code: AudioProviderCode
    audio_session_status_code: AudioSessionStatusCode
    room_name: str
    provider_room_url: str | None = None
    recording_enabled: bool
    operator_participant_identity: str
    client_participant_identity: str
    practitioner_participant_identity: str | None = None


class AudioSessionJoinRead(MerlinSchema):
    audio_session_id: str
    room_name: str
    participant_identity: str
    provider_code: AudioProviderCode
    ws_url: str
    token: str
