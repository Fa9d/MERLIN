from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import AppRole, RecordStatus
from app.schemas.auth import PraticienPublic

router = APIRouter(prefix="/praticiens", tags=["praticiens"])


@router.get("", response_model=list[PraticienPublic])
def list_praticiens(db: Session = Depends(get_db)) -> list[AppUser]:
    users = db.scalars(
        select(AppUser)
        .where(AppUser.is_publicly_listed == True)  # noqa: E712
        .where(AppUser.role == AppRole.practitioner)
        .where(AppUser.record_status == RecordStatus.active)
        .order_by(AppUser.display_name)
    ).all()
    return list(users)
