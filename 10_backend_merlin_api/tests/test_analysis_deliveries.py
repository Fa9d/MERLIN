"""Restitutions client (étape 4) — validation humaine, gates §8.3, Loi 21.

Vérifie : livraison par le praticien assigné, refus des capacités non
livrables, croisement exigeant recognized_by_order, filtre Loi 21 sur la
triade, lecture client limitée à SON dossier, retrait par le livreur seul.
Fixtures autonettoyantes (ordre FK).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_analysis_deliveries.db").resolve()
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
from app.models.analysis_delivery import AnalysisDelivery
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import AppRole
from app.models.session import SessionRecord

init_models()

TRIADE = {
    "observation": "Ton journal montre deux nuits complètes en fin de semaine.",
    "hypothese": "Le rituel du soir que tu as mis en place pourrait y contribuer.",
    "orientation": "On pourrait regarder ensemble ce qui a rendu ces soirs différents.",
}


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
    praticien = _mk_user(db, f"dl-prat-{tag}@example.com", AppRole.practitioner)
    autre = _mk_user(db, f"dl-autre-{tag}@example.com", AppRole.practitioner)
    client_user = _mk_user(db, f"dl-client-{tag}@example.com", AppRole.public_client)
    db.add(PractitionerCredential(
        practitioner_user_id=praticien.id, order_body="OPQ",
        status=CredentialStatus.verified, recognized_by_order=False,
    ))

    client = Client(first_name_or_alias="Client Repères", app_user_id=client_user.id)
    db.add(client)
    db.flush()
    seance = SessionRecord(
        client_id=client.id, session_sequence_number=1,
        operator_user_id=praticien.id, praticien_id=praticien.id,
    )
    db.add(seance)
    db.flush()

    def _ar(capability, sensitivity):
        r = AnalysisResult(
            capability=capability, sensitivity=sensitivity,
            client_id=client.id, session_id=seance.id,
            payload_json=json.dumps({"synthese": "x"}),
        )
        db.add(r)
        db.flush()
        return r.id

    ids = {
        "praticien": praticien.id, "autre": autre.id, "client_user": client_user.id,
        "client": client.id, "seance": seance.id,
        "ar_journal": _ar("journal_semantic", AnalysisSensitivity.hypothese),
        "ar_prosodie": _ar("prosody_local", AnalysisSensitivity.observation),
        "ar_croisement": _ar("croisement_prosodie_semantique", AnalysisSensitivity.inference_clinique),
    }
    db.commit()
    db.close()

    yield ids

    from app.models.analysis import AnalysisAccessLog

    db = SessionLocal()
    db.query(AnalysisDelivery).filter_by(client_id=ids["client"]).delete()
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
        practitioner_user_id=ids["praticien"]
    ).delete()
    db.query(AppUser).filter(
        AppUser.id.in_([ids["praticien"], ids["autre"], ids["client_user"]])
    ).delete(synchronize_session=False)
    db.commit()
    db.close()


def _auth(user_id: str, role: str = "practitioner") -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


def test_livraison_et_lecture_client(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/analysis/deliveries",
            json={"analysis_result_id": ctx["ar_journal"], **TRIADE},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 201, r.text
        delivery_id = r.json()["id"]

        # Le client voit SON repère
        r = http.get("/api/v1/me/reperes", headers=_auth(ctx["client_user"], "public_client"))
        assert r.status_code == 200 and len(r.json()) == 1
        assert "rituel du soir" in r.json()[0]["hypothese"]

        # Retrait par un AUTRE praticien : refusé
        r = http.delete(
            f"/api/v1/analysis/deliveries/{delivery_id}", headers=_auth(ctx["autre"])
        )
        assert r.status_code == 403, r.text
        # Retrait par le livreur : ok, et le client ne le voit plus
        r = http.delete(
            f"/api/v1/analysis/deliveries/{delivery_id}", headers=_auth(ctx["praticien"])
        )
        assert r.status_code == 204, r.text
        r = http.get("/api/v1/me/reperes", headers=_auth(ctx["client_user"], "public_client"))
        assert r.json() == []


def test_capacite_non_livrable_refusee(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/analysis/deliveries",
            json={"analysis_result_id": ctx["ar_prosodie"], **TRIADE},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 403, r.text
        assert "livrable" in r.json()["detail"]


def test_croisement_exige_recognized_by_order(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        # Credential vérifié mais SANS recognized_by_order → refus
        r = http.post(
            "/api/v1/analysis/deliveries",
            json={"analysis_result_id": ctx["ar_croisement"], **TRIADE},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 403, r.text
        assert "recognized_by_order" in r.json()["detail"]

    # On accorde le droit → livraison possible
    db = SessionLocal()
    cred = db.query(PractitionerCredential).filter_by(
        practitioner_user_id=ctx["praticien"]
    ).first()
    cred.recognized_by_order = True
    db.add(cred)
    db.commit()
    db.close()

    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/analysis/deliveries",
            json={"analysis_result_id": ctx["ar_croisement"], **TRIADE},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 201, r.text


def test_triade_filtree_loi21_et_assignation(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        # Vocabulaire interdit → 400
        mauvaise = dict(TRIADE, hypothese="Cela ressemble à un trouble du sommeil à traiter.")
        r = http.post(
            "/api/v1/analysis/deliveries",
            json={"analysis_result_id": ctx["ar_journal"], **mauvaise},
            headers=_auth(ctx["praticien"]),
        )
        assert r.status_code == 400 and "Loi 21" in r.json()["detail"]

        # Praticien non assigné → 403
        r = http.post(
            "/api/v1/analysis/deliveries",
            json={"analysis_result_id": ctx["ar_journal"], **TRIADE},
            headers=_auth(ctx["autre"]),
        )
        assert r.status_code == 403, r.text
