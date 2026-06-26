"""Tests des insights comportementaux (sans réseau — appel Claude monkeypatché)."""
import json

import pytest

from app.services import behavioral_insights as bi

PROFIL = {
    "ocean": {"openness": 0.7, "extraversion": 0.4, "neuroticism": 0.6},
    "schwartz": {"benevolence": 0.9, "security": 0.5},
    "love": {"soutien_emotionnel": 0.9, "contact_physique": 0.2},
    "attachment": {"primary_style": "preoccupe", "self_model_anxiety": 0.7},
    "vad": {"valence": -0.2, "arousal": 0.3, "dominance": -0.1},
}


def test_build_input_omet_couches_absentes_et_ajoute_fiabilite():
    p = {"ocean": {"openness": 0.5}}
    out = bi.build_insights_input(p, fiabilite="à nuancer")
    assert out["ocean"] == {"openness": 0.5}
    assert "schwartz" not in out
    assert out["fiabilite"] == "à nuancer"


def test_render_prompt_charge_le_template_et_injecte_le_profil():
    prompt = bi.render_insights_prompt(bi.build_insights_input(PROFIL))
    assert "Observation" in prompt and "Orientation" in prompt   # triade du template
    assert "preoccupe" in prompt                                 # profil injecté
    assert "Entrée (profil du client)" in prompt


@pytest.mark.asyncio
async def test_generate_parse_et_valide(monkeypatch):
    fake = {
        "praticien": {
            "style_communication": "Rythme posé, reformulations douces.",
            "points_attention": ["Besoin de réassurance possible."],
            "approches": ["Nommer ce qui est entendu avant d'orienter."],
        },
        "tensions_internes": [
            {"description": "Fort besoin de soutien émotionnel, peu de recherche de contact.",
             "indices": ["soutien_emotionnel élevé", "contact_physique bas"]}
        ],
        "ressources_exercices": [{"titre": "Journal des appuis", "pourquoi": "Repérer ce qui sécurise."}],
        "resume_client": "Vous accordez de l'importance à vous sentir entendu·e. C'est un beau point d'appui.",
    }

    async def _fake_call(prompt):
        return "```json\n" + json.dumps(fake, ensure_ascii=False) + "\n```"

    monkeypatch.setattr(bi, "_call_claude", _fake_call)
    res = await bi.generate_behavioral_insights(PROFIL)
    assert res["praticien"]["style_communication"]
    assert res["resume_client"]


@pytest.mark.asyncio
async def test_generate_rejette_json_incomplet(monkeypatch):
    async def _bad_call(prompt):
        return json.dumps({"resume_client": "ok"})  # manque praticien/tensions/ressources

    monkeypatch.setattr(bi, "_call_claude", _bad_call)
    with pytest.raises(bi.BehavioralInsightsError):
        await bi.generate_behavioral_insights(PROFIL)
