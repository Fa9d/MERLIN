"""Tests unitaires du sélecteur de provider de transcription (sans DB, sans réseau).

Couvre la logique de bascule AssemblyAI → faster-whisper (Loi 25) :
  - résolution `auto` selon la disponibilité du package faster-whisper ;
  - forçage explicite et rejet des valeurs inconnues ;
  - erreur claire si faster-whisper est forcé sans être installé.

Lancer : pytest tests/test_transcription_provider.py -v
"""

import asyncio

import pytest

from app.core.config import settings
from app.services import transcription


@pytest.fixture
def provider_setting():
    """Permet de forcer settings.transcription_provider et le restaure après le test."""

    original = settings.transcription_provider

    def _set(value: str) -> None:
        object.__setattr__(settings, "transcription_provider", value)

    yield _set
    object.__setattr__(settings, "transcription_provider", original)


@pytest.fixture(autouse=True)
def reset_model_cache():
    """Vide le cache du modèle whisper avant/après chaque test."""

    transcription._whisper_model.cache_clear()
    yield
    transcription._whisper_model.cache_clear()


class TestResolveProvider:

    def test_auto_sans_faster_whisper_retombe_sur_assemblyai(
        self, provider_setting, monkeypatch
    ) -> None:
        provider_setting("auto")
        monkeypatch.setattr(transcription, "faster_whisper_disponible", lambda: False)
        assert transcription.resolve_provider() == "assemblyai"

    def test_auto_avec_faster_whisper_prefere_le_local(
        self, provider_setting, monkeypatch
    ) -> None:
        provider_setting("auto")
        monkeypatch.setattr(transcription, "faster_whisper_disponible", lambda: True)
        assert transcription.resolve_provider() == "faster_whisper"

    def test_forcage_explicite_respecte(self, provider_setting) -> None:
        provider_setting("assemblyai")
        assert transcription.resolve_provider() == "assemblyai"
        provider_setting("faster_whisper")
        assert transcription.resolve_provider() == "faster_whisper"

    def test_provider_inconnu_rejete(self, provider_setting) -> None:
        provider_setting("openai_whisper_api")
        with pytest.raises(transcription.TranscriptionError, match="inconnu"):
            transcription.resolve_provider()

    def test_casse_et_espaces_toleres(self, provider_setting) -> None:
        provider_setting("  Faster_Whisper  ")
        assert transcription.resolve_provider() == "faster_whisper"


class TestFasterWhisperIndisponible:

    def test_erreur_claire_si_package_absent(self, monkeypatch) -> None:
        monkeypatch.setattr(transcription, "faster_whisper_disponible", lambda: False)
        with pytest.raises(transcription.TranscriptionError, match="requirements-transcription"):
            asyncio.run(
                transcription.transcribe_with_faster_whisper("/tmp/seance-fictive.ogg")
            )
