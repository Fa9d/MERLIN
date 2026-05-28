from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import RecordStatus
from app.models.session import SessionRecord
from app.models.session_temporal_anchor import SessionTemporalAnchor
from app.schemas.session_temporal_anchor import (
    SessionTemporalAnchorCreate,
    SessionTemporalAnchorRead,
    SessionTemporalAnchorUpdate,
)

router = APIRouter(prefix="/sessions/{session_id}/temporal-anchors", tags=["temporal-anchors"])


def _get_session_or_404(session_id: str, db: Session) -> SessionRecord:
    session = db.get(SessionRecord, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Séance introuvable.")
    return session


def _compute_gap(anchor: SessionTemporalAnchor, session: SessionRecord) -> int | None:
    """Calcule gap_years = année séance − event_year_approx."""
    if anchor.event_year_approx is None:
        return None
    session_year = None
    if session.actual_start_at:
        session_year = session.actual_start_at.year
    elif session.scheduled_start_at:
        session_year = session.scheduled_start_at.year
    if session_year is None:
        return None
    return session_year - anchor.event_year_approx


@router.get("", response_model=list[SessionTemporalAnchorRead])
def list_temporal_anchors(
    session_id: str,
    include_archived: bool = Query(default=False),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[SessionTemporalAnchor]:
    _get_session_or_404(session_id, db)
    stmt = (
        select(SessionTemporalAnchor)
        .where(SessionTemporalAnchor.session_id == session_id)
        .order_by(SessionTemporalAnchor.said_at_offset_sec.asc().nullslast())
    )
    if not include_archived:
        stmt = stmt.where(SessionTemporalAnchor.record_status != RecordStatus.archived)
    return list(db.scalars(stmt))


@router.post("", response_model=SessionTemporalAnchorRead, status_code=status.HTTP_201_CREATED)
def create_temporal_anchor(
    session_id: str,
    payload: SessionTemporalAnchorCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionTemporalAnchor:
    session = _get_session_or_404(session_id, db)
    data = payload.model_dump()
    data["session_id"] = session_id
    data["id"] = str(uuid4())
    now = datetime.now(timezone.utc)
    data["created_at"] = now
    data["updated_at"] = now
    anchor = SessionTemporalAnchor(**data)
    # Calcul automatique du gap si non fourni
    if anchor.gap_years is None:
        anchor.gap_years = _compute_gap(anchor, session)
    db.add(anchor)
    db.commit()
    db.refresh(anchor)
    return anchor


@router.get("/{anchor_id}", response_model=SessionTemporalAnchorRead)
def get_temporal_anchor(
    session_id: str,
    anchor_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionTemporalAnchor:
    _get_session_or_404(session_id, db)
    anchor = db.scalar(
        select(SessionTemporalAnchor).where(
            SessionTemporalAnchor.id == anchor_id,
            SessionTemporalAnchor.session_id == session_id,
        )
    )
    if anchor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ancrage introuvable.")
    return anchor


@router.patch("/{anchor_id}", response_model=SessionTemporalAnchorRead)
def update_temporal_anchor(
    session_id: str,
    anchor_id: str,
    payload: SessionTemporalAnchorUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> SessionTemporalAnchor:
    session = _get_session_or_404(session_id, db)
    anchor = db.scalar(
        select(SessionTemporalAnchor).where(
            SessionTemporalAnchor.id == anchor_id,
            SessionTemporalAnchor.session_id == session_id,
        )
    )
    if anchor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ancrage introuvable.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(anchor, field, value)
    anchor.updated_at = datetime.now(timezone.utc)
    # Recalcul du gap si event_year_approx a changé et gap non fourni explicitement
    if "event_year_approx" in payload.model_dump(exclude_unset=True) and "gap_years" not in payload.model_dump(exclude_unset=True):
        anchor.gap_years = _compute_gap(anchor, session)
    db.add(anchor)
    db.commit()
    db.refresh(anchor)
    return anchor


@router.delete("/{anchor_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_temporal_anchor(
    session_id: str,
    anchor_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> None:
    _get_session_or_404(session_id, db)
    anchor = db.scalar(
        select(SessionTemporalAnchor).where(
            SessionTemporalAnchor.id == anchor_id,
            SessionTemporalAnchor.session_id == session_id,
        )
    )
    if anchor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ancrage introuvable.")
    anchor.record_status = RecordStatus.archived
    anchor.updated_at = datetime.now(timezone.utc)
    db.add(anchor)
    db.commit()
