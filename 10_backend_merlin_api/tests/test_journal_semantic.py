"""Capacité journal_semantic (étape 2 chantier Analyses) — gardes et pipeline.

L'appel Anthropic est MOCKÉ (aucune API réelle) : on teste les verrous
(consentement, assignation, interrupteur LLM), le stockage AnalysisResult,
la propagation de la vigilance et le pare-feu Loi 21.

NB : la fixture autouse ``reset_app_users`` (conftest) vide app_users avant
chaque test — données créées DANS les tests, emails uniques.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_journal_semantic.db").resolve()
if _TEST_DB_PATH.exists():
    _TEST_DB_PATH.unlink()
os.environ["MERLIN_DATABASE_URL"] = f"sqlite:///{_TEST_DB_PATH.as_posix()}"
os.environ["MERLIN_AUTO_CREATE_TABLES"] = "true"
os.environ["MERLIN_INSIGHTS_ENABLED"] = "true"
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
from app.models.client_journal_entry import ClientJournalEntry
from app.models.consent import Consent
from app.models.enums import AppRole, ConsentTypeCode, GrantedByActorCode
from app.models.session import SessionRecord

init_models()

SORTIE_VALIDE = {
    "synthese": "La période montre un mouvement d'apaisement progressif.",
    "fils": [
        {
            "titre": "Sommeil",
            "observation": "Deux nuits complètes rapportées en fin de période.",
            "hypothese": "Le rythme du soir mis en place pourrait y contribuer.",
        }
    ],
    "axes_touches": ["corps"],
    "mouvements_intentions": [
        {"intention": "Retrouver le sommeil", "mouvement": "avance", "indice": "nuits complètes"}
    ],
    "vigilance": {"niveau": "aucun", "raison": None},
    "triade": {
        "observation": "Le journal décrit des nuits en amélioration.",
        "hypothese": "L'accompagnement du rythme du soir semblerait porter.",
        "orientation": "Reprendre en séance ce qui a aidé ces deux nuits.",
    },
}


@pytest.fixture(autouse=True)
def _enable_llm():
    """Active l'interrupteur LLM sur le singleton settings (l'env var posée en tête
    de module est sans effet en CI : settings est déjà construit par un import
    antérieur). Le dataclass est gelé → object.__setattr__ + restauration."""
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
    praticien = _mk_user(db, f"js-praticien-{tag}@example.com", AppRole.practitioner)
    autre = _mk_user(db, f"js-autre-{tag}@example.com", AppRole.practitioner)

    client = Client(first_name_or_alias="Client Journal")
    db.add(client)
    db.flush()

    s1 = SessionRecord(
        client_id=client.id, session_sequence_number=1,
        operator_user_id=praticien.id, praticien_id=praticien.id,
    )
    s2 = SessionRecord(
        client_id=client.id, session_sequence_number=2,
        operator_user_id=praticien.id, praticien_id=praticien.id,
    )
    db.add_all([s1, s2])
    db.flush()
    db.add(ClientJournalEntry(client_id=client.id, body_text="Deux bonnes nuits cette semaine."))
    ids = {"praticien": praticien.id, "autre": autre.id, "client": client.id, "s2": s2.id}
    db.commit()
    db.close()

    yield ids

    # Nettoyage complet (ordre FK) : la fixture autouse reset_app_users ne peut pas
    # supprimer des utilisateurs encore référencés par des séances — on efface donc
    # tout ce qu'on a créé, sinon les tests suivants (bootstrap) trouvent une base sale.
    from app.models.analysis import AnalysisAccessLog, AnalysisResult

    db = SessionLocal()
    res_ids = [
        r.id for r in db.query(AnalysisResult).filter_by(client_id=ids["client"])
    ]
    if res_ids:
        db.query(AnalysisAccessLog).filter(
            AnalysisAccessLog.analysis_result_id.in_(res_ids)
        ).delete(synchronize_session=False)
        db.query(AnalysisResult).filter(AnalysisResult.id.in_(res_ids)).delete(
            synchronize_session=False
        )
    db.query(SessionRecord).filter_by(client_id=ids["client"]).delete()
    db.query(ClientJournalEntry).filter_by(client_id=ids["client"]).delete()
    db.query(Consent).filter_by(client_id=ids["client"]).delete()
    db.query(Client).filter_by(id=ids["client"]).delete()
    db.query(AppUser).filter(
        AppUser.id.in_([ids["praticien"], ids["autre"]])
    ).delete(synchronize_session=False)
    db.commit()
    db.close()


def _grant_consent(client_id: str) -> None:
    db = SessionLocal()
    db.add(
        Consent(
            client_id=client_id,
            consent_type_code=ConsentTypeCode.consent_history,
            consent_value=True,
            granted_by_actor_code=GrantedByActorCode.client,
        )
    )
    db.commit()
    db.close()


def _auth(user_id: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, 'practitioner')}"}


def _mock_claude(monkeypatch, sortie: dict) -> None:
    import app.services.journal_semantic as js

    async def _fake_call(prompt: str):
        assert "PROMPT — Synthèse sémantique du journal" in prompt
        return json.dumps(sortie, ensure_ascii=False), {"input_tokens": 10, "output_tokens": 5}

    monkeypatch.setattr(js, "_call_claude", _fake_call)


def test_journal_synthese_refuse_sans_consentement(ctx, monkeypatch) -> None:
    from app.main import app

    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s2']}/journal-synthese",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 403, r.text
        assert "consent" in r.json()["detail"].lower()


def test_journal_synthese_refuse_praticien_non_assigne(ctx, monkeypatch) -> None:
    from app.main import app

    _grant_consent(ctx["client"])
    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s2']}/journal-synthese",
            headers=_auth(ctx["autre"]),
        )
        assert r.status_code == 403, r.text


def test_journal_synthese_produit_et_stocke(ctx, monkeypatch) -> None:
    from app.main import app

    _grant_consent(ctx["client"])
    _mock_claude(monkeypatch, SORTIE_VALIDE)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s2']}/journal-synthese",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["capability"] == "journal_semantic"
        assert body["sensitivity"] == "hypothese"
        assert body["payload"]["n_entrees"] == 1
        assert body["payload"]["vigilance"]["niveau"] == "aucun"
        assert body["payload"]["triade"]["orientation"]


def test_journal_synthese_bloque_vocabulaire_loi21(ctx, monkeypatch) -> None:
    from app.main import app

    _grant_consent(ctx["client"])
    interdite = dict(SORTIE_VALIDE)
    interdite["synthese"] = "Un vrai travail thérapeutique s'amorce."  # mot interdit
    _mock_claude(monkeypatch, interdite)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s2']}/journal-synthese",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 502, r.text


def test_journal_synthese_propage_vigilance_urgence(ctx, monkeypatch) -> None:
    from app.main import app

    _grant_consent(ctx["client"])
    urgence = json.loads(json.dumps(SORTIE_VALIDE))
    urgence["vigilance"] = {"niveau": "urgence", "raison": "Évocation directe d'en finir."}
    _mock_claude(monkeypatch, urgence)
    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/analysis/sessions/{ctx['s2']}/journal-synthese",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text
        assert r.json()["payload"]["vigilance"]["niveau"] == "urgence"
