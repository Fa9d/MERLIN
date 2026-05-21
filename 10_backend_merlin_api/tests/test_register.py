from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

_TEST_DB_PATH = Path("test_register.db").resolve()
if _TEST_DB_PATH.exists():
    _TEST_DB_PATH.unlink()
os.environ["MERLIN_DATABASE_URL"] = f"sqlite:///{_TEST_DB_PATH.as_posix()}"
os.environ["MERLIN_AUTO_CREATE_TABLES"] = "true"

from app.db.base import init_models

init_models()


def test_register_client_returns_email_failure_state() -> None:
    from app.main import app
    from app.api.routes import register as register_routes

    original_send_email = register_routes.send_email
    register_routes.send_email = AsyncMock(return_value=False)

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/register/client",
                json={
                    "email": "testclient01@fa9.quebec",
                    "password": "TestMerlin1",
                    "display_name": "ClientTest",
                },
            )

        assert response.status_code == 201, response.text
        payload = response.json()
        assert payload["email"] == "testclient01@fa9.quebec"
        assert payload["email_sent"] is False
        assert "a échoué temporairement" in payload["message"]
    finally:
        register_routes.send_email = original_send_email
