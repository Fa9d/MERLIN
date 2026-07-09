"""Administration des comptes & accès — /admin/accounts.

Réservé aux admins (require_admin : rôle admin_tech OU courriel en liste blanche).
Voir les inscriptions, renvoyer un lien de confirmation, vérifier manuellement,
changer le rôle, activer/suspendre. Adossé à AppUser + Client (profil complété).
"""
import logging
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import is_admin, require_admin
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.audio_recording import AudioRecording
from app.models.audio_session import AudioSession
from app.models.client import Client
from app.models.consent import Consent
from app.models.derived_document import DerivedDocument
from app.models.enums import AppRole, RecordStatus, InsightDepth
from app.models.intake_request import IntakeRequest
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.models.session_temporal_anchor import SessionTemporalAnchor
from app.schemas.common import MerlinSchema
from app.services.email import make_verification_email, send_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/accounts", tags=["admin-comptes"])


class AdminAccountRead(MerlinSchema):
    id: str
    email: str
    display_name: str
    role: str
    email_verified: bool
    record_status: str
    is_admin: bool
    profile_complete: bool
    subscription_status: str
    subscription_since: datetime | None
    acquisition_source: str | None
    created_at: datetime


class RoleUpdate(MerlinSchema):
    role: AppRole


class StatusUpdate(MerlinSchema):
    suspend: bool  # True → closed (suspendu) ; False → active


class SubscriptionUpdate(MerlinSchema):
    status: str  # "active" | "unpaid" | "inactive"


class AdminGrantUpdate(MerlinSchema):
    grant: bool  # True → accorde le droit admin (drapeau) ; False → le retire


class InsightDepthUpdate(MerlinSchema):
    insight_depth: InsightDepth  # basic | intermediate | expert


class AdminActionAck(MerlinSchema):
    status: str
    account: AdminAccountRead


def _to_read(u: AppUser, profile_complete: bool) -> AdminAccountRead:
    return AdminAccountRead(
        id=u.id,
        email=u.email,
        display_name=u.display_name,
        role=u.role.value,
        email_verified=u.email_verified,
        record_status=u.record_status.value,
        is_admin=is_admin(u),
        profile_complete=profile_complete,
        subscription_status=u.subscription_status,
        subscription_since=u.subscription_since,
        acquisition_source=u.acquisition_source,
        created_at=u.created_at,
    )


def _profile_map(db: Session, user_ids: list[str]) -> dict[str, bool]:
    """profile_complete par app_user_id (via la fiche Client liée)."""
    rows = db.scalars(select(Client).where(Client.app_user_id.in_(user_ids))).all()
    return {c.app_user_id: c.profile_complete for c in rows if c.app_user_id}


@router.get("", response_model=list[AdminAccountRead])
def list_accounts(
    q: str | None = Query(default=None, description="Filtre courriel ou nom (contient)"),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> list[AdminAccountRead]:
    stmt = select(AppUser).order_by(AppUser.created_at.desc()).limit(limit)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where((AppUser.email.ilike(like)) | (AppUser.display_name.ilike(like)))
    users = list(db.scalars(stmt))
    pmap = _profile_map(db, [u.id for u in users])
    return [_to_read(u, pmap.get(u.id, False)) for u in users]


def _get_user(db: Session, user_id: str) -> AppUser:
    user = db.get(AppUser, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")
    return user


@router.post("/{user_id}/resend-verification", response_model=AdminActionAck)
async def resend_verification(
    user_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Régénère le lien de confirmation et le renvoie au courriel du compte."""
    user = _get_user(db, user_id)
    if user.email_verified:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Courriel déjà vérifié.")
    token = secrets.token_urlsafe(48)
    user.email_verification_token = token
    user.token_expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    db.add(user)
    db.commit()
    db.refresh(user)

    url = f"{settings.frontend_url}/verify-email?{urlencode({'token': token})}"
    html, text = make_verification_email(user.display_name, url)
    sent = await send_email(user.email, "Confirmez votre adresse — IVIA", html, text)
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Le courriel n'a pas pu être envoyé (SMTP).",
        )
    logger.info("Lien de vérification renvoyé (admin) à %s", user.email)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="sent", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/verify", response_model=AdminActionAck)
def verify_manually(
    user_id: str,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Marque le courriel comme vérifié sans passer par le lien (dépannage admin)."""
    user = _get_user(db, user_id)
    user.email_verified = True
    user.email_verification_token = None
    user.token_expires_at = None
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="verified", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/subscription", response_model=AdminActionAck)
def update_subscription(
    user_id: str,
    payload: SubscriptionUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Suivi interne de l'abonnement praticien : active / unpaid / inactive (sans Stripe)."""
    from datetime import datetime, timezone

    if payload.status not in {"active", "unpaid", "inactive"}:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Statut d'abonnement invalide.")
    user = _get_user(db, user_id)
    user.subscription_status = payload.status
    if payload.status == "active" and user.subscription_since is None:
        user.subscription_since = datetime.now(timezone.utc)
    if payload.status == "inactive":
        user.subscription_since = None
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="subscription_updated", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/role", response_model=AdminActionAck)
def update_role(
    user_id: str,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Change le rôle métier (client/praticien/opérateur/superviseur/admin_tech).

    NB : le droit « admin » par liste blanche (MERLIN_ADMIN_EMAILS) est séparé et
    se règle dans la config, pas ici.
    """
    user = _get_user(db, user_id)
    user.role = payload.role
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="role_updated", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/status", response_model=AdminActionAck)
def update_status(
    user_id: str,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
    admin: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Suspend (closed) ou réactive (active) un compte."""
    user = _get_user(db, user_id)
    # Garde-fou : un admin ne peut pas se suspendre lui-même (verrouillage hors de l'app).
    if payload.suspend and str(user.id) == str(admin.id):
        raise HTTPException(
            status_code=400,
            detail="Vous ne pouvez pas suspendre votre propre compte.",
        )
    user.record_status = RecordStatus.closed if payload.suspend else RecordStatus.active
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="status_updated", account=_to_read(user, pmap.get(user.id, False)))


@router.post("/{user_id}/admin", response_model=AdminActionAck)
def update_admin_grant(
    user_id: str,
    payload: AdminGrantUpdate,
    db: Session = Depends(get_db),
    admin: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Accorde ou retire le droit admin (drapeau is_platform_admin), en cumul du rôle.

    Le droit admin par liste blanche (MERLIN_ADMIN_EMAILS) et le rôle admin_tech
    restent prioritaires : retirer le drapeau ne révoque pas un admin allowlisté.
    """
    user = _get_user(db, user_id)
    # Garde-fou : un admin ne peut pas retirer son propre droit (verrouillage hors admin).
    if not payload.grant and str(user.id) == str(admin.id):
        raise HTTPException(
            status_code=400,
            detail="Vous ne pouvez pas retirer votre propre droit admin.",
        )
    user.is_platform_admin = payload.grant
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="admin_updated", account=_to_read(user, pmap.get(user.id, False)))


@router.patch("/{user_id}/insight-depth", response_model=AdminActionAck)
def update_insight_depth(
    user_id: str,
    payload: InsightDepthUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> AdminActionAck:
    """Configure la profondeur des insights recommandés pour ce praticien (basic/intermediate/expert)."""
    user = _get_user(db, user_id)
    if user.role != AppRole.practitioner:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La profondeur des insights ne s'applique qu'aux praticiens.",
        )
    user.insight_depth = payload.insight_depth
    db.add(user)
    db.commit()
    db.refresh(user)
    pmap = _profile_map(db, [user.id])
    return AdminActionAck(status="insight_depth_updated", account=_to_read(user, pmap.get(user.id, False)))


@router.delete("/{user_id}")
def delete_account(
    user_id: str,
    db: Session = Depends(get_db),
    admin: AppUser = Depends(require_admin()),
) -> dict:
    """Supprime définitivement un compte et ses données liées (effacement — Loi 25).

    Cascade : séances opérées par le compte + dépendances (audio, notes, documents,
    ancres) ; consentements et références d'intake neutralisés ; puis le compte
    (la fiche Client et les paiements sont dissociés au niveau DB). Journalisé.
    Un admin ne peut pas supprimer son propre compte.
    """
    user = _get_user(db, user_id)
    if str(user.id) == str(admin.id):
        raise HTTPException(
            status_code=400,
            detail="Vous ne pouvez pas supprimer votre propre compte.",
        )

    # ids seulement (évite le décodage d'un enum legacy en chargeant les séances).
    sess_ids = list(
        db.scalars(select(SessionRecord.id).where(SessionRecord.operator_user_id == user.id))
    )
    if sess_ids:
        audio_ids = list(
            db.scalars(select(AudioSession.id).where(AudioSession.session_id.in_(sess_ids)))
        )
        if audio_ids:
            db.execute(delete(AudioRecording).where(AudioRecording.audio_session_id.in_(audio_ids)))
        db.execute(delete(AudioSession).where(AudioSession.session_id.in_(sess_ids)))
        db.execute(delete(DerivedDocument).where(DerivedDocument.session_id.in_(sess_ids)))
        db.execute(delete(SessionNote).where(SessionNote.session_id.in_(sess_ids)))
        db.execute(delete(SessionTemporalAnchor).where(SessionTemporalAnchor.session_id.in_(sess_ids)))
        db.execute(update(Consent).where(Consent.session_id.in_(sess_ids)).values(session_id=None))
        db.execute(delete(SessionRecord).where(SessionRecord.id.in_(sess_ids)))
    db.execute(
        update(IntakeRequest)
        .where(IntakeRequest.handled_by_user_id == user.id)
        .values(handled_by_user_id=None)
    )
    db.execute(
        update(IntakeRequest)
        .where(IntakeRequest.assigned_practitioner_id == user.id)
        .values(assigned_practitioner_id=None)
    )
    email = user.email
    db.execute(delete(AppUser).where(AppUser.id == user.id))
    db.commit()
    logger.warning(
        "Compte supprimé par admin %s : %s (%d séances effacées)", admin.email, email, len(sess_ids)
    )
    return {"status": "account_deleted", "id": user_id}


# ── Transfert de praticien (relation d'accompagnement durable) ────────────────
# Décision fondateur 2026-07-09 : mode 'resume' par défaut (le nouveau
# praticien repart du fil visible) ; 'integral' exige le consentement client.
from app.models.client import Client as _Client
from app.models.client_transfer import ClientPractitionerTransfer as _Transfer


class ClientTransferIn(MerlinSchema):
    praticien_id: str | None  # None = le client devient AUTONOME (journal seul)
    mode: str = "resume"
    client_consent_obtained: bool = False
    note: str | None = None


class ClientTransferRead(MerlinSchema):
    client_id: str
    from_praticien_id: str | None
    to_praticien_id: str | None
    mode: str


@router.post("/clients/{client_id}/praticien", response_model=ClientTransferRead)
def transfer_client_practitioner(
    client_id: str,
    payload: ClientTransferIn,
    db: Session = Depends(get_db),
    admin: AppUser = Depends(require_admin()),
) -> ClientTransferRead:
    client = db.get(_Client, client_id)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Client introuvable.")
    if payload.mode not in ("resume", "integral"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Mode invalide (resume|integral).")
    if payload.mode == "integral" and not payload.client_consent_obtained:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Le mode integral exige le consentement explicite du client "
            "(client_consent_obtained=true) — sa parole ne voyage pas sans lui.",
        )
    if payload.praticien_id is not None:
        nouveau = db.get(AppUser, payload.praticien_id)
        if nouveau is None or getattr(nouveau.role, "value", nouveau.role) != "practitioner":
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Praticien cible introuvable.")
    if payload.note and len(payload.note) > 1000:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Note trop longue (max 1000).")

    transfer = _Transfer(
        client_id=client.id,
        from_praticien_id=client.praticien_id,
        to_praticien_id=payload.praticien_id,
        mode=payload.mode,
        client_consent_obtained=payload.client_consent_obtained,
        note=payload.note,
        transferred_by_user_id=admin.id,
    )
    client.praticien_id = payload.praticien_id
    db.add_all([transfer, client])
    db.commit()
    return ClientTransferRead(
        client_id=client.id,
        from_praticien_id=transfer.from_praticien_id,
        to_praticien_id=transfer.to_praticien_id,
        mode=transfer.mode,
    )
