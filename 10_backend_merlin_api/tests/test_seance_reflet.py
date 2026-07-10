"""Reflet de séance (mode autonome) — appartenance, idempotence, urgence EN CODE.

Vérifie : le client ne peut demander la lecture QUE de son propre
enregistrement transcrit ; un reflet par enregistrement (2e appel = même
reflet, pas de 2e appel LLM) ; protocole d'urgence appliqué en code.
Données fictives uniquement.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_seance_reflet.db").resolve()
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
from app.models.analysis import AnalysisResult
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import AppRole, SessionChannelCode, SessionModeCode
from app.models.llm_usage import LlmUsageEvent
from app.models.session import SessionRecord
from app.services.session_reflection import RESSOURCES_URGENCE

init_models()

REFLET_DOUX = {
    "reflet": "Tu as parlé de tes samedis au bord de l'eau — « je redeviens moi-même », c'est ton mot.",
    "fils": [{"titre": "Le samedi qui t'appartient", "echo": "« j'ai dit oui à tout le monde »"}],
    "question_ouverte": "",
    "piste": "",
    "vigilance": {"niveau": "aucun", "raison": None},
    "ressources": None,
}

REFLET_URGENCE = {
    "reflet": "Ce que tu as dit est lourd, et tu n'as pas à le porter seul·e.",
    "fils": [{"titre": "Ne doit pas apparaître", "echo": "analyse interdite"}],
    "question_ouverte": "Ne doit pas apparaître",
    "piste": "Ne doit pas apparaître",
    "vigilance": {"niveau": "urgence", "raison": "Idées suicidaires exprimées."},
    "ressources": "Texte modèle remplacé par le protocole en code.",
}


@pytest.fixture(autouse=True)
def _enable_llm():
    from app.core.config import settings

    original = settings.insights_enabled
    object.__setattr__(settings, "insights_enabled", True)
    yield
    object.__setattr__(settings, "insights_enabled", original)


@pytest.fixture()
def ctx() -> dict:
    from uuid import uuid4

    tag = uuid4().hex[:8]
    db = SessionLocal()
    u1 = AppUser(email=f"cl-un-{tag}@example.com", password_hash=hash_password("x-test-x"),
                 display_name="Client Un", role=AppRole.public_client, email_verified=True)
    u2 = AppUser(email=f"cl-deux-{tag}@example.com", password_hash=hash_password("x-test-x"),
                 display_name="Client Deux", role=AppRole.public_client, email_verified=True)
    db.add_all([u1, u2])
    db.flush()
    c1 = Client(first_name_or_alias="Client Un", app_user_id=u1.id)
    c2 = Client(first_name_or_alias="Client Deux", app_user_id=u2.id)
    db.add_all([c1, c2])
    db.flush()
    rec = SessionRecord(
        client_id=c1.id,
        session_sequence_number=1,
        operator_user_id=u1.id,  # solo : le client est son propre opérateur
        session_channel_code=SessionChannelCode.audio_async,
        session_mode_code=SessionModeCode.standard,
        transcript_text="Cette semaine j'ai dit oui à tout le monde. Le samedi au bord de l'eau je redeviens moi-même.",
        duration_minutes=12,
    )
    db.add(rec)
    db.flush()
    ids = {"u1": u1.id, "u2": u2.id, "c1": c1.id, "c2": c2.id, "rec": rec.id}
    db.commit()
    db.close()

    yield ids

    db = SessionLocal()
    db.query(AnalysisResult).filter(
        AnalysisResult.client_id.in_([ids["c1"], ids["c2"]])
    ).delete(synchronize_session=False)
    db.query(LlmUsageEvent).filter(
        LlmUsageEvent.client_id.in_([ids["c1"], ids["c2"]])
    ).delete(synchronize_session=False)
    db.query(SessionRecord).filter(SessionRecord.id == ids["rec"]).delete(
        synchronize_session=False
    )
    db.query(Client).filter(Client.id.in_([ids["c1"], ids["c2"]])).delete(
        synchronize_session=False
    )
    db.query(AppUser).filter(AppUser.id.in_([ids["u1"], ids["u2"]])).delete(
        synchronize_session=False
    )
    db.commit()
    db.close()


def _auth(user_id: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, 'public_client')}"}


def _mock_claude(monkeypatch, sortie: dict):
    import app.services.session_reflection as sr

    calls = {"n": 0}

    async def _fake_call(prompt: str):
        calls["n"] += 1
        assert "ta parole enregistrée" in prompt
        return json.dumps(sortie, ensure_ascii=False), {"input_tokens": 10, "output_tokens": 5}

    monkeypatch.setattr(sr, "_call_claude", _fake_call)
    return calls


def test_appartenance_et_idempotence(ctx, monkeypatch) -> None:
    from app.main import app

    calls = _mock_claude(monkeypatch, REFLET_DOUX)
    with HttpClient(app) as http:
        url = f"/api/v1/me/recordings/{ctx['rec']}/reflet"
        # L'autre client ne voit PAS cet enregistrement
        assert http.post(url, headers=_auth(ctx["u2"])).status_code == 404

        r = http.post(url, headers=_auth(ctx["u1"]))
        assert r.status_code == 201, r.text
        assert "je redeviens moi-même" in r.json()["reflet"]
        rid = r.json()["id"]

        # Idempotent : même reflet, AUCUN second appel LLM
        r2 = http.post(url, headers=_auth(ctx["u1"]))
        assert r2.status_code == 201 and r2.json()["id"] == rid
        assert calls["n"] == 1

        # Et il apparaît dans GET /me/reflets
        assert any(x["id"] == rid for x in http.get("/api/v1/me/reflets", headers=_auth(ctx["u1"])).json())


def test_protocole_urgence_en_code(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, REFLET_URGENCE)
    with HttpClient(app) as http:
        r = http.post(f"/api/v1/me/recordings/{ctx['rec']}/reflet", headers=_auth(ctx["u1"]))
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["ressources"] == RESSOURCES_URGENCE
        assert "9-8-8" in body["ressources"]
        assert body["fils"] == [] and body["question_ouverte"] == "" and body["piste"] == ""
