"""Croisement prosodie × sémantique (étape 3b) — verrou credential et pipeline.

Vérifie : refus sans credential vérifié (403), refus si l'une des deux
lectures manque (409), production et stockage en inference_clinique,
rejet d'une sortie sans double ancrage. LLM mocké ; fixtures autonettoyantes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_croisement.db").resolve()
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
from app.models.analysis import (
    AnalysisResult,
    AnalysisSensitivity,
    CredentialStatus,
    PractitionerCredential,
)
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import AppRole
from app.models.session import SessionRecord

init_models()

SORTIE_VALIDE = {
    "registre_vocal": "Voix posée en ouverture, qui se resserre au milieu de la séance.",
    "croisements": [
        {
            "type": "divergence",
            "prosodie": "chute d'énergie et débit ralenti sur le dernier tiers",
            "semantique": "thème « décision apaisée » (verbatim : je vais dire non)",
            "inference": "L'apaisement dit pourrait coexister avec un coût énergétique réel.",
            "attention": "Observer comment le corps porte cette décision en présence.",
        }
    ],
    "synthese": "Le croisement suggérerait une décision sincère mais coûteuse — à accueillir sans presser.",
    "limites": "Ces mesures ne détectent ni mensonge ni état interne ; la fatigue ou la pudeur produisent les mêmes signatures.",
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
    verifie = _mk_user(db, f"cr-verifie-{tag}@example.com", AppRole.practitioner)
    simple = _mk_user(db, f"cr-simple-{tag}@example.com", AppRole.practitioner)
    db.add(
        PractitionerCredential(
            practitioner_user_id=verifie.id,
            order_body="OPQ",
            status=CredentialStatus.verified,
        )
    )

    client = Client(first_name_or_alias="Client Croisement")
    db.add(client)
    db.flush()
    complete = SessionRecord(
        client_id=client.id, session_sequence_number=1,
        operator_user_id=verifie.id, praticien_id=verifie.id,
    )
    sans_analyses = SessionRecord(
        client_id=client.id, session_sequence_number=2,
        operator_user_id=verifie.id, praticien_id=verifie.id,
    )
    seance_simple = SessionRecord(
        client_id=client.id, session_sequence_number=3,
        operator_user_id=simple.id, praticien_id=simple.id,
    )
    db.add_all([complete, sans_analyses, seance_simple])
    db.flush()
    # Les deux lectures préalables de la séance complète
    db.add(AnalysisResult(
        capability="prosody_local", sensitivity=AnalysisSensitivity.observation,
        client_id=client.id, session_id=complete.id,
        payload_json=json.dumps({"duree_s": 1800, "f0_moyenne": 180, "debit": 3.1}),
    ))
    db.add(AnalysisResult(
        capability="semantic_llm", sensitivity=AnalysisSensitivity.hypothese,
        client_id=client.id, session_id=complete.id,
        payload_json=json.dumps({"synthese": "Décision apaisée.", "themes": []}),
    ))
    ids = {
        "verifie": verifie.id, "simple": simple.id, "client": client.id,
        "complete": complete.id, "sans": sans_analyses.id, "s_simple": seance_simple.id,
    }
    db.commit()
    db.close()

    yield ids

    from app.models.analysis import AnalysisAccessLog

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
    db.query(PractitionerCredential).filter_by(
        practitioner_user_id=ids["verifie"]
    ).delete()
    db.query(AppUser).filter(
        AppUser.id.in_([ids["verifie"], ids["simple"]])
    ).delete(synchronize_session=False)
    db.commit()
    db.close()


def _auth(user_id: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, 'practitioner')}"}


def _mock_claude(monkeypatch, sortie: dict) -> None:
    import app.services.croisement as cr

    async def _fake_call(prompt: str):
        assert "Croisement prosodie" in prompt
        return json.dumps(sortie, ensure_ascii=False), {"input_tokens": 10, "output_tokens": 5}

    monkeypatch.setattr(cr, "_call_claude", _fake_call)


def test_croisement_refuse_sans_credential(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s_simple']}/croisement",
            headers=_auth(ctx["simple"]),
        )
        assert r.status_code == 403, r.text
        assert "reconnaissance professionnelle" in r.json()["detail"]


def test_croisement_refuse_si_lecture_manquante(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['sans']}/croisement",
            headers=_auth(ctx["verifie"]),
        )
        assert r.status_code == 409, r.text


def test_croisement_produit_en_inference_clinique(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['complete']}/croisement",
            headers=_auth(ctx["verifie"]),
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["capability"] == "croisement_prosodie_semantique"
        assert body["sensitivity"] == "inference_clinique"
        assert body["payload"]["limites"]
        assert body["payload"]["croisements"][0]["type"] == "divergence"


def test_croisement_rejette_sortie_sans_double_ancrage(ctx, monkeypatch) -> None:
    from app.main import app

    invalide = json.loads(json.dumps(SORTIE_VALIDE))
    invalide["croisements"][0]["prosodie"] = ""  # ancrage prosodique manquant
    _mock_claude(monkeypatch, invalide)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['complete']}/croisement",
            headers=_auth(ctx["verifie"]),
        )
        assert r.status_code == 409, r.text
        assert "double ancrage" in r.json()["detail"]
