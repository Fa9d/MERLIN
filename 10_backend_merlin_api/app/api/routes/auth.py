from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_optional_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import AppRole, RecordStatus
from app.schemas.auth import LoginRequest, RegisterUserRequest, TokenResponse, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: RegisterUserRequest,
    db: Session = Depends(get_db),
    current_user: AppUser | None = Depends(get_optional_current_user),
) -> AppUser:
    user_count = db.scalar(select(func.count()).select_from(AppUser)) or 0
    if user_count == 0:
        if payload.role != AppRole.admin_tech:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le premier utilisateur doit etre admin_tech.",
            )
    else:
        if current_user is None or current_user.role != AppRole.admin_tech:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seul un admin_tech peut creer un utilisateur.",
            )

    existing = db.scalar(select(AppUser).where(AppUser.email == payload.email))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un utilisateur existe deja avec cet email.",
        )

    user = AppUser(
        email=payload.email,
        password_hash=hash_password(payload.password),
        display_name=payload.display_name,
        role=payload.role,
        record_status=RecordStatus.active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(AppUser).where(AppUser.email == payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides.",
        )

    if user.record_status != RecordStatus.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif.",
        )

    token = create_access_token(subject=user.id, role=user.role.value)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserRead.model_validate(user),
    )


@router.get("/me", response_model=UserRead)
def me(current_user: AppUser = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)


class SetPasswordRequest(BaseModel):
    new_password: str = Field(min_length=8, max_length=128)
    current_password: str | None = Field(default=None, max_length=128)


class SetPasswordResponse(BaseModel):
    message: str


@router.post("/set-password", response_model=SetPasswordResponse)
def set_password(
    payload: SetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> SetPasswordResponse:
    """Permet à l'utilisateur connecté de définir ou changer son mot de passe.

    - Si `current_password` est fourni, il est vérifié contre le hash actuel
      (cas d'un utilisateur qui a déjà un mot de passe et veut le changer).
    - Si `current_password` est omis, on accepte le changement uniquement
      sur la base du JWT (cas d'un utilisateur magic-link qui n'a jamais
      défini de mot de passe : son `password_hash` est un placeholder
      aléatoire jamais communiqué).
    """
    if payload.current_password is not None:
        if not verify_password(payload.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Mot de passe actuel incorrect.",
            )

    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    return SetPasswordResponse(message="Mot de passe mis à jour.")
