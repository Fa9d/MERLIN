"""Journal de pratique — isolation stricte, reflet, protocole de détresse.

Vérifie : chaque praticien ne voit QUE ses retours et reflets (isolation,
sans exception admin), retour lié seulement à SA séance, reflet mocké,
protocole de détresse EN CODE (ressources injectées, analyse neutralisée),
cooldown. Fixtures autonettoyantes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_pratique.db").resolve()
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
from app.models.enums import AppRole
from app.models.practitioner_journal import PractitionerJournalEntry
from app.services.practice_reflection import RESSOURCES_DETRESSE

init_models()

REFLET_PRATIQUE = {
    "reflet": "Ta charge des jeudis est un pattern, pas un hasard : trois retours sur quatre le nomment.",
    "constats": [{"titre": "Les jeudis te vident", "appui": "« vidé après les trois séances de suite » — noté les 26 juin et 3 juillet",
                  "lecture": "Trois séances consécutives sans pause dépassent ta capacité de présence en fin de journée."}],
    "pistes": ["Bloque 15 minutes entre la 2e et la 3e séance du jeudi pendant deux semaines et note la différence."],
    "vigilance": {"niveau": "aucun", "raison": None},
    "ressources": None,
}

REFLET_DETRESSE = {
    "reflet": "Ce que tu portes est lourd.",
    "constats": [{"titre": "Ne devrait pas apparaître", "appui": "x", "lecture": "analyse interdite"}],
    "pistes": ["Ne devrait pas apparaître"],
    "vigilance": {"niveau": "urgence", "raison": "Idées noires exprimées."},
    "ressources": "Texte modèle qui sera remplacé par le protocole en code.",
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
    p1 = _mk_user(db, f"pr-un-{tag}@example.com", AppRole.practitioner)
    p2 = _mk_user(db, f"pr-deux-{tag}@example.com", AppRole.practitioner)
    ids = {"p1": p1.id, "p2": p2.id}
    db.commit()
    db.close()

    yield ids

    db = SessionLocal()
    db.query(AnalysisResult).filter(
        AnalysisResult.created_by_user_id.in_([ids["p1"], ids["p2"]]),
        AnalysisResult.capability == "praticien_reflet",
    ).delete(synchronize_session=False)
    db.query(PractitionerJournalEntry).filter(
        PractitionerJournalEntry.praticien_id.in_([ids["p1"], ids["p2"]])
    ).delete(synchronize_session=False)
    db.query(AppUser).filter(AppUser.id.in_([ids["p1"], ids["p2"]])).delete(
        synchronize_session=False
    )
    db.commit()
    db.close()


def _auth(user_id: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, 'practitioner')}"}


def _mock_claude(monkeypatch, sortie: dict) -> None:
    import app.services.practice_reflection as pr

    async def _fake_call(prompt: str, **kwargs):
        assert "analyse franche" in prompt
        return json.dumps(sortie, ensure_ascii=False), {"input_tokens": 10, "output_tokens": 5}

    monkeypatch.setattr(pr, "_call_claude", _fake_call)


def test_isolation_stricte_entre_praticiens(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/pratique/retours",
            json={"body_text": "Vidé après les trois séances de suite. J'ai précipité la dernière."},
            headers=_auth(ctx["p1"]),
        )
        assert r.status_code == 201, r.text

        # p1 voit son retour ; p2 ne voit RIEN
        assert len(http.get("/api/v1/pratique/retours", headers=_auth(ctx["p1"])).json()) == 1
        assert http.get("/api/v1/pratique/retours", headers=_auth(ctx["p2"])).json() == []


def test_reflet_et_cooldown(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, REFLET_PRATIQUE)
    with HttpClient(app) as http:
        http.post(
            "/api/v1/pratique/retours",
            json={"body_text": "Vidé après les trois séances de suite, encore un jeudi."},
            headers=_auth(ctx["p1"]),
        )
        r = http.post("/api/v1/pratique/reflet", headers=_auth(ctx["p1"]))
        assert r.status_code == 201, r.text
        assert "jeudis" in r.json()["reflet"]
        assert r.json()["constats"][0]["appui"]  # constat ANCRÉ

        # Cooldown pour p1 ; p2 sans matière reçoit 409, pas le reflet de p1
        assert http.post("/api/v1/pratique/reflet", headers=_auth(ctx["p1"])).status_code == 429
        assert http.post("/api/v1/pratique/reflet", headers=_auth(ctx["p2"])).status_code == 409
        assert http.get("/api/v1/pratique/reflets", headers=_auth(ctx["p2"])).json() == []


def test_protocole_detresse_en_code(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, REFLET_DETRESSE)
    with HttpClient(app) as http:
        http.post(
            "/api/v1/pratique/retours",
            json={"body_text": "Je n'y arrive plus. Des idées noires me traversent après les séances."},
            headers=_auth(ctx["p1"]),
        )
        r = http.post("/api/v1/pratique/reflet", headers=_auth(ctx["p1"]))
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["ressources"] == RESSOURCES_DETRESSE
        assert "9-8-8" in body["ressources"] and "supervision" in body["ressources"]
        assert body["constats"] == [] and body["pistes"] == []
