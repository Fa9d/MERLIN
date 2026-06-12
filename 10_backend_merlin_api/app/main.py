from contextlib import asynccontextmanager
import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.audio_sessions import router as audio_sessions_router
from app.api.routes.audio_recordings import router as audio_recordings_router
from app.api.routes.auth import router as auth_router
from app.api.routes.clients import router as clients_router
from app.api.routes.client_entitlements import router as client_entitlements_router
from app.api.routes.client_life_events import router as client_life_events_router
from app.api.routes.client_journal_entries import router as client_journal_entries_router
from app.api.routes.me_journal import router as me_journal_router
from app.api.routes.me_recordings import router as me_recordings_router
from app.api.routes.consents import router as consents_router
from app.api.routes.derived_documents import router as derived_documents_router
from app.api.routes.era_contexts import router as era_contexts_router
from app.api.routes.health import router as health_router
from app.api.routes.intake_requests import router as intake_requests_router
from app.api.routes.praticiens import router as praticiens_router
from app.api.routes.referentiels import router as referentiels_router
from app.api.routes.public_intake import router as public_intake_router
from app.api.routes.sessions import router as sessions_router
from app.api.routes.session_notes import router as session_notes_router
from app.api.routes.session_temporal_anchors import router as session_temporal_anchors_router
from app.api.routes.schedules import router as schedules_router
from app.api.routes.register import router as register_router
from app.api.routes.verify_email import router as verify_email_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.matching import router as matching_router
from app.api.routes.payments import router as payments_router
from app.core.config import settings
from app.db.base import init_models
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

_REMINDER_INTERVAL_SECONDS = 1800  # toutes les 30 min


async def _reminder_loop() -> None:
    """Tâche de fond : rappels 24h — exécutée toutes les 30 min."""
    from app.services.booking_flow import send_appointment_reminders
    await asyncio.sleep(60)  # délai initial au démarrage
    while True:
        try:
            db = SessionLocal()
            try:
                n = await send_appointment_reminders(db)
                if n > 0:
                    logger.info("Rappels 24h : %d envoyé(s)", n)
            finally:
                db.close()
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Erreur tâche rappels : %s", exc)
        await asyncio.sleep(_REMINDER_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.auto_create_tables:
        try:
            init_models()
        except SQLAlchemyError as exc:
            logger.warning("Initialisation BDD ignoree au demarrage: %s", exc)
    task = asyncio.create_task(_reminder_loop())
    logger.info("Tâche rappels 24h démarrée (intervalle %ds)", _REMINDER_INTERVAL_SECONDS)
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(audio_recordings_router, prefix=settings.api_v1_prefix)
app.include_router(audio_sessions_router, prefix=settings.api_v1_prefix)
app.include_router(clients_router, prefix=settings.api_v1_prefix)
app.include_router(client_entitlements_router, prefix=settings.api_v1_prefix)
app.include_router(client_life_events_router, prefix=settings.api_v1_prefix)
app.include_router(client_journal_entries_router, prefix=settings.api_v1_prefix)
app.include_router(me_journal_router, prefix=settings.api_v1_prefix)
app.include_router(me_recordings_router, prefix=settings.api_v1_prefix)
app.include_router(era_contexts_router, prefix=settings.api_v1_prefix)
app.include_router(intake_requests_router, prefix=settings.api_v1_prefix)
app.include_router(consents_router, prefix=settings.api_v1_prefix)
app.include_router(derived_documents_router, prefix=settings.api_v1_prefix)
app.include_router(praticiens_router, prefix=settings.api_v1_prefix)
app.include_router(referentiels_router, prefix=settings.api_v1_prefix)
app.include_router(public_intake_router, prefix=settings.api_v1_prefix)
app.include_router(sessions_router, prefix=settings.api_v1_prefix)
app.include_router(session_notes_router, prefix=settings.api_v1_prefix)
app.include_router(session_temporal_anchors_router, prefix=settings.api_v1_prefix)
app.include_router(schedules_router, prefix=settings.api_v1_prefix)
app.include_router(register_router, prefix=settings.api_v1_prefix)
app.include_router(verify_email_router, prefix=settings.api_v1_prefix)
app.include_router(bookings_router, prefix=settings.api_v1_prefix)
app.include_router(matching_router, prefix=settings.api_v1_prefix)
app.include_router(payments_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "ok",
        "docs": "/docs",
    }
