"""Tests du matching comportemental (sans base — logique pure NumPy)."""
from app.services.profile_matching import (
    LayerConfig,
    LayerMode,
    match_profiles,
)


def _full(ocean, schwartz, love, attach, vad):
    return {"ocean": ocean, "schwartz": schwartz, "love": love,
            "attachment": attach, "vad": vad}


def test_identique_donne_score_eleve():
    """Deux profils identiques (couches similarité) → score haut."""
    p = _full(
        {"openness": .8, "conscientiousness": .6, "extraversion": .5, "agreeableness": .7, "neuroticism": .3},
        {"benevolence": .9, "universalism": .8, "security": .5, "self_direction": .6, "stimulation": .4,
         "hedonism": .3, "achievement": .5, "power": .2, "conformity": .4, "tradition": .3},
        {"moments_qualite": .8, "soutien_emotionnel": .7, "paroles_valorisantes": .6, "contact_physique": .4,
         "services_rendus": .5, "cadeaux": .2, "espace_autonomie": .5, "engagement_fiabilite": .8},
        {"primary_style": "secure", "self_model_anxiety": .2, "other_model_avoidance": .2},
        {"valence": .4, "arousal": .1, "dominance": .3},
    )
    res = match_profiles(p, p)
    assert res.score >= 80
    assert res.explanation


def test_valeurs_opposees_baissent_le_score():
    """Valeurs (similarité) opposées → la couche valeurs tire le score vers le bas."""
    a = _full({}, {"benevolence": .9, "universalism": .9, "security": .1, "power": .1}, {}, {}, {})
    b = _full({}, {"benevolence": .1, "universalism": .1, "security": .9, "power": .9}, {}, {}, {})
    res = match_profiles(a, b)
    assert res.per_layer["schwartz"]["score"] < 0.5


def test_attachement_complementaire_secure_eleve():
    """Un praticien sécure complète mieux qu'un appariement anxieux-évitant."""
    client = {"attachment": {"primary_style": "preoccupe", "self_model_anxiety": .8, "other_model_avoidance": .3}}
    prat_secure = {"attachment": {"primary_style": "secure", "self_model_anxiety": .2, "other_model_avoidance": .2}}
    prat_detache = {"attachment": {"primary_style": "detache", "self_model_anxiety": .3, "other_model_avoidance": .8}}
    s_secure = match_profiles(client, prat_secure).per_layer["attachment"]["score"]
    s_piege = match_profiles(client, prat_detache).per_layer["attachment"]["score"]
    assert s_secure > s_piege
    assert s_secure >= 0.8


def test_score_borne_0_100_et_explication():
    res = match_profiles(
        {"ocean": {"openness": .5, "extraversion": .5, "agreeableness": .5}},
        {"ocean": {"openness": .5, "extraversion": .5, "agreeableness": .5}},
    )
    assert 0 <= res.score <= 100
    assert isinstance(res.explanation, list)
    assert res.dominant_dimensions


def test_profil_vide_renvoie_zero():
    res = match_profiles({}, {})
    assert res.score == 0


def test_dimensions_manquantes_renormalisent_les_poids():
    """Si seules 2 couches sont présentes, les poids se renormalisent (somme = 1)."""
    a = _full({"openness": .5}, {"benevolence": .5}, {}, {}, {})
    b = _full({"openness": .5}, {"benevolence": .5}, {}, {}, {})
    res = match_profiles(a, b)
    total = sum(v["weight"] for v in res.per_layer.values())
    assert abs(total - 1.0) < 1e-6


def test_config_personnalisee_change_le_resultat():
    """Pondérations configurables : mettre tout le poids sur une couche change le score."""
    a = _full({"openness": .9}, {"benevolence": .1}, {}, {}, {})
    b = _full({"openness": .9}, {"benevolence": .9}, {}, {}, {})
    only_ocean = {"ocean": LayerConfig(1.0, LayerMode.similarity)}
    res = match_profiles(a, b, config=only_ocean)
    assert res.score >= 80  # ocean identique → haut, valeurs ignorées
