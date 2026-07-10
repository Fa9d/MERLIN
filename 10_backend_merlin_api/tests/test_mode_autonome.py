"""Mode autonome — reflet de journal sans praticien + transfert de praticien.

Vérifie : reflet produit pour un client SANS praticien (le cœur de la
décision), protocole d'urgence appliqué EN CODE (ressources injectées,
analyse neutralisée), cooldown 20 h, transfert admin (resume défaut,
integral exige le consentement). LLM mocké ; fixtures autonettoyantes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_mode_autonome.db").resolve()
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
from app.models.client_journal_entry import ClientJournalEntry
from app.models.client_transfer import ClientPractitionerTransfer
from app.models.enums import AppRole
from app.services.journal_reflection import RESSOURCES_URGENCE

init_models()

REFLET_DOUX = {
    "reflet": "Ta période montre un mouvement d'apaisement, deux soirs plus doux.",
    "fils": [{"titre": "Le sommeil", "echo": "« deux bonnes nuits » — tes mots."}],
    "question_ouverte": "Qu'est-ce que ces soirs-là avaient de différent, selon toi ?",
    "piste": "Si l'envie est là, note ce soir une chose qui a aidé.",
    "vigilance": {"niveau": "aucun", "raison": None},
    "ressources": None,
}

REFLET_URGENCE = {
    "reflet": "Ce que tu as déposé est lourd, et il compte.",
    "fils": [{"titre": "Un fil qui ne devrait pas apparaître", "echo": "analyse interdite ici"}],
    "question_ouverte": "Une question qui ne devrait pas apparaître",
    "piste": "Une piste qui ne devrait pas apparaître",
    "vigilance": {"niveau": "urgence", "raison": "Évocation directe d'en finir."},
    "ressources": "Texte du modèle qui sera remplacé par le protocole en code.",
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
    admin = _mk_user(db, f"ma-admin-{tag}@example.com", AppRole.admin_tech)
    praticien = _mk_user(db, f"ma-prat-{tag}@example.com", AppRole.practitioner)
    autonome_user = _mk_user(db, f"ma-solo-{tag}@example.com", AppRole.public_client)

    # Client AUTONOME : aucun praticien — l'état central de la décision
    autonome = Client(first_name_or_alias="Client Autonome", app_user_id=autonome_user.id)
    db.add(autonome)
    db.flush()
    db.add(ClientJournalEntry(
        client_id=autonome.id,
        body_text="Deux bonnes nuits cette semaine, enfin. J'écris pour moi.",
    ))
    ids = {
        "admin": admin.id, "praticien": praticien.id,
        "autonome_user": autonome_user.id, "autonome": autonome.id,
    }
    db.commit()
    db.close()

    yield ids

    from app.models.analysis import AnalysisAccessLog

    db = SessionLocal()
    res_ids = [r.id for r in db.query(AnalysisResult).filter_by(client_id=ids["autonome"])]
    if res_ids:
        db.query(AnalysisAccessLog).filter(
            AnalysisAccessLog.analysis_result_id.in_(res_ids)
        ).delete(synchronize_session=False)
        db.query(AnalysisResult).filter(AnalysisResult.id.in_(res_ids)).delete(
            synchronize_session=False
        )
    db.query(ClientPractitionerTransfer).filter_by(client_id=ids["autonome"]).delete()
    db.query(ClientJournalEntry).filter_by(client_id=ids["autonome"]).delete()
    db.query(Client).filter_by(id=ids["autonome"]).delete()
    db.query(AppUser).filter(
        AppUser.id.in_([ids["admin"], ids["praticien"], ids["autonome_user"]])
    ).delete(synchronize_session=False)
    db.commit()
    db.close()


def _auth(user_id: str, role: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


def _mock_claude(monkeypatch, sortie: dict) -> None:
    import app.services.journal_reflection as jr

    async def _fake_call(prompt: str, **kwargs):
        assert "Reflet de journal" in prompt
        return json.dumps(sortie, ensure_ascii=False), {"input_tokens": 10, "output_tokens": 5}

    monkeypatch.setattr(jr, "_call_claude", _fake_call)


def test_reflet_sans_praticien_et_cooldown(ctx, monkeypatch) -> None:
    """Le cœur du mode autonome : un client SANS praticien reçoit son reflet."""
    from app.main import app

    _mock_claude(monkeypatch, REFLET_DOUX)
    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/me/journal/reflet",
            headers=_auth(ctx["autonome_user"], "public_client"),
        )
        assert r.status_code == 201, r.text
        body = r.json()
        assert "apaisement" in body["reflet"]
        assert body["vigilance"]["niveau"] == "aucun"
        assert body["ressources"] is None

        # Cooldown : un second reflet immédiat est refusé avec douceur
        r = http.post(
            "/api/v1/me/journal/reflet",
            headers=_auth(ctx["autonome_user"], "public_client"),
        )
        assert r.status_code == 429, r.text

        # L'historique reste lisible
        r = http.get("/api/v1/me/reflets", headers=_auth(ctx["autonome_user"], "public_client"))
        assert r.status_code == 200 and len(r.json()) == 1


def test_protocole_urgence_applique_en_code(ctx, monkeypatch) -> None:
    """Signal d'urgence : ressources injectées EN CODE, analyse neutralisée."""
    from app.main import app

    _mock_claude(monkeypatch, REFLET_URGENCE)
    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/me/journal/reflet",
            headers=_auth(ctx["autonome_user"], "public_client"),
        )
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["vigilance"]["niveau"] == "urgence"
        # Les ressources sont EXACTEMENT celles du protocole (pas celles du modèle)
        assert body["ressources"] == RESSOURCES_URGENCE
        assert "9-8-8" in body["ressources"]
        # Toute analyse est neutralisée
        assert body["fils"] == []
        assert body["question_ouverte"] == ""
        assert body["piste"] == ""


def test_transfert_praticien_admin(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        # integral SANS consentement → refus
        r = http.post(
            f"/api/v1/admin/accounts/clients/{ctx['autonome']}/praticien",
            json={"praticien_id": ctx["praticien"], "mode": "integral"},
            headers=_auth(ctx["admin"], "admin_tech"),
        )
        assert r.status_code == 400, r.text
        assert "consentement" in r.json()["detail"]

        # resume (défaut) : le client autonome rejoint un praticien
        r = http.post(
            f"/api/v1/admin/accounts/clients/{ctx['autonome']}/praticien",
            json={"praticien_id": ctx["praticien"], "mode": "resume"},
            headers=_auth(ctx["admin"], "admin_tech"),
        )
        assert r.status_code == 200, r.text
        assert r.json()["to_praticien_id"] == ctx["praticien"]

        # retour au mode autonome (praticien_id = null) — un état normal
        r = http.post(
            f"/api/v1/admin/accounts/clients/{ctx['autonome']}/praticien",
            json={"praticien_id": None, "mode": "resume"},
            headers=_auth(ctx["admin"], "admin_tech"),
        )
        assert r.status_code == 200, r.text
        assert r.json()["to_praticien_id"] is None

    # L'audit garde les trois mouvements
    db = SessionLocal()
    n = db.query(ClientPractitionerTransfer).filter_by(client_id=ctx["autonome"]).count()
    db.close()
    assert n == 2  # l'integral refusé n'écrit rien
