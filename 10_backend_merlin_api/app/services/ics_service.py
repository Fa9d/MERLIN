"""ICS calendar export service for Apple/Google Calendar compatibility."""

from ics import Calendar, Event
from datetime import datetime, timezone
from typing import List, Optional
import logging

from app.models.appointment import Appointment

logger = logging.getLogger(__name__)


class IcsExportService:
    """Generates RFC-compliant ICS calendar files for appointments."""
    
    @staticmethod
    def generate_ics(
        appointments: List[Appointment],
        calendar_name: str = "IVIA Appointments",
        client_name: Optional[str] = None
    ) -> str:
        """
        Generate ICS (iCalendar) file from appointments.
        
        Args:
            appointments: List of Appointment objects
            calendar_name: Calendar title
            client_name: Client name for personalization
        
        Returns:
            RFC 5545 compliant ICS string
        """
        cal = Calendar()
        
        # Set calendar properties
        cal.name = calendar_name
        cal.prodid = '-//IVIA//Maison du Vivant//FR'  # RFC 5545 Product ID
        cal.version = '2.0'
        
        for appt in appointments:
            event = Event()
            
            # Event properties
            event.name = f"Séance avec {appt.practitioner.display_name}"
            event.begin = appt.start_time
            event.end = appt.end_time
            
            # Description includes status
            status_text = {
                'scheduled': 'Confirmée',
                'confirmed': 'Confirmée par praticien',
                'paid': 'Payée',
                'noted': 'Notes de séance disponibles'
            }.get(appt.status, appt.status)
            
            event.description = f"Statut: {status_text}\nRéférence: {appt.id}"
            
            # Location
            event.location = "IVIA — Maison du Vivant"
            
            # UID for RFC compliance (allows proper calendar updates)
            event.uid = f"{appt.id}@ivia.quebec"
            
            # Timestamps
            event.created = appt.created_at
            event.last_modified = appt.updated_at
            
            # Add event to calendar
            cal.events.add(event)
        
        logger.info(f"Generated ICS calendar with {len(appointments)} appointments")
        return cal.serialize()
    
    @staticmethod
    def get_export_filename(client_name: Optional[str] = None) -> str:
        """
        Generate filename for ICS export.
        
        Args:
            client_name: Client name for filename
        
        Returns:
            Filename (e.g., "IVIA_Calendar_Jean_Dupont_2026-07-03.ics")
        """
        now = datetime.now().strftime("%Y-%m-%d")
        if client_name:
            # Remove special chars from name
            safe_name = "".join(c if c.isalnum() or c in "-_ " else "" for c in client_name)
            return f"IVIA_Calendar_{safe_name}_{now}.ics"
        return f"IVIA_Calendar_{now}.ics"
    
    @staticmethod
    def validate_ics(ics_content: str) -> bool:
        """
        Validate ICS content format.
        
        Args:
            ics_content: ICS string
        
        Returns:
            True if valid RFC 5545 format
        """
        try:
            # Try to parse the ICS content
            Calendar(ics_content)
            logger.info("ICS validation passed")
            return True
        except Exception as e:
            logger.error(f"ICS validation failed: {e}")
            return False
    
    @staticmethod
    def generate_ics_event_only(
        appointment: Appointment,
        include_description: bool = True
    ) -> str:
        """
        Generate ICS for single appointment (useful for email attachments).
        
        Args:
            appointment: Appointment object
            include_description: Whether to include full description
        
        Returns:
            RFC 5545 compliant ICS string (single event)
        """
        cal = Calendar()
        cal.name = "IVIA Appointment"
        cal.prodid = '-//IVIA//Maison du Vivant//FR'
        
        event = Event()
        event.name = f"Séance avec {appointment.practitioner.display_name}"
        event.begin = appointment.start_time
        event.end = appointment.end_time
        event.uid = f"{appointment.id}@ivia.quebec"
        event.location = "IVIA — Maison du Vivant"
        
        if include_description:
            event.description = f"Rendez-vous praticien: {appointment.practitioner.display_name}"
        
        cal.events.add(event)
        
        logger.info(f"Generated single-event ICS for appointment {appointment.id}")
        return cal.serialize()


class IcsImportHelper:
    """Helpers for ICS import (reference only — imports are client-side)."""
    
    @staticmethod
    def get_google_calendar_import_url(ics_url: str) -> str:
        """
        Get Google Calendar import URL.
        
        Args:
            ics_url: URL to ICS file
        
        Returns:
            Google Calendar import URL
        """
        return f"https://calendar.google.com/calendar/u/0/r/settings/addbyurl?url={ics_url}"
    
    @staticmethod
    def get_apple_calendar_instructions() -> str:
        """Get instructions for Apple Calendar import."""
        return """
Apple Calendar (macOS/iOS):
1. Download the ICS file
2. Double-click the file → Calendar app opens
3. Select calendar to import into
4. Click "Add" to confirm

Or email the ICS file to yourself and open in Calendar app.
        """
