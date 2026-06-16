from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_optional_current_user, require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import RecordStatus, RequestForCode, RiskLevelCode
from app.models.intake_request import IntakeRequest
from app.schemas.intake_request import IntakeHandlingUpdate, IntakeRequestCreate, IntakeRequestRead
from app.services.intake_analysis import IntakeSignal, analyse_intake_text


class IntakeSignalSchema(BaseModel):
    code: str
    label: str
    severity: str


class IntakeAnalysisResponse(BaseModel):
    intake_request_id: str
    risk_signals: list[IntakeSignalSchema]
    gap_signals: list[IntakeSignalSchema]
    suggested_urgency: str
    current_urgency: str
    has_risk: bool
    has_gaps: bool
    urgency_upgrade_suggested: bool

router = APIRouter(prefix="/intake-requests", tags=["intake_requests"])


def _validate_create_access(payload: IntakeRequestCreate, current_user: AppUser | None) -> None:
    if current_user is not None:
        return

    if payload.request_channel_code != "web_form":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce type de demande d'entree.",
        )

    if payload.request_for_code != RequestForCode.self:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce type de demande d'entree.",
        )

    if payload.perceived_urgency_code not in {
        RiskLevelCode.non_urgent,
        RiskLevelCode.priority,
    }:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce niveau d'urgence.",
        )

    if payload.record_status != RecordStatus.active or payload.referential_version != "v1":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise pour ce type de demande d'entree.",
        )


@router.get("", response_model=list[IntakeRequestRead])
def list_intake_requests(
    client_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[IntakeRequest]:
    statement = select(IntakeRequest).order_by(IntakeRequest.created_at.desc()).limit(limit)
    if client_id is not None:
        statement = statement.where(IntakeRequest.client_id == client_id)
    return list(db.scalars(statement))


@router.post("", response_model=IntakeRequestRead, status_code=status.HTTP_201_CREATED)
def create_intake_request(
    payload: IntakeRequestCreate,
    db: Session = Depends(get_db),
    current_user: AppUser | None = Depends(get_optional_current_user),
) -> IntakeRequest:
    _validate_create_access(payload, current_user)

    client = db.get(Client, payload.client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    intake_request = IntakeRequest(**payload.model_dump())
    db.add(intake_request)
    db.commit()
    db.refresh(intake_request)
    return intake_request


@router.get("/{intake_request_id}", response_model=IntakeRequestRead)
def get_intake_request(
    intake_request_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> IntakeRequest:
    intake_request = db.get(IntakeRequest, intake_request_id)
    if intake_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demande d'entree introuvable.",
        )
    return intake_request


@router.patch("/{intake_request_id}/handling", response_model=IntakeRequestRead)
def update_intake_handling(
    intake_request_id: str,
    payload: IntakeHandlingUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_internal_clinical_roles()),
) -> IntakeRequest:
    """Traite une demande d'entrée : statut (new/à rappeler/contacté/planifié/
    vigilance/hors-cadre) + note. Trace l'opérateur et la date de traitement."""
    from datetime import datetime, timezone

    intake_request = db.get(IntakeRequest, intake_request_id)
    if intake_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demande d'entree introuvable.")
    intake_request.handling_status_code = payload.handling_status_code
    if payload.handling_notes is not None:
        intake_request.handling_notes = payload.handling_notes
    intake_request.handled_by_user_id = current_user.id
    intake_request.handled_at = datetime.now(timezone.utc)
    db.add(intake_request)
    db.commit()
    db.refresh(intake_request)
    return intake_request


@router.get("/{intake_request_id}/analyse", response_model=IntakeAnalysisResponse)
def analyse_intake_request(
    intake_request_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> IntakeAnalysisResponse:
    """
    Analyse le texte libre d'une demande d'entree et retourne les signaux detectes.
    Aucune modification de la base — lecture seule.
    """
    intake_request = db.get(IntakeRequest, intake_request_id)
    if intake_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demande d'entree introuvable.",
        )

    combined_text = " ".join(filter(None, [
        intake_request.entry_summary_text,
        intake_request.requested_outcome_text,
    ]))
    current_urgency = intake_request.perceived_urgency_code.value

    analysis = analyse_intake_text(combined_text, current_urgency)

    def _signal_to_schema(s: IntakeSignal) -> IntakeSignalSchema:
        return IntakeSignalSchema(code=s.code, label=s.label, severity=s.severity)

    from app.services.intake_analysis import _URGENCY_RANK  # noqa: PLC0415
    urgency_upgrade = (
        _URGENCY_RANK.get(analysis.suggested_urgency, 0)
        > _URGENCY_RANK.get(current_urgency, 0)
    )

    return IntakeAnalysisResponse(
        intake_request_id=intake_request_id,
        risk_signals=[_signal_to_schema(s) for s in analysis.risk_signals],
        gap_signals=[_signal_to_schema(s) for s in analysis.gap_signals],
        suggested_urgency=analysis.suggested_urgency,
        current_urgency=current_urgency,
        has_risk=analysis.has_risk,
        has_gaps=analysis.has_gaps,
        urgency_upgrade_suggested=urgency_upgrade,
    )
