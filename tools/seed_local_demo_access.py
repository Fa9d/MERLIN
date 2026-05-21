"""Restore local MERLIN demo accounts with known temporary passwords.

This script is intended for local Docker/PostgreSQL validation only. It does not
print password hashes or tokens.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import psycopg


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "10_backend_merlin_api"
sys.path.insert(0, str(BACKEND_DIR))

from app.core.security import hash_password  # noqa: E402


DB_URL = os.getenv(
    "MERLIN_DATABASE_URL",
    "postgresql://postgres:postgres@127.0.0.1:55432/merlin_v1",
).replace("postgresql+psycopg://", "postgresql://")

ACCOUNTS = [
    ("admin-postgres-1778696254@example.com", "admin_tech", "Admin Postgres", "Merlin-Admin-2026!"),
    ("operator-local-e2e@ivia.quebec", "operator", "Operateur E2E", "Merlin-Operator-2026!"),
    ("operator.local@ivia.quebec", "operator", "Operateur Local", "Merlin-Operator-2026!"),
    ("operator-postgres-1778696254@example.com", "operator", "Operateur Postgres", "Merlin-Operator-2026!"),
    ("client-postgres-1778696254@example.com", "public_client", "Client Postgres", "Merlin-Client-2026!"),
    ("pilote.aelis@ivia.quebec", "practitioner", "Aelis", "Merlin-Praticien-2026!"),
    ("pilote.nael@ivia.quebec", "practitioner", "Nael", "Merlin-Praticien-2026!"),
    ("pilote.nori@ivia.quebec", "practitioner", "Nori", "Merlin-Praticien-2026!"),
    ("pilote.seve@ivia.quebec", "practitioner", "Seve", "Merlin-Praticien-2026!"),
    ("pilote.solene@ivia.quebec", "practitioner", "Solene", "Merlin-Praticien-2026!"),
    ("pilote.telma@ivia.quebec", "practitioner", "Telma", "Merlin-Praticien-2026!"),
]


def upsert_account(cur, email: str, role: str, display_name: str, password: str, now: datetime) -> str:
    cur.execute("SELECT id FROM app_users WHERE email = %s", (email,))
    row = cur.fetchone()
    password_hash = hash_password(password)
    if row:
        user_id = row[0]
        cur.execute(
            """
            UPDATE app_users
            SET password_hash = %s,
                display_name = %s,
                role = %s,
                record_status = 'active',
                email_verified = true,
                email_verification_token = NULL,
                token_expires_at = NULL,
                updated_at = %s
            WHERE id = %s
            """,
            (password_hash, display_name, role, now, user_id),
        )
        return user_id

    user_id = str(uuid4())
    cur.execute(
        """
        INSERT INTO app_users (
            id, email, password_hash, display_name, role, record_status,
            email_verified, is_publicly_listed, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, 'active', true, %s, %s, %s)
        """,
        (user_id, email, password_hash, display_name, role, role == "practitioner", now, now),
    )
    return user_id


def ensure_client(cur, app_user_id: str, now: datetime) -> None:
    email = "client-postgres-1778696254@example.com"
    cur.execute("SELECT id FROM clients WHERE app_user_id = %s OR email = %s", (app_user_id, email))
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE clients
            SET app_user_id = %s,
                first_name_or_alias = 'Client Postgres',
                email = %s,
                record_status = 'active',
                updated_at = %s
            WHERE id = %s
            """,
            (app_user_id, email, now, row[0]),
        )
        return

    cur.execute(
        """
        INSERT INTO clients (
            id, public_client_code, first_name_or_alias, email, app_user_id,
            language_code, timezone, territory_code, is_adult_confirmed,
            record_status, data_sensitivity_class, created_at, updated_at
        ) VALUES (%s, %s, 'Client Postgres', %s, %s, 'fr-CA', 'America/Toronto',
            'QC', true, 'active', 'high', %s, %s)
        """,
        (str(uuid4()), "CLI-DEMOLOCAL", email, app_user_id, now, now),
    )


def main() -> int:
    now = datetime.now(timezone.utc)
    restored: list[tuple[str, str]] = []
    client_user_id: str | None = None

    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            for email, role, display_name, password in ACCOUNTS:
                user_id = upsert_account(cur, email, role, display_name, password, now)
                restored.append((email, role))
                if role == "public_client":
                    client_user_id = user_id
            if client_user_id:
                ensure_client(cur, client_user_id, now)
        conn.commit()

    print("email|role")
    for email, role in restored:
        print(f"{email}|{role}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())