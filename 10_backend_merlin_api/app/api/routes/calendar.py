"""Calendar export routes (ICS format) + Stripe payment integration."""

import json
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone

from app.core.config import settings
from app.core.deps import get_db, require_client, require_practitioner
from app.services.ics_service import IcsExportService
from app.services.payment_service import StripePaymentService
from app.services.email import make_appointment_status_email, send_email
from app.models.appointment import Appointment
from app.models.app_user import AppUser
from app.schemas.payment import CheckoutRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/export.ics")
async def export_calendar_ics(
    current_user: AppUser = Depends(require_client()),
    db: Session = Depends(get_db)
) -> Response:
    """
    Export client's paid appointments as ICS calendar file.
    
    Returns:
        RFC 5545 ICS file (can be imported into Apple/Google/Outlook Calendar)
    """
    try:
        # Get client's paid and noted appointments
        appointments = db.query(Appointment).filter(
            Appointment.client_id == current_user.id,
            Appointment.status.in_(['paid', 'noted'])
        ).order_by(Appointment.start_time).all()
        
        if not appointments:
            logger.info(f"No paid appointments to export for client {current_user.id}")
        
        # Generate ICS
        ics_content = IcsExportService.generate_ics(
            appointments=appointments,
            calendar_name=f"IVIA - {current_user.display_name}",
            client_name=current_user.display_name
        )
        
        # Get filename
        filename = IcsExportService.get_export_filename(current_user.display_name)
        
        logger.info(f"Exported {len(appointments)} appointments for client {current_user.id}")
        
        return Response(
            content=ics_content,
            media_type="text/calendar; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Cache-Control": "no-cache, no-store, must-revalidate"
            }
        )
    except Exception as e:
        logger.error(f"Calendar export failed for client {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to export calendar")


@router.get("/practitioner/export.ics")
async def export_practitioner_calendar_ics(
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db)
) -> Response:
    """
    Export praticien's appointments (all statuses) as ICS calendar.
    
    Shows scheduled, confirmed, paid, and noted appointments.
    
    Returns:
        RFC 5545 ICS file
    """
    try:
        # Get praticien's appointments (all statuses except cancelled)
        appointments = db.query(Appointment).filter(
            Appointment.practitioner_id == current_user.id,
            Appointment.status != 'cancelled'
        ).order_by(Appointment.start_time).all()
        
        if not appointments:
            logger.info(f"No appointments to export for practitioner {current_user.id}")
        
        # Generate ICS
        ics_content = IcsExportService.generate_ics(
            appointments=appointments,
            calendar_name=f"IVIA - {current_user.display_name} (Agenda)",
            client_name=current_user.display_name
        )
        
        # Get filename
        filename = IcsExportService.get_export_filename(f"{current_user.display_name}_Agenda")
        
        logger.info(f"Exported {len(appointments)} appointments for practitioner {current_user.id}")
        
        return Response(
            content=ics_content,
            media_type="text/calendar; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Cache-Control": "no-cache, no-store, must-revalidate"
            }
        )
    except Exception as e:
        logger.error(f"Practitioner calendar export failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to export calendar")


@router.get("/export-format")
async def get_export_format_info() -> dict:
    """
    Get information about ICS export format and compatibility.
    
    Returns:
        Format info and instructions
    """
    return {
        "format": "iCalendar (RFC 5545)",
        "file_extension": "ics",
        "compatible_apps": [
            "Apple Calendar (macOS, iOS, iPad)",
            "Google Calendar (web, Android)",
            "Microsoft Outlook (Desktop, Web)",
            "Mozilla Thunderbird",
            "Any RFC 5545 compatible calendar app"
        ],
        "unidirectional": True,
        "description": "One-way export from IVIA to your calendar. Changes in external calendars won't sync back to IVIA.",
        "instructions": {
            "apple_calendar": [
                "Download the ICS file",
                "Double-click → Calendar app opens automatically",
                "Select calendar to import into",
                "Click 'Add'"
            ],
            "google_calendar": [
                "Download the ICS file",
                "Go to Google Calendar settings",
                "Click 'Import & Export' → 'Select file from your computer'",
                "Choose the ICS file and select target calendar"
            ],
            "outlook": [
                "Download the ICS file",
                "Open Outlook",
                "File → Open & Export → Import ICS file",
                "Select target calendar"
            ]
        }
    }


# ── PAYMENT ENDPOINTS ──────────────────────────────────────────────────────

@router.post("/checkout", status_code=status.HTTP_200_OK)
async def create_checkout_session(
    checkout_request: CheckoutRequest,
    current_user: AppUser = Depends(require_client()),
    db: Session = Depends(get_db)
) -> dict:
    """
    Create Stripe checkout session for appointment payment.
    
    Args:
        checkout_request: {appointment_id, amount_cents}
    
    Returns:
        {checkout_url: "https://checkout.stripe.com/pay/..."}
    """
    try:
        # Fetch appointment
        appointment = db.query(Appointment).filter(
            Appointment.id == checkout_request.appointment_id,
            Appointment.client_id == current_user.id
        ).first()
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        
        # Create Stripe session
        payment_service = StripePaymentService()
        stripe_session_id = payment_service.create_checkout_session(
            amount_cents=checkout_request.amount_cents,
            appointment_id=appointment.id,
            client_email=current_user.email,
            return_url=f"{settings.frontend_url}/client/appointment/{appointment.id}/success"
        )
        
        # Save stripe_session_id to appointment
        appointment.stripe_session_id = stripe_session_id
        appointment.amount_cents = checkout_request.amount_cents
        db.add(appointment)
        db.commit()
        
        logger.info(f"Stripe session created for appointment {appointment.id}: {stripe_session_id}")
        
        # Return Stripe checkout URL
        return {
            "checkout_url": f"https://checkout.stripe.com/pay/{stripe_session_id}"
        }
    except Exception as e:
        logger.error(f"Failed to create checkout session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session"
        )


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def handle_stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
) -> dict:
    """
    Handle Stripe webhook events (checkout.session.completed).
    
    Verifies webhook signature and updates appointment payment status.
    """
    try:
        # Read body
        body = await request.body()
        sig_header = request.headers.get("stripe-signature")
        
        # Verify and construct event
        payment_service = StripePaymentService()
        event = payment_service.construct_webhook_event(body, sig_header)
        
        logger.info(f"Stripe webhook received: {event['type']}")
        
        if event["type"] == "checkout.session.completed":
            session_data = event["data"]["object"]
            payment_info = payment_service.handle_checkout_completed(session_data)
            
            # Find appointment by stripe_session_id
            appointment = db.query(Appointment).filter(
                Appointment.stripe_session_id == session_data["id"]
            ).first()
            
            if appointment:
                # Update appointment status to paid
                appointment.status = "paid"
                appointment.paid_at = datetime.now(timezone.utc)
                appointment.amount_cents = payment_info.get("amount_cents")
                appointment.payment_intent_id = payment_info.get("payment_intent_id")
                db.add(appointment)
                db.commit()
                
                logger.info(f"Appointment {appointment.id} marked as paid")
                
                # Send payment confirmation email (non-blocking)
                try:
                    client = db.query(AppUser).filter(
                        AppUser.id == appointment.client_id
                    ).first()
                    
                    if client:
                        made = make_appointment_status_email(
                            display_name=client.display_name or "Client",
                            status_code="paid",
                        )
                        if made:
                            html, text = made
                            await send_email(
                                to_email=client.email,
                                subject="Paiement reçu — IVIA",
                                html_body=html,
                                text_body=text,
                            )
                except Exception as e:
                    logger.error(f"Failed to send payment email: {e}")
        
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Webhook handling failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook verification failed"
        )
