from pydantic import EmailStr

from app.models.enums import DataSensitivityClass, RecordStatus
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class ClientCreate(MerlinSchema):
    first_name_or_alias: str
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    language_code: str = "fr-CA"
    timezone: str = "America/Toronto"
    territory_code: str = "QC"
    is_adult_confirmed: bool = True
    record_status: RecordStatus = RecordStatus.active
    data_sensitivity_class: DataSensitivityClass = DataSensitivityClass.high


class ClientRead(TimestampedReadSchema):
    id: str
    public_client_code: str
    first_name_or_alias: str
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    language_code: str
    timezone: str
    territory_code: str
    is_adult_confirmed: bool
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
