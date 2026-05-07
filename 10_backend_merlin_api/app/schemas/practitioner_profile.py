from pydantic import Field

from app.schemas.common import MerlinSchema, TimestampedReadSchema


class PractitionerProfileCreate(MerlinSchema):
    user_id: str
    display_name: str | None = None
    bio: str | None = None
    modalites: list[str] = Field(default_factory=list)
    langues: list[str] = Field(default_factory=list)
    approches: list[str] = Field(default_factory=list)
    public_visible: bool = False
    accepting_clients: bool = True


class PractitionerProfileUpdate(MerlinSchema):
    display_name: str | None = None
    bio: str | None = None
    modalites: list[str] | None = None
    langues: list[str] | None = None
    approches: list[str] | None = None
    public_visible: bool | None = None
    accepting_clients: bool | None = None


class PractitionerProfileRead(TimestampedReadSchema):
    id: int
    user_id: str
    display_name: str | None
    bio: str | None
    modalites: list[str]
    langues: list[str]
    approches: list[str]
    public_visible: bool
    accepting_clients: bool
