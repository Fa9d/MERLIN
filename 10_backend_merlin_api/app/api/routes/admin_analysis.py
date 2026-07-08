"""Console admin du moteur d'analyse — interrupteurs un-clic + credentials praticiens.

- ``GET/PATCH /admin/analysis-capabilities`` : matrice (profil × capacité).
  Valider/invalider une capacité selon l'utilisation (IVIA Québec vs recherche)
  se fait ici, en un clic, sans redéploiement.
- ``/admin/practitioner-credentials`` : enregistrement et vérification de la
  reconnaissance professionnelle (ordre, permis). Le drapeau
  ``recognized_by_order`` gouverne le droit de transmettre au client des
  contenus de niveau inference_clinique.

Accès réservé ``require_admin`` (cf. app/core/deps.py).
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.analysis import CredentialStatus, PractitionerCredential
from app.models.app_user import AppUser
from app.models.session_type import SessionType, SessionTypeCapability
from app.schemas.common import MerlinSchema
from app.services import capability_gate

router = APIRouter(prefix="/admin/analysis", tags=["admin-analyse"])


# ── Interrupteurs de capacités ────────────────────────────────────────────────
class CapabilityMatrix(MerlinSchema):
    profiles: dict[str, str]                 # {profil: label}
    capabilities: dict[str, dict]            # catalogue (label, category, ...)
    matrix: dict[str, dict[str, bool]]       # {profil: {capacité: activée}}


class CapabilityPatch(MerlinSchema):
    profile: str
    capability: str
    enabled: bool


def _matrix(db: Session) -> CapabilityMatrix:
    return CapabilityMatrix(
        profiles={p: cfg["label"] for p, cfg in capability_gate.PROFILES.items()},
        capabilities={
            c: {
                "label": cfg["label"],
                "category": cfg["category"],
                "max_sensitivity": cfg["max_sensitivity"].value,
                "data_leaves_server": cfg["data_leaves_server"],
            }
            for c, cfg in capability_gate.CAPABILITIES.items()
        },
        matrix=capability_gate.capability_matrix(db),
    )


@router.get("/capabilities", response_model=CapabilityMatrix)
def get_capabilities(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> CapabilityMatrix:
    return _matrix(db)


@router.patch("/capabilities", response_model=CapabilityMatrix)
def patch_capability(
    payload: CapabilityPatch,
    db: Session = Depends(get_db),
    admin: AppUser = Depends(require_admin()),
) -> CapabilityMatrix:
    if payload.profile not in capability_gate.PROFILES:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profil inconnu.")
    if payload.capability not in capability_gate.CAPABILITIES:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Capacité inconnue.")
    capability_gate.set_capability(
        db, payload.profile, payload.capability, payload.enabled, admin.id
    )
    db.commit()
    return _matrix(db)


# ── Credentials praticiens ────────────────────────────────────────────────────
class CredentialCreate(MerlinSchema):
    practitioner_user_id: str
    order_body: str
    license_number: str | None = None
    scope_notes: str | None = None
    expires_at: datetime | None = None


class CredentialUpdate(MerlinSchema):
    status: CredentialStatus | None = None
    recognized_by_order: bool | None = None
    scope_notes: str | None = None
    expires_at: datetime | None = None


class CredentialRead(MerlinSchema):
    id: str
    practitioner_user_id: str
    order_body: str
    license_number: str | None
    scope_notes: str | None
    status: CredentialStatus
    recognized_by_order: bool
    verified_by_user_id: str | None
    verified_at: datetime | None
    expires_at: datetime | None
    created_at: datetime


@router.get("/credentials", response_model=list[CredentialRead])
def list_credentials(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> list[PractitionerCredential]:
    return list(
        db.execute(
            select(PractitionerCredential).order_by(PractitionerCredential.created_at.desc())
        ).scalars()
    )


@router.post("/credentials", response_model=CredentialRead, status_code=status.HTTP_201_CREATED)
def create_credential(
    payload: CredentialCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> PractitionerCredential:
    if db.get(AppUser, payload.practitioner_user_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilisateur praticien introuvable.")
    cred = PractitionerCredential(
        practitioner_user_id=payload.practitioner_user_id,
        order_body=payload.order_body,
        license_number=payload.license_number,
        scope_notes=payload.scope_notes,
        expires_at=payload.expires_at,
    )
    db.add(cred)
    db.commit()
    db.refresh(cred)
    return cred


@router.patch("/credentials/{credential_id}", response_model=CredentialRead)
def update_credential(
    credential_id: str,
    payload: CredentialUpdate,
    db: Session = Depends(get_db),
    admin: AppUser = Depends(require_admin()),
) -> PractitionerCredential:
    cred = db.get(PractitionerCredential, credential_id)
    if cred is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Credential introuvable.")
    if payload.status is not None and payload.status != cred.status:
        cred.status = payload.status
        if payload.status == CredentialStatus.verified:
            cred.verified_by_user_id = admin.id
            cred.verified_at = datetime.now(timezone.utc)
    if payload.recognized_by_order is not None:
        cred.recognized_by_order = payload.recognized_by_order
    if payload.scope_notes is not None:
        cred.scope_notes = payload.scope_notes
    if payload.expires_at is not None:
        cred.expires_at = payload.expires_at
    db.add(cred)
    db.commit()
    db.refresh(cred)
    return cred


# ── Atelier des lectures : types de séance × capacités ───────────────────────
# Le type de séance gouverne QUELLES lectures s'appliquent à une rencontre
# (enabled) et lesquelles se déclenchent automatiquement après transcription
# (auto_run). Défaut permissif : sans ligne, la capacité reste permise mais ne
# s'auto-déclenche pas. La vanne profil×capacité demeure le verrou principal.


class SessionTypeRead(MerlinSchema):
    code: str
    label: str
    description: str | None
    active: bool
    capabilities: dict[str, dict]  # {capacité: {enabled, auto_run}}


class SessionTypeCreate(MerlinSchema):
    code: str
    label: str
    description: str | None = None


class SessionTypePatch(MerlinSchema):
    label: str | None = None
    description: str | None = None
    active: bool | None = None


class SessionTypeCapabilityPatch(MerlinSchema):
    capability: str
    enabled: bool | None = None
    auto_run: bool | None = None


def _type_read(db: Session, st: SessionType) -> SessionTypeRead:
    rows = db.execute(
        select(SessionTypeCapability).where(
            SessionTypeCapability.session_type_code == st.code
        )
    ).scalars()
    overrides = {r.capability: r for r in rows}
    caps = {}
    for cap in capability_gate.CAPABILITIES:
        row = overrides.get(cap)
        caps[cap] = {
            "enabled": True if row is None else bool(row.enabled),
            "auto_run": False if row is None else bool(row.auto_run),
        }
    return SessionTypeRead(
        code=st.code, label=st.label, description=st.description,
        active=st.active, capabilities=caps,
    )


@router.get("/session-types", response_model=list[SessionTypeRead])
def list_session_types(
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> list[SessionTypeRead]:
    types = db.execute(select(SessionType).order_by(SessionType.code)).scalars()
    return [_type_read(db, st) for st in types]


@router.post("/session-types", response_model=SessionTypeRead, status_code=status.HTTP_201_CREATED)
def create_session_type(
    payload: SessionTypeCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> SessionTypeRead:
    code = payload.code.strip().lower()
    if not code.isidentifier() or not (2 <= len(code) <= 32):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Code invalide (slug de 2 à 32 caractères, ex. suivi_long).",
        )
    if not (1 <= len(payload.label.strip()) <= 120):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Nom invalide (1 à 120 caractères).")
    if payload.description and len(payload.description) > 500:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Description trop longue (max 500).")
    if db.get(SessionType, code) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Le type '{code}' existe déjà.")
    st = SessionType(code=code, label=payload.label.strip(), description=payload.description)
    db.add(st)
    db.commit()
    db.refresh(st)
    return _type_read(db, st)


@router.patch("/session-types/{code}", response_model=SessionTypeRead)
def patch_session_type(
    code: str,
    payload: SessionTypePatch,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> SessionTypeRead:
    st = db.get(SessionType, code)
    if st is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Type de séance introuvable.")
    # Mêmes bornes qu'à la création : l'API refuse proprement (400) ce que la
    # colonne refuserait brutalement (500).
    if payload.label is not None:
        if not (1 <= len(payload.label.strip()) <= 120):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Nom invalide (1 à 120 caractères).")
        st.label = payload.label.strip()
    if payload.description is not None:
        if len(payload.description) > 500:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Description trop longue (max 500).")
        st.description = payload.description
    if payload.active is not None:
        st.active = payload.active
    db.add(st)
    db.commit()
    db.refresh(st)
    return _type_read(db, st)


@router.patch("/session-types/{code}/capabilities", response_model=SessionTypeRead)
def patch_session_type_capability(
    code: str,
    payload: SessionTypeCapabilityPatch,
    db: Session = Depends(get_db),
    _: AppUser = Depends(require_admin()),
) -> SessionTypeRead:
    st = db.get(SessionType, code)
    if st is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Type de séance introuvable.")
    if payload.capability not in capability_gate.CAPABILITIES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Capacité inconnue.")
    row = db.scalar(
        select(SessionTypeCapability).where(
            SessionTypeCapability.session_type_code == code,
            SessionTypeCapability.capability == payload.capability,
        )
    )
    if row is None:
        row = SessionTypeCapability(session_type_code=code, capability=payload.capability)
    if payload.enabled is not None:
        row.enabled = payload.enabled
    if payload.auto_run is not None:
        row.auto_run = payload.auto_run
    if row.auto_run and not row.enabled:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "auto_run exige que la capacité soit permise (enabled) pour ce type.",
        )
    db.add(row)
    db.commit()
    return _type_read(db, st)
