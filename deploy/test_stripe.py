# Outil ops — vérification Stripe READ-ONLY via le code réel de l'app, DANS le conteneur API prod.
# Ne crée rien, ne facture rien : Account.retrieve + WebhookEndpoint.list seulement.
# Usage (depuis le poste Windows) :
#   Get-Content C:\MERLIN\deploy\test_stripe.py | ssh ubuntu@137.74.42.121 `
#     "cd /opt/merlin && docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T api python -"
# Aucun secret affiché (préfixe de clé seulement : sk_test / sk_live).

import stripe

from app.core.config import settings

key = settings.stripe_secret_key or ""
print("Cle secrete    :", (key[:8] + "...") if key else "(VIDE)")
print("Webhook secret :", "défini" if settings.stripe_webhook_secret else "(VIDE)")
print("Success URL    :", settings.stripe_checkout_success_url or "(VIDE)")
print("Cancel URL     :", settings.stripe_checkout_cancel_url or "(VIDE)")
print("Audio async    :", settings.stripe_audio_async_amount_cents, settings.stripe_audio_async_currency)

if not key:
    print("VERDICT : ECHEC — MERLIN_STRIPE_SECRET_KEY absente de .env.prod")
else:
    stripe.api_key = key
    try:
        acct = stripe.Account.retrieve()
        print("Compte Stripe  :", acct.get("id"), "| charges_enabled :", acct.get("charges_enabled"))
        endpoints = stripe.WebhookEndpoint.list(limit=10)
        if not endpoints.data:
            print("Webhooks       : AUCUN endpoint declare cote Stripe")
        for ep in endpoints.data:
            print("Webhook        :", ep.url, "| statut :", ep.status, "| events :", len(ep.enabled_events))
        attendu = "https://api.ivia.quebec/api/v1/payments/stripe/webhook"
        ok_webhook = any(ep.url == attendu and ep.status == "enabled" for ep in endpoints.data)
        ok = bool(acct.get("charges_enabled")) and bool(settings.stripe_webhook_secret) and ok_webhook
        print("VERDICT :", "PRET POUR PAIEMENTS" if ok else "INCOMPLET — voir lignes ci-dessus (webhook attendu : " + attendu + ")")
    except Exception as exc:
        print("VERDICT : ECHEC — appel Stripe refuse :", exc)
