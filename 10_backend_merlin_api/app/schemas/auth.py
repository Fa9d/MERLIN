from pydantic import EmailStr

from app.models.enums import AppRole, RecordStatus
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class RegisterUserRequest(MerlinSchema):
    email: EmailStr
    password: str
    display_name: str
    role: AppRole


class LoginRequest(MerlinSchema):
    email: EmailStr
    password: str


class UserRead(TimestampedReadSchema):
    id: str
    email: EmailStr
    display_name: str
    role: AppRole
    record_status: RecordStatus


class TokenResponse(MerlinSchema):
    access_token: str
    token_type: str
    user: UserRead
