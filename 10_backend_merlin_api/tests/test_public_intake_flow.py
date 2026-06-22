from __future__ import annotations

import os
from pathlib import Path

_TEST_DB_PATH = Path("test_public_intake_flow.db").resolve()
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

from fastapi.testclient import TestClient

from app.db.base import init_models

init_models()


def test_public_rendez_vous_intake_accepts_required_consents() -> None:
    from app.main import app

    with TestClient(app) as client:
        client_response = client.post(
            "/api/v1/clients",
            json={
                "first_name_or_alias": "Client pilote",
                "email": "client-pilote@example.com",
                "phone": "5140000000",
                "is_adult_confirmed": True,
            },
        )
        assert client_response.status_code == 201, client_response.text
        client_id = client_response.json()["id"]

        intake_response = client.post(
            "/api/v1/intake-requests",
            json={
                "client_id": client_id,
                "request_channel_code": "web_form",
                "request_for_code": "self",
                "primary_need_code": "support",
                "perceived_urgency_code": "non_urgent",
                "support_already_in_place": False,
                "requested_outcome_text": "Je veux prendre un premier rendez-vous IVIA.",
            },
        )
        assert intake_response.status_code == 201, intake_response.text

        # Doctrine §16 : SEULS 3 consentements sont autorisés en entrée publique.
        public_consent_types = [
            "consent_session",
            "consent_session_note",
            "consent_history",
        ]
        for consent_type in public_consent_types:
            consent_response = client.post(
                "/api/v1/consents",
                json={
                    "client_id": client_id,
                    "consent_type_code": consent_type,
                    "consent_value": True,
                    "granted_by_actor_code": "client",
                },
            )
            assert consent_response.status_code == 201, (
                f"{consent_type} should be accepted in public intake; "
                f"got {consent_response.status_code}: {consent_response.text}"
            )

        # consent_recording / consent_transcription NE doivent PAS être acceptés en public :
        # ils sont captés plus tard, authentifiés, au moment de la séance (doctrine §16).
        for restricted in ("consent_recording", "consent_transcription"):
            resp = client.post(
                "/api/v1/consents",
                json={
                    "client_id": client_id,
                    "consent_type_code": restricted,
                    "consent_value": True,
                    "granted_by_actor_code": "client",
                },
            )
            assert resp.status_code == 401, (
                f"{restricted} ne doit PAS être accepté en entrée publique; got {resp.status_code}: {resp.text}"
            )


def test_public_intake_still_rejects_third_party_transmission_consent() -> None:
    from app.main import app

    with TestClient(app) as client:
        client_response = client.post(
            "/api/v1/clients",
            json={
                "first_name_or_alias": "Client pilote 2",
                "email": "client-pilote-2@example.com",
                "is_adult_confirmed": True,
            },
        )
        assert client_response.status_code == 201, client_response.text
        client_id = client_response.json()["id"]

        consent_response = client.post(
            "/api/v1/consents",
            json={
                "client_id": client_id,
                "consent_type_code": "consent_third_party_transmission",
                "consent_value": True,
                "granted_by_actor_code": "client",
            },
        )
        assert consent_response.status_code == 401
