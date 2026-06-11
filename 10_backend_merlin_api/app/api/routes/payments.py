import json
import logging
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_operator
from app.db.session import get_db
from app.models.client_entitlement import ClientEntitlement
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.enums import SessionChannelCode, SessionModeCode, SessionStatusCode
from app.models.intake_request import IntakeRequest
from app.models.payment_order import PaymentOrder
from app.models.schedule import BookingSlot
from app.models.session import SessionRecord
from app.services.booking_flow import confirm_slot_for_client_record, send_booking_confirmation_email_for_slot
from app.services.email import send_email
from app.schemas.payment import (
    InteracEtransferCreate,
    InteracEtransferRequestRead,
    ManualPaymentAck,
    PaymentCheckoutCreate,
    StripeAudioAsyncCheckoutCreate,
    StripeCheckoutSessionRead,
    StripeWebhookAck,
)
from app.models.enums import (
    PaymentFulfillmentModeCode,
    PaymentOrderStatusCode,
    PaymentProductKindCode,
    PaymentProviderCode,
    SlotStatus,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["payments"])


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


def _resolve_checkout_urls_generic(payload: PaymentCheckoutCreate) -> tuple[str, str]:
    success_url = (
        payload.success_url
        or settings.stripe_checkout_success_url
        or f"{settings.frontend_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}"
    )
    cancel_url = payload.cancel_url or settings.stripe_checkout_cancel_url or f"{settings.frontend_url}/checkout/cancel"
    return success_url, cancel_url


def _append_checkout_params(url: str, params: dict[str, str]) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({key: value for key, value in params.items() if value})
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _validate_checkout_references(
    db: Session,
    *,
    client_id: str,
    operator_user_id: str | None,
    intake_request_id: str | None,
) -> None:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.")

    if operator_user_id is not None:
        operator = db.get(AppUser, operator_user_id)
        if operator is None or operator.role not in {"operator", "practitioner", "supervisor"}:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Operateur/praticien introuvable.",
            )

    if intake_request_id is not None:
        intake_request = db.get(IntakeRequest, intake_request_id)
        if intake_request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Demande d'entree introuvable.",
            )
        if intake_request.client_id != client_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le client et la demande d'entree ne correspondent pas.",
            )


def _build_audio_async_checkout_payload(
    payload: StripeAudioAsyncCheckoutCreate,
) -> PaymentCheckoutCreate:
    return PaymentCheckoutCreate(
        client_id=payload.client_id,
        operator_user_id=payload.operator_user_id,
        intake_request_id=payload.intake_request_id,
        slot_id=None,
        product_code="audio_async_follow_up",
        product_label="MERLIN Audio Async",
        product_kind_code=PaymentProductKindCode.audio_async_follow_up,
        fulfillment_mode_code=(
            PaymentFulfillmentModeCode.grant_entitlement_and_create_audio_async_session
        ),
        amount_cents=settings.stripe_audio_async_amount_cents,
        currency=settings.stripe_audio_async_currency,
        entitlement_type_code="follow_up_session_credit",
        entitlement_quantity=1,
        success_url=payload.success_url,
        cancel_url=payload.cancel_url,
    )


def _create_payment_order(
    db: Session,
    payload: PaymentCheckoutCreate | InteracEtransferCreate,
    provider_code: PaymentProviderCode = PaymentProviderCode.stripe,
) -> PaymentOrder:
    metadata_json = None
    if payload.slot_id:
        metadata_json = json.dumps({"slot_id": payload.slot_id}, ensure_ascii=False)

    order = PaymentOrder(
        client_id=payload.client_id,
        operator_user_id=payload.operator_user_id,
        intake_request_id=payload.intake_request_id,
        provider_code=provider_code,
        product_code=payload.product_code,
        product_label=payload.product_label,
        product_kind_code=payload.product_kind_code,
        fulfillment_mode_code=payload.fulfillment_mode_code,
        entitlement_type_code=payload.entitlement_type_code,
        entitlement_quantity=payload.entitlement_quantity,
        amount_cents=payload.amount_cents,
        currency=payload.currency,
        status_code=PaymentOrderStatusCode.pending,
        metadata_json=metadata_json,
    )
    db.add(order)
    db.flush()
    return order


def _create_stripe_checkout_for_order(
    order: PaymentOrder,
    payload: PaymentCheckoutCreate,
) -> stripe.checkout.Session:
    success_url, cancel_url = _resolve_checkout_urls_generic(payload)
    success_url = _append_checkout_params(
        success_url,
        {
            "order_id": order.id,
            "client_id": order.client_id,
            "intake_request_id": order.intake_request_id or "",
            "product_code": order.product_code,
            "slot_id": payload.slot_id or "",
        },
    )
    cancel_url = _append_checkout_params(
        cancel_url,
        {
            "order_id": order.id,
            "client_id": order.client_id,
            "intake_request_id": order.intake_request_id or "",
            "product_code": order.product_code,
            "slot_id": payload.slot_id or "",
        },
    )
    stripe.api_key = settings.stripe_secret_key
    return stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": order.currency,
                    "unit_amount": order.amount_cents,
                    "product_data": {
                        "name": order.product_label,
                        "description": f"Produit {order.product_code}",
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={
            "payment_order_id": order.id,
            "product_code": order.product_code,
            "client_id": order.client_id,
            "operator_user_id": order.operator_user_id or "",
            "intake_request_id": order.intake_request_id or "",
            "slot_id": payload.slot_id or "",
            "session_mode_code": SessionModeCode.follow_up.value,
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )


def _build_checkout_response(
    order: PaymentOrder,
    checkout_session: stripe.checkout.Session,
) -> StripeCheckoutSessionRead:
    return StripeCheckoutSessionRead(
        order_id=order.id,
        product_code=order.product_code,
        checkout_session_id=checkout_session.id,
        checkout_url=checkout_session.url,
        amount_cents=order.amount_cents,
        currency=order.currency,
    )


def _find_existing_audio_async_session(db: Session, order: PaymentOrder) -> SessionRecord | None:
    if not order.operator_user_id:
        return None
    return db.scalar(
        select(SessionRecord)
        .where(SessionRecord.client_id == order.client_id)
        .where(SessionRecord.operator_user_id == order.operator_user_id)
        .where(SessionRecord.session_channel_code == SessionChannelCode.audio_async)
        .where(SessionRecord.intake_request_id == order.intake_request_id)
        .where(SessionRecord.created_at >= order.created_at)
        .order_by(SessionRecord.created_at.desc())
    )


def _grant_entitlement(db: Session, order: PaymentOrder) -> ClientEntitlement | None:
    if order.entitlement_type_code is None or order.entitlement_quantity is None:
        return None

    existing = db.scalar(
        select(ClientEntitlement).where(ClientEntitlement.payment_order_id == order.id)
    )
    if existing is not None:
        return existing

    entitlement = ClientEntitlement(
        client_id=order.client_id,
        payment_order_id=order.id,
        entitlement_type_code=order.entitlement_type_code,
        quantity_total=order.entitlement_quantity,
        quantity_remaining=order.entitlement_quantity,
    )
    db.add(entitlement)
    db.flush()
    return entitlement


def _create_audio_async_session_from_order(db: Session, order: PaymentOrder) -> SessionRecord | None:
    existing_session = _find_existing_audio_async_session(db, order)
    if existing_session is not None:
        return existing_session

    if not order.operator_user_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Commande sans operateur pour creer une session audio_async.",
        )

    latest_sequence_number = db.scalar(
        select(func.max(SessionRecord.session_sequence_number)).where(
            SessionRecord.client_id == order.client_id
        )
    )

    session_record = SessionRecord(
        client_id=order.client_id,
        intake_request_id=order.intake_request_id,
        session_sequence_number=(latest_sequence_number or 0) + 1,
        session_mode_code=SessionModeCode.follow_up,
        session_channel_code=SessionChannelCode.audio_async,
        session_status_code=SessionStatusCode.pending_review,
        operator_user_id=order.operator_user_id,
    )
    db.add(session_record)
    db.flush()
    return session_record


def _fulfill_paid_order(
    db: Session,
    order: PaymentOrder,
) -> tuple[ClientEntitlement | None, SessionRecord | None]:
    entitlement = _grant_entitlement(db, order)
    session_record: SessionRecord | None = None
    if (
        order.fulfillment_mode_code
        == PaymentFulfillmentModeCode.grant_entitlement_and_create_audio_async_session
    ):
        session_record = _create_audio_async_session_from_order(db, order)
    order.fulfilled_at = datetime.now(timezone.utc)
    db.add(order)
    return entitlement, session_record


def _create_checkout_order(
    payload: PaymentCheckoutCreate,
    db: Session,
) -> StripeCheckoutSessionRead:
    _ensure_stripe_config()
    _validate_checkout_references(
        db,
        client_id=payload.client_id,
        operator_user_id=payload.operator_user_id,
        intake_request_id=payload.intake_request_id,
    )

    order = _create_payment_order(db, payload, PaymentProviderCode.stripe)
    checkout_session = _create_stripe_checkout_for_order(order, payload)
    order.provider_checkout_session_id = checkout_session.id
    metadata = _load_order_metadata(order)
    metadata.update(checkout_session.metadata or {})
    order.metadata_json = json.dumps(metadata, ensure_ascii=False)
    db.add(order)
    db.commit()
    db.refresh(order)
    return _build_checkout_response(order, checkout_session)


def _build_interac_instructions(order: PaymentOrder) -> tuple[str, str]:
    reference = f"IVIA-{order.id.split('-')[0].upper()}"
    instructions = (
        f"{settings.interac_etransfer_notice} "
        f"Ajoutez la reference {reference} dans le message du virement."
    )
    return reference, instructions


def _load_order_metadata(order: PaymentOrder) -> dict[str, str]:
    if not order.metadata_json:
        return {}
    try:
        raw = json.loads(order.metadata_json)
    except json.JSONDecodeError:
        return {}
    if isinstance(raw, dict):
        return {str(key): "" if value is None else str(value) for key, value in raw.items()}
    return {}


async def _auto_confirm_paid_slot_if_any(
    db: Session,
    order: PaymentOrder,
) -> BookingSlot | None:
    metadata = _load_order_metadata(order)
    slot_id = metadata.get("slot_id")
    if not slot_id:
        return None

    slot = db.get(BookingSlot, slot_id)
    if slot is None:
        return None
    if slot.status == SlotStatus.confirmed:
        return slot

    client_record = db.get(Client, order.client_id)
    if client_record is None or client_record.app_user_id is None:
        return None
    if slot.client_id != client_record.app_user_id:
        return None

    try:
        confirm_slot_for_client_record(
            db,
            slot,
            client_record,
            user_id=client_record.app_user_id,
        )
    except HTTPException:
        logger.info(
            "Auto-confirmation ignoree pour la commande %s et le slot %s.",
            order.id,
            slot.id,
        )
        return None

    user = db.get(AppUser, client_record.app_user_id)
    if user is not None:
        await send_booking_confirmation_email_for_slot(db, slot, user)
    return slot


async def _create_interac_order(
    payload: InteracEtransferCreate,
    db: Session,
) -> InteracEtransferRequestRead:
    _validate_checkout_references(
        db,
        client_id=payload.client_id,
        operator_user_id=payload.operator_user_id,
        intake_request_id=payload.intake_request_id,
    )
    order = _create_payment_order(db, payload, PaymentProviderCode.interac_etransfer)
    transfer_reference, instructions_text = _build_interac_instructions(order)
    metadata = _load_order_metadata(order)
    metadata.update(
        {
            "transfer_reference": transfer_reference,
            "recipient_name": settings.interac_etransfer_recipient_name,
            "recipient_email": settings.interac_etransfer_email,
            "instructions_text": instructions_text,
        }
    )
    order.metadata_json = json.dumps(metadata, ensure_ascii=False)
    db.add(order)
    db.commit()
    db.refresh(order)

    client = db.get(Client, payload.client_id)
    instructions_emailed = False
    if client and client.email:
        from app.services.email import make_interac_etransfer_email

        html, text = make_interac_etransfer_email(
            display_name=client.first_name_or_alias,
            recipient_name=settings.interac_etransfer_recipient_name,
            recipient_email=settings.interac_etransfer_email,
            transfer_reference=transfer_reference,
            amount_cents=order.amount_cents,
            currency=order.currency,
            instructions_text=instructions_text,
        )
        instructions_emailed = await send_email(
            client.email,
            f"Instructions Interac — {order.product_label}",
            html,
            text,
        )

    return InteracEtransferRequestRead(
        order_id=order.id,
        status=order.status_code.value,
        amount_cents=order.amount_cents,
        currency=order.currency,
        recipient_name=settings.interac_etransfer_recipient_name,
        recipient_email=settings.interac_etransfer_email,
        transfer_reference=transfer_reference,
        instructions_text=instructions_text,
        instructions_emailed=instructions_emailed,
    )
@router.post(
    "/stripe/checkout",
    response_model=StripeCheckoutSessionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_checkout_session(
    payload: PaymentCheckoutCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> StripeCheckoutSessionRead:
    _ = current_user
    return _create_checkout_order(payload, db)


def _public_catalog_amount(kind: PaymentProductKindCode) -> tuple[int, str] | None:
    """Catalogue serveur des produits achetables sans authentification.

    Sécurité (anti-manipulation de prix) : la route publique n'honore JAMAIS le
    montant fourni par le client — il est remplacé par le prix serveur du produit.
    """
    catalog: dict[PaymentProductKindCode, tuple[int, str]] = {
        PaymentProductKindCode.audio_async_follow_up: (
            settings.stripe_audio_async_amount_cents,
            settings.stripe_audio_async_currency,
        ),
        PaymentProductKindCode.session_intake: (
            settings.stripe_seance_amount_cents,
            settings.stripe_seance_currency,
        ),
        PaymentProductKindCode.session_follow_up: (
            settings.stripe_seance_amount_cents,
            settings.stripe_seance_currency,
        ),
    }
    return catalog.get(kind)


@router.post(
    "/stripe/public-checkout",
    response_model=StripeCheckoutSessionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_public_checkout_session(
    payload: PaymentCheckoutCreate,
    db: Session = Depends(get_db),
) -> StripeCheckoutSessionRead:
    """Checkout sans authentification — restreint au catalogue serveur.

    Le montant et la devise du payload sont écrasés par le prix serveur ; les
    produits hors catalogue (`custom`, `journal_days_pack`) exigent la route
    opérateur authentifiée `/stripe/checkout`.
    """
    server_price = _public_catalog_amount(payload.product_kind_code)
    if server_price is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Produit non disponible en checkout public.",
        )
    payload = payload.model_copy(
        update={"amount_cents": server_price[0], "currency": server_price[1]}
    )
    return _create_checkout_order(payload, db)


@router.post(
    "/stripe/checkout/audio-async",
    response_model=StripeCheckoutSessionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_audio_async_checkout_session(
    payload: StripeAudioAsyncCheckoutCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> StripeCheckoutSessionRead:
    """Crée une session Stripe Checkout pour le flux audio-async.

    Sécurité (BACK-PAY-001) : route réservée aux opérateurs internes.
    Le webhook Stripe (POST /payments/stripe/webhook) reste public — il est
    sécurisé par vérification de signature serveur (stripe-signature header).
    """
    _ = current_user  # garde appliqué par Depends ; variable conservée pour audit futur
    return _create_checkout_order(_build_audio_async_checkout_payload(payload), db)


@router.post("/stripe/webhook", response_model=StripeWebhookAck)
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
    payment_order_id = metadata.get("payment_order_id")
    order: PaymentOrder | None = None
    if payment_order_id:
        order = db.get(PaymentOrder, payment_order_id)
    if order is None:
        order = db.scalar(
            select(PaymentOrder).where(
                PaymentOrder.provider_checkout_session_id == checkout_data.id
            )
        )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commande de paiement introuvable.",
        )

    if order.status_code == PaymentOrderStatusCode.paid:
        existing_entitlement = db.scalar(
            select(ClientEntitlement).where(ClientEntitlement.payment_order_id == order.id)
        )
        existing_session = _find_existing_audio_async_session(db, order)
        return StripeWebhookAck(
            status="already_processed",
            order_id=order.id,
            entitlement_id=existing_entitlement.id if existing_entitlement else None,
            session_id=existing_session.id if existing_session else None,
        )

    order.status_code = PaymentOrderStatusCode.paid
    order.provider_payment_intent_id = checkout_data.payment_intent or None
    order.paid_at = datetime.now(timezone.utc)
    merged_metadata = _load_order_metadata(order)
    merged_metadata.update(metadata)
    order.metadata_json = json.dumps(merged_metadata, ensure_ascii=False)
    db.add(order)

    entitlement, session_record = _fulfill_paid_order(db, order)
    confirmed_slot = await _auto_confirm_paid_slot_if_any(db, order)
    db.commit()
    db.refresh(order)

    return StripeWebhookAck(
        status="created",
        order_id=order.id,
        entitlement_id=entitlement.id if entitlement else None,
        session_id=(session_record.id if session_record else confirmed_slot.id if confirmed_slot else None),
    )


@router.post(
    "/interac/etransfer/request",
    response_model=InteracEtransferRequestRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_interac_etransfer_request(
    payload: InteracEtransferCreate,
    db: Session = Depends(get_db),
) -> InteracEtransferRequestRead:
    return await _create_interac_order(payload, db)


@router.post(
    "/interac/etransfer/{order_id}/mark-paid",
    response_model=ManualPaymentAck,
    status_code=status.HTTP_200_OK,
)
async def mark_interac_etransfer_paid(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),
) -> ManualPaymentAck:
    _ = current_user
    order = db.get(PaymentOrder, order_id)
    if order is None or order.provider_code != PaymentProviderCode.interac_etransfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande Interac introuvable.")

    if order.status_code == PaymentOrderStatusCode.paid:
        existing_entitlement = db.scalar(
            select(ClientEntitlement).where(ClientEntitlement.payment_order_id == order.id)
        )
        existing_session = _find_existing_audio_async_session(db, order)
        return ManualPaymentAck(
            status="already_processed",
            order_id=order.id,
            entitlement_id=existing_entitlement.id if existing_entitlement else None,
            session_id=existing_session.id if existing_session else None,
        )

    order.status_code = PaymentOrderStatusCode.paid
    order.paid_at = datetime.now(timezone.utc)
    db.add(order)
    entitlement, session_record = _fulfill_paid_order(db, order)
    confirmed_slot = await _auto_confirm_paid_slot_if_any(db, order)
    db.commit()
    db.refresh(order)
    return ManualPaymentAck(
        status="created",
        order_id=order.id,
        entitlement_id=entitlement.id if entitlement else None,
        session_id=(session_record.id if session_record else confirmed_slot.id if confirmed_slot else None),
    )
