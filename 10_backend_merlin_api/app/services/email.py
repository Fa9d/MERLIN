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


def make_magic_link_email(
    display_name: str,
    magic_link_url: str,
    ttl_days: int = 7,
) -> tuple[str, str]:
    """Lien magique post-intake : un clic, le compte est actif, l'espace membre s'ouvre."""
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Nous avons bien reçu votre demande. Pour ouvrir votre espace IVIA et poursuivre votre démarche, cliquez sur le bouton ci-dessous.</p>
    <a class="btn" href="{magic_link_url}">Ouvrir mon espace IVIA</a>
    <p style="color:#888;font-size:13px;">Ce lien est valide {ttl_days} jours. Vous pourrez ensuite, si vous le souhaitez, définir un mot de passe pour revenir facilement.</p>
    <p style="color:#888;font-size:13px;">Si vous n'êtes pas à l'origine de cette demande, ignorez ce message — aucun compte n'est activé tant que le lien n'est pas suivi.</p>
  </div>
  <div class="footer">IVIA · Maison du vivant · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Nous avons bien reçu votre demande. Pour ouvrir votre espace IVIA "
        "et poursuivre votre démarche, suivez ce lien :\n"
        f"{magic_link_url}\n\n"
        f"Ce lien est valide {ttl_days} jours.\n\n"
        "— IVIA"
    )
    return html, text


def make_appointment_reminder_email(
    display_name: str,
    praticien_name: str,
    slot_date: str,
    slot_time: str,
    session_type_label: str,
    join_url: str,
) -> tuple[str, str]:
    """Rappel 24h avant le rendez-vous."""
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Votre rendez-vous est <strong>demain</strong> — voici un rappel.</p>
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
    <a class="btn" href="{join_url}">Accéder à ma séance</a>
    <p style="color:#888;font-size:13px;">Si vous ne pouvez pas vous présenter, contactez votre praticien·ne ou annulez depuis votre espace IVIA.</p>
  </div>
  <div class="footer">IVIA · Maison du vivant · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Votre rendez-vous est demain !\n\n"
        f"Praticien·ne : {praticien_name}\n"
        f"Date         : {slot_date}\n"
        f"Heure        : {slot_time}\n"
        f"Type         : {session_type_label}\n\n"
        f"Accéder à votre séance : {join_url}\n\n— IVIA"
    )
    return html, text


def make_appointment_status_email(
    display_name: str,
    status_code: str,
    praticien_name: str | None = None,
) -> tuple[str, str] | None:
    """Notification de changement de statut d'un rendez-vous.

    Retourne None si le statut ne mérite pas de courriel (ex. scheduled).
    Vocabulaire non clinique (Loi 21) — jamais de contenu par courriel.
    """
    messages = {
        "confirmed": ("Rendez-vous confirmé", "Votre praticien·ne a confirmé votre rendez-vous."),
        "paid": ("Paiement reçu", "Votre paiement a bien été reçu — votre séance est réservée."),
        "noted": ("Un écho vous attend", "Un nouvel écho de votre séance est disponible dans votre espace."),
        "cancelled": ("Rendez-vous annulé", "Votre rendez-vous a été annulé. Vous pouvez en réserver un autre depuis votre espace."),
    }
    if status_code not in messages:
        return None
    title, msg = messages[status_code]
    praticien_line = (
        f'<p style="color:#888;">Praticien·ne : <strong>{praticien_name}</strong></p>'
        if praticien_name else ""
    )
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>{msg}</p>
    {praticien_line}
    <a class="btn" href="https://ivia.quebec/client/agenda.html">Ouvrir mon espace</a>
    <p style="color:#888;font-size:13px;">Pour votre confidentialité, aucun contenu n'est transmis
       par courriel — tout reste dans votre espace sécurisé, hébergé au Québec.</p>
  </div>
  <div class="footer">IVIA · Maison du vivant · ivia.quebec</div>
</div>
</body></html>"""
    text = (
        f"Bonjour {display_name},\n\n{title} — {msg}\n"
        + (f"Praticien·ne : {praticien_name}\n" if praticien_name else "")
        + "\nOuvrir mon espace : https://ivia.quebec/client/agenda.html\n\n— IVIA"
    )
    return html, text


def make_practitioner_reply_email(
    display_name: str,
    login_url: str,
) -> tuple[str, str]:
    """Notification : un·e praticien·ne a déposé un élément dans l'espace du client.

    Notification seule — jamais le contenu (confidentialité Loi 25). Vocabulaire
    non clinique (Loi 21) : « écho », « espace », pas « analyse / note clinique ».
    """
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Votre praticien·ne IVIA vous a <strong>répondu</strong> : un nouvel écho à votre
       dernière rencontre vient d'être déposé dans votre espace.</p>
    <a class="btn" href="{login_url}">Ouvrir mon espace</a>
    <p style="color:#888;font-size:13px;">Pour votre confidentialité, le contenu n'est jamais
       transmis par courriel — il reste dans votre espace sécurisé, hébergé au Québec.</p>
  </div>
  <div class="footer">IVIA · Maison du vivant · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Votre praticien·ne IVIA vous a répondu : un nouvel écho à votre dernière "
        "rencontre vient d'être déposé dans votre espace.\n\n"
        f"Ouvrir mon espace : {login_url}\n\n"
        "Pour votre confidentialité, le contenu n'est jamais transmis par courriel.\n\n— IVIA"
    )
    return html, text


def make_interac_etransfer_email(
    display_name: str,
    recipient_name: str,
    recipient_email: str,
    transfer_reference: str,
    amount_cents: int,
    currency: str,
    instructions_text: str,
) -> tuple[str, str]:
    amount = f"{amount_cents / 100:.2f} {currency.upper()}"
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Votre demande de paiement par <strong>Interac e-Transfer</strong> est prête.</p>
    <table style="width:100%;border-collapse:collapse;margin:16px 0;">
      <tr><td style="padding:8px 0;color:#888;width:160px;">Montant</td>
          <td style="padding:8px 0;font-weight:600;">{amount}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Destinataire</td>
          <td style="padding:8px 0;font-weight:600;">{recipient_name}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Courriel Interac</td>
          <td style="padding:8px 0;font-weight:600;">{recipient_email}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Reference</td>
          <td style="padding:8px 0;font-weight:600;">{transfer_reference}</td></tr>
    </table>
    <p>{instructions_text}</p>
    <p style="color:#888;font-size:13px;">Important: indiquez exactement la reference <strong>{transfer_reference}</strong> dans le message du virement pour accelerer la reconciliation.</p>
  </div>
  <div class="footer">IVIA · Plateforme de soins intégrée · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Votre demande de paiement par Interac e-Transfer est prête.\n\n"
        f"Montant        : {amount}\n"
        f"Destinataire   : {recipient_name}\n"
        f"Courriel       : {recipient_email}\n"
        f"Reference      : {transfer_reference}\n\n"
        f"{instructions_text}\n\n"
        f"Utilisez la reference {transfer_reference} dans le message du virement.\n\n— IVIA"
    )
    return html, text


def make_followup_reminder_email(
    display_name: str,
    login_url: str,
    custom_message: str | None = None,
) -> tuple[str, str]:
    """Courriel de relance envoyé par un praticien pour inviter le client à reprendre son chemin.

    Ton chaleureux, non clinique (Loi 21). Le contenu reste dans l'espace — jamais
    dans le courriel (confidentialité Loi 25).
    """
    custom_block = ""
    custom_text_block = ""
    if custom_message:
        custom_block = f'<p style="background:#f8f8f8;border-left:3px solid #4a4a4a;padding:12px;border-radius:4px;font-style:italic;">{custom_message}</p>'
        custom_text_block = f"\n\nMessage de votre praticien·ne :\n{custom_message}"

    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Votre praticien·ne IVIA pense à vous et vous invite à reprendre votre chemin
       quand vous vous sentez prêt·e.</p>
    {custom_block}
    <p>Votre espace vous attend, à votre rythme.</p>
    <a class="btn" href="{login_url}">Reprendre mon chemin</a>
    <p style="color:#888;font-size:13px;">Pour votre confidentialité, aucun contenu n'est
       transmis par courriel — votre espace est sécurisé et hébergé au Québec.</p>
  </div>
  <div class="footer">IVIA · Maison du vivant · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Votre praticien·ne IVIA pense à vous et vous invite à reprendre votre chemin "
        "quand vous vous sentez prêt·e."
        f"{custom_text_block}\n\n"
        f"Reprendre mon chemin : {login_url}\n\n"
        "Pour votre confidentialité, aucun contenu n'est transmis par courriel.\n\n— IVIA"
    )
    return html, text


def make_practitioner_direct_email(
    display_name: str,
    practitioner_name: str,
    message: str,
    login_url: str,
) -> tuple[str, str]:
    """Courriel libre rédigé par un praticien pour son client, depuis la fiche client.

    Paramètres : nom d'affichage du client, nom du praticien, message libre
    (échappé — texte saisi par le praticien), URL de connexion à l'espace.
    Sortie : tuple (html, text).
    Le message est celui du praticien ; le gabarit n'ajoute aucun vocabulaire
    clinique (Loi 21) et rappelle que l'espace sécurisé reste le lieu des contenus
    sensibles (Loi 25).
    """
    from html import escape

    message_html = escape(message).replace("\n", "<br>")

    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{escape(display_name)}</strong>,</p>
    <p><strong>{escape(practitioner_name)}</strong>, votre praticien·ne d'écoute IVIA,
       vous a écrit :</p>
    <p style="background:#f8f8f8;border-left:3px solid #4a4a4a;padding:12px;border-radius:4px;">{message_html}</p>
    <a class="btn" href="{login_url}">Ouvrir mon espace</a>
    <p style="color:#888;font-size:13px;">Pour votre confidentialité, les documents et
       contenus de séance restent dans votre espace sécurisé, hébergé au Québec.
       En cas de détresse, appelez le 811 option 2, ou le 988 (24/7).</p>
  </div>
  <div class="footer">IVIA · Maison du vivant · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        f"{practitioner_name}, votre praticien·ne d'écoute IVIA, vous a écrit :\n\n"
        f"{message}\n\n"
        f"Ouvrir mon espace : {login_url}\n\n"
        "Pour votre confidentialité, les documents et contenus de séance restent "
        "dans votre espace sécurisé.\n"
        "En cas de détresse : 811 option 2, ou 988 (24/7).\n\n— IVIA"
    )
    return html, text


def make_reprise_lien_email(display_name: str, reserve_url: str) -> tuple[str, str]:
    """Courriel de reprise de lien 48 h après une demande d'entrée restée sans suite.

    Ton chaleureux, sans pression, non clinique (Loi 21). Une seule relance,
    un seul geste proposé : réserver un moment d'écoute. Aucun contenu personnel
    dans le courriel (Loi 25).
    """
    html = f"""<!DOCTYPE html><html><head>{_BASE_STYLE}</head><body>
<div class="wrap">
  <div class="header"><h1>IVI<span>A</span></h1></div>
  <div class="body">
    <p>Bonjour <strong>{display_name}</strong>,</p>
    <p>Il y a deux jours, vous avez ouvert une porte chez IVIA. Elle est toujours ouverte.</p>
    <p>Faire une place pour soi n'est pas toujours simple — il n'y a aucune presse.
       Quand le moment sera bon pour vous, un moment d'écoute vous attend,
       avec une personne qui écoute pour vrai.</p>
    <a class="btn" href="{reserve_url}">Réserver mon moment d'écoute</a>
    <p style="color:#888;font-size:13px;">Ce courriel est la seule relance que vous recevrez.
       Si vous préférez ne pas donner suite, vous n'avez rien à faire.
       En cas de détresse, appelez le 811 option 2, ou le 988 (24/7).</p>
  </div>
  <div class="footer">IVIA · Maison du vivant · ivia.quebec</div>
</div>
</body></html>"""

    text = (
        f"Bonjour {display_name},\n\n"
        "Il y a deux jours, vous avez ouvert une porte chez IVIA. Elle est toujours ouverte.\n\n"
        "Faire une place pour soi n'est pas toujours simple — il n'y a aucune presse. "
        "Quand le moment sera bon pour vous, un moment d'écoute vous attend, "
        "avec une personne qui écoute pour vrai.\n\n"
        f"Réserver mon moment d'écoute : {reserve_url}\n\n"
        "Ce courriel est la seule relance que vous recevrez. "
        "Si vous préférez ne pas donner suite, vous n'avez rien à faire.\n"
        "En cas de détresse : 811 option 2, ou 988 (24/7).\n\n— IVIA"
    )
    return html, text

