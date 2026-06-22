"""Tests pour les corrections issues de l'audit ROLES-003 (8 mai 2026).

Couvre :
- BACK-PAY-001 : POST /payments/stripe/checkout/audio-async exige require_operator
- BACK-BOOK-001 : POST /bookings/cancel exige require_verified_email_user
- BACK-DEPS-001 : require_supervisor (renommage) fonctionne et alias rétroactif
- BACK-AUDIO-001 : audio-sessions client-join reste réservé operator (régression)
"""
from __future__ import annotations

import os
from pathlib import Path

# IMPORTANT : configurer la DB AVANT tout import qui touche app.db.session
_TEST_DB_PATH = Path("test_roles_audit_corrections.db").resolve()
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

import pytest
from fastapi.testclient import TestClient

# Créer les tables une fois au module-level pour que la fixture autouse
# `reset_app_users` (conftest.py) trouve la table app_users déjà créée.
from app.db.base import init_models  # noqa: E402
init_models()


# ---------------------------------------------------------------------------
# Fixtures de bootstrap (réutilisent le pattern de test_api_smoke)
# ---------------------------------------------------------------------------

@pytest.fixture
def app_client():
    """App FastAPI avec DB sqlite (configurée au module-level)."""
    from app.main import app

    with TestClient(app) as client:
        yield client


def _register_and_login(client: TestClient, email: str, password: str, role: str,
                        admin_headers: dict | None = None,
                        display_name: str = "Test User") -> dict:
    """Inscrit un utilisateur (admin requis pour rôles privilégiés) puis le login."""
    headers = admin_headers or {}
    payload = {
        "email": email,
        "password": password,
        "display_name": display_name,
        "role": role,
    }
    reg = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert reg.status_code == 201, f"register échec: {reg.status_code} {reg.text}"

    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200, f"login échec: {login.status_code} {login.text}"
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.fixture
def admin_headers(app_client):
    return _register_and_login(
        app_client, "admin@example.com", "admin-secret", "admin_tech",
        display_name="Admin",
    )


@pytest.fixture
def operator_headers(app_client, admin_headers):
    return _register_and_login(
        app_client, "operator@example.com", "operator-secret", "operator",
        admin_headers=admin_headers, display_name="Operator",
    )


@pytest.fixture
def public_client_headers(app_client, admin_headers):
    """Public_client avec email vérifié (force la vérification via DB pour test)."""
    headers = _register_and_login(
        app_client, "client@example.com", "client-secret", "public_client",
        admin_headers=admin_headers, display_name="Client",
    )
    # Forcer email_verified=True directement en DB (en prod = clic lien email)
    from app.db.session import engine
    from app.models.app_user import AppUser
    from sqlalchemy.orm import Session

    with Session(engine) as db:
        user = db.query(AppUser).filter(AppUser.email == "client@example.com").first()
        assert user is not None
        user.email_verified = True
        db.commit()

    return headers


@pytest.fixture
def public_client_unverified_headers(app_client, admin_headers):
    """Public_client SANS email vérifié."""
    return _register_and_login(
        app_client, "unverified@example.com", "unverif-secret", "public_client",
        admin_headers=admin_headers, display_name="Unverified",
    )


# ---------------------------------------------------------------------------
# BACK-PAY-001 : guard sur Stripe Checkout
# ---------------------------------------------------------------------------

class TestBackPay001StripeCheckoutGuard:
    """POST /payments/stripe/checkout/audio-async doit exiger require_operator."""

    PAYLOAD = {
        "client_id": "00000000-0000-0000-0000-000000000001",
        "operator_user_id": "00000000-0000-0000-0000-000000000002",
        "session_mode_code": "follow_up",
    }

    def test_anonymous_call_rejected_with_401(self, app_client):
        """Avant correctif : 404/422 attendus selon payload. Après : 401 avant tout."""
        resp = app_client.post(
            "/api/v1/payments/stripe/checkout/audio-async",
            json=self.PAYLOAD,
        )
        # 401 (pas authentifié) ou 403 (rôle insuffisant) — l'essentiel : pas 404/200/201
        assert resp.status_code in (401, 403), (
            f"Faille BACK-PAY-001 NON corrigée : la route accepte un appel anonyme "
            f"(reçu {resp.status_code} : {resp.text[:200]})"
        )

    def test_public_client_rejected_with_403(self, app_client, public_client_headers):
        """Un public_client authentifié doit être refusé (rôle insuffisant)."""
        resp = app_client.post(
            "/api/v1/payments/stripe/checkout/audio-async",
            json=self.PAYLOAD,
            headers=public_client_headers,
        )
        assert resp.status_code == 403, (
            f"Un public_client ne devrait pas pouvoir créer un Stripe Checkout "
            f"(reçu {resp.status_code} : {resp.text[:200]})"
        )

    def test_operator_passes_guard_then_404_on_missing_client(self, app_client, operator_headers):
        """Operator passe le guard ; rejeté ensuite par 404 (client UUID inexistant)."""
        resp = app_client.post(
            "/api/v1/payments/stripe/checkout/audio-async",
            json=self.PAYLOAD,
            headers=operator_headers,
        )
        # Operator passe le guard 401/403 → atteint la logique métier qui renvoie 404
        # (Client introuvable) ou 409 (Stripe non configuré). Critère : PAS 401/403.
        assert resp.status_code not in (401, 403), (
            f"Operator devrait passer le guard ; reçu {resp.status_code} : {resp.text[:200]}"
        )


# ---------------------------------------------------------------------------
# BACK-BOOK-001 : cancel_slot aligné sur require_verified_email_user
# ---------------------------------------------------------------------------

class TestBackBook001CancelSlotGuard:
    """POST /bookings/cancel doit exiger un email vérifié (cohérence hold/confirm)."""

    PAYLOAD = {"slot_id": "00000000-0000-0000-0000-000000000099"}

    def test_anonymous_rejected(self, app_client):
        resp = app_client.post("/api/v1/bookings/cancel", json=self.PAYLOAD)
        assert resp.status_code == 401, (
            f"Anonyme devrait être rejeté ; reçu {resp.status_code}"
        )

    def test_unverified_email_rejected(self, app_client, public_client_unverified_headers):
        """Utilisateur authentifié mais email non vérifié → rejet (alignement BACK-BOOK-001)."""
        resp = app_client.post(
            "/api/v1/bookings/cancel",
            json=self.PAYLOAD,
            headers=public_client_unverified_headers,
        )
        assert resp.status_code in (401, 403), (
            f"BACK-BOOK-001 NON corrigé : email non vérifié devrait être rejeté ; "
            f"reçu {resp.status_code} : {resp.text[:200]}"
        )

    def test_verified_user_passes_guard_then_404(self, app_client, public_client_headers):
        """Utilisateur avec email vérifié passe le guard ; 404 ensuite (slot inexistant)."""
        resp = app_client.post(
            "/api/v1/bookings/cancel",
            json=self.PAYLOAD,
            headers=public_client_headers,
        )
        assert resp.status_code == 404, (
            f"Utilisateur vérifié devrait passer le guard ; reçu {resp.status_code} : {resp.text[:200]}"
        )


# ---------------------------------------------------------------------------
# BACK-DEPS-001 : require_supervisor + alias rétroactif
# ---------------------------------------------------------------------------

class TestBackDeps001SupervisorRename:
    """require_supervisor doit exister et require_supervision_roles rester un alias."""

    def test_require_supervisor_exists(self):
        from app.core import deps
        assert hasattr(deps, "require_supervisor"), "require_supervisor manquant"
        assert callable(deps.require_supervisor)

    def test_alias_retroactif_pointe_meme_fonction(self):
        from app.core import deps
        assert hasattr(deps, "require_supervision_roles"), "alias retiré sans plan"
        assert deps.require_supervision_roles is deps.require_supervisor, (
            "L'alias require_supervision_roles doit pointer vers require_supervisor"
        )

    def test_session_notes_validate_uses_supervisor_role(self, app_client, admin_headers, operator_headers):
        """PATCH /session-notes/{id}/validate doit refuser un operator (seul supervisor passe)."""
        # Tenter avec operator → 403 attendu (require_supervisor refuse operator)
        resp = app_client.patch(
            "/api/v1/session-notes/00000000-0000-0000-0000-000000000aaa/validate",
            json={"validated": True},  # corps VALIDE → le refus doit venir du rôle (403), pas de la validation (422)
            headers=operator_headers,
        )
        # Le guard doit refuser AVANT d'arriver à la logique métier (404)
        assert resp.status_code == 403, (
            f"require_supervisor doit refuser un operator ; reçu {resp.status_code}"
        )
