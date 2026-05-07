from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base, load_models
from app.models.app_user import AppUser
from app.models.enums import AppRole, RecordStatus
from app.models.practitioner_profile import PractitionerProfile
from app.schemas.practitioner_profile import (
    PractitionerProfileCreate,
    PractitionerProfileRead,
    PractitionerProfileUpdate,
)


def _setup_in_memory_db() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    load_models()
    Base.metadata.create_all(bind=engine)
    return Session(bind=engine)


def _create_user(db: Session) -> AppUser:
    user = AppUser(
        email="praticien@example.com",
        password_hash="hash",
        display_name="Praticien Test",
        role=AppRole.practitioner,
        record_status=RecordStatus.active,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_practitioner_profile_create_and_read() -> None:
    db = _setup_in_memory_db()
    user = _create_user(db)

    payload = PractitionerProfileCreate(
        user_id=user.id,
        display_name="Camille",
        bio="Accompagnement centré sur la clarté.",
        modalites=["video", "audio"],
        langues=["fr", "en"],
        approches=["ecoute_active", "narratif"],
        public_visible=True,
        accepting_clients=True,
    )

    profile = PractitionerProfile(**payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)

    assert profile.id is not None
    assert profile.user_id == user.id
    assert profile.display_name == "Camille"
    assert profile.bio == "Accompagnement centré sur la clarté."
    assert profile.modalites == ["video", "audio"]
    assert profile.langues == ["fr", "en"]
    assert profile.approches == ["ecoute_active", "narratif"]
    assert profile.public_visible is True
    assert profile.accepting_clients is True

    read_schema = PractitionerProfileRead.model_validate(profile)
    assert read_schema.id == profile.id
    assert read_schema.user_id == user.id

    db.close()


def test_practitioner_profile_update() -> None:
    db = _setup_in_memory_db()
    user = _create_user(db)

    profile = PractitionerProfile(
        user_id=user.id,
        display_name="Initial",
        bio=None,
        modalites=["audio"],
        langues=["fr"],
        approches=["ecoute_active"],
        public_visible=False,
        accepting_clients=True,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    update = PractitionerProfileUpdate(
        display_name="Mise à jour",
        bio="Bio mise à jour.",
        modalites=["video"],
        public_visible=True,
        accepting_clients=False,
    )

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    db.add(profile)
    db.commit()
    db.refresh(profile)

    assert profile.display_name == "Mise à jour"
    assert profile.bio == "Bio mise à jour."
    assert profile.modalites == ["video"]
    assert profile.public_visible is True
    assert profile.accepting_clients is False

    db.close()
