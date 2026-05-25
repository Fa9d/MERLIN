"""Seed des créneaux de test pour valider le flow booking complet."""
import sys
sys.path.insert(0, "/app")

# Charger TOUS les modèles pour résoudre les relations SQLAlchemy
from app.db.base import load_models
load_models()

from app.db.session import SessionLocal
from app.models.schedule import BookingSlot
from app.models.enums import SessionTypeCode, SlotStatus
from sqlalchemy import text
from datetime import date, time, timedelta

db = SessionLocal()

praticiens = db.execute(
    text("SELECT id, display_name FROM app_users WHERE role='practitioner' ORDER BY display_name")
).fetchall()
print(f"Praticiens: {[(p.display_name, p.id) for p in praticiens]}")

tomorrow   = date.today() + timedelta(days=1)
day_after  = date.today() + timedelta(days=2)
next_week  = date.today() + timedelta(days=7)

slots_created = 0
for prat in praticiens[:3]:
    for slot_date, t_start, t_end in [
        (tomorrow,  time(9,  0), time(10, 0)),
        (tomorrow,  time(14, 0), time(15, 0)),
        (day_after, time(10, 0), time(11, 0)),
        (next_week, time(11, 0), time(12, 0)),
    ]:
        db.add(BookingSlot(
            praticien_id=prat.id,
            slot_date=slot_date,
            start_time=t_start,
            end_time=t_end,
            session_type=SessionTypeCode.intake,
            status=SlotStatus.available,
        ))
        slots_created += 1

db.commit()
total = db.execute(text("SELECT COUNT(*) FROM booking_slots")).scalar()
print(f"Created {slots_created} slots — total in DB: {total}")
db.close()


db = SessionLocal()

praticiens = db.execute(
    text("SELECT id, display_name FROM app_users WHERE role='practitioner' ORDER BY display_name")
).fetchall()
print(f"Praticiens: {[(p.display_name, p.id) for p in praticiens]}")

tomorrow   = date.today() + timedelta(days=1)
day_after  = date.today() + timedelta(days=2)
next_week  = date.today() + timedelta(days=7)

slots_created = 0
for prat in praticiens[:3]:
    for slot_date, t_start, t_end in [
        (tomorrow,  time(9,  0), time(10, 0)),
        (tomorrow,  time(14, 0), time(15, 0)),
        (day_after, time(10, 0), time(11, 0)),
        (next_week, time(11, 0), time(12, 0)),
    ]:
        db.add(BookingSlot(
            praticien_id=prat.id,
            slot_date=slot_date,
            start_time=t_start,
            end_time=t_end,
            session_type=SessionTypeCode.intake,
            status=SlotStatus.available,
        ))
        slots_created += 1

db.commit()
total = db.execute(text("SELECT COUNT(*) FROM booking_slots")).scalar()
print(f"Created {slots_created} slots — total in DB: {total}")
db.close()


db: Session = SessionLocal()

# Trouver les user_id des praticiens
praticiens = db.execute(
    text("SELECT id, display_name FROM app_users WHERE role='practitioner' ORDER BY display_name")
).fetchall()

print(f"Praticiens: {[(p.display_name, p.id) for p in praticiens]}")

tomorrow = date.today() + timedelta(days=1)
day_after = date.today() + timedelta(days=2)
next_week = date.today() + timedelta(days=7)

slots_created = 0
for prat in praticiens[:3]:  # 3 premiers praticiens
    for slot_date, slot_time_start, slot_time_end in [
        (tomorrow, time(9, 0), time(10, 0)),
        (tomorrow, time(14, 0), time(15, 0)),
        (day_after, time(10, 0), time(11, 0)),
        (next_week, time(11, 0), time(12, 0)),
    ]:
        slot = BookingSlot(
            praticien_id=prat.id,
            slot_date=slot_date,
            start_time=slot_time_start,
            end_time=slot_time_end,
            session_type=SessionTypeCode.intake,
            status=SlotStatus.available,
        )
        db.add(slot)
        slots_created += 1

db.commit()
print(f"Created {slots_created} booking slots.")

# Vérification
total = db.execute(text("SELECT COUNT(*) FROM booking_slots")).scalar()
print(f"Total slots in DB: {total}")
db.close()
