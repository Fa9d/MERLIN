from enum import Enum


class RecordStatus(str, Enum):
    draft = "draft"
    active = "active"
    validated = "validated"
    closed = "closed"
    deprecated = "deprecated"
    archived = "archived"


class AppRole(str, Enum):
    public_client = "public_client"
    operator = "operator"
    supervisor = "supervisor"
    admin_tech = "admin_tech"


class DataSensitivityClass(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    restricted = "restricted"


class RetentionClass(str, Enum):
    ephemeral = "ephemeral"
    short_term = "short_term"
    standard = "standard"
    extended = "extended"
    archival = "archival"


class RequestForCode(str, Enum):
    self = "self"
    relative = "relative"
    other = "other"


class NeedCode(str, Enum):
    clarification = "clarification"
    support = "support"
    orientation = "orientation"
    loneliness = "loneliness"
    distress = "distress"
    other = "other"


class RiskLevelCode(str, Enum):
    non_urgent = "non_urgent"
    watch = "watch"
    priority = "priority"
    urgent = "urgent"


class ConsentTypeCode(str, Enum):
    consent_session = "consent_session"
    consent_session_note = "consent_session_note"
    consent_history = "consent_history"
    consent_recording = "consent_recording"
    consent_transcription = "consent_transcription"
    consent_client_delivery = "consent_client_delivery"
    consent_third_party_transmission = "consent_third_party_transmission"


class RevocationScopeCode(str, Enum):
    future_only = "future_only"
    future_and_pending = "future_and_pending"


class GrantedByActorCode(str, Enum):
    client = "client"
    operator = "operator"
    system = "system"


class SessionModeCode(str, Enum):
    standard = "standard"
    intake = "intake"
    follow_up = "follow_up"


class SessionChannelCode(str, Enum):
    phone = "phone"
    video = "video"
    in_person = "in_person"
    async_mode = "async"


class SessionStatusCode(str, Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"
    escalated = "escalated"


class AudioProviderCode(str, Enum):
    livekit = "livekit"
    manual = "manual"


class AudioSessionStatusCode(str, Enum):
    provisioned = "provisioned"
    active = "active"
    closed = "closed"
    failed = "failed"


class AudioRecordingStatusCode(str, Enum):
    starting = "starting"
    recording = "recording"
    ready = "ready"
    failed = "failed"


class AnalysisNextStepCode(str, Enum):
    continue_to_structure = "continue_to_structure"
    clarify_major_point = "clarify_major_point"
    stabilize_rhythm_and_load = "stabilize_rhythm_and_load"
    mobilize_relational_resource = "mobilize_relational_resource"
    orient_to_appropriate_service = "orient_to_appropriate_service"
    propose_follow_up = "propose_follow_up"
    escalate_immediate_relay = "escalate_immediate_relay"
