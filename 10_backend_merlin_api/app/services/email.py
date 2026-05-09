"""Service d'envoi de courriels via SMTP (SSL).

Mode pilote : si MERLIN_PILOT_EMAIL_OVERRIDE est activé,
tous les courriels sont redirigés vers les adresses Gmail de pilote
(davidphaneuf@gmail.com pour clients/praticiens, lagent009@gmail.com pour admin).
Le destinataire d'origine est conservé dans l'objet du courriel pour traçabilité.
"""
from __future__ import annotations

import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mode pilote — override courriels vers Gmail David
# ---------------------------------------------------------------------------

_PILOT_OVERRIDE_ENABLED = os.getenv("MERLIN_PILOT_EMAIL_OVERRIDE", "0").strip().lower() in {"1", "true", "yes", "on"}
_PILOT_CLIENT_PRACTITIONER_EMAIL = os.getenv("MERLIN_PILOT_CLIENT_PRACTITIONER_EMAIL", "davidphaneuf@gmail.com")
_PILOT_ADMIN_EMAIL = os.getenv("MERLIN_PILOT_ADMIN_EMAIL", "lagent009@gmail.com")


def _resolve_pilot_recipient(to_email: str, audience: str = "client") -> tuple[str, str]:
    """Résout l'adresse de destination en mode pilote.

    Retourne (effective_to, prefix_for_subject).
    Si pilote désactivé, retourne (to_email, "").
    """
    if not _PILOT_OVERRIDE_ENABLED:
        return to_email, ""
    target = _PILOT_ADMIN_EMAIL if audience == "admin" else _PILOT_CLIENT_PRACTITIONER_EMAIL
    prefix = f"[PILOTE→{to_email}] "
    return target, prefix


async def send_email(
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str | None = None,
    audience: str = "client",
) -> bool:
    """Envoie un courriel. Retourne True si succès, False si erreur.

    En mode pilote (MERLIN_PILOT_EMAIL_OVERRIDE=1), redirige vers les Gmail
    de pilote selon l'audience : 'client'/'praticien' → davidphaneuf@gmail.com,
    'admin' → lagent009@gmail.com. L'objet du courriel est préfixé par
    [PILOTE→adresse_originale] pour traçabilité.
    """
    if not settings.smtp_username or not settings.smtp_password:
        logger.warning("SMTP non configuré — courriel non envoyé à %s", to_email)
        return False

    effective_to, subject_prefix = _resolve_pilot_recipient(to_email, audience)
    final_subject = f"{subject_prefix}{subject}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = final_subject
    msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    msg["To"] = effective_to
    msg["X-IVIA-Original-Recipient"] = to_email
    msg["X-IVIA-Audience"] = audience
    if _PILOT_OVERRIDE_ENABLED:
        msg["X-IVIA-Pilot-Mode"] = "1"

    if text_body:
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=settings.smtp_use_ssl,       # SSL immédiat (port 465)
            start_tls=settings.smtp_use_tls,     # STARTTLS (port 587)
        )
        if _PILOT_OVERRIDE_ENABLED and effective_to != to_email:
            logger.info(
                "Courriel pilote envoyé à %s (override depuis %s, audience=%s) — %s",
                effective_to, to_email, audience, subject,
            )
        else:
            logger.info("Courriel envoyé à %s — %s", effective_to, subject)
        return True
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Erreur envoi courriel à %s: %s", effective_to, exc)
        return False


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

_BASE_STYLE = """
<style>
  body { font-family: 'Helvetica Neue', Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 0; }
  .wrap { max-width: 560px; margin: 40px auto; background: #fff; border-radius: 12px;
          box-shadow: 0 2px 12px rgba(0,0,0,.08); overflow: hidden; }
  .header { background: #1a1a2e; padding: 32px 40px; }
  .header h1 { color: #fff; margin: 0; font-size: 22px; font-weight: 700; letter-spacing: .5px; }
  .header span { color: #a78bfa; }
  .body { padding: 32px 40px; color: #333; line-height: 1.6; }
  .btn { display: inline-block; margin: 24px 0 8px; padding: 14px 32px;
         background: #7c3aed; color: #fff !important; text-decoration: none;
         border-radius: 8px; font-weight: 600; font-size: 15px; }
  .footer { padding: 20px 40px; background: #fafafa; color: #888; font-size: 12px; border-top: 1px solid #eee; }
</style>
"""


def make_verification_email(display_name: str, verification_url: str) -> tuple[str, str]:
    """Retourne (html, text) pour le courriel de vérification d'adresse."""
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Merci de vous être inscrit·e sur la plateforme <strong>IVIA</strong>. Pour activer votre compte,
    veuillez confirmer votre adresse courriel en cliquant sur le bouton ci-dessous.</p>
    <a class="btn" href="{verification_url}">Confirmer mon adresse</a>
    <p style="color:#888;font-size:13px;">Ce lien est valide 24 heures. Si vous n'avez pas demandé ce compte, ignorez simplement ce message.</p>
  </div>
  <div class="footer">IVIA · Plateforme de soins intégrée · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Confirmez votre adresse courriel en visitant le lien suivant :\n"
        f"{verification_url}\n\n"
        "Ce lien est valide 24 heures.\n\n— IVIA"
    )
    return html, text


def make_booking_confirmation_email(
    display_name: str,
    praticien_name: str,
    slot_date: str,        # ex. "lundi 5 mai 2025"
    slot_time: str,        # ex. "14h00"
    session_type_label: str,  # ex. "Consultation standard (60 min)"
    cancel_url: str,
) -> tuple[str, str]:
    """Retourne (html, text) pour la confirmation de réservation."""
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Votre rendez-vous est confirmé !</p>
    <table style="width:100%;border-collapse:collapse;margin:16px 0;">
      <tr><td style="padding:8px 0;color:#888;width:140px;">Praticien·ne</td>
          <td style="padding:8px 0;font-weight:600;">{praticien_name}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Date</td>
          <td style="padding:8px 0;font-weight:600;">{slot_date}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Heure</td>
          <td style="padding:8px 0;font-weight:600;">{slot_time}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Type</td>
          <td style="padding:8px 0;">{session_type_label}</td></tr>
    </table>
    <p style="color:#888;font-size:13px;">Pour annuler ou modifier votre rendez-vous :</p>
    <a class="btn" href="{cancel_url}" style="background:#dc2626;">Annuler</a>
  </div>
  <div class="footer">IVIA · Plateforme de soins intégrée · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Votre rendez-vous est confirmé !\n\n"
        f"Praticien·ne : {praticien_name}\n"
        f"Date         : {slot_date}\n"
        f"Heure        : {slot_time}\n"
        f"Type         : {session_type_label}\n\n"
        f"Pour annuler : {cancel_url}\n\n— IVIA"
    )
    return html, text
