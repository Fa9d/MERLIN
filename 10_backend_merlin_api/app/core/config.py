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
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
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
