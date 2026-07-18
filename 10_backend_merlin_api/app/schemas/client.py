from datetime import datetime

from pydantic import EmailStr, Field

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


class MyClientUpdate(MerlinSchema):
    """Mise à jour partielle de la fiche client par son propre titulaire."""

    first_name_or_alias: str | None = None
    last_name: str | None = None
    phone: str | None = None
    language_code: str | None = None
    timezone: str | None = None
    territory_code: str | None = None
    birth_year: int | None = None
    gender_identity: str | None = None
    birthplace: str | None = None


class ClientEmailSend(MerlinSchema):
    """Courriel libre envoyé par un praticien à son client depuis la fiche."""

    subject: str = Field(min_length=1, max_length=150)
    message: str = Field(min_length=1, max_length=4000)


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
    app_user_id: str | None = None
    birth_year: int | None = None
    gender_identity: str | None = None
    birthplace: str | None = None
    # Vrai si les champs obligatoires du profil sont remplis (piloté côté serveur).
    profile_complete: bool = False
    activation_invited_at: datetime | None = None
    activation_accepted_at: datetime | None = None
