import json
import logging
from datetime import datetime, timedelta, timezone

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import SessionChannelCode, SessionModeCode, SessionStatusCode
from app.models.intake_request import IntakeRequest
from app.models.session import SessionRecord
from app.schemas.payment import (
    StripeAudioAsyncCheckoutCreate,
    StripeCheckoutSessionRead,
    StripeWebhookAck,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments/stripe", tags=["payments"])


def _ensure_stripe_config() -> None:
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MERLIN_STRIPE_SECRET_KEY est absent.",
        )


def _resolve_checkout_urls(payload: StripeAudioAsyncCheckoutCreate) -> tuple[str, str]:
    success_url = (
        payload.success_url
        or settings.stripe_checkout_success_url
        or f"{settings.frontend_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}"
    )
    cancel_url = payload.cancel_url or settings.stripe_checkout_cancel_url or f"{settings.frontend_url}/checkout/cancel"
    return success_url, cancel_url


@router.post(
    "/checkout/audio-async",
    response_model=StripeCheckoutSessionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_audio_async_checkout_session(
    payload: StripeAudioAsyncCheckoutCreate,
    db: Session = Depends(get_db),
) -> StripeCheckoutSessionRead:
    _ensure_stripe_config()

    client = db.get(Client, payload.client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    operator = db.get(AppUser, payload.operator_user_id)
    if operator is None or operator.role not in {"operator", "practitioner", "supervisor"}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operateur/praticien introuvable.",
        )

    if payload.intake_request_id is not None:
        intake_request = db.get(IntakeRequest, payload.intake_request_id)
        if intake_request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Demande d'entree introuvable.",
            )
        if intake_request.client_id != payload.client_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le client et la demande d'entree ne correspondent pas.",
            )

    success_url, cancel_url = _resolve_checkout_urls(payload)

    stripe.api_key = settings.stripe_secret_key
    checkout_session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": settings.stripe_audio_async_currency,
                    "unit_amount": settings.stripe_audio_async_amount_cents,
                    "product_data": {
                        "name": "MERLIN Audio Async",
                        "description": "Analyse professionnelle personnalisee + reponse praticien",
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={
            "flow": "audio_async",
            "client_id": payload.client_id,
            "operator_user_id": payload.operator_user_id,
            "intake_request_id": payload.intake_request_id or "",
            "session_mode_code": payload.session_mode_code.value,
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return StripeCheckoutSessionRead(
        checkout_session_id=checkout_session.id,
        checkout_url=checkout_session.url,
        amount_cents=settings.stripe_audio_async_amount_cents,
        currency=settings.stripe_audio_async_currency,
    )


@router.post("/webhook", response_model=StripeWebhookAck)
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
) -> StripeWebhookAck:
    _ensure_stripe_config()
    stripe.api_key = settings.stripe_secret_key

    payload_bytes = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        if settings.stripe_webhook_secret:
            event = stripe.Webhook.construct_event(
                payload=payload_bytes,
                sig_header=sig_header,
                secret=settings.stripe_webhook_secret,
            )
        else:
            raw_event = json.loads(payload_bytes.decode("utf-8"))
            event = stripe.Event.construct_from(raw_event, stripe.api_key)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Webhook Stripe invalide: %s", exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Webhook invalide.") from exc

    event_type = event.type
    if event_type != "checkout.session.completed":
        return StripeWebhookAck(status="ignored")

    checkout_data = event.data.object
    if checkout_data.payment_status != "paid":
        return StripeWebhookAck(status="ignored")

    _raw_metadata = checkout_data.metadata
    metadata: dict = _raw_metadata.to_dict() if _raw_metadata else {}
    if metadata.get("flow") != "audio_async":
        return StripeWebhookAck(status="ignored")

    client_id = metadata.get("client_id")
    operator_user_id = metadata.get("operator_user_id")
    intake_request_id = metadata.get("intake_request_id") or None
    raw_session_mode_code = metadata.get("session_mode_code") or SessionModeCode.follow_up.value
    try:
        session_mode_code = SessionModeCode(raw_session_mode_code)
    except ValueError:
        session_mode_code = SessionModeCode.follow_up

    if not client_id or not operator_user_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Metadata Stripe incomplete pour creer la session.",
        )

    now_utc = datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(hours=24)
    existing_session = db.scalar(
        select(SessionRecord)
        .where(SessionRecord.client_id == client_id)
        .where(SessionRecord.operator_user_id == operator_user_id)
        .where(SessionRecord.session_channel_code == SessionChannelCode.audio_async)
        .where(SessionRecord.intake_request_id == intake_request_id)
        .where(SessionRecord.created_at >= cutoff)
        .order_by(SessionRecord.created_at.desc())
    )
    if existing_session is not None:
        return StripeWebhookAck(status="already_processed", session_id=existing_session.id)

    latest_sequence_number = db.scalar(
        select(func.max(SessionRecord.session_sequence_number)).where(
            SessionRecord.client_id == client_id
        )
    )

    session_record = SessionRecord(
        client_id=client_id,
        intake_request_id=intake_request_id,
        session_sequence_number=(latest_sequence_number or 0) + 1,
        session_mode_code=session_mode_code,
        session_channel_code=SessionChannelCode.audio_async,
        session_status_code=SessionStatusCode.pending_review,
        operator_user_id=operator_user_id,
    )
    db.add(session_record)
    db.commit()
    db.refresh(session_record)

    return StripeWebhookAck(status="created", session_id=session_record.id)
