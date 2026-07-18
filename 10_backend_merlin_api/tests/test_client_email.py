"""Courriel praticien → client depuis la fiche client.

Vérifie : envoi accepté pour un praticien authentifié, 404 si client inconnu,
422 si aucune adresse au dossier, 502 si l'envoi SMTP échoue, refus des rôles
non cliniques. L'envoi SMTP réel est remplacé par un stub.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_client_email.db").resolve()
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
from app.models.enums import AppRole

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


def _auth(user_id: str, role: str = "practitioner") -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


@pytest.fixture()
def ctx() -> dict:
    from uuid import uuid4

    tag = uuid4().hex[:8]
    db = SessionLocal()
    praticien = _mk_user(db, f"ce-prat-{tag}@example.com", AppRole.practitioner)
    client_user = _mk_user(db, f"ce-client-{tag}@example.com", AppRole.public_client)

    avec_courriel = Client(
        first_name_or_alias="Client Courriel",
        app_user_id=client_user.id,
        email=f"ce-client-{tag}@example.com",
    )
    sans_courriel = Client(first_name_or_alias="Client Muet")
    db.add_all([avec_courriel, sans_courriel])
    db.flush()
    db.commit()

    data = {
        "praticien": praticien.id,
        "client_user": client_user.id,
        "avec_courriel": avec_courriel.id,
        "sans_courriel": sans_courriel.id,
        "client_email": avec_courriel.email,
    }
    db.close()
    yield data


PAYLOAD = {"subject": "Petit mot de suivi", "message": "Bonjour,\nà bientôt."}


def _stub_send(result: bool, sink: list):
    async def _send(**kwargs):
        sink.append(kwargs)
        return result
    return _send


def test_envoi_accepte_et_gabarit(ctx, monkeypatch) -> None:
    from app.api.routes import clients as clients_module
    from app.main import app

    envois: list = []
    monkeypatch.setattr(clients_module, "send_email", _stub_send(True, envois))

    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/clients/{ctx['avec_courriel']}/email",
            json=PAYLOAD,
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 202, r.text
        assert r.json() == {"sent": True, "to": ctx["client_email"]}

    assert len(envois) == 1
    envoi = envois[0]
    assert envoi["to_email"] == ctx["client_email"]
    assert envoi["subject"] == "Petit mot de suivi"
    assert envoi["audience"] == "client"
    # Le message du praticien figure dans les deux corps, échappé côté HTML.
    assert "à bientôt." in envoi["text_body"]
    assert "à bientôt." in envoi["html_body"]


def test_message_html_echappe(ctx, monkeypatch) -> None:
    from app.api.routes import clients as clients_module
    from app.main import app

    envois: list = []
    monkeypatch.setattr(clients_module, "send_email", _stub_send(True, envois))

    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/clients/{ctx['avec_courriel']}/email",
            json={"subject": "s", "message": "<script>alert(1)</script>"},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 202, r.text
    assert "<script>" not in envois[0]["html_body"]
    assert "&lt;script&gt;" in envois[0]["html_body"]


def test_client_inconnu_404(ctx, monkeypatch) -> None:
    from app.api.routes import clients as clients_module
    from app.main import app

    monkeypatch.setattr(clients_module, "send_email", _stub_send(True, []))
    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/clients/inexistant/email",
            json=PAYLOAD,
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 404, r.text


def test_sans_adresse_422(ctx, monkeypatch) -> None:
    from app.api.routes import clients as clients_module
    from app.main import app

    envois: list = []
    monkeypatch.setattr(clients_module, "send_email", _stub_send(True, envois))
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/clients/{ctx['sans_courriel']}/email",
            json=PAYLOAD,
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 422, r.text
    assert envois == []


def test_echec_smtp_502(ctx, monkeypatch) -> None:
    from app.api.routes import clients as clients_module
    from app.main import app

    monkeypatch.setattr(clients_module, "send_email", _stub_send(False, []))
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/clients/{ctx['avec_courriel']}/email",
            json=PAYLOAD,
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 502, r.text


def test_role_client_refuse(ctx, monkeypatch) -> None:
    from app.api.routes import clients as clients_module
    from app.main import app

    monkeypatch.setattr(clients_module, "send_email", _stub_send(True, []))
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/clients/{ctx['avec_courriel']}/email",
            json=PAYLOAD,
            headers=_auth(ctx["client_user"], "public_client"),
        )
        assert r.status_code == 403, r.text
