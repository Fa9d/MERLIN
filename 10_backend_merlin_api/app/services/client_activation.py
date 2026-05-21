"""Helpers for client account activation invitations."""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from app.models.client import Client

ACTIVATION_TOKEN_TTL_DAYS = 7


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def generate_activation_token() -> str:
    return secrets.token_urlsafe(48)


def hash_activation_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def set_activation_token(client: Client, token: str) -> datetime:
    expires_at = utc_now() + timedelta(days=ACTIVATION_TOKEN_TTL_DAYS)
    client.activation_token_hash = hash_activation_token(token)
    client.activation_token_expires_at = expires_at
    client.activation_invited_at = utc_now()
    return expires_at


def activation_is_expired(client: Client) -> bool:
    if client.activation_token_expires_at is None:
        return True
    return normalize_datetime(client.activation_token_expires_at) < utc_now()


def clear_activation_token(client: Client) -> None:
    client.activation_token_hash = None
    client.activation_token_expires_at = None