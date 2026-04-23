from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.audio_sessions import router as audio_sessions_router
from app.api.routes.audio_recordings import router as audio_recordings_router
from app.api.routes.auth import router as auth_router
from app.api.routes.clients import router as clients_router
from app.api.routes.consents import router as consents_router
from app.api.routes.derived_documents import router as derived_documents_router
from app.api.routes.health import router as health_router
from app.api.routes.intake_requests import router as intake_requests_router
from app.api.routes.sessions import router as sessions_router
from app.api.routes.session_notes import router as session_notes_router
from app.core.config import settings
from app.db.base import init_models

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.auto_create_tables:
        try:
            init_models()
        except SQLAlchemyError as exc:
            logger.warning("Initialisation BDD ignoree au demarrage: %s", exc)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(audio_recordings_router, prefix=settings.api_v1_prefix)
app.include_router(audio_sessions_router, prefix=settings.api_v1_prefix)
app.include_router(clients_router, prefix=settings.api_v1_prefix)
app.include_router(intake_requests_router, prefix=settings.api_v1_prefix)
app.include_router(consents_router, prefix=settings.api_v1_prefix)
app.include_router(derived_documents_router, prefix=settings.api_v1_prefix)
app.include_router(sessions_router, prefix=settings.api_v1_prefix)
app.include_router(session_notes_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "ok",
        "docs": "/docs",
    }
