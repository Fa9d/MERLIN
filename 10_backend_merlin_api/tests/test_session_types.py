"""Types de séance × capacités (Atelier des lectures) — CRUD admin et vanne 3D.

Vérifie : CRUD admin (création, matrice enabled/auto_run, garde auto_run⊂enabled),
défaut permissif (séance sans type → analyses permises), et blocage effectif
d'une capacité pour un type donné. LLM mocké ; fixtures autonettoyantes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_session_types.db").resolve()
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
from app.models.session_type import SessionType, SessionTypeCapability

init_models()

SORTIE_VALIDE = {
    "synthese": "Mouvement d'ensemble sobre.",
    "themes": [],
    "moments": [],
    "axes_touches": [],
    "focus_prevu": {"statut": "sans_objet", "commentaire": ""},
    "vigilance": {"niveau": "aucun", "raison": None},
    "triade": {"observation": "Peu de matière.", "hypothese": "Rien à avancer.", "orientation": "Écouter."},
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
    admin = _mk_user(db, f"st-admin-{tag}@example.com", AppRole.admin_tech)
    praticien = _mk_user(db, f"st-prat-{tag}@example.com", AppRole.practitioner)

    client = Client(first_name_or_alias="Client Types")
    db.add(client)
    db.flush()
    seance = SessionRecord(
        client_id=client.id, session_sequence_number=1,
        operator_user_id=praticien.id, praticien_id=praticien.id,
        transcript_text="matière suffisante pour une lecture",
    )
    db.add(seance)
    db.flush()
    ids = {
        "admin": admin.id, "praticien": praticien.id,
        "client": client.id, "seance": seance.id, "tag": tag,
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
    db.query(SessionTypeCapability).filter(
        SessionTypeCapability.session_type_code.like(f"t{ids['tag']}%")
    ).delete(synchronize_session=False)
    db.query(SessionType).filter(SessionType.code.like(f"t{ids['tag']}%")).delete(
        synchronize_session=False
    )
    db.query(AppUser).filter(
        AppUser.id.in_([ids["admin"], ids["praticien"]])
    ).delete(synchronize_session=False)
    db.commit()
    db.close()


def _auth(user_id: str, role: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


def _mock_claude(monkeypatch, sortie: dict) -> None:
    import app.services.session_semantic as ss

    async def _fake_call(prompt: str):
        return json.dumps(sortie, ensure_ascii=False), {"input_tokens": 5, "output_tokens": 5}

    monkeypatch.setattr(ss, "_call_claude", _fake_call)


def test_crud_admin_et_garde_auto_run(ctx) -> None:
    from app.main import app

    code = f"t{ctx['tag']}"
    with HttpClient(app) as http:
        # Création
        r = http.post(
            "/api/v1/admin/analysis/session-types",
            json={"code": code, "label": "Type de test", "description": "essai"},
            headers=_auth(ctx["admin"], "admin_tech"),
        )
        assert r.status_code == 201, r.text
        body = r.json()
        # Défaut permissif : toutes capacités enabled, aucune auto_run
        assert all(c["enabled"] for c in body["capabilities"].values())
        assert not any(c["auto_run"] for c in body["capabilities"].values())

        # auto_run sur capacité désactivée → 400
        http.patch(
            f"/api/v1/admin/analysis/session-types/{code}/capabilities",
            json={"capability": "semantic_llm", "enabled": False},
            headers=_auth(ctx["admin"], "admin_tech"),
        )
        r = http.patch(
            f"/api/v1/admin/analysis/session-types/{code}/capabilities",
            json={"capability": "semantic_llm", "auto_run": True},
            headers=_auth(ctx["admin"], "admin_tech"),
        )
        assert r.status_code == 400, r.text

        # Un praticien n'a pas accès à l'admin
        r = http.get(
            "/api/v1/admin/analysis/session-types",
            headers=_auth(ctx["praticien"], "practitioner"),
        )
        assert r.status_code == 403, r.text


def test_sans_type_reste_permis(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['seance']}/semantique",
            headers=_auth(ctx["praticien"], "practitioner"),
        )
        assert r.status_code == 200, r.text


def test_type_bloque_la_capacite(ctx, monkeypatch) -> None:
    from app.main import app

    code = f"t{ctx['tag']}b"
    db = SessionLocal()
    db.add(SessionType(code=code, label="Écoute stricte"))
    db.add(
        SessionTypeCapability(
            session_type_code=code, capability="semantic_llm", enabled=False
        )
    )
    seance = db.get(SessionRecord, ctx["seance"])
    seance.session_type_code = code
    db.add(seance)
    db.commit()
    db.close()

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['seance']}/semantique",
            headers=_auth(ctx["praticien"], "practitioner"),
        )
        assert r.status_code == 403, r.text
        assert "type de séance" in r.json()["detail"]
