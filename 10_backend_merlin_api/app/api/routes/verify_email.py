"""Vérification d'adresse courriel via token."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.app_user import AppUser

router = APIRouter(prefix="/verify-email", tags=["register"])


class VerifyEmailOut(BaseModel):
    message: str


@router.get(
    "/{token}",
    response_model=VerifyEmailOut,
    summary="Activer un compte via le token de vérification",
)
def verify_email(token: str, db: Session = Depends(get_db)) -> VerifyEmailOut:
    user: AppUser | None = (
        db.query(AppUser)
        .filter(AppUser.email_verification_token == token)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token invalide.",
        )

    if user.email_verified:
        return VerifyEmailOut(message="Compte déjà activé.")

    now = datetime.now(timezone.utc)
    if user.token_expires_at and user.token_expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Ce lien de vérification a expiré. Veuillez vous réinscrire.",
        )

    user.email_verified = True
    user.email_verification_token = None
    user.token_expires_at = None
    db.commit()

    return VerifyEmailOut(message="Adresse courriel confirmée. Vous pouvez maintenant vous connecter.")
