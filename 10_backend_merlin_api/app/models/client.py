from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import DataSensitivityClass, RecordStatus


def _public_client_code() -> str:
    return f"CLI-{uuid4().hex[:10].upper()}"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    public_client_code: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False,
        default=_public_client_code,
    )
    first_name_or_alias: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    app_user_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
        index=True,
    )
    # Relation d'accompagnement DURABLE (décision fondateur 2026-07-09) :
    # le praticien choisi par le client. NULL = client AUTONOME (journal seul,
    # sans praticien) — un état normal, pas une anomalie. Les séances gardent
    # leur praticien historique ; ce lien porte la relation courante.
    praticien_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    language_code: Mapped[str] = mapped_column(String(16), nullable=False, default="fr-CA")
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="America/Toronto")
    territory_code: Mapped[str] = mapped_column(String(16), nullable=False, default="QC")
    is_adult_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # Année de naissance (approximative acceptable) — pour calcul d'âge aux événements
    birth_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Genre tel que vécu et exprimé par le sujet (champ libre, non normatif)
    gender_identity: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Lieu de naissance (ville/région ou pays) — profil de détermination
    birthplace: Mapped[str | None] = mapped_column(String(120), nullable=True)
    activation_token_hash: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    activation_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    activation_invited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    activation_accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False),
        nullable=False,
        default=RecordStatus.active,
    )
    data_sensitivity_class: Mapped[DataSensitivityClass] = mapped_column(
        Enum(DataSensitivityClass, native_enum=False),
        nullable=False,
        default=DataSensitivityClass.high,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def profile_complete(self) -> bool:
        """Vrai si les champs obligatoires du profil sont remplis.

        Requis pour accéder au parcours payant/séance : tranche d'âge (birth_year),
        genre, lieu de naissance, territoire.
        """
        return bool(
            self.birth_year
            and self.gender_identity
            and self.birthplace
            and self.territory_code
        )

    intake_requests = relationship("IntakeRequest", back_populates="client")
    consents = relationship("Consent", back_populates="client")
    sessions = relationship("SessionRecord", back_populates="client")
    derived_documents = relationship("DerivedDocument", back_populates="client")
    life_events = relationship("ClientLifeEvent", back_populates="client")
    journal_entries = relationship("ClientJournalEntry", back_populates="client")
    temporal_anchors = relationship("SessionTemporalAnchor", back_populates="client")
