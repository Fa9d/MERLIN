"""
ivia-audio-pipeline
Pipeline de transcription et analyse des séances IVIA.
"""
import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class PipelineResult:
    client_id: str
    session_date: str
    transcript: str = ""
    diarization: list = field(default_factory=list)
    rgnr_scores: dict = field(default_factory=lambda: {
        "corps": 0, "emotions": 0, "pensees": 0, "environnement": 0
    })
    insights: str = ""
    tags: list = field(default_factory=list)
    duration_seconds: float = 0.0
    processing_time_seconds: float = 0.0


class IVIAAudioPipeline:
    """
    Pipeline complet : Audio → Whisper → SpeechBrain → MERLIN → Dashboard
    """

    def __init__(self, client_id: str, session_date: str, practitioner_id: str):
        self.client_id = client_id
        self.session_date = session_date
        self.practitioner_id = practitioner_id
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.language = os.getenv("LANGUAGE", "fr")

    def preprocess(self, audio_path: str) -> str:
        """Normalise et découpe l'audio si > 25MB."""
        # TODO: ffmpeg normalisation + chunking
        return audio_path

    def transcribe(self, audio_path: str) -> dict:
        """Whisper API transcription avec timestamps."""
        import openai
        client = openai.OpenAI(api_key=self.openai_api_key)
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=self.language,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        return result

    def diarize(self, audio_path: str, transcript: dict) -> list:
        """SpeechBrain diarisation — identifie praticien vs client."""
        # TODO: SpeechBrain ECAPA-TDNN diarisation
        return []

    def analyze_rgnr(self, transcript_text: str, diarization: list) -> dict:
        """MERLIN analyse RGNR via GPT-4o."""
        import openai
        client = openai.OpenAI(api_key=self.openai_api_key)

        prompt = f"""Tu es MERLIN, l'IA d'analyse thérapeutique d'IVIA.
Analyse cette transcription de séance et retourne un JSON structuré avec :
- rgnr_scores: {{corps: 0-100, emotions: 0-100, pensees: 0-100, environnement: 0-100}}
- insights: paragraphe d'analyse clinique (200-300 mots)
- tags: liste de thèmes cliniques identifiés (TCC, ACT, DBT, etc.)
- alerts: liste d'alertes si nécessaire

Transcription :
{transcript_text[:8000]}
"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        import json
        return json.loads(response.choices[0].message.content)

    def deliver(self, result: PipelineResult) -> bool:
        """Envoie les résultats à l'API IVIA."""
        import requests
        api_url = os.getenv("IVIA_API_URL", "https://api.ivia.app/v1")
        api_key = os.getenv("IVIA_API_KEY")
        # TODO: POST vers /sessions/{session_id}/analysis
        return True

    def process(self, audio_path: str) -> PipelineResult:
        """Orchestre l'ensemble du pipeline."""
        import time
        start = time.time()

        result = PipelineResult(
            client_id=self.client_id,
            session_date=self.session_date
        )

        print(f"[IVIA Pipeline] ▶ Traitement : {audio_path}")

        # 1. Préprocessing
        processed_path = self.preprocess(audio_path)

        # 2. Transcription
        print("[IVIA Pipeline] 🎙 Transcription Whisper...")
        transcript_data = self.transcribe(processed_path)
        result.transcript = transcript_data.get("text", "")

        # 3. Diarisation
        print("[IVIA Pipeline] 👥 Diarisation SpeechBrain...")
        result.diarization = self.diarize(processed_path, transcript_data)

        # 4. Analyse MERLIN
        print("[IVIA Pipeline] 🧠 Analyse MERLIN RGNR...")
        analysis = self.analyze_rgnr(result.transcript, result.diarization)
        result.rgnr_scores = analysis.get("rgnr_scores", result.rgnr_scores)
        result.insights = analysis.get("insights", "")
        result.tags = analysis.get("tags", [])

        # 5. Livraison
        print("[IVIA Pipeline] 📡 Livraison au dashboard...")
        self.deliver(result)

        result.processing_time_seconds = time.time() - start
        print(f"[IVIA Pipeline] ✅ Terminé en {result.processing_time_seconds:.1f}s")
        return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <audio_file> [client_id] [session_date]")
        sys.exit(1)

    pipeline = IVIAAudioPipeline(
        client_id=sys.argv[2] if len(sys.argv) > 2 else "test-client",
        session_date=sys.argv[3] if len(sys.argv) > 3 else "2026-07-09",
        practitioner_id="test-practitioner"
    )
    result = pipeline.process(sys.argv[1])
    print(f"\nRGNR Scores: {result.rgnr_scores}")
    print(f"Tags: {result.tags}")
    print(f"Insights:\n{result.insights}")
