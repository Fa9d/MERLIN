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
from app.api.routes.profiling import router as profiling_router
from app.api.routes.me_journal import router as me_journal_router
from app.api.routes.me_intentions import router as me_intentions_router
from app.api.routes.me_recordings import router as me_recordings_router
from app.api.routes.me_documents import router as me_documents_router
from app.api.routes.express import router as express_router
from app.api.routes.admin_settings import router as admin_settings_router
from app.api.routes.admin_analysis import router as admin_analysis_router
from app.api.routes.analysis import router as analysis_router
from app.api.routes.admin_accounts import router as admin_accounts_router
from app.api.routes.admin_accounting import router as admin_accounting_router
from app.api.routes.admin_economics import router as admin_economics_router
from app.api.routes.admin_overview import router as admin_overview_router
from app.api.routes.admin_clients import router as admin_clients_router
from app.api.routes.consents import router as consents_router
from app.api.routes.derived_documents import router as derived_documents_router
from app.api.routes.era_contexts import router as era_contexts_router
from app.api.routes.health import router as health_router
from app.api.routes.intake_requests import router as intake_requests_router
from app.api.routes.praticiens import router as praticiens_router
from app.api.routes.practitioner_audio_profiles import router as practitioner_audio_profiles_router, public_router as practitioner_audio_public_router
from app.api.routes.referentiels import router as referentiels_router
from app.api.routes.public_intake import router as public_intake_router
from app.api.routes.sessions import router as sessions_router
from app.api.routes.session_preparation import router as session_preparation_router
from app.api.routes.exercises import router as exercises_router
from app.api.routes.analysis_deliveries import router as analysis_deliveries_router
from app.api.routes.me_carte import router as me_carte_router
from app.api.routes.me_reflets import router as me_reflets_router
from app.api.routes.praticien_pratique import router as praticien_pratique_router
from app.api.routes.session_notes import router as session_notes_router
from app.api.routes.session_temporal_anchors import router as session_temporal_anchors_router
from app.api.routes.schedules import router as schedules_router
from app.api.routes.register import router as register_router
from app.api.routes.verify_email import router as verify_email_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.matching import router as matching_router
from app.api.routes.payments import router as payments_router
from app.api.routes.appointments import router as appointments_router
from app.api.routes.calendar import router as calendar_router
from app.api.routes.timeline import router as timeline_router
from app.core.config import settings
from app.db.base import init_models
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

_REMINDER_INTERVAL_SECONDS = 1800  # toutes les 30 min


async def _requeue_orphan_transcriptions() -> None:
    """Reprise au démarrage : transcriptions tuées par un redémarrage du conteneur.

    Un enregistrement avec fichier audio mais sans transcript, plus vieux que
    5 minutes, est un orphelin (la tâche de fond est morte avec le processus).
    Trou révélé par le test fondateur du 2026-07-10 (séance express de 17 min
    perdue par un deploy --build pendant la transcription).
    """
    from datetime import datetime, timedelta, timezone

    from sqlalchemy import select

    from app.models.session import SessionRecord
    from app.services.livekit_audio import run_post_recording_pipeline

    await asyncio.sleep(30)  # laisser l'app finir de démarrer
    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=5)
        orphans = list(
            db.execute(
                select(SessionRecord).where(
                    SessionRecord.audio_file_path.is_not(None),
                    SessionRecord.transcript_text.is_(None),
                    SessionRecord.created_at < cutoff,
                    SessionRecord.created_at > cutoff - timedelta(days=2),
                )
            ).scalars()
        )
    finally:
        db.close()
    for record in orphans:
        logger.warning(
            "Reprise transcription orpheline session=%s (fichier=%s)",
            record.id, record.audio_file_path,
        )
        try:
            await run_post_recording_pipeline(record.id, record.audio_file_path)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Reprise transcription %s échouée : %s", record.id, exc)


async def _reminder_loop() -> None:
    """Tâche de fond : rappels 24h + reprises de lien 48h — toutes les 30 min."""
    from app.services.booking_flow import send_appointment_reminders, send_intake_reprise_48h
    await asyncio.sleep(60)  # délai initial au démarrage
    while True:
        try:
            db = SessionLocal()
            try:
                n = await send_appointment_reminders(db)
                if n > 0:
                    logger.info("Rappels 24h : %d envoyé(s)", n)
                r = await send_intake_reprise_48h(db)
                if r > 0:
                    logger.info("Reprises 48h : %d envoyée(s)", r)
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
    asyncio.create_task(_requeue_orphan_transcriptions())
    logger.info("Tâche rappels 24h démarrée (intervalle %ds)", _REMINDER_INTERVAL_SECONDS)
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# ── Vue OpenAPI : description et ordre des groupes dans /docs ────────────────
API_DESCRIPTION = """API MERLIN — cœur d'analyse et de gouvernance d'IVIA (ivia.quebec).

**Posture non médicale (constitution MERLIN)** : aucune sortie ne pose de
diagnostic ni de prescription — triade Observation / Hypothèse / Orientation,
validation humaine sur les notes, données hébergées au Québec (Loi 25).

Authentification : `Authorization: Bearer <JWT>` (obtenu via `POST /auth/login`).
Collection de tests : `docs/api/merlin_postman_collection.json` dans le dépôt.
"""

OPENAPI_TAGS = [
    # Entrée & comptes
    {"name": "health", "description": "Sonde de vie de l'API."},
    {"name": "auth", "description": "Inscription, connexion (JWT), mot de passe."},
    {"name": "register", "description": "Parcours public d'entrée (intake orchestré + magic link)."},
    {"name": "consents", "description": "Consentements du client (N1/N2/N3)."},
    # Séances & enregistrements
    {"name": "sessions", "description": "Séances : création, démarrage, clôture (note générée), livraison."},
    {"name": "audio-sessions", "description": "Salles LiveKit : provision, jetons praticien/client."},
    {"name": "audio-recordings", "description": "Enregistrements de séance : démarrage, arrêt, transcription."},
    {"name": "enregistrements-client", "description": "Enregistrements solo du client (voix, transcription locale)."},
    {"name": "seance-express", "description": "Séance express par lien (praticien → client)."},
    {"name": "bookings", "description": "Réservation de créneaux : hold 10 min, confirmation, agenda praticien."},
    {"name": "schedules", "description": "Disponibilités du praticien (gabarits, exceptions)."},
    {"name": "calendar", "description": "Vues calendaires."},
    # Notes & restitutions
    {"name": "session-notes", "description": "Notes de séance — VALIDATION HUMAINE obligatoire avant toute diffusion."},
    {"name": "derived-documents", "description": "Documents dérivés d'une note (reformulation client)."},
    {"name": "documents-client", "description": "Lectures livrées, visibles par le client."},
    {"name": "restitutions", "description": "Restitutions praticien→client (triade relue, éditée, livrée)."},
    # Analyses (moteur plein, vannes par profil)
    {"name": "analyses", "description": "Moteur d'analyse : prosodie locale, sémantique, croisement — filtré par capability_gate."},
    {"name": "reflets", "description": "Mode autonome : miroirs directs au client (journal, séance) sous triple verrou."},
    {"name": "carte-de-vie", "description": "Horizon / Carte de Vie : constellation des onze axes, historique daté."},
    {"name": "profilage", "description": "Profilage comportemental (6 couches) — hypothèses, jamais diagnostics."},
    {"name": "matching", "description": "Appariement client-praticien (similarité/complémentarité)."},
    # Espace client
    {"name": "journal-client", "description": "Journal intime du client (entrées datées, axes MERLIN)."},
    {"name": "journal", "description": "Journal structuré (check-ins, exercices validés)."},
    {"name": "intentions-client", "description": "Intentions actives du client."},
    {"name": "exercices", "description": "Exercices : invitations praticien, jamais des devoirs."},
    {"name": "clients", "description": "Fiche et profil du client connecté."},
    {"name": "client-entitlements", "description": "Crédits et droits d'usage du client."},
    {"name": "life-events", "description": "Événements de vie (ligne de vie praticien)."},
    {"name": "era-contexts", "description": "Contextes d'époque."},
    {"name": "temporal-anchors", "description": "Ancrages temporels de séance."},
    {"name": "timeline", "description": "Chronologies agrégées."},
    # Praticien
    {"name": "praticiens", "description": "Praticiens publiés (profils publics)."},
    {"name": "pratique", "description": "Journal de pratique du praticien — strictement personnel, analyse franc jeu."},
    # Paiements & référentiels
    {"name": "payments", "description": "Stripe : checkout, confirmation test, entitlements."},
    {"name": "referentiels", "description": "Taxonomies vivantes (axes, tensions) — source doctrine."},
    # Console admin
    {"name": "admin-vue", "description": "Vue d'ensemble + vigilances [admin]."},
    {"name": "admin-dossiers", "description": "Dossiers clients [admin]."},
    {"name": "admin-comptes", "description": "Comptes & accès [admin]."},
    {"name": "admin-comptabilite", "description": "Grand livre comptable [admin]."},
    {"name": "admin-economie", "description": "Économie IA : coûts LLM réels, bénéfices par séance [admin]."},
    {"name": "admin-facturation", "description": "Interrupteurs payant/gratuit par offre [admin]."},
    {"name": "admin-analyse", "description": "Vannes capacités × profils, credentials, types de séance [admin]."},
]

app = FastAPI(
    title=settings.app_name,
    version="2026.07",
    description=API_DESCRIPTION,
    openapi_tags=OPENAPI_TAGS,
    contact={"name": "IVIA — fondateur", "url": "https://ivia.quebec"},
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
app.include_router(me_intentions_router, prefix=settings.api_v1_prefix)
app.include_router(me_recordings_router, prefix=settings.api_v1_prefix)
app.include_router(profiling_router, prefix=settings.api_v1_prefix)
app.include_router(me_documents_router, prefix=settings.api_v1_prefix)
app.include_router(practitioner_audio_profiles_router, prefix=settings.api_v1_prefix)
app.include_router(practitioner_audio_public_router, prefix=settings.api_v1_prefix)
app.include_router(express_router, prefix=settings.api_v1_prefix)
app.include_router(admin_settings_router, prefix=settings.api_v1_prefix)
app.include_router(admin_analysis_router, prefix=settings.api_v1_prefix)
app.include_router(analysis_router, prefix=settings.api_v1_prefix)
app.include_router(admin_accounts_router, prefix=settings.api_v1_prefix)
app.include_router(admin_accounting_router, prefix=settings.api_v1_prefix)
app.include_router(admin_economics_router, prefix=settings.api_v1_prefix)
app.include_router(admin_overview_router, prefix=settings.api_v1_prefix)
app.include_router(admin_clients_router, prefix=settings.api_v1_prefix)
app.include_router(era_contexts_router, prefix=settings.api_v1_prefix)
app.include_router(intake_requests_router, prefix=settings.api_v1_prefix)
app.include_router(consents_router, prefix=settings.api_v1_prefix)
app.include_router(derived_documents_router, prefix=settings.api_v1_prefix)
app.include_router(praticiens_router, prefix=settings.api_v1_prefix)
app.include_router(referentiels_router, prefix=settings.api_v1_prefix)
app.include_router(public_intake_router, prefix=settings.api_v1_prefix)
app.include_router(sessions_router, prefix=settings.api_v1_prefix)
app.include_router(session_preparation_router, prefix=settings.api_v1_prefix)
app.include_router(exercises_router, prefix=settings.api_v1_prefix)
app.include_router(analysis_deliveries_router, prefix=settings.api_v1_prefix)
app.include_router(me_carte_router, prefix=settings.api_v1_prefix)
app.include_router(me_reflets_router, prefix=settings.api_v1_prefix)
app.include_router(praticien_pratique_router, prefix=settings.api_v1_prefix)
app.include_router(session_notes_router, prefix=settings.api_v1_prefix)
app.include_router(session_temporal_anchors_router, prefix=settings.api_v1_prefix)
app.include_router(schedules_router, prefix=settings.api_v1_prefix)
app.include_router(register_router, prefix=settings.api_v1_prefix)
app.include_router(verify_email_router, prefix=settings.api_v1_prefix)
app.include_router(bookings_router, prefix=settings.api_v1_prefix)
app.include_router(matching_router, prefix=settings.api_v1_prefix)
app.include_router(payments_router, prefix=settings.api_v1_prefix)
app.include_router(appointments_router, prefix=settings.api_v1_prefix)
app.include_router(calendar_router, prefix=settings.api_v1_prefix)
app.include_router(timeline_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "ok",
        "docs": "/docs",
    }
