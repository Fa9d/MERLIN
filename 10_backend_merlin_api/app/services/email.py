"""Service d'envoi de courriels via SMTP (SSL)."""
from __future__ import annotations

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str | None = None,
) -> bool:
    """Envoie un courriel. Retourne True si succès, False si erreur."""
    if not settings.smtp_username or not settings.smtp_password:
        logger.warning("SMTP non configuré — courriel non envoyé à %s", to_email)
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    msg["To"] = to_email

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
        logger.info("Courriel envoyé à %s — %s", to_email, subject)
        return True
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Erreur envoi courriel à %s: %s", to_email, exc)
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
