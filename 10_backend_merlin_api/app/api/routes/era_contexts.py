from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_internal_clinical_roles
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.era_context import EraContext
from app.schemas.era_context import EraContextCreate, EraContextRead, EraContextUpdate

router = APIRouter(prefix="/era-contexts", tags=["era-contexts"])


@router.get("", response_model=list[EraContextRead])
def list_era_contexts(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> list[EraContext]:
    return list(db.scalars(select(EraContext).order_by(EraContext.period_start)))


@router.post("", response_model=EraContextRead, status_code=status.HTTP_201_CREATED)
def create_era_context(
    payload: EraContextCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> EraContext:
    if db.get(EraContext, payload.tag):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Un contexte avec le tag '{payload.tag}' existe déjà.",
        )
    era = EraContext(**payload.model_dump())
    db.add(era)
    db.commit()
    db.refresh(era)
    return era


@router.get("/{tag}", response_model=EraContextRead)
def get_era_context(
    tag: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> EraContext:
    era = db.get(EraContext, tag)
    if era is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contexte introuvable.")
    return era


@router.patch("/{tag}", response_model=EraContextRead)
def update_era_context(
    tag: str,
    payload: EraContextUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_internal_clinical_roles()),
) -> EraContext:
    era = db.get(EraContext, tag)
    if era is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contexte introuvable.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(era, field, value)
    db.add(era)
    db.commit()
    db.refresh(era)
    return era
