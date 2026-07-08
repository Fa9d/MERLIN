"""Stripe payment processing service."""

import stripe
from typing import Optional
import logging
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)

stripe.api_key = settings.stripe_secret_key


class StripePaymentService:
    """Manages Stripe checkout sessions, payment verification, and webhooks."""
    
    @staticmethod
    def create_checkout_session(
        amount_cents: int,
        appointment_id: str,
        client_email: str,
        client_name: Optional[str] = None,
        practitioner_name: Optional[str] = None
    ) -> str:
        """
        Create Stripe checkout session for appointment payment.
        
        Args:
            amount_cents: Amount in cents (e.g., 3500 = $35.00 CAD)
            appointment_id: UUID of appointment
            client_email: Client email address
            client_name: Client display name
            practitioner_name: Practitioner name for invoice
        
        Returns:
            Stripe session ID
        
        Raises:
            Exception: If session creation fails
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'cad',
                        'product_data': {
                            'name': f'Séance — {practitioner_name or "IVIA"}',
                            'description': f'Appointment {appointment_id}'
                        },
                        'unit_amount': amount_cents
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=f"{settings.frontend_url}/client/seances.html?payment=success&appointment_id={appointment_id}",
                cancel_url=f"{settings.frontend_url}/client/agenda.html?payment=cancelled",
                customer_email=client_email,
                metadata={
                    'appointment_id': appointment_id,
                    'client_name': client_name or 'unknown'
                }
            )
            logger.info(f"Created Stripe session {session.id} for appointment {appointment_id}")
            return session.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe session creation failed: {e}")
            raise Exception(f"Failed to create payment session: {str(e)}")
    
    @staticmethod
    def verify_payment(session_id: str) -> dict:
        """
        Verify payment completion by checking session status.
        
        Args:
            session_id: Stripe session ID
        
        Returns:
            Dict with: {
                'paid': bool,
                'amount_total': int (cents),
                'currency': str,
                'customer_email': str,
                'payment_intent_id': str,
                'metadata': dict
            }
        
        Raises:
            Exception: If verification fails
        """
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            result = {
                'paid': session.payment_status == 'paid',
                'amount_total': session.amount_total,
                'currency': session.currency,
                'customer_email': session.customer_email,
                'payment_intent_id': session.payment_intent,
                'metadata': session.metadata or {}
            }
            
            logger.info(f"Verified Stripe session {session_id}: paid={result['paid']}")
            return result
        except stripe.error.StripeError as e:
            logger.error(f"Stripe verification failed for {session_id}: {e}")
            raise Exception(f"Failed to verify payment: {str(e)}")
    
    @staticmethod
    def refund_payment(payment_intent_id: str, amount_cents: Optional[int] = None) -> bool:
        """
        Refund a payment (full or partial).
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount_cents: Amount to refund (None = full refund)
        
        Returns:
            True if refund succeeded
        
        Raises:
            Exception: If refund fails
        """
        try:
            refund_params = {'payment_intent': payment_intent_id}
            if amount_cents:
                refund_params['amount'] = amount_cents
            
            refund = stripe.Refund.create(**refund_params)
            logger.info(f"Created refund {refund.id} for payment intent {payment_intent_id}")
            return refund.status == 'succeeded'
        except stripe.error.StripeError as e:
            logger.error(f"Stripe refund failed: {e}")
            raise Exception(f"Failed to refund payment: {str(e)}")
    
    @staticmethod
    def construct_webhook_event(payload: bytes, sig_header: str) -> dict:
        """
        Verify and construct webhook event from Stripe signature.
        
        Args:
            payload: Raw request body
            sig_header: Stripe-Signature header value
        
        Returns:
            Verified event dict
        
        Raises:
            ValueError: If signature verification fails
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.stripe_webhook_secret
            )
            logger.info(f"Verified Stripe webhook event: {event['type']}")
            return event
        except ValueError as e:
            logger.error(f"Webhook signature verification failed: {e}")
            raise ValueError(f"Invalid webhook signature: {str(e)}")
        except stripe.error.StripeError as e:
            logger.error(f"Webhook construction failed: {e}")
            raise ValueError(f"Failed to construct webhook event: {str(e)}")
    
    @staticmethod
    def handle_checkout_completed(session_data: dict) -> dict:
        """
        Extract appointment payment info from completed checkout session.
        
        Args:
            session_data: Stripe session data dict
        
        Returns:
            Dict with: {
                'appointment_id': str,
                'amount_paid': int (cents),
                'payment_intent_id': str,
                'paid_at': datetime
            }
        """
        return {
            'appointment_id': session_data['metadata'].get('appointment_id'),
            'amount_paid': session_data.get('amount_total'),
            'payment_intent_id': session_data.get('payment_intent'),
            'paid_at': datetime.utcnow()
        }
