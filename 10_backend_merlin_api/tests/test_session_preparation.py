"""Dossier de préparation d'entretien (étape 1 chantier Analyses) — accès et consentement.

Vérifie les gardes du endpoint GET /sessions/{id}/preparation :
1. le praticien ASSIGNÉ voit le dossier, journal inclus si consent_history actif ;
2. sans consent_history, le contenu du journal est TU (drapeau false, liste vide) ;
3. un praticien NON assigné reçoit 403 ; un compte client reçoit 403.

NB : la fixture autouse ``reset_app_users`` (conftest) vide app_users avant CHAQUE
test — toutes les données sont donc créées à l'intérieur des tests, jamais au module.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_session_preparation.db").resolve()
if _TEST_DB_PATH.exists():
    _TEST_DB_PATH.unlink()
os.environ["MERLIN_DATABASE_URL"] = f"sqlite:///{_TEST_DB_PATH.as_posix()}"
os.environ["MERLIN_AUTO_CREATE_TABLES"] = "true"
os.environ.setdefault("MERLIN_MEDIA_LIVEKIT_WS_URL", "wss://livekit.example.test")
os.environ.setdefault("MERLIN_MEDIA_LIVEKIT_PUBLIC_WS_URL", "wss://livekit.example.test")
os.environ.setdefault("MERLIN_MEDIA_LIVEKIT_API_KEY", "devkey")
os.environ.setdefault("MERLIN_MEDIA_LIVEKIT_API_SECRET", "devsecret-devsecret-devsecret-2026")
os.environ.setdefault("MERLIN_MEDIA_RECORDING_STRATEGY", "metadata_only")
os.environ.setdefault("MERLIN_STRIPE_SECRET_KEY", "sk_test_dummy")

from fastapi.testclient import TestClient as HttpClient

from app.core.security import create_access_token, hash_password
from app.db.base import init_models
from app.db.session import SessionLocal
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_intention import ClientIntention
from app.models.client_journal_entry import ClientJournalEntry
from app.models.consent import Consent
from app.models.enums import AppRole, ConsentTypeCode, GrantedByActorCode
from app.models.session import SessionRecord

init_models()


def _mk_user(db, email: str, role: AppRole) -> AppUser:
    user = AppUser(
        email=email,
        password_hash=hash_password("x-test-x"),
        display_name=email.split("@")[0],
        role=role,
        email_verified=True,
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def ctx() -> dict:
    """Client + praticien assigné + 2 séances + intention + entrée de journal.

    Emails uniques par test : en CI (Postgres), la fixture ``reset_app_users`` ne
    peut pas purger app_users (FK depuis sessions) — on évite toute collision.
    """
    from uuid import uuid4

    tag = uuid4().hex[:8]
    db = SessionLocal()
    praticien = _mk_user(db, f"prep-praticien-{tag}@example.com", AppRole.practitioner)
    autre = _mk_user(db, f"prep-autre-{tag}@example.com", AppRole.practitioner)
    client_user = _mk_user(db, f"prep-client-{tag}@example.com", AppRole.public_client)

    client = Client(first_name_or_alias="Client Préparation")
    db.add(client)
    db.flush()

    s1 = SessionRecord(
        client_id=client.id,
        session_sequence_number=1,
        operator_user_id=praticien.id,
        praticien_id=praticien.id,
    )
    s2 = SessionRecord(
        client_id=client.id,
        session_sequence_number=2,
        operator_user_id=praticien.id,
        praticien_id=praticien.id,
    )
    db.add_all([s1, s2])
    db.flush()

    db.add(
        ClientIntention(
            client_id=client.id, text="Retrouver le sommeil", created_by="client"
        )
    )
    db.add(
        ClientJournalEntry(
            client_id=client.id, body_text="Semaine difficile mais deux bonnes nuits."
        )
    )
    ids = {
        "praticien": praticien.id,
        "autre": autre.id,
        "client_user": client_user.id,
        "client": client.id,
        "s2": s2.id,
    }
    db.commit()
    db.close()
    return ids


def _auth(user_id: str, role: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


def test_preparation_sans_consentement_tait_le_journal(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.get(
            f"/api/v1/sessions/{ctx['s2']}/preparation",
            headers=_auth(ctx["praticien"], "practitioner"),
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["journal_access_granted"] is False
        assert body["journal_entries"] == []
        assert len(body["intentions"]) == 1
        assert body["previous_session"]["session_sequence_number"] == 1
        assert body["client"]["first_name_or_alias"] == "Client Préparation"


def test_preparation_avec_consentement_expose_le_journal(ctx) -> None:
    from app.main import app

    db = SessionLocal()
    db.add(
        Consent(
            client_id=ctx["client"],
            consent_type_code=ConsentTypeCode.consent_history,
            consent_value=True,
            granted_by_actor_code=GrantedByActorCode.client,
        )
    )
    db.commit()
    db.close()

    with HttpClient(app) as http:
        r = http.get(
            f"/api/v1/sessions/{ctx['s2']}/preparation",
            headers=_auth(ctx["praticien"], "practitioner"),
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["journal_access_granted"] is True
        assert len(body["journal_entries"]) == 1
        assert "bonnes nuits" in body["journal_entries"][0]["body_text"]


def test_preparation_praticien_non_assigne_403(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.get(
            f"/api/v1/sessions/{ctx['s2']}/preparation",
            headers=_auth(ctx["autre"], "practitioner"),
        )
        assert r.status_code == 403, r.text


def test_preparation_client_refuse(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.get(
            f"/api/v1/sessions/{ctx['s2']}/preparation",
            headers=_auth(ctx["client_user"], "public_client"),
        )
        assert r.status_code == 403, r.text
