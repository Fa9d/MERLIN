"""Capacité semantic_llm (étape 3a chantier Analyses) — gardes et pipeline.

Appel Anthropic MOCKÉ. Fixtures autonettoyantes (ordre FK) et settings patché
via object.__setattr__ (dataclass gelé) — leçons des étapes 1-2.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_session_semantic.db").resolve()
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
from app.models.session import SessionRecord

init_models()

SORTIE_VALIDE = {
    "synthese": "La séance s'ouvre sur la fatigue et se referme sur une décision posée.",
    "themes": [
        {
            "titre": "Fatigue au travail",
            "observation": "Le client décrit trois semaines sans pause réelle.",
            "hypothese": "Le rythme actuel semblerait dépasser ses ressources du moment.",
        }
    ],
    "moments": [
        {"verbatim": "je pense que je vais dire non", "lecture": "Une limite se formule pour la première fois."}
    ],
    "axes_touches": ["travail", "corps"],
    "focus_prevu": {"statut": "sans_objet", "commentaire": "Première séance documentée."},
    "vigilance": {"niveau": "aucun", "raison": None},
    "triade": {
        "observation": "La séance montre une parole qui se précise autour du travail.",
        "hypothese": "La capacité à poser une limite semblerait émerger.",
        "orientation": "Revenir sur ce « non » et ce qu'il ouvre.",
    },
}


@pytest.fixture(autouse=True)
def _enable_llm():
    from app.core.config import settings

    original = settings.insights_enabled
    object.__setattr__(settings, "insights_enabled", True)
    yield
    object.__setattr__(settings, "insights_enabled", original)


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
    from uuid import uuid4

    tag = uuid4().hex[:8]
    db = SessionLocal()
    praticien = _mk_user(db, f"ss-praticien-{tag}@example.com", AppRole.practitioner)
    autre = _mk_user(db, f"ss-autre-{tag}@example.com", AppRole.practitioner)

    client = Client(first_name_or_alias="Client Séance")
    db.add(client)
    db.flush()

    avec_transcript = SessionRecord(
        client_id=client.id, session_sequence_number=1,
        operator_user_id=praticien.id, praticien_id=praticien.id,
        transcript_text="… trois semaines sans vraie pause … je pense que je vais dire non …",
    )
    sans_transcript = SessionRecord(
        client_id=client.id, session_sequence_number=2,
        operator_user_id=praticien.id, praticien_id=praticien.id,
    )
    db.add_all([avec_transcript, sans_transcript])
    db.flush()
    ids = {
        "praticien": praticien.id,
        "autre": autre.id,
        "client": client.id,
        "s_ok": avec_transcript.id,
        "s_vide": sans_transcript.id,
    }
    db.commit()
    db.close()

    yield ids

    from app.models.analysis import AnalysisAccessLog, AnalysisResult

    db = SessionLocal()
    res_ids = [r.id for r in db.query(AnalysisResult).filter_by(client_id=ids["client"])]
    if res_ids:
        db.query(AnalysisAccessLog).filter(
            AnalysisAccessLog.analysis_result_id.in_(res_ids)
        ).delete(synchronize_session=False)
        db.query(AnalysisResult).filter(AnalysisResult.id.in_(res_ids)).delete(
            synchronize_session=False
        )
    db.query(SessionRecord).filter_by(client_id=ids["client"]).delete()
    db.query(Client).filter_by(id=ids["client"]).delete()
    db.query(AppUser).filter(
        AppUser.id.in_([ids["praticien"], ids["autre"]])
    ).delete(synchronize_session=False)
    db.commit()
    db.close()


def _auth(user_id: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, 'practitioner')}"}


def _mock_claude(monkeypatch, sortie: dict) -> None:
    import app.services.session_semantic as ss

    async def _fake_call(prompt: str, **kwargs):
        assert "PROMPT — Synthèse sémantique d'une séance" in prompt
        return json.dumps(sortie, ensure_ascii=False), {"input_tokens": 10, "output_tokens": 5}

    monkeypatch.setattr(ss, "_call_claude", _fake_call)


def test_semantique_produit_et_stocke(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s_ok']}/semantique",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["capability"] == "semantic_llm"
        assert body["sensitivity"] == "hypothese"
        assert body["payload"]["transcript_tronque"] is False
        assert body["payload"]["moments"][0]["verbatim"]


def test_semantique_refuse_sans_transcript(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s_vide']}/semantique",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 409, r.text


def test_semantique_refuse_praticien_non_assigne(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s_ok']}/semantique",
            headers=_auth(ctx["autre"]),
        )
        assert r.status_code == 403, r.text


def test_semantique_bloque_vocabulaire_loi21(ctx, monkeypatch) -> None:
    from app.main import app

    interdite = json.loads(json.dumps(SORTIE_VALIDE))
    interdite["triade"]["orientation"] = "Poursuivre le traitement entamé."  # mot interdit
    _mock_claude(monkeypatch, interdite)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s_ok']}/semantique",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 502, r.text
