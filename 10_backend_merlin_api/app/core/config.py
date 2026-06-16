from dataclasses import dataclass, field
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_list(value: str | None, default: list[str] | None = None) -> list[str]:
    if value is None:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("MERLIN_APP_NAME", "MERLIN API")
    environment: str = os.getenv("MERLIN_ENV", "development")
    api_v1_prefix: str = os.getenv("MERLIN_API_V1_PREFIX", "/api/v1")
    database_url: str = os.getenv(
        "MERLIN_DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@127.0.0.1:55432/merlin_v1",
    )
    auth_secret_key: str = os.getenv("MERLIN_AUTH_SECRET_KEY", "change-this-secret-in-dev")
    auth_access_token_expire_minutes: int = int(
        os.getenv("MERLIN_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "120")
    )
    media_provider_code: str = os.getenv("MERLIN_MEDIA_PROVIDER_CODE", "livekit")
    media_livekit_ws_url: str | None = os.getenv("MERLIN_MEDIA_LIVEKIT_WS_URL")
    media_livekit_public_ws_url: str | None = os.getenv("MERLIN_MEDIA_LIVEKIT_PUBLIC_WS_URL") or os.getenv(
        "MERLIN_MEDIA_LIVEKIT_WS_URL"
    )
    media_livekit_api_key: str | None = os.getenv("MERLIN_MEDIA_LIVEKIT_API_KEY")
    media_livekit_api_secret: str | None = os.getenv("MERLIN_MEDIA_LIVEKIT_API_SECRET")
    livekit_url: str | None = os.getenv("LIVEKIT_URL") or os.getenv("MERLIN_MEDIA_LIVEKIT_WS_URL")
    livekit_api_key: str | None = os.getenv("LIVEKIT_API_KEY") or os.getenv(
        "MERLIN_MEDIA_LIVEKIT_API_KEY"
    )
    livekit_api_secret: str | None = os.getenv("LIVEKIT_API_SECRET") or os.getenv(
        "MERLIN_MEDIA_LIVEKIT_API_SECRET"
    )
    media_recording_enabled: bool = _as_bool(
        os.getenv("MERLIN_MEDIA_RECORDING_ENABLED"),
        default=True,
    )
    media_recording_strategy: str = os.getenv(
        "MERLIN_MEDIA_RECORDING_STRATEGY",
        "metadata_only",
    )
    media_recordings_dir: str = os.getenv(
        "MERLIN_MEDIA_RECORDINGS_DIR",
        str(Path(__file__).resolve().parents[2] / "storage" / "recordings"),
    )
    livekit_recording_storage: str = os.getenv("LIVEKIT_RECORDING_STORAGE", "local")
    livekit_recording_local_dir: str = os.getenv(
        "LIVEKIT_RECORDING_LOCAL_DIR",
        os.getenv(
            "MERLIN_MEDIA_RECORDINGS_DIR",
            str(Path(__file__).resolve().parents[2] / "storage" / "recordings"),
        ),
    )
    livekit_s3_endpoint: str | None = os.getenv("LIVEKIT_S3_ENDPOINT")
    livekit_s3_bucket: str | None = os.getenv("LIVEKIT_S3_BUCKET")
    livekit_s3_access_key: str | None = os.getenv("LIVEKIT_S3_ACCESS_KEY")
    livekit_s3_secret_key: str | None = os.getenv("LIVEKIT_S3_SECRET_KEY")
    livekit_s3_region: str | None = os.getenv("LIVEKIT_S3_REGION")
    livekit_s3_force_path_style: bool = _as_bool(
        os.getenv("LIVEKIT_S3_FORCE_PATH_STYLE"),
        default=True,
    )
    assemblyai_api_key: str | None = os.getenv("ASSEMBLYAI_API_KEY")
    # Transcription des séances — provider local faster-whisper (données Québec, Loi 25)
    # ou AssemblyAI (tiers, legacy). `auto` = faster-whisper si installé, sinon AssemblyAI.
    transcription_provider: str = os.getenv("MERLIN_TRANSCRIPTION_PROVIDER", "auto")
    whisper_model_size: str = os.getenv("MERLIN_WHISPER_MODEL", "medium")
    whisper_device: str = os.getenv("MERLIN_WHISPER_DEVICE", "cpu")
    whisper_compute_type: str = os.getenv("MERLIN_WHISPER_COMPUTE_TYPE", "int8")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    stripe_secret_key: str | None = os.getenv("MERLIN_STRIPE_SECRET_KEY")
    stripe_webhook_secret: str | None = os.getenv("MERLIN_STRIPE_WEBHOOK_SECRET")
    stripe_checkout_success_url: str | None = os.getenv("MERLIN_STRIPE_CHECKOUT_SUCCESS_URL")
    stripe_checkout_cancel_url: str | None = os.getenv("MERLIN_STRIPE_CHECKOUT_CANCEL_URL")
    # Grille IVIA (prix TTC en cents) — enregistrement + rappel = 49 $
    stripe_audio_async_amount_cents: int = int(os.getenv("MERLIN_STRIPE_AUDIO_ASYNC_AMOUNT_CENTS", "4900"))
    stripe_audio_async_currency: str = os.getenv("MERLIN_STRIPE_AUDIO_ASYNC_CURRENCY", "cad")
    # Prix serveur d'une séance live réservée (jamais fourni par le client — anti-manipulation) = 75 $
    stripe_seance_amount_cents: int = int(os.getenv("MERLIN_STRIPE_SEANCE_AMOUNT_CENTS", "7500"))
    stripe_seance_currency: str = os.getenv("MERLIN_STRIPE_SEANCE_CURRENCY", "cad")
    # Enregistrement solo 30 min, sans praticien = 35 $
    stripe_solo_amount_cents: int = int(os.getenv("MERLIN_STRIPE_SOLO_AMOUNT_CENTS", "3500"))
    stripe_solo_currency: str = os.getenv("MERLIN_STRIPE_SOLO_CURRENCY", "cad")
    # Comptabilité — assujettissement aux taxes (TPS/TVQ). False tant que sous le
    # seuil de petit fournisseur (30 000 $). Les prix sont alors 100 % revenu ;
    # une fois True, la décomposition TTC → HT + TPS + TVQ s'active (voir services/billing.py).
    tax_registered: bool = os.getenv("MERLIN_TAX_REGISTERED", "false").lower() == "true"
    tps_rate: float = float(os.getenv("MERLIN_TPS_RATE", "0.05"))       # TPS fédérale
    tvq_rate: float = float(os.getenv("MERLIN_TVQ_RATE", "0.09975"))    # TVQ Québec
    # SMTP
    smtp_host: str = os.getenv("SMTP_HOST", "ssl0.ovh.net")
    smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
    smtp_username: str | None = os.getenv("SMTP_USERNAME")
    smtp_password: str | None = os.getenv("SMTP_PASSWORD")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "noreply@ivia.quebec")
    smtp_from_name: str = os.getenv("SMTP_FROM_NAME", "IVIA")
    smtp_use_tls: bool = _as_bool(os.getenv("SMTP_USE_TLS"), default=False)
    smtp_use_ssl: bool = _as_bool(os.getenv("SMTP_USE_SSL"), default=True)
    interac_etransfer_email: str = os.getenv(
        "INTERAC_ETRANSFER_EMAIL",
        os.getenv("SMTP_FROM_EMAIL", "noreply@ivia.quebec"),
    )
    interac_etransfer_recipient_name: str = os.getenv(
        "INTERAC_ETRANSFER_RECIPIENT_NAME",
        os.getenv("SMTP_FROM_NAME", "IVIA"),
    )
    interac_etransfer_notice: str = os.getenv(
        "INTERAC_ETRANSFER_NOTICE",
        "Envoyez le virement a l'adresse ci-dessous et utilisez la reference indiquee dans le message du virement.",
    )
    frontend_url: str = os.getenv("FRONTEND_URL", "https://ivia.quebec")
    cors_origins: list[str] = field(
        default_factory=lambda: _as_list(
            os.getenv("MERLIN_CORS_ORIGINS"),
            default=["http://127.0.0.1:3000", "http://localhost:3000"],
        )
    )
    auto_create_tables: bool = _as_bool(
        os.getenv("MERLIN_AUTO_CREATE_TABLES"),
        default=True,
    )


settings = Settings()
