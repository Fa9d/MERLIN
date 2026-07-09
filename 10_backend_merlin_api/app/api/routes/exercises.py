"""Exercices — catalogue (admin), proposition (praticien), cheminement (client).

Trois surfaces, trois niveaux d'accès :
- ``/admin/exercises``       [require_admin]  : CRUD du catalogue (Atelier des lectures).
- ``/exercises``             [praticien/op]   : lire le catalogue actif, proposer à un
  client de SA séance, suivre les propositions de ses clients.
- ``/me/exercises``          [client]         : voir ses exercices, avancer son statut,
  déposer une note de vécu.

Posture : un exercice est une INVITATION, jamais une prescription. Le client
avance à son rythme ; « abandonné » est un choix respecté. Les consignes du
catalogue sont rédigées par des humains dans le vocabulaire autorisé (Loi 21).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_user,
    is_admin,
    require_admin,
    require_practitioner_or_operator,
)
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import ExerciseStatusCode, RecordStatus
from app.models.exercise import ClientExercise, Exercise
from app.models.session import SessionRecord
from app.schemas.common import MerlinSchema
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.exercises")

router = APIRouter(tags=["exercices"])


# ── Schémas ───────────────────────────────────────────────────────────────────


class ExerciseRead(MerlinSchema):
    id: str
    code: str
    title: str
    instructions: str
    dimension: str | None
    active: bool


class ExerciseCreate(MerlinSchema):
    code: str
    title: str
    instructions: str
    dimension: str | None = None


class ExercisePatch(MerlinSchema):
    title: str | None = None
    instructions: str | None = None
    dimension: str | None = None
    active: bool | None = None


class ClientExerciseRead(MerlinSchema):
    id: str
    exercise: ExerciseRead
    session_id: str | None
    message: str | None
    status: ExerciseStatusCode
    client_note: str | None
    proposed_at: datetime
    done_at: datetime | None


class ProposeExercise(MerlinSchema):
    session_id: str
    exercise_id: str
    message: str | None = None


class MyExercisePatch(MerlinSchema):
    status: ExerciseStatusCode | None = None
    client_note: str | None = None


def _ce_read(ce: ClientExercise, ex: Exercise) -> ClientExerciseRead:
    return ClientExerciseRead(
        id=ce.id,
        exercise=ExerciseRead.model_validate(ex),
        session_id=ce.session_id,
        message=ce.message,
        status=ce.status,
        client_note=ce.client_note,
        proposed_at=ce.proposed_at,
        done_at=ce.done_at,
    )


def _validate_dimension(dimension: str | None) -> None:
    if dimension is not None and len(dimension) > 32:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Axe invalide (max 32 caractères).")


def _validate_exercise_text(title: str, instructions: str, message: str | None = None) -> None:
    """Bornes + vocabulaire Loi 21 sur tout texte destiné au client."""
    if not (1 <= len(title.strip()) <= 160):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Titre invalide (1 à 160 caractères).")
    if not (10 <= len(instructions.strip()) <= 2000):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Consignes invalides (10 à 2000 caractères)."
        )
    if message is not None and len(message) > 500:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Message trop long (max 500).")
    try:
        assert_client_safe(title)
        assert_client_safe(instructions)
        if message:
            assert_client_safe(message)
    except Loi21ViolationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Vocabulaire non conforme (Loi 21) : {exc}",
        ) from exc


# ── Catalogue (admin) ─────────────────────────────────────────────────────────


@router.get("/admin/exercises", response_model=list[ExerciseRead])
def admin_list_exercises(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> list[Exercise]:
    return list(db.execute(select(Exercise).order_by(Exercise.code)).scalars())


@router.post("/admin/exercises", response_model=ExerciseRead, status_code=status.HTTP_201_CREATED)
def admin_create_exercise(
    payload: ExerciseCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> Exercise:
    code = payload.code.strip().lower()
    if not code.isidentifier() or not (2 <= len(code) <= 48):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Code invalide (slug de 2 à 48 caractères, ex. respiration_ancrage).",
        )
    if db.scalar(select(Exercise).where(Exercise.code == code)) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, f"L'exercice '{code}' existe déjà.")
    _validate_exercise_text(payload.title, payload.instructions)
    _validate_dimension(payload.dimension)
    ex = Exercise(
        code=code,
        title=payload.title.strip(),
        instructions=payload.instructions.strip(),
        dimension=payload.dimension,
    )
    db.add(ex)
    db.commit()
    db.refresh(ex)
    return ex


@router.patch("/admin/exercises/{exercise_id}", response_model=ExerciseRead)
def admin_patch_exercise(
    exercise_id: str,
    payload: ExercisePatch,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> Exercise:
    ex = db.get(Exercise, exercise_id)
    if ex is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Exercice introuvable.")
    _validate_exercise_text(
        payload.title if payload.title is not None else ex.title,
        payload.instructions if payload.instructions is not None else ex.instructions,
    )
    _validate_dimension(payload.dimension)
    if payload.title is not None:
        ex.title = payload.title.strip()
    if payload.instructions is not None:
        ex.instructions = payload.instructions.strip()
    if payload.dimension is not None:
        ex.dimension = payload.dimension
    if payload.active is not None:
        ex.active = payload.active
    db.add(ex)
    db.commit()
    db.refresh(ex)
    return ex


# ── Praticien : catalogue actif + proposition + suivi ─────────────────────────


@router.get("/exercises", response_model=list[ExerciseRead])
def list_active_exercises(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_practitioner_or_operator()),
) -> list[Exercise]:
    return list(
        db.execute(
            select(Exercise).where(Exercise.active.is_(True)).order_by(Exercise.code)
        ).scalars()
    )


@router.post("/exercises/propose", response_model=ClientExerciseRead, status_code=status.HTTP_201_CREATED)
def propose_exercise(
    payload: ProposeExercise,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> ClientExerciseRead:
    record = db.get(SessionRecord, payload.session_id)
    if record is None or record.record_status != RecordStatus.active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Séance introuvable.")
    # Modele IVIA reel : clients + praticiens choisis + admin. Aucun role
    # intermediaire (operateur = vestige) ne contourne l'assignation.
    if not is_admin(current_user) and record.praticien_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Cette séance n'est pas assignée à ce praticien."
        )
    ex = db.get(Exercise, payload.exercise_id)
    if ex is None or not ex.active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Exercice introuvable ou inactif.")
    if payload.message:
        _validate_exercise_text(ex.title, ex.instructions, payload.message)

    ce = ClientExercise(
        client_id=record.client_id,
        exercise_id=ex.id,
        session_id=record.id,
        assigned_by_user_id=current_user.id,
        message=(payload.message or "").strip() or None,
    )
    db.add(ce)
    db.commit()
    db.refresh(ce)
    logger.info("Exercice %s propose (seance %s, par %s).", ex.code, record.id, current_user.id)
    return _ce_read(ce, ex)


@router.get("/exercises/session/{session_id}", response_model=list[ClientExerciseRead])
def list_session_exercises(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_practitioner_or_operator()),
) -> list[ClientExerciseRead]:
    """Exercices du client de cette séance (toutes propositions confondues)."""
    record = db.get(SessionRecord, session_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Séance introuvable.")
    # Modele IVIA reel : clients + praticiens choisis + admin. Aucun role
    # intermediaire (operateur = vestige) ne contourne l'assignation.
    if not is_admin(current_user) and record.praticien_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Cette séance n'est pas assignée à ce praticien."
        )
    rows = db.execute(
        select(ClientExercise, Exercise)
        .join(Exercise, Exercise.id == ClientExercise.exercise_id)
        .where(
            ClientExercise.client_id == record.client_id,
            ClientExercise.record_status == RecordStatus.active,
        )
        .order_by(ClientExercise.proposed_at.desc())
    ).all()
    return [_ce_read(ce, ex) for ce, ex in rows]


# ── Client : mes exercices ────────────────────────────────────────────────────


def _get_my_client(current_user: AppUser, db: Session) -> Client:
    client = db.scalar(select(Client).where(Client.app_user_id == current_user.id))
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier client introuvable. Complétez votre inscription.",
        )
    return client


@router.get("/me/exercises", response_model=list[ClientExerciseRead])
def list_my_exercises(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> list[ClientExerciseRead]:
    client = _get_my_client(current_user, db)
    rows = db.execute(
        select(ClientExercise, Exercise)
        .join(Exercise, Exercise.id == ClientExercise.exercise_id)
        .where(
            ClientExercise.client_id == client.id,
            ClientExercise.record_status == RecordStatus.active,
        )
        .order_by(ClientExercise.proposed_at.desc())
    ).all()
    return [_ce_read(ce, ex) for ce, ex in rows]


@router.patch("/me/exercises/{client_exercise_id}", response_model=ClientExerciseRead)
def update_my_exercise(
    client_exercise_id: str,
    payload: MyExercisePatch,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> ClientExerciseRead:
    client = _get_my_client(current_user, db)
    ce = db.get(ClientExercise, client_exercise_id)
    if ce is None or ce.client_id != client.id or ce.record_status != RecordStatus.active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Exercice introuvable.")
    if payload.status is not None:
        ce.status = payload.status
        if payload.status in (ExerciseStatusCode.termine, ExerciseStatusCode.abandonne):
            ce.done_at = datetime.now(timezone.utc)
        else:
            ce.done_at = None
    if payload.client_note is not None:
        if len(payload.client_note) > 2000:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Note trop longue (max 2000).")
        ce.client_note = payload.client_note.strip() or None
    db.add(ce)
    db.commit()
    db.refresh(ce)
    ex = db.get(Exercise, ce.exercise_id)
    return _ce_read(ce, ex)
