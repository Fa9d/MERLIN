from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from app.db.session import engine


class Base(DeclarativeBase):
    pass


def load_models() -> None:
    import app.models.app_user  # noqa: F401
    import app.models.audio_recording  # noqa: F401
    import app.models.audio_session  # noqa: F401
    import app.models.client_entitlement  # noqa: F401
    import app.models.client  # noqa: F401
    import app.models.consent  # noqa: F401
    import app.models.derived_document  # noqa: F401
    import app.models.intake_request  # noqa: F401
    import app.models.payment_order  # noqa: F401
    import app.models.session  # noqa: F401
    import app.models.session_note  # noqa: F401
    import app.models.schedule  # noqa: F401
    import app.models.practitioner_profile  # noqa: F401
    import app.models.practitioner_audio_profile  # noqa: F401
    import app.models.era_context  # noqa: F401
    import app.models.client_life_event  # noqa: F401
    import app.models.client_journal_entry  # noqa: F401
    import app.models.client_intention  # noqa: F401
    import app.models.session_temporal_anchor  # noqa: F401
    import app.models.behavioral_profile  # noqa: F401
    import app.models.appointment  # noqa: F401
    import app.models.session_type  # noqa: F401
    import app.models.exercise  # noqa: F401
    import app.models.analysis_delivery  # noqa: F401


def init_models() -> None:
    load_models()

    if settings.auto_create_tables:
        Base.metadata.create_all(bind=engine)
