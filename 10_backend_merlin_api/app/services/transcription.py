"""Transcription audio des séances — provider local d'abord (Loi 25).

Deux providers :

- ``faster_whisper`` : open source, auto-hébergé — l'audio ne quitte jamais le serveur.
  C'est la cible doctrinale (données Québec, Loi 25, préférence open source).
- ``assemblyai`` : service tiers historique, conservé en repli le temps de la migration
  (voir ``app/services/livekit_audio.py`` pour l'implémentation legacy).

Sélection via ``MERLIN_TRANSCRIPTION_PROVIDER`` :

- ``auto`` (défaut) : faster-whisper si le package est installé, sinon AssemblyAI ;
- ``faster_whisper`` / ``assemblyai`` : forçage explicite.

faster-whisper est volontairement hors de ``requirements.txt`` (dépendance lourde,
ctranslate2 + téléchargement de modèle) : installer via ``requirements-transcription.txt``
dans l'image de prod. Le modèle est chargé une seule fois par process (cache).
"""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from functools import lru_cache
from importlib import util as importlib_util

import httpx

from app.core.config import settings

logger = logging.getLogger("merlin.transcription")

_PROVIDERS_VALIDES = {"faster_whisper", "assemblyai"}


class TranscriptionError(RuntimeError):
    """Échec de transcription audio (provider local ou distant)."""


def faster_whisper_disponible() -> bool:
    """Vrai si le package `faster_whisper` est importable dans cet environnement."""

    return importlib_util.find_spec("faster_whisper") is not None


def resolve_provider() -> str:
    """Résout le provider de transcription effectif d'après la configuration."""

    provider = (settings.transcription_provider or "auto").strip().lower()
    if provider == "auto":
        return "faster_whisper" if faster_whisper_disponible() else "assemblyai"
    if provider not in _PROVIDERS_VALIDES:
        raise TranscriptionError(
            f"Provider de transcription inconnu : '{provider}' "
            "(attendu : auto | faster_whisper | assemblyai)."
        )
    return provider


@lru_cache(maxsize=1)
def _whisper_model():
    """Charge (une fois par process) le modèle faster-whisper configuré."""

    if not faster_whisper_disponible():
        raise TranscriptionError(
            "faster-whisper n'est pas installé — "
            "`pip install -r requirements-transcription.txt`, "
            "ou forcer MERLIN_TRANSCRIPTION_PROVIDER=assemblyai."
        )

    from faster_whisper import WhisperModel

    logger.info(
        "Chargement du modèle faster-whisper '%s' (device=%s, compute=%s).",
        settings.whisper_model_size,
        settings.whisper_device,
        settings.whisper_compute_type,
    )
    return WhisperModel(
        settings.whisper_model_size,
        device=settings.whisper_device,
        compute_type=settings.whisper_compute_type,
    )


def _transcribe_sync(audio_path: str) -> str:
    """Transcrit un fichier audio local en français (exécution CPU bloquante)."""

    segments, info = _whisper_model().transcribe(
        audio_path,
        language="fr",
        vad_filter=True,
    )
    texte = " ".join(segment.text.strip() for segment in segments).strip()
    logger.info(
        "Transcription locale terminée (%.1fs d'audio, langue %s).",
        getattr(info, "duration", 0.0),
        getattr(info, "language", "fr"),
    )
    return texte


async def _telecharger_audio(url: str) -> str:
    """Rapatrie un audio distant (ex. egress S3) en fichier temporaire local."""

    suffix = os.path.splitext(url.split("?", 1)[0])[1] or ".ogg"
    fd, local_path = tempfile.mkstemp(prefix="merlin_audio_", suffix=suffix)
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                with os.fdopen(fd, "wb") as out:
                    async for chunk in response.aiter_bytes():
                        out.write(chunk)
    except Exception:
        os.unlink(local_path)
        raise
    return local_path


async def transcribe_with_faster_whisper(audio_path: str) -> str:
    """Transcrit un audio (chemin local ou URL) avec faster-whisper, hors event loop."""

    temp_path: str | None = None
    try:
        if audio_path.startswith(("http://", "https://")):
            temp_path = await _telecharger_audio(audio_path)
            audio_path = temp_path
        # CPU-bound : délégué à un thread pour ne pas bloquer l'event loop.
        return await asyncio.to_thread(_transcribe_sync, audio_path)
    except TranscriptionError:
        raise
    except Exception as exc:
        raise TranscriptionError(f"Échec transcription faster-whisper : {exc}") from exc
    finally:
        if temp_path is not None and os.path.exists(temp_path):
            os.unlink(temp_path)
