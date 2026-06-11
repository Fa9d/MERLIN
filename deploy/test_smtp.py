# Outil ops — test d'envoi SMTP via le code réel de l'app, exécuté DANS le conteneur API prod.
# Usage (depuis le poste Windows) :
#   Get-Content C:\MERLIN\deploy\test_smtp.py | ssh ubuntu@137.74.42.121 `
#     "cd /opt/merlin && docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T api python -"
# Aucun secret affiché ; le courriel part vers l'adresse pilote du fondateur.

import asyncio

from app.core.config import settings
from app.services.email import send_email

print("SMTP host :", settings.smtp_host, "| port :", settings.smtp_port)
print("From      :", settings.smtp_from_name, "<" + settings.smtp_from_email + ">")
print("Username  :", "défini" if settings.smtp_username else "(VIDE)")
print("Password  :", "défini" if settings.smtp_password else "(VIDE)")

ok = asyncio.run(
    send_email(
        "davidphaneuf@gmail.com",
        "Test SMTP IVIA - verification prod",
        "<p>Test SMTP depuis le conteneur API prod (IVIA / MERLIN). Si tu lis ceci, la chaine courriel fonctionne.</p>",
        "Test SMTP depuis le conteneur API prod (IVIA / MERLIN). Si tu lis ceci, la chaine courriel fonctionne.",
        audience="client",
    )
)
print("ENVOI :", "SUCCES - verifie ta boite davidphaneuf@gmail.com" if ok else "ECHEC - voir make prod-logs-api")
