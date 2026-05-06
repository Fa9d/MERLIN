from app.db.base import Base, load_models
load_models()
from app.db.session import SessionLocal
from app.models.practitioner_profile import PractitionerProfile
from app.models.app_user import AppUser
from app.models.enums import AppRole, RecordStatus

db = SessionLocal()
user = AppUser(
    email='marie.tremblay@test.com',
    password_hash='test_hash_non_utilise',
    display_name='Marie Tremblay',
    role=AppRole.practitioner,
    record_status=RecordStatus.active,
    is_publicly_listed=True
)
db.add(user)
db.flush()
praticien = PractitionerProfile(
    user_id=user.id,
    display_name='Marie Tremblay',
    title_line='Psychotherapeute',
    intro_text='Specialisee en anxiete et gestion du stress.',
    langues='["fr"]',
    domaines='["anxiete"]',
    approches='["cognitif_comportemental"]',
    disponibilites='["matin"]',
    tarif_horaire_cents=9000,
    actif=True
)
db.add(praticien)
db.commit()
print('OK — user.id:', user.id, '| praticien.id:', praticien.id)
db.close()
