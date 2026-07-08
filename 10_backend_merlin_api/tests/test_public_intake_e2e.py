"""E2E happy path du parcours public d'entrée (doctrine CLAUDE.md §16) — item M11.

Rejoue le parcours complet d'une vraie personne :
1. soumission du formulaire /rendez-vous via l'orchestrateur POST /public/intake/start ;
2. réception du magic link (interception du courriel — le lien n'existe qu'en clair là) ;
3. activation POST /public/activate/{token} → JWT ;
4. arrivée dans /mon-espace : GET /clients/me authentifié ;
5. le magic link est à usage unique (2e activation → 404).

Casser l'orchestrateur, l'activation ou la fiche client fait échouer ce test.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

_TEST_DB_PATH = Path("test_public_intake_e2e.db").resolve()
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


def test_e2e_intake_magic_link_activation_mon_espace(monkeypatch) -> None:
    import app.api.routes.public_intake as public_intake
    from app.main import app

    courriel_capture: dict = {}

    async def _send_email_intercepte(
        to_email, subject, html_body, text_body=None, audience="client"
    ) -> bool:
        courriel_capture["to"] = to_email
        courriel_capture["html"] = html_body
        return True

    monkeypatch.setattr(public_intake, "send_email", _send_email_intercepte)

    with TestClient(app) as client:
        # 1. Soumission du formulaire public (un seul appel orchestrateur)
        start = client.post(
            "/api/v1/public/intake/start",
            json={
                "first_name_or_alias": "Client E2E",
                "email": "client-e2e@example.com",
                "is_adult_confirmed": True,
                "consent_terms_accepted": True,
                "requested_outcome_text": "Je veux prendre un premier rendez-vous IVIA.",
            },
        )
        assert start.status_code == 201, start.text
        body = start.json()
        assert body["magic_link_sent"] is True
        assert body["client_id"]
        assert body["intake_request_id"]

        # 2. Le magic link arrive par courriel (intercepté ici)
        assert courriel_capture, "aucun courriel envoyé par l'orchestrateur"
        lien = re.search(r"/activer\?token=([A-Za-z0-9_\-]+)", courriel_capture["html"])
        assert lien, "magic link absent du courriel d'activation"
        token = lien.group(1)

        # 3. Activation : le token ouvre une session (JWT)
        activate = client.post(f"/api/v1/public/activate/{token}")
        assert activate.status_code == 200, activate.text
        jwt = activate.json()["access_token"]
        assert jwt

        # 4. /mon-espace : la fiche client répond, au bon nom
        me = client.get(
            "/api/v1/clients/me",
            headers={"Authorization": f"Bearer {jwt}"},
        )
        assert me.status_code == 200, me.text
        assert me.json()["first_name_or_alias"] == "Client E2E"

        # 5. Le magic link est à usage unique
        rejoue = client.post(f"/api/v1/public/activate/{token}")
        assert rejoue.status_code == 404, (
            f"un magic link consommé doit être invalide; got {rejoue.status_code}: {rejoue.text}"
        )
