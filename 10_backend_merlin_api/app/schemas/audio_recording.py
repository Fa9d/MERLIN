from datetime import datetime

from app.models.enums import AudioProviderCode, AudioRecordingStatusCode
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class AudioRecordingRead(TimestampedReadSchema):
    id: str
    audio_session_id: str
    provider_code: AudioProviderCode
    audio_recording_status_code: AudioRecordingStatusCode
    provider_recording_id: str | None = None
    output_location: str | None = None
    failure_reason: str | None = None
    requested_by_user_id: str
    started_at: datetime | None = None
    ended_at: datetime | None = None


class AudioRecordingStart(MerlinSchema):
    pass
