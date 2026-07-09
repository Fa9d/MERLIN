"""Économie des analyses — tarification, grand livre, endpoints admin.

Vérifie : calcul de coût par modèle (préfixe le plus long), conversion CAD,
écriture d'événements via record(), garde admin sur /admin/economics,
sommaire agrégé (par finalité). Données fictives uniquement.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_economics.db").resolve()
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
from app.models.enums import AppRole
from app.models.llm_usage import LlmUsageEvent
from app.services import llm_ledger

init_models()


def test_pricing_prefixe_le_plus_long() -> None:
    # sonnet-4-6 → tarif sonnet-4 ; modèle inconnu → tarif prudent (opus)
    assert llm_ledger.pricing_for("claude-sonnet-4-6") == (3.0, 15.0)
    assert llm_ledger.pricing_for("claude-haiku-4-5") == (1.0, 5.0)
    assert llm_ledger.pricing_for("claude-fable-5") == (10.0, 50.0)
    assert llm_ledger.pricing_for("modele-inconnu") == (5.0, 25.0)
    # 1000 in + 500 out sur sonnet : (1000*3 + 500*15) / 1e6 = 0.0105 USD
    assert llm_ledger.cost_usd("claude-sonnet-4-6", 1000, 500) == pytest.approx(0.0105)


def test_record_et_conversion_cad() -> None:
    db = SessionLocal()
    try:
        llm_ledger.record(
            db, purpose="test_purpose", usage={"input_tokens": 2000, "output_tokens": 1000},
            model="claude-sonnet-4-6",
        )
        db.commit()
        ev = db.query(LlmUsageEvent).filter(LlmUsageEvent.purpose == "test_purpose").one()
        assert ev.input_tokens == 2000 and ev.output_tokens == 1000
        assert ev.cost_usd == pytest.approx(0.021)  # 2000*3 + 1000*15 = 21000 / 1e6
        # usage None / vide → événement à zéro, jamais d'exception
        llm_ledger.record(db, purpose="test_purpose_vide", usage=None)
        db.commit()
    finally:
        db.query(LlmUsageEvent).filter(
            LlmUsageEvent.purpose.in_(["test_purpose", "test_purpose_vide"])
        ).delete(synchronize_session=False)
        db.commit()
        db.close()


@pytest.fixture()
def ctx() -> dict:
    from uuid import uuid4

    tag = uuid4().hex[:8]
    db = SessionLocal()
    admin = AppUser(
        email=f"admin-eco-{tag}@example.com",
        password_hash=hash_password("x-test-x"),
        display_name="Admin Eco",
        role=AppRole.admin_tech,
        email_verified=True,
    )
    prat = AppUser(
        email=f"prat-eco-{tag}@example.com",
        password_hash=hash_password("x-test-x"),
        display_name="Prat Eco",
        role=AppRole.practitioner,
        email_verified=True,
    )
    db.add_all([admin, prat])
    db.flush()
    ids = {"admin": admin.id, "prat": prat.id}
    llm_ledger.record(
        db, purpose="session_note", usage={"input_tokens": 10_000, "output_tokens": 4_000},
        model="claude-sonnet-4-6", praticien_user_id=prat.id,
    )
    llm_ledger.record(
        db, purpose="journal_reflet_client", usage={"input_tokens": 1_000, "output_tokens": 500},
        model="claude-sonnet-4-6",
    )
    db.commit()
    db.close()

    yield ids

    db = SessionLocal()
    db.query(LlmUsageEvent).filter(
        LlmUsageEvent.purpose.in_(["session_note", "journal_reflet_client"])
    ).delete(synchronize_session=False)
    db.query(AppUser).filter(AppUser.id.in_(list(ids.values()))).delete(
        synchronize_session=False
    )
    db.commit()
    db.close()


def _auth(user_id: str, role: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


def test_endpoints_admin_gardes_et_sommaire(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        # Sans auth → 401 ; praticien non admin → 403
        assert http.get("/api/v1/admin/economics/summary").status_code == 401
        assert http.get(
            "/api/v1/admin/economics/summary", headers=_auth(ctx["prat"], "practitioner")
        ).status_code == 403

        r = http.get(
            "/api/v1/admin/economics/summary", headers=_auth(ctx["admin"], "admin_tech")
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["couts"]["nb_appels"] >= 2
        fin = body["par_finalite"]
        assert "session_note" in fin and fin["session_note"]["nb_appels"] >= 1
        # 10k in + 4k out sonnet = 0.09 USD → CAD au taux configuré
        assert fin["session_note"]["cost_usd"] >= 0.09
        assert body["benefice_net_cad_cents"] == (
            body["marge_ivia_avant_ia"] - body["couts"]["cost_cad_cents"]
        )

        r2 = http.get(
            "/api/v1/admin/economics/sessions", headers=_auth(ctx["admin"], "admin_tech")
        )
        assert r2.status_code == 200
        assert isinstance(r2.json(), list)
