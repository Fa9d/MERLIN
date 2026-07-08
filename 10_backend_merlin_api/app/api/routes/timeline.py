"""Routes pour timeline client et historique rendez-vous (Phase 5)."""
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.appointment import Appointment
from app.models.app_user import AppUser
from app.schemas.timeline import (
    AddSessionNotesRequest,
    AppointmentDetailResponse,
    AppointmentHistoryItem,
    AppointmentHistoryResponse,
    AuditTrailEntry,
    PractitionerStatsResponse,
)


router = APIRouter(tags=["timeline"])


@router.get(
    "/appointments/history",
    response_model=AppointmentHistoryResponse,
    summary="Get client appointment history (timeline)",
)
async def get_appointment_history(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[AppUser, Depends(get_current_user)],
    status: Annotated[str | None, Query(regex="^(all|scheduled|confirmed|paid|noted|cancelled)$")] = "all",
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> AppointmentHistoryResponse:
    """
    Retrieve appointment history for current client.
    
    Sorted by most recent first.
    Status filter: all | scheduled | confirmed | paid | noted | cancelled
    """
    # Build query
    query = select(Appointment).where(
        Appointment.client_id == current_user.id
    )

    # Filter by status if not "all"
    if status != "all":
        query = query.where(Appointment.status == status)

    # Order by newest first
    query = query.order_by(desc(Appointment.created_at))

    # Pagination
    query = query.limit(limit).offset(offset)

    # Execute
    appointments = db.execute(query).scalars().all()

    # Build response items
    items = []
    for apt in appointments:
        # Build audit trail
        audit_trail = _build_audit_trail(apt)

        item = AppointmentHistoryItem(
            id=apt.id,
            created_at=apt.created_at,
            scheduled_at=apt.start_time,
            duration_minutes=apt.duration_minutes or 60,
            practitioner_id=apt.practitioner_id,
            practitioner_name=apt.practitioner.display_name if apt.practitioner else "Inconnu",
            status=apt.status,
            confirmed_at=apt.confirmed_at,
            paid_at=apt.paid_at,
            noted_at=apt.noted_at,
            amount_cents=apt.amount_cents,
            session_notes=apt.session_notes,
            practitioner_notes=apt.practitioner_notes if current_user.id == apt.practitioner_id else None,  # Only praticien sees internal notes
            audit_trail=audit_trail,
        )
        items.append(item)

    return AppointmentHistoryResponse(count=len(items), appointments=items)


@router.get(
    "/me/appointments/stats",
    response_model=PractitionerStatsResponse,
    summary="Get practitioner workload stats",
)
async def get_practitioner_stats(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[AppUser, Depends(get_current_user)],
) -> PractitionerStatsResponse:
    """
    Retrieve workload stats for current practitioner.
    - Appointments this week/month
    - Total revenue
    - Completed sessions
    - Pending confirmations
    """
    # Ensure user is practitioner (or admin)
    from app.core.deps import is_admin
    from app.models.enums import AppRole

    if current_user.role != AppRole.practitioner and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only practitioners can access this endpoint")

    from datetime import datetime, timedelta
    from sqlalchemy import func

    now = datetime.now(datetime.now().astimezone().tzinfo)
    week_start = now - timedelta(days=now.weekday())
    month_start = now.replace(day=1)

    # Stats queries
    stats_query = select(
        func.count(Appointment.id).filter(
            and_(
                Appointment.practitioner_id == current_user.id,
                Appointment.created_at >= week_start,
            )
        ).label("week_count"),
        func.count(Appointment.id).filter(
            and_(
                Appointment.practitioner_id == current_user.id,
                Appointment.created_at >= month_start,
            )
        ).label("month_count"),
        func.sum(Appointment.amount_cents).filter(
            and_(
                Appointment.practitioner_id == current_user.id,
                Appointment.status == "paid",
            )
        ).label("total_revenue"),
        func.count(Appointment.id).filter(
            and_(
                Appointment.practitioner_id == current_user.id,
                Appointment.status == "noted",
            )
        ).label("completed_count"),
        func.count(Appointment.id).filter(
            and_(
                Appointment.practitioner_id == current_user.id,
                Appointment.status == "confirmed",
            )
        ).label("pending_count"),
    )

    result = db.execute(stats_query).first()

    # Get upcoming appointments (next 5)
    upcoming_query = (
        select(Appointment)
        .where(
            and_(
                Appointment.practitioner_id == current_user.id,
                Appointment.start_time >= now,
                Appointment.status != "cancelled",
            )
        )
        .order_by(Appointment.start_time)
        .limit(5)
    )
    upcoming = db.execute(upcoming_query).scalars().all()

    # Build upcoming items
    upcoming_items = []
    for apt in upcoming:
        item = AppointmentHistoryItem(
            id=apt.id,
            created_at=apt.created_at,
            scheduled_at=apt.start_time,
            duration_minutes=apt.duration_minutes or 60,
            practitioner_id=apt.practitioner_id,
            practitioner_name=apt.practitioner.display_name if apt.practitioner else "Inconnu",
            client_id=apt.client_id,
            client_name=apt.client.display_name if apt.client else "Inconnu",
            status=apt.status,
            confirmed_at=apt.confirmed_at,
            paid_at=apt.paid_at,
            amount_cents=apt.amount_cents,
        )
        upcoming_items.append(item)

    return PractitionerStatsResponse(
        appointments_this_week=result.week_count or 0,
        appointments_this_month=result.month_count or 0,
        total_revenue_cents=result.total_revenue or 0,
        completed_count=result.completed_count or 0,
        pending_confirmations=result.pending_count or 0,
        upcoming_appointments=upcoming_items,
    )


@router.get(
    "/appointments/{appointment_id}",
    response_model=AppointmentDetailResponse,
    summary="Get appointment detail with audit trail",
)
async def get_appointment_detail(
    appointment_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[AppUser, Depends(get_current_user)],
) -> AppointmentDetailResponse:
    """
    Get full appointment details including audit trail.
    User must be client or practitioner of this appointment.
    """
    apt = db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    ).scalar_one_or_none()

    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Check access
    if apt.client_id != current_user.id and apt.practitioner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Build audit trail
    audit_trail = _build_audit_trail(apt)

    return AppointmentDetailResponse(
        id=apt.id,
        created_at=apt.created_at,
        scheduled_at=apt.start_time,
        duration_minutes=apt.duration_minutes or 60,
        practitioner_id=apt.practitioner_id,
        practitioner_name=apt.practitioner.display_name if apt.practitioner else "Inconnu",
        status=apt.status,
        confirmed_at=apt.confirmed_at,
        paid_at=apt.paid_at,
        noted_at=apt.noted_at,
        amount_cents=apt.amount_cents,
        session_notes=apt.session_notes,
        practitioner_notes=apt.practitioner_notes if current_user.id == apt.practitioner_id else None,
        audit_trail=audit_trail,
    )


@router.patch(
    "/appointments/{appointment_id}/notes",
    response_model=AppointmentDetailResponse,
    summary="Add or update session notes",
)
async def add_session_notes(
    appointment_id: str,
    request: AddSessionNotesRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[AppUser, Depends(get_current_user)],
) -> AppointmentDetailResponse:
    """
    Add session notes to appointment.
    Only practitioner can add notes.
    Updates appointment.status to 'noted' and sets noted_at timestamp.
    """
    apt = db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    ).scalar_one_or_none()

    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Check access (only practitioner)
    if apt.practitioner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only practitioner can add notes")

    # Update appointment
    apt.session_notes = request.session_notes
    apt.practitioner_notes = request.practitioner_notes
    apt.status = "noted"
    apt.noted_at = datetime.now(datetime.now().astimezone().tzinfo)

    db.add(apt)
    db.commit()
    db.refresh(apt)

    # Build response
    audit_trail = _build_audit_trail(apt)

    return AppointmentDetailResponse(
        id=apt.id,
        created_at=apt.created_at,
        scheduled_at=apt.start_time,
        duration_minutes=apt.duration_minutes or 60,
        practitioner_id=apt.practitioner_id,
        practitioner_name=apt.practitioner.display_name if apt.practitioner else "Inconnu",
        status=apt.status,
        confirmed_at=apt.confirmed_at,
        paid_at=apt.paid_at,
        noted_at=apt.noted_at,
        amount_cents=apt.amount_cents,
        session_notes=apt.session_notes,
        practitioner_notes=apt.practitioner_notes,
        audit_trail=audit_trail,
    )


def _build_audit_trail(apt: Appointment) -> list[AuditTrailEntry]:
    """Build audit trail for an appointment."""
    trail = []

    # Created
    trail.append(
        AuditTrailEntry(
            action="created",
            by=apt.client.email if apt.client else "unknown",
            at=apt.created_at,
        )
    )

    # Confirmed
    if apt.confirmed_at:
        trail.append(
            AuditTrailEntry(
                action="confirmed",
                by=apt.practitioner.email if apt.practitioner else "unknown",
                at=apt.confirmed_at,
            )
        )

    # Paid
    if apt.paid_at:
        trail.append(
            AuditTrailEntry(
                action="paid",
                by="stripe",  # Payment via Stripe
                at=apt.paid_at,
            )
        )

    # Noted
    if apt.noted_at:
        trail.append(
            AuditTrailEntry(
                action="noted",
                by=apt.practitioner.email if apt.practitioner else "unknown",
                at=apt.noted_at,
            )
        )

    return trail
