"""Inscription publique d'un client avec vérification courriel."""
from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import AppRole
from app.services.email import make_verification_email, send_email
from app.core.security import hash_password

router = APIRouter(prefix="/register", tags=["register"])

_TOKEN_TTL_HOURS = 24


class ClientRegisterIn(BaseModel):
    email: EmailStr
    password: str
    display_name: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        return v


class ClientRegisterOut(BaseModel):
    id: str
    email: str
    display_name: str
    message: str


@router.post(
    "/client",
    response_model=ClientRegisterOut,
    status_code=status.HTTP_201_CREATED,
    summary="Inscription publique d'un client",
)
async def register_client(
    body: ClientRegisterIn,
    db: Session = Depends(get_db),
) -> ClientRegisterOut:
    # Unicité de l'email (insensible à la casse)
    existing = db.query(AppUser).filter(AppUser.email == body.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte existe déjà avec cet email.",
        )

    token = secrets.token_urlsafe(48)
    expires = datetime.now(timezone.utc) + timedelta(hours=_TOKEN_TTL_HOURS)

    user = AppUser(
        email=body.email.lower(),
        password_hash=hash_password(body.password),
        display_name=body.display_name,
        role=AppRole.public_client,
        email_verified=False,
        email_verification_token=token,
        token_expires_at=expires,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    verification_url = f"{settings.frontend_url}/verify-email?token={token}"
    html, text = make_verification_email(user.display_name, verification_url)
    await send_email(user.email, "Confirmez votre adresse — IVIA", html, text)

    return ClientRegisterOut(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        message="Compte créé. Vérifiez votre courriel pour activer votre compte.",
    )
