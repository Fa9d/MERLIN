"""Routes de gestion des disponibilités praticien et des créneaux de réservation."""
from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.deps import require_practitioner
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import AppRole, ExceptionType, SlotStatus
from app.models.schedule import BookingSlot, PractitionerSchedule, ScheduleException
from app.schemas.schedule import (
    AvailableSlotOut,
    ScheduleExceptionCreate,
    ScheduleExceptionOut,
    ScheduleSlotCreate,
    ScheduleSlotOut,
    ScheduleSlotUpdate,
    SESSION_TYPE_LABELS,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/schedules", tags=["schedules"])


# ---------------------------------------------------------------------------
# GABARIT HEBDOMADAIRE — endpoints praticien
# ---------------------------------------------------------------------------

@router.get("/my", response_model=list[ScheduleSlotOut])
def get_my_schedule(
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Retourne le gabarit hebdomadaire du praticien connecté."""
    rows = db.execute(
        select(PractitionerSchedule)
        .where(PractitionerSchedule.praticien_id == current_user.id)
        .order_by(PractitionerSchedule.day_of_week, PractitionerSchedule.start_time)
    ).scalars().all()
    return [ScheduleSlotOut.from_orm_with_labels(r) for r in rows]


@router.post("/my", response_model=ScheduleSlotOut, status_code=status.HTTP_201_CREATED)
def create_schedule_slot(
    body: ScheduleSlotCreate,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Ajoute un bloc de disponibilité au gabarit hebdomadaire."""
    slot = PractitionerSchedule(
        praticien_id=current_user.id,
        **body.model_dump(),
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return ScheduleSlotOut.from_orm_with_labels(slot)


@router.patch("/my/{slot_id}", response_model=ScheduleSlotOut)
def update_schedule_slot(
    slot_id: str,
    body: ScheduleSlotUpdate,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Modifie un bloc existant."""
    slot = db.get(PractitionerSchedule, slot_id)
    if slot is None or slot.praticien_id != current_user.id:
        raise HTTPException(status_code=404, detail="Créneau introuvable.")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(slot, field, value)

    db.commit()
    db.refresh(slot)
    return ScheduleSlotOut.from_orm_with_labels(slot)


@router.delete("/my/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule_slot(
    slot_id: str,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Supprime un bloc du gabarit."""
    slot = db.get(PractitionerSchedule, slot_id)
    if slot is None or slot.praticien_id != current_user.id:
        raise HTTPException(status_code=404, detail="Créneau introuvable.")
    db.delete(slot)
    db.commit()


# ---------------------------------------------------------------------------
# EXCEPTIONS (congés, jours bloqués)
# ---------------------------------------------------------------------------

@router.get("/my/exceptions", response_model=list[ScheduleExceptionOut])
def get_my_exceptions(
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
):
    stmt = select(ScheduleException).where(
        ScheduleException.praticien_id == current_user.id
    )
    if from_date:
        stmt = stmt.where(ScheduleException.exception_date >= from_date)
    if to_date:
        stmt = stmt.where(ScheduleException.exception_date <= to_date)
    stmt = stmt.order_by(ScheduleException.exception_date)
    return db.execute(stmt).scalars().all()


@router.post("/my/exceptions", response_model=ScheduleExceptionOut, status_code=201)
def create_exception(
    body: ScheduleExceptionCreate,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    exc = ScheduleException(praticien_id=current_user.id, **body.model_dump())
    db.add(exc)
    db.commit()
    db.refresh(exc)
    return exc


@router.delete("/my/exceptions/{exc_id}", status_code=204)
def delete_exception(
    exc_id: str,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    exc = db.get(ScheduleException, exc_id)
    if exc is None or exc.praticien_id != current_user.id:
        raise HTTPException(status_code=404, detail="Exception introuvable.")
    db.delete(exc)
    db.commit()


# ---------------------------------------------------------------------------
# CRÉNEAUX DISPONIBLES (accès public — pas de JWT requis)
# ---------------------------------------------------------------------------

@router.get("/available", response_model=list[AvailableSlotOut])
def get_available_slots(
    praticien_id: str = Query(...),
    date_from: date = Query(...),
    date_to: date = Query(...),
    duration_minutes: int | None = Query(default=None, ge=15, le=240),
    db: Session = Depends(get_db),
):
    """
    Calcule les créneaux disponibles pour un praticien sur une plage de dates.
    Endpoint public (pas de JWT requis).
    """
    if (date_to - date_from).days > 90:
        raise HTTPException(status_code=400, detail="Plage maximale : 90 jours.")

    # Vérifier que le praticien existe
    praticien = db.get(AppUser, praticien_id)
    if praticien is None or praticien.role != AppRole.practitioner:
        raise HTTPException(status_code=404, detail="Praticien introuvable.")

    # Charger le gabarit actif
    schedules = db.execute(
        select(PractitionerSchedule)
        .where(
            and_(
                PractitionerSchedule.praticien_id == praticien_id,
                PractitionerSchedule.is_active == True,
            )
        )
    ).scalars().all()

    # Charger les exceptions sur la plage
    exceptions = db.execute(
        select(ScheduleException)
        .where(
            and_(
                ScheduleException.praticien_id == praticien_id,
                ScheduleException.exception_date >= date_from,
                ScheduleException.exception_date <= date_to,
            )
        )
    ).scalars().all()

    blocked_dates: set[date] = set()
    blocked_ranges: list[tuple[date, time, time]] = []
    extra_ranges: list[tuple[date, time, time, str]] = []

    for exc in exceptions:
        if exc.exception_type == ExceptionType.blocked:
            if exc.start_time is None:
                blocked_dates.add(exc.exception_date)
            else:
                blocked_ranges.append((exc.exception_date, exc.start_time, exc.end_time))
        elif exc.exception_type == ExceptionType.extra and exc.start_time and exc.end_time:
            extra_ranges.append((exc.exception_date, exc.start_time, exc.end_time, "standard"))

    # Charger les slots déjà confirmés / en hold
    booked_slots = db.execute(
        select(BookingSlot)
        .where(
            and_(
                BookingSlot.praticien_id == praticien_id,
                BookingSlot.slot_date >= date_from,
                BookingSlot.slot_date <= date_to,
                BookingSlot.status.in_([SlotStatus.confirmed, SlotStatus.hold]),
            )
        )
    ).scalars().all()

    # Expirer les hold dépassés ; sinon, mémoriser la PLAGE réservée (début→fin)
    # pour exclure tout créneau qui la chevauche (réservations de durée libre).
    now_utc = datetime.now(timezone.utc)
    booked_ranges_by_date: dict[date, list[tuple[time, time]]] = {}
    for bs in booked_slots:
        if bs.status == SlotStatus.hold and bs.hold_expires_at and bs.hold_expires_at < now_utc:
            bs.status = SlotStatus.available
            db.add(bs)
        else:
            booked_ranges_by_date.setdefault(bs.slot_date, []).append((bs.start_time, bs.end_time))
    db.commit()

    def _overlaps(a_start: time, a_end: time, b_start: time, b_end: time) -> bool:
        return a_start < b_end and b_start < a_end

    slots: list[AvailableSlotOut] = []

    current = date_from
    while current <= date_to:
        dow = current.weekday()  # 0=lundi
        day_schedules = [s for s in schedules if s.day_of_week == dow]
        booked_today = booked_ranges_by_date.get(current, [])

        for sched in day_schedules:
            # Filtrer si hors validité
            if sched.valid_from and current < sched.valid_from:
                continue
            if sched.valid_until and current > sched.valid_until:
                continue
            # Journée entière bloquée
            if current in blocked_dates:
                continue

            # La durée vient de l'offre choisie (paramètre) ; sinon, défaut de la fenêtre.
            slot_len = duration_minutes or sched.session_duration_minutes
            # Pas = durée du créneau (pavage propre, ancré au début de la plage) : une
            # plage 10h–12h en 1 h donne 10h/11h ; en 30 min, 10h/10h30/11h/11h30. On ne
            # propose pas de départ en milieu de plage qui laisserait une demi-heure orpheline.
            step = timedelta(minutes=slot_len)
            cursor = datetime.combine(current, sched.start_time)
            end_dt = datetime.combine(current, sched.end_time)

            while cursor + timedelta(minutes=slot_len) <= end_dt:
                slot_start: time = cursor.time()
                slot_end: time = (cursor + timedelta(minutes=slot_len)).time()

                # Exclure si le créneau chevauche une plage bloquée (exception) ou réservée.
                blocked = any(
                    d == current and _overlaps(slot_start, slot_end, s, e)
                    for d, s, e in blocked_ranges
                )
                booked = any(_overlaps(slot_start, slot_end, bs, be) for bs, be in booked_today)

                if not blocked and not booked:
                    slots.append(AvailableSlotOut(
                        praticien_id=praticien_id,
                        praticien_name=praticien.display_name,
                        slot_date=current,
                        start_time=slot_start,
                        end_time=slot_end,
                        session_type=sched.session_type,
                        session_type_label=SESSION_TYPE_LABELS.get(sched.session_type, sched.session_type),
                        duration_minutes=slot_len,
                    ))
                cursor += step

        current += timedelta(days=1)

    return sorted(slots, key=lambda s: (s.slot_date, s.start_time))
