from datetime import datetime

from app.schemas.common import MerlinSchema


class EraContextCreate(MerlinSchema):
    tag: str
    label: str
    period_start: int
    period_end: int | None = None
    territory_code: str = "QC"
    data: dict | None = None


class EraContextUpdate(MerlinSchema):
    label: str | None = None
    period_start: int | None = None
    period_end: int | None = None
    territory_code: str | None = None
    data: dict | None = None


class EraContextRead(MerlinSchema):
    tag: str
    label: str
    period_start: int
    period_end: int | None = None
    territory_code: str
    data: dict | None = None
    created_at: datetime
