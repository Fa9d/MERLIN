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

_GOOD = {
    "praticien": {
        "style_communication": "Rythme posé, reformulations douces.",
        "points_attention": ["Besoin de réassurance possible."],
        "approches": ["Nommer ce qui est entendu avant d'orienter."],
    },
    "tensions_internes": [{"description": "Soutien fort, contact faible.", "indices": ["x"]}],
    "ressources_exercices": [{"titre": "Journal des appuis", "pourquoi": "Repérer ce qui sécurise."}],
    "resume_client": "Vous accordez de l'importance à vous sentir entendu·e. C'est un bel appui.",
}


def _fake_call(text, usage=None):
    async def _c(prompt):
        return text, (usage or {"input_tokens": 500, "output_tokens": 200})
    return _c


def test_build_input_omet_couches_absentes():
    out = bi.build_insights_input({"ocean": {"openness": 0.5}}, fiabilite="à nuancer")
    assert out["ocean"] == {"openness": 0.5} and "schwartz" not in out and out["fiabilite"] == "à nuancer"


def test_render_prompt_charge_template_et_injecte_profil():
    prompt = bi.render_insights_prompt(bi.build_insights_input(PROFIL))
    assert "Observation" in prompt and "preoccupe" in prompt


@pytest.mark.asyncio
async def test_nominal(monkeypatch):
    bi._DAILY_COUNT.clear()
    monkeypatch.setattr(bi, "_call_claude", _fake_call("```json\n" + json.dumps(_GOOD, ensure_ascii=False) + "\n```"))
    res = await bi.generate_behavioral_insights(PROFIL)
    assert res["resume_client"] and res["praticien"]["style_communication"]


@pytest.mark.asyncio
async def test_postfiltre_loi21_rejette_resume_interdit(monkeypatch):
    bi._DAILY_COUNT.clear()
    bad = dict(_GOOD, resume_client="Vous avez un trouble de l'attachement.")
    monkeypatch.setattr(bi, "_call_claude", _fake_call(json.dumps(bad, ensure_ascii=False)))
    with pytest.raises(bi.BehavioralInsightsError):
        await bi.generate_behavioral_insights(PROFIL)


@pytest.mark.asyncio
async def test_fallback_sur_sortie_non_conforme(monkeypatch):
    bi._DAILY_COUNT.clear()
    bad = dict(_GOOD, resume_client="C'est une pathologie.")
    monkeypatch.setattr(bi, "_call_claude", _fake_call(json.dumps(bad, ensure_ascii=False)))
    out = await bi.generate_with_fallback(PROFIL)
    assert out["degraded"] is True and out["insights"] is bi._FALLBACK


@pytest.mark.asyncio
async def test_fallback_sur_echec_api(monkeypatch):
    bi._DAILY_COUNT.clear()
    async def _boom(prompt):
        raise bi.BehavioralInsightsError("Anthropic indisponible")
    monkeypatch.setattr(bi, "_call_claude", _boom)
    out = await bi.generate_with_fallback(PROFIL)
    assert out["ok"] is False and out["degraded"] is True


@pytest.mark.asyncio
async def test_cap_de_cout_quotidien():
    from datetime import date
    cap = bi.settings.insights_daily_cap
    assert cap and cap > 0          # garde-fou actif par défaut
    bi._DAILY_COUNT.clear()
    bi._DAILY_COUNT[date.today().isoformat()] = cap   # plafond déjà atteint
    out = await bi.generate_with_fallback(PROFIL)
    assert out["degraded"] is True and out["reason"] == "cap"
    bi._DAILY_COUNT.clear()


def test_estimation_cout():
    c = bi._estimate_cost_cents("claude-sonnet-4-6", {"input_tokens": 1000, "output_tokens": 1000})
    assert c > 0
