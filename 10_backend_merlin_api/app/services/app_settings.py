"""Accès aux réglages runtime (table app_settings)."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.app_setting import AppSetting


def get_value(db: Session, key: str, default: str | None = None) -> str | None:
    row = db.get(AppSetting, key)
    return row.value if row is not None else default


def get_bool(db: Session, key: str, default: bool) -> bool:
    raw = get_value(db, key)
    if raw is None:
        return default
    return raw.strip().lower() == "true"


def set_value(db: Session, key: str, value: str) -> None:
    row = db.get(AppSetting, key)
    if row is None:
        row = AppSetting(key=key, value=value)
    else:
        row.value = value
        row.updated_at = datetime.now(timezone.utc)
    db.add(row)
