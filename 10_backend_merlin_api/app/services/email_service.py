"""Email notification service for bookings and status updates."""

import logging
from typing import Optional, List
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Sends transactional emails via SMTP (OVH)."""
    
    @staticmethod
    def send_booking_confirmation(
        client_email: str,
        client_name: str,
        practitioner_name: str,
        appointment_start: datetime,
        appointment_id: str,
        duration_minutes: int = 60
    ) -> bool:
        """
        Send booking confirmation email to client.
        
        Args:
            client_email: Client email address
            client_name: Client display name
            practitioner_name: Practitioner name
            appointment_start: Appointment start time
            appointment_id: Appointment UUID
            duration_minutes: Session duration
        
        Returns:
            True if email sent successfully
        """
        try:
            # Format appointment details
            start_fmt = appointment_start.strftime("%d %B %Y à %H:%M")
            duration_fmt = f"{duration_minutes} minutes" if duration_minutes else "durée variable"
            
            # HTML email body
            html_content = f"""
            <html>
                <body style="font-family: 'Raleway', sans-serif; color: #1A2E1D; background: #F0F7F2; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; border: 1px solid #D4E8D0;">
                        <h2 style="color: #2D6A4F; margin-bottom: 20px;">✓ Réservation confirmée</h2>
                        
                        <p>Bonjour {client_name},</p>
                        
                        <p>Votre séance a été réservée avec succès!</p>
                        
                        <div style="background: #F0F7F2; padding: 15px; border-left: 4px solid #2D6A4F; margin: 20px 0;">
                            <p style="margin: 5px 0;"><strong>Praticien:</strong> {practitioner_name}</p>
                            <p style="margin: 5px 0;"><strong>Date et heure:</strong> {start_fmt}</p>
                            <p style="margin: 5px 0;"><strong>Durée:</strong> {duration_fmt}</p>
                            <p style="margin: 5px 0;"><strong>Référence:</strong> {appointment_id}</p>
                        </div>
                        
                        <p><a href="https://ivia.quebec/client/seances.html" style="color: #2D6A4F; text-decoration: none; font-weight: bold;">→ Voir vos séances</a></p>
                        
                        <hr style="border: none; border-top: 1px solid #D4E8D0; margin: 30px 0;">
                        
                        <p style="color: #4B6350; font-size: 13px;">
                            IVIA — Maison du Vivant<br>
                            Pour toute question, contactez-nous à support@ivia.quebec
                        </p>
                    </div>
                </body>
            </html>
            """
            
            # Plain text fallback
            text_content = f"""
Réservation confirmée

Bonjour {client_name},

Votre séance a été réservée avec succès!

Praticien: {practitioner_name}
Date et heure: {start_fmt}
Durée: {duration_fmt}
Référence: {appointment_id}

Voir vos séances: https://ivia.quebec/client/seances.html

---
IVIA — Maison du Vivant
support@ivia.quebec
            """
            
            return EmailService._send_smtp(
                to_email=client_email,
                subject="Confirmation de votre réservation IVIA",
                html_body=html_content,
                text_body=text_content
            )
        except Exception as e:
            logger.error(f"Failed to send booking confirmation to {client_email}: {e}")
            return False
    
    @staticmethod
    def send_payment_confirmation(
        client_email: str,
        client_name: str,
        amount: float,
        appointment_id: str
    ) -> bool:
        """
        Send payment confirmation email.
        
        Args:
            client_email: Client email
            client_name: Client name
            amount: Amount paid (in CAD)
            appointment_id: Appointment UUID
        
        Returns:
            True if sent successfully
        """
        try:
            html_content = f"""
            <html>
                <body style="font-family: 'Raleway', sans-serif; color: #1A2E1D; background: #F0F7F2; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; border: 1px solid #D4E8D0;">
                        <h2 style="color: #2D6A4F; margin-bottom: 20px;">✓ Paiement confirmé</h2>
                        
                        <p>Bonjour {client_name},</p>
                        
                        <p>Votre paiement a été traité avec succès.</p>
                        
                        <div style="background: #F0F7F2; padding: 15px; border-left: 4px solid #2D6A4F; margin: 20px 0;">
                            <p style="margin: 5px 0;"><strong>Montant payé:</strong> ${amount:.2f} CAD</p>
                            <p style="margin: 5px 0;"><strong>Référence:</strong> {appointment_id}</p>
                            <p style="margin: 5px 0;"><strong>Date:</strong> {datetime.now().strftime("%d %B %Y")}</p>
                        </div>
                        
                        <p><a href="https://ivia.quebec/client/seances.html" style="color: #2D6A4F; text-decoration: none; font-weight: bold;">→ Voir vos séances</a></p>
                        
                        <hr style="border: none; border-top: 1px solid #D4E8D0; margin: 30px 0;">
                        
                        <p style="color: #4B6350; font-size: 13px;">
                            IVIA — Maison du Vivant<br>
                            Pour toute question, contactez-nous à support@ivia.quebec
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailService._send_smtp(
                to_email=client_email,
                subject="Paiement confirmé — IVIA",
                html_body=html_content
            )
        except Exception as e:
            logger.error(f"Failed to send payment confirmation to {client_email}: {e}")
            return False
    
    @staticmethod
    def send_status_update(
        client_email: str,
        client_name: str,
        status: str,
        practitioner_name: Optional[str] = None
    ) -> bool:
        """
        Send appointment status update.
        
        Args:
            client_email: Client email
            client_name: Client name
            status: New status (confirmed, paid, noted)
            practitioner_name: Practitioner name
        
        Returns:
            True if sent successfully
        """
        try:
            status_messages = {
                'confirmed': ('Confirmée', 'Votre séance a été confirmée par le praticien.'),
                'paid': ('Payée', 'Paiement confirmé. Votre séance est réservée.'),
                'noted': ('Notes prêtes', 'Les notes de votre séance sont maintenant disponibles.')
            }
            
            status_title, status_msg = status_messages.get(status, (status, ''))
            
            html_content = f"""
            <html>
                <body style="font-family: 'Raleway', sans-serif; color: #1A2E1D; background: #F0F7F2; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; border: 1px solid #D4E8D0;">
                        <h2 style="color: #2D6A4F; margin-bottom: 20px;">✓ Mise à jour: {status_title}</h2>
                        
                        <p>Bonjour {client_name},</p>
                        
                        <p>{status_msg}</p>
                        
                        {f'<p><strong>Praticien:</strong> {practitioner_name}</p>' if practitioner_name else ''}
                        
                        <p><a href="https://ivia.quebec/client/seances.html" style="color: #2D6A4F; text-decoration: none; font-weight: bold;">→ Voir vos séances</a></p>
                        
                        <hr style="border: none; border-top: 1px solid #D4E8D0; margin: 30px 0;">
                        
                        <p style="color: #4B6350; font-size: 13px;">
                            IVIA — Maison du Vivant<br>
                            support@ivia.quebec
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailService._send_smtp(
                to_email=client_email,
                subject=f"Mise à jour: Séance {status_title.lower()} — IVIA",
                html_body=html_content
            )
        except Exception as e:
            logger.error(f"Failed to send status update to {client_email}: {e}")
            return False
    
    @staticmethod
    def _send_smtp(
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send email via SMTP (OVH).
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text fallback
            cc: CC addresses
            bcc: BCC addresses
        
        Returns:
            True if sent successfully
        """
        try:
            # Build MIME message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.MAIL_FROM
            msg['To'] = to_email
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Attach text and HTML
            if text_body:
                msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Send via SMTP
            with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
                server.starttls()
                server.login(settings.MAIL_FROM, settings.MAIL_PASSWORD)
                
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                server.sendmail(settings.MAIL_FROM, recipients, msg.as_string())
            
            logger.info(f"Email sent to {to_email}: {subject}")
            return True
        except Exception as e:
            logger.error(f"SMTP send failed to {to_email}: {e}")
            return False
