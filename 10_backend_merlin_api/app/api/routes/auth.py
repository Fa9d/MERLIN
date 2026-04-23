from fastapi import APIRouter, Depends, HTTPException, status
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
