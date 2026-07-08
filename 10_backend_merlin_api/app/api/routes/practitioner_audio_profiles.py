"""Routes pour profils audio praticiens."""
import logging
import os
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_practitioner
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.practitioner_audio_profile import PractitionerAudioProfile
from app.schemas.practitioner_audio_profile import (
    PractitionerAudioProfileOut,
)
from app.services.s3_service import S3AudioService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/me/audio-profile", tags=["audio_profiles"])

# Contraintes upload
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_MIMETYPES = {"audio/webm", "audio/mpeg", "audio/mp3", "audio/wav"}


def _extract_duration_from_file(file_path: str) -> int | None:
    """Extrait la durée audio (en secondes) du fichier uploadé.
    
    Pour l'instant : estimation simple via ffprobe ou lib externe.
    Implémentation basique : retourne None (on peut l'améliorer plus tard).
    TODO: Installer ffmpeg-python ou pydub pour extraction automatique.
    """
    try:
        # Placeholder : on peut ajouter ffprobe ici
        # Pour l'MVP : retour None
        return None
    except Exception as e:
        logger.warning(f"Could not extract duration from {file_path}: {e}")
        return None


@router.post("", response_model=PractitionerAudioProfileOut, status_code=status.HTTP_201_CREATED)
async def upload_audio_profile(
    file: UploadFile = File(...),
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Upload profil audio praticien (WebM, MP3, WAV).
    
    - Max 5 MB
    - Remplace le profil existant si déjà présent
    - Stocke fichier en mémoire (ou OVH S3 si intégration)
    """
    # Validation MIME type
    if file.content_type not in ALLOWED_MIMETYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"MIME type {file.content_type} not supported. Use WebM, MP3, or WAV.",
        )

    # Lecture fichier
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max {MAX_FILE_SIZE_MB} MB.",
        )

    # Génère clé S3 unique
    # Format: praticien_{id}_{timestamp}_{uuid}.ext
    ext = file.filename.split(".")[-1] if file.filename else "webm"
    s3_key = f"praticien_audio/{current_user.id}/{datetime.now(timezone.utc).timestamp()}_{uuid4().hex[:8]}.{ext}"

    file_size_kb = len(content) // 1024

    # Supprime ancien profil si existe
    old_profile = db.execute(
        select(PractitionerAudioProfile)
        .where(PractitionerAudioProfile.practitioner_id == current_user.id)
    ).scalar()

    if old_profile:
        db.delete(old_profile)

    # Crée nouveau profil
    new_profile = PractitionerAudioProfile(
        id=str(uuid4()),
        practitioner_id=current_user.id,
        s3_key=s3_key,
        duration_seconds=_extract_duration_from_file(s3_key),  # TODO: extract real duration
        file_size_kb=file_size_kb,
        is_active=True,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    logger.info(f"Audio profile created for practitioner {current_user.id}: {s3_key} ({file_size_kb} KB)")

    return PractitionerAudioProfileOut.from_orm(new_profile)


@router.get("", response_model=PractitionerAudioProfileOut | None)
def get_audio_profile(
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Récupère profil audio praticien (métadonnées seulement)."""
    profile = db.execute(
        select(PractitionerAudioProfile)
        .where(PractitionerAudioProfile.practitioner_id == current_user.id)
        .where(PractitionerAudioProfile.is_active == True)  # noqa: E712
    ).scalar()

    if not profile:
        return None

    return PractitionerAudioProfileOut.from_orm(profile)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_audio_profile(
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Désactive profil audio praticien (soft delete)."""
    profile = db.execute(
        select(PractitionerAudioProfile)
        .where(PractitionerAudioProfile.practitioner_id == current_user.id)
        .where(PractitionerAudioProfile.is_active == True)  # noqa: E712
    ).scalar()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio profile not found.",
        )

    profile.is_active = False
    profile.updated_at = datetime.now(timezone.utc)
    db.add(profile)
    db.commit()

    logger.info(f"Audio profile deactivated for practitioner {current_user.id}")


# Router public pour télécharger l'audio d'un praticien (lecture seule)
public_router = APIRouter(prefix="/praticiens", tags=["audio_profiles_public"])


@public_router.get("/{practitioner_id}/audio", status_code=status.HTTP_200_OK)
def get_practitioner_audio_public(
    practitioner_id: str,
    db: Session = Depends(get_db),
):
    """Récupère le profil audio public d'un praticien (client peut écouter).
    
    Retourne un placeholder JSON avec s3_key et métadonnées.
    Le frontend télécharge le fichier via S3 presigned URL.
    """
    profile = db.execute(
        select(PractitionerAudioProfile)
        .where(PractitionerAudioProfile.practitioner_id == practitioner_id)
        .where(PractitionerAudioProfile.is_active == True)  # noqa: E712
    ).scalar()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio profile not available for this practitioner.",
        )

    # TODO: Générer presigned URL S3 avec TTL 7 jours
    # Pour l'instant : retour métadonnées brutes
    return {
        "id": profile.id,
        "practitioner_id": profile.practitioner_id,
        "s3_key": profile.s3_key,
        "duration_seconds": profile.duration_seconds,
        "file_size_kb": profile.file_size_kb,
        "created_at": profile.created_at,
        # "presigned_url": "https://s3.bhs.io.cloud.ovh.net/...?X-Amz-Signature=...",  # TODO
    }

