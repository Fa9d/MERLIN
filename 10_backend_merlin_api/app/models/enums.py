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
    practitioner = "practitioner"
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


class RequestChannelCode(str, Enum):
    web_form = "web_form"
    phone = "phone"
    email = "email"
    referral = "referral"
    other = "other"


class IntakeHandlingStatusCode(str, Enum):
    new = "new"
    a_rappeler = "a_rappeler"
    contacte = "contacte"
    planifie = "planifie"
    vigilance = "vigilance"
    hors_cadre = "hors_cadre"
    archive = "archive"


class ConsentTypeCode(str, Enum):
    consent_session = "consent_session"
    consent_session_note = "consent_session_note"
    consent_history = "consent_history"
    consent_recording = "consent_recording"
    consent_transcription = "consent_transcription"
    consent_client_delivery = "consent_client_delivery"
    consent_third_party_transmission = "consent_third_party_transmission"


class PaymentStatusCode(str, Enum):
    """Statut de paiement d'une séance — métadonnée praticien, pas un flux Stripe."""
    gratuit = "gratuit"            # consultation découverte, urgence, geste offert
    prepaye = "prepaye"           # déjà réglé hors ligne (virement, espèces…)
    a_payer_apres = "a_payer_apres"  # à régler après la séance


# --------------- Schedule / Booking ----------------------------------------

class DayOfWeek(int, Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6


class SessionTypeCode(str, Enum):
    intake = "intake"           # Évaluation initiale (90 min)
    standard = "standard"       # Consultation standard (60 min)
    follow_up = "follow_up"     # Suivi court (45 min)
    any = "any"                 # Type libre


class ExceptionType(str, Enum):
    blocked = "blocked"   # Plage bloquée (vacances, indispo)
    extra = "extra"       # Plage supplémentaire hors gabarit


class SlotStatus(str, Enum):
    available = "available"
    hold = "hold"           # Réservé temporairement (15 min)
    confirmed = "confirmed"
    cancelled = "cancelled"


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
    audio_live  = "audio_live"
    audio_async = "audio_async"


class SessionStatusCode(str, Enum):
    scheduled      = "scheduled"
    pending_review = "pending_review"
    in_progress    = "in_progress"
    completed      = "completed"
    cancelled      = "cancelled"
    no_show        = "no_show"
    escalated      = "escalated"


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


class PaymentProviderCode(str, Enum):
    stripe = "stripe"
    interac_terminal = "interac_terminal"
    interac_etransfer = "interac_etransfer"


class PaymentOrderStatusCode(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    cancelled = "cancelled"
    refunded = "refunded"


class PaymentProductKindCode(str, Enum):
    session_intake = "session_intake"
    session_follow_up = "session_follow_up"
    journal_days_pack = "journal_days_pack"
    audio_async_follow_up = "audio_async_follow_up"
    solo_recording = "solo_recording"
    custom = "custom"


class PaymentFulfillmentModeCode(str, Enum):
    grant_entitlement_only = "grant_entitlement_only"
    grant_entitlement_and_create_audio_async_session = (
        "grant_entitlement_and_create_audio_async_session"
    )


class ClientEntitlementTypeCode(str, Enum):
    intake_session_credit = "intake_session_credit"
    follow_up_session_credit = "follow_up_session_credit"
    journal_day = "journal_day"
    solo_recording_credit = "solo_recording_credit"


# --------------- Temporal model (ligne de vie) --------------------------------

class LifeStageCode(str, Enum):
    enfant        = "enfant"          # 0–11
    adolescent    = "adolescent"      # 12–17
    jeune_adulte  = "jeune_adulte"    # 18–25
    adulte        = "adulte"          # 26–59
    parent        = "parent"          # rôle (peut chevaucher autre stade)
    senior        = "senior"          # 60+


class EventTypeCode(str, Enum):
    naissance           = "naissance"
    deces               = "deces"
    rupture             = "rupture"
    separation_parentale = "separation_parentale"
    migration           = "migration"
    perte_emploi        = "perte_emploi"
    trauma              = "trauma"
    maladie             = "maladie"
    violence            = "violence"
    relation_significative = "relation_significative"
    reussite            = "reussite"
    transition          = "transition"
    autre               = "autre"


class EmotionalChargeCode(str, Enum):
    faible   = "faible"
    moyen    = "moyen"
    fort     = "fort"
    tres_fort = "tres_fort"


class JournalEntryTypeCode(str, Enum):
    aujourd_hui = "aujourd_hui"   # vécu du moment présent
    souvenir    = "souvenir"      # référence au passé
    reflexion   = "reflexion"     # introspection sans ancrage précis


class AuthoredByCode(str, Enum):
    client       = "client"
    practitioner = "practitioner"
    system       = "system"


# ── Profilage comportemental à 5 couches (cf. app/models/behavioral_profile.py) ──
# Posture (constitution IVIA, opposable) : ces profils sont des OBSERVATIONS /
# HYPOTHÈSES versionnées, jamais des diagnostics.

class ProfileSubjectKind(str, Enum):
    """Le sujet d'un profil comportemental : un client OU un praticien (matching)."""
    client       = "client"
    practitioner = "practitioner"


class ProfileSource(str, Enum):
    """Provenance d'un score — traçabilité Loi 25 + posture non-diagnostic."""
    self_report              = "self_report"               # auto-déclaré par le sujet
    practitioner_observation = "practitioner_observation"  # observé en relation
    ai_inferred              = "ai_inferred"               # inféré (IA) — toujours hypothèse
    blended                  = "blended"                   # composite


class ProfileStatus(str, Enum):
    """Statut d'un score. Défaut = hypothèse : JAMAIS présenté comme diagnostic."""
    hypothese     = "hypothese"
    en_validation = "en_validation"
    valide_humain = "valide_humain"   # relu/validé par un humain
    retire        = "retire"


class AttachmentStyle(str, Enum):
    """Bartholomew (4 quadrants) — modèle de soi × modèle de l'autre."""
    secure    = "secure"
    preoccupe = "preoccupe"   # anxious-preoccupied
    detache   = "detache"     # dismissing-avoidant
    craintif  = "craintif"    # fearful-avoidant
