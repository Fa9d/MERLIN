"""Circuit de relecture de la transcription (praticien reprend la main).

Vérifie : correction (original conservé, statut), validation (horodatée,
signée), figement post-validation, régénération d'analyse conditionnée à la
transcription validée, rédaction de la note interdite après validation,
périmètre praticien (404 hors séance possédée). Génération IA remplacée par un stub.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_transcript_review.db").resolve()
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
from app.models.session_note import SessionNote

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


FAUX_PAYLOAD_IA = {
    "production_note": {
        "summary_text": "Résumé régénéré sur transcription validée.",
        "observations_text": "Observation régénérée.",
    },
    "client_delivery": {"client_facing_summary_text": "Reformulation régénérée."},
    "supervision": {},
    "research": {},
    "metadata": {"model_used": "stub", "prompt_version": "test"},
}


@pytest.fixture()
def ctx(monkeypatch) -> dict:
    from uuid import uuid4

    from app.api.routes import sessions as sessions_module

    async def _faux_generateur(transcript_text, session_context=None):
        return FAUX_PAYLOAD_IA

    monkeypatch.setattr(sessions_module, "generate_session_note_from_transcript", _faux_generateur)
    monkeypatch.setattr(sessions_module.llm_ledger, "record", lambda *a, **k: None)

    tag = uuid4().hex[:8]
    db = SessionLocal()
    praticien = _mk_user(db, f"tr-prat-{tag}@example.com", AppRole.practitioner)
    autre = _mk_user(db, f"tr-autre-{tag}@example.com", AppRole.practitioner)
    client = Client(first_name_or_alias="Client Transcription")
    db.add(client)
    db.flush()
    seance = SessionRecord(
        client_id=client.id,
        session_sequence_number=1,
        operator_user_id=praticien.id,
        praticien_id=praticien.id,
        transcript_text="bonjour je vien vous parler",
    )
    db.add(seance)
    db.flush()
    db.commit()
    data = {"praticien": praticien.id, "autre": autre.id, "client": client.id, "seance": seance.id}
    db.close()
    yield data


def test_correction_conserve_original_et_statut(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.patch(
            f"/api/v1/sessions/{ctx['seance']}/transcript",
            json={"transcript_text": "Bonjour, je viens vous parler."},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text
        s = r.json()
        assert s["transcript_status"] == "corrected"
        assert s["transcript_text"] == "Bonjour, je viens vous parler."
        assert s["transcript_original_text"] == "bonjour je vien vous parler"

        # Deuxième correction : l'original machine reste le premier texte.
        r = http.patch(
            f"/api/v1/sessions/{ctx['seance']}/transcript",
            json={"transcript_text": "Bonjour, je viens vous parler aujourd'hui."},
            headers=_auth(ctx["praticien"]),
        )
        assert r.json()["transcript_original_text"] == "bonjour je vien vous parler"


def test_hors_perimetre_404(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.patch(
            f"/api/v1/sessions/{ctx['seance']}/transcript",
            json={"transcript_text": "intrusion"},
            headers=_auth(ctx["autre"]),
        )
        assert r.status_code == 404, r.text


def test_validation_puis_figement(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/sessions/{ctx['seance']}/transcript/validate",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text
        s = r.json()
        assert s["transcript_status"] == "validated"
        assert s["transcript_validated_at"] is not None
        assert s["transcript_validated_by_user_id"] == ctx["praticien"]

        # Corriger après validation : figé.
        r = http.patch(
            f"/api/v1/sessions/{ctx['seance']}/transcript",
            json={"transcript_text": "trop tard"},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 409, r.text


def test_regeneration_exige_transcription_validee(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.post(
            f"/api/v1/sessions/{ctx['seance']}/regenerate-note",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 409, r.text
        assert "Validez d'abord" in r.json()["detail"]

        http.post(f"/api/v1/sessions/{ctx['seance']}/transcript/validate", headers=_auth(ctx["praticien"]))
        r = http.post(
            f"/api/v1/sessions/{ctx['seance']}/regenerate-note",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text
        res = r.json()
        assert res["generated_note"]["summary_text"] == "Résumé régénéré sur transcription validée."
        assert res["generated_note"]["validated_by_practitioner"] is False


def test_note_redigeable_puis_figee(ctx) -> None:
    from app.main import app

    db = SessionLocal()
    note = SessionNote(
        session_id=ctx["seance"], client_id=ctx["client"],
        note_sequence_number=1, summary_text="Brouillon initial.",
    )
    db.add(note)
    db.commit()
    note_id = note.id
    db.close()

    with HttpClient(app) as http:
        r = http.patch(
            f"/api/v1/session-notes/{note_id}",
            json={"summary_text": "Résumé réécrit par le praticien.", "observations_text": "Mon observation."},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text
        assert r.json()["summary_text"] == "Résumé réécrit par le praticien."

        r = http.patch(
            f"/api/v1/session-notes/{note_id}/validate",
            json={"validated": True},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 200, r.text

        # Note validée = figée.
        r = http.patch(
            f"/api/v1/session-notes/{note_id}",
            json={"summary_text": "trop tard"},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 409, r.text

        # Et la régénération refuse d'écraser une lecture validée.
        http.post(f"/api/v1/sessions/{ctx['seance']}/transcript/validate", headers=_auth(ctx["praticien"]))
        r = http.post(
            f"/api/v1/sessions/{ctx['seance']}/regenerate-note",
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 409, r.text
