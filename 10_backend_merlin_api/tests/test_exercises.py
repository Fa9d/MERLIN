"""Exercices — catalogue, proposition, cheminement client, gardes.

Vérifie : bornes + filtre Loi 21 sur le catalogue (admin), proposition limitée
au praticien assigné, cheminement client (statut + note) limité à SON dossier.
Fixtures autonettoyantes (ordre FK).
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

_TEST_DB_PATH = Path("test_exercises.db").resolve()
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
from app.models.exercise import ClientExercise, Exercise
from app.models.session import SessionRecord

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


@pytest.fixture()
def ctx() -> dict:
    from uuid import uuid4

    tag = uuid4().hex[:8]
    db = SessionLocal()
    admin = _mk_user(db, f"ex-admin-{tag}@example.com", AppRole.admin_tech)
    praticien = _mk_user(db, f"ex-prat-{tag}@example.com", AppRole.practitioner)
    autre = _mk_user(db, f"ex-autre-{tag}@example.com", AppRole.practitioner)
    client_user = _mk_user(db, f"ex-client-{tag}@example.com", AppRole.public_client)

    client = Client(first_name_or_alias="Client Exercices", app_user_id=client_user.id)
    db.add(client)
    db.flush()
    seance = SessionRecord(
        client_id=client.id, session_sequence_number=1,
        operator_user_id=praticien.id, praticien_id=praticien.id,
    )
    exercice = Exercise(
        code=f"ex_{tag}",
        title="Respiration test",
        instructions="Respire calmement pendant trois minutes, sans te juger.",
        dimension="corps",
    )
    db.add_all([seance, exercice])
    db.flush()
    ids = {
        "admin": admin.id, "praticien": praticien.id, "autre": autre.id,
        "client_user": client_user.id, "client": client.id,
        "seance": seance.id, "exercice": exercice.id, "tag": tag,
    }
    db.commit()
    db.close()

    yield ids

    db = SessionLocal()
    db.query(ClientExercise).filter_by(client_id=ids["client"]).delete()
    db.query(SessionRecord).filter_by(client_id=ids["client"]).delete()
    db.query(Client).filter_by(id=ids["client"]).delete()
    db.query(Exercise).filter(Exercise.code.like(f"ex_{ids['tag']}%")).delete(
        synchronize_session=False
    )
    db.query(AppUser).filter(
        AppUser.id.in_([ids["admin"], ids["praticien"], ids["autre"], ids["client_user"]])
    ).delete(synchronize_session=False)
    db.commit()
    db.close()


def _auth(user_id: str, role: str) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


def test_catalogue_admin_refuse_vocabulaire_interdit(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/admin/exercises",
            json={
                "code": f"ex_{ctx['tag']}_bad",
                "title": "Exercice de thérapie",  # mot interdit Loi 21
                "instructions": "Consignes suffisamment longues pour la borne.",
            },
            headers=_auth(ctx["admin"], "admin_tech"),
        )
        assert r.status_code == 400, r.text
        assert "Loi 21" in r.json()["detail"]


def test_proposition_limitee_au_praticien_assigne(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        r = http.post(
            "/api/v1/exercises/propose",
            json={"session_id": ctx["seance"], "exercise_id": ctx["exercice"]},
            headers=_auth(ctx["autre"], "practitioner"),
        )
        assert r.status_code == 403, r.text


def test_cycle_complet_proposition_et_cheminement(ctx) -> None:
    from app.main import app

    with HttpClient(app) as http:
        # Le praticien assigné propose, avec un mot d'accompagnement
        r = http.post(
            "/api/v1/exercises/propose",
            json={
                "session_id": ctx["seance"],
                "exercise_id": ctx["exercice"],
                "message": "À ton rythme cette semaine.",
            },
            headers=_auth(ctx["praticien"], "practitioner"),
        )
        assert r.status_code == 201, r.text
        ce_id = r.json()["id"]
        assert r.json()["status"] == "propose"

        # Le client voit sa proposition
        r = http.get("/api/v1/me/exercises", headers=_auth(ctx["client_user"], "public_client"))
        assert r.status_code == 200, r.text
        assert len(r.json()) == 1
        assert r.json()[0]["exercise"]["title"] == "Respiration test"

        # Il chemine : en cours, puis terminé avec une note
        r = http.patch(
            f"/api/v1/me/exercises/{ce_id}",
            json={"status": "en_cours"},
            headers=_auth(ctx["client_user"], "public_client"),
        )
        assert r.status_code == 200 and r.json()["done_at"] is None
        r = http.patch(
            f"/api/v1/me/exercises/{ce_id}",
            json={"status": "termine", "client_note": "Trois soirs sur sept — ça aide."},
            headers=_auth(ctx["client_user"], "public_client"),
        )
        assert r.status_code == 200, r.text
        assert r.json()["done_at"] is not None

        # Le praticien assigné suit le cheminement
        r = http.get(
            f"/api/v1/exercises/session/{ctx['seance']}",
            headers=_auth(ctx["praticien"], "practitioner"),
        )
        assert r.status_code == 200 and r.json()[0]["status"] == "termine"


def test_client_ne_touche_pas_au_dossier_d_autrui(ctx) -> None:
    from app.main import app
    from uuid import uuid4

    # Un second client avec sa propre proposition
    db = SessionLocal()
    tag2 = uuid4().hex[:8]
    autre_user = _mk_user(db, f"ex-c2-{tag2}@example.com", AppRole.public_client)
    autre_client = Client(first_name_or_alias="Autre", app_user_id=autre_user.id)
    db.add(autre_client)
    db.flush()
    ce = ClientExercise(client_id=autre_client.id, exercise_id=ctx["exercice"])
    db.add(ce)
    db.commit()
    ce_id, autre_user_id, autre_client_id = ce.id, autre_user.id, autre_client.id
    db.close()

    try:
        with HttpClient(app) as http:
            r = http.patch(
                f"/api/v1/me/exercises/{ce_id}",
                json={"status": "termine"},
                headers=_auth(ctx["client_user"], "public_client"),
            )
            assert r.status_code == 404, r.text  # pas 403 : on ne révèle pas l'existence
    finally:
        db = SessionLocal()
        db.query(ClientExercise).filter_by(id=ce_id).delete()
        db.query(Client).filter_by(id=autre_client_id).delete()
        db.query(AppUser).filter_by(id=autre_user_id).delete()
        db.commit()
        db.close()
