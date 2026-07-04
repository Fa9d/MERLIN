"""Analyse prosodique locale — le *comment* c'est dit, pas le *quoi*.

Extraction 100 % locale (Loi 25 : l'audio ne quitte jamais le serveur), sur le
modèle de ``transcription.py`` : dépendance lourde (librosa) hors
``requirements.txt``, installée via ``requirements-analysis.txt`` dans l'image
prod ; dégradation propre si absente.

Indicateurs produits (niveau ``observation`` — descriptifs, non interprétés) :

- durée, ratio parole/silence (pauses), nombre de segments de pause longs ;
- hauteur (F0) : moyenne, écart-type, étendue — variabilité vocale ;
- énergie (RMS) : moyenne, écart-type — intensité et modulation ;
- débit approximatif (onsets/s sur les segments voisés).

L'interprétation croisée (divergence prosodie/sémantique, aplatissement vocal…)
relève d'une capacité distincte de niveau ``inference_clinique`` — réservée aux
praticiens vérifiés via la vanne (``capability_gate``).
"""
from __future__ import annotations

import logging
from importlib import util as importlib_util

logger = logging.getLogger("merlin.prosody")

ENGINE_VERSION = "prosody-local-v1.0"


class ProsodyError(RuntimeError):
    """Échec d'analyse prosodique locale."""


def prosody_disponible() -> bool:
    """Vrai si librosa est importable dans cet environnement."""
    return importlib_util.find_spec("librosa") is not None


def analyse_fichier_audio(path: str) -> dict:
    """Extrait les descripteurs prosodiques d'un fichier audio local.

    Retourne un dict JSON-sérialisable ; lève ProsodyError si librosa absent
    ou fichier illisible.
    """
    if not prosody_disponible():
        raise ProsodyError(
            "librosa non installé — installer requirements-analysis.txt "
            "(analyse locale requise, Loi 25)."
        )

    import librosa
    import numpy as np

    try:
        y, sr = librosa.load(path, sr=16000, mono=True)
    except Exception as exc:  # noqa: BLE001
        raise ProsodyError(f"Lecture audio impossible : {exc}") from exc
    if y.size == 0:
        raise ProsodyError("Fichier audio vide.")

    duration_s = float(len(y) / sr)

    # ── Énergie (RMS) et détection de silence ────────────────────────────────
    frame_length, hop_length = 2048, 512
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_db = librosa.amplitude_to_db(rms + 1e-10, ref=np.max)
    silence_mask = rms_db < -35.0  # frames sous -35 dB relatif = silence
    frame_dur = hop_length / sr
    pause_ratio = float(np.mean(silence_mask))

    # segments de pause continus > 1 s
    long_pauses = 0
    run = 0
    for s in silence_mask:
        run = run + 1 if s else 0
        if run == int(1.0 / frame_dur):
            long_pauses += 1

    # ── Hauteur (F0) via pYIN ────────────────────────────────────────────────
    f0, voiced_flag, _ = librosa.pyin(
        y, fmin=65.0, fmax=400.0, sr=sr, frame_length=frame_length, hop_length=hop_length
    )
    f0_voiced = f0[~np.isnan(f0)] if f0 is not None else np.array([])
    voiced_ratio = float(np.mean(voiced_flag)) if voiced_flag is not None else 0.0

    # ── Débit approximatif : onsets par seconde de parole ────────────────────
    onsets = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)
    speech_time = max(duration_s * (1.0 - pause_ratio), 1e-6)
    onset_rate = float(len(onsets) / speech_time)

    def _stat(arr, fn, default=None):
        return float(fn(arr)) if arr.size else default

    return {
        "engine_version": ENGINE_VERSION,
        "duration_s": round(duration_s, 2),
        "pause_ratio": round(pause_ratio, 4),
        "long_pauses_count": int(long_pauses),
        "voiced_ratio": round(voiced_ratio, 4),
        "f0_mean_hz": _stat(f0_voiced, np.mean),
        "f0_std_hz": _stat(f0_voiced, np.std),
        "f0_range_hz": (
            round(float(np.percentile(f0_voiced, 95) - np.percentile(f0_voiced, 5)), 2)
            if f0_voiced.size
            else None
        ),
        "rms_db_mean": round(float(np.mean(rms_db)), 2),
        "rms_db_std": round(float(np.std(rms_db)), 2),
        "onset_rate_per_s": round(onset_rate, 3),
    }
