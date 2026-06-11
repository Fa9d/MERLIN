# Outil ops — diagnostic + renvoi du lien de vérification courriel d'un compte.
# Usage (poste Windows) :
#   Get-Content C:\MERLIN\deploy\resend_verification.py | ssh ubuntu@137.74.42.121 `
#     "cd /opt/merlin && docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T api python -"
# Imprime l'état du compte, l'état du mode pilote, le résultat d'envoi ET le lien direct
# (dépannage : cliquer le lien vaut réception du courriel).

import asyncio
import os
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.config import settings
from app.db.base import load_models
from app.db.session import SessionLocal

# Enregistre tous les modèles (relations AppUser <-> PractitionerProfile, etc.)
load_models()
from app.models.app_user import AppUser
from app.services.email import make_verification_email, send_email

EMAIL = "lagent009@gmail.com"

with SessionLocal() as db:
    user = db.scalar(select(AppUser).where(AppUser.email == EMAIL))
    if user is None:
        print("AUCUN COMPTE pour", EMAIL)
        raise SystemExit(0)

    print("Compte   :", user.email, "| role :", user.role.value)
    print("Vérifié  :", user.email_verified)
    print("Token exp:", user.token_expires_at)

    if user.email_verified:
        print("VERDICT  : DÉJÀ VÉRIFIÉ — déconnectez-vous puis reconnectez-vous, le bandeau disparaîtra.")
        raise SystemExit(0)

    token = secrets.token_urlsafe(48)
    user.email_verification_token = token
    user.token_expires_at = datetime.now(timezone.utc) + timedelta(hours=48)
    db.commit()

    url = f"{settings.frontend_url}/verify-email?token={token}"
    html, text = make_verification_email(user.display_name, url)
    ok = asyncio.run(send_email(user.email, "Confirmez votre adresse — IVIA", html, text))

    print("Pilote   :", "ACTIF -> courriels rediriges vers davidphaneuf@gmail.com"
          if os.getenv("MERLIN_PILOT_EMAIL_OVERRIDE") == "1" else "inactif (envoi direct au destinataire)")
    print("ENVOI    :", "SUCCES" if ok else "ECHEC (voir make prod-logs-api)")
    print("LIEN DIRECT (cliquez-le si le courriel n'arrive pas) :")
    print(url)
