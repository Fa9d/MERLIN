"""Reset all practitioner/operator passwords to IVIA2026!"""
import os
from sqlalchemy import create_engine, text
from app.core.security import hash_password

db_url = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://merlin:change-me@postgres:5432/merlin_v1"
)
eng = create_engine(db_url)
h = hash_password("IVIA2026!")

emails = [
    "pilote.aelis@ivia.quebec",
    "pilote.nael@ivia.quebec",
    "pilote.nori@ivia.quebec",
    "pilote.seve@ivia.quebec",
    "pilote.solene@ivia.quebec",
    "pilote.telma@ivia.quebec",
    "jean.beaumont@example.com",
]

with eng.connect() as conn:
    for email in emails:
        r = conn.execute(
            text("UPDATE app_users SET password_hash = :h WHERE email = :e"),
            {"h": h, "e": email}
        )
        print(f"  {email}: {r.rowcount} row updated")
    conn.commit()
    print("Done. Password = IVIA2026!")
