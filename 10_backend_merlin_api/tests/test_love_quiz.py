"""Tests du quiz adaptatif des 8 Expressions de l'Amour (logique pure)."""
from app.services.love_quiz import (
    DIMENSIONS,
    QUESTION_BANK,
    QuizSession,
    build_narrative_context,
    detect_biases,
    score,
)


def test_banque_40_items_5_par_dimension():
    assert len(QUESTION_BANK) == 40
    for d in DIMENSIONS:
        items = [q for q in QUESTION_BANK if q.dim == d]
        assert len(items) == 5, d
        assert any(q.reverse for q in items)      # au moins un item inverse (acquiescence)


def test_ids_uniques():
    ids = [q.id for q in QUESTION_BANK]
    assert len(ids) == len(set(ids))


def test_selection_adaptative_couvre_les_dimensions():
    """L'adaptation sert d'abord les dimensions les moins couvertes."""
    s = QuizSession(max_items=18, min_per_dim=2)
    guard = 0
    while not s.is_complete() and guard < 50:
        q = s.next_item()
        if q is None:
            break
        s.answer(q.id, 4)
        guard += 1
    counts = {d: sum(1 for iid in s.responses if iid.startswith(d)) for d in DIMENSIONS}
    assert all(c >= 2 for c in counts.values())   # chaque dimension mesurée ≥ 2 fois


def test_scoring_normalise_0_1_et_inverse_corrige():
    # Répondre 5 à un item normal -> haut ; 5 à un item inverse -> bas (corrigé)
    fwd = next(q for q in QUESTION_BANK if q.dim == "cadeaux" and not q.reverse)
    rev = next(q for q in QUESTION_BANK if q.dim == "cadeaux" and q.reverse)
    sc_fwd = score({fwd.id: 5})["cadeaux"]
    sc_rev = score({rev.id: 5})["cadeaux"]
    assert sc_fwd > 0.9
    assert sc_rev < 0.1
    assert 0.0 <= sc_fwd <= 1.0 and 0.0 <= sc_rev <= 1.0


def test_detection_acquiescence():
    """Approuver fortement un item ET son inverse → acquiescence signalée."""
    resp = {}
    for d in DIMENSIONS:
        for q in QUESTION_BANK:
            if q.dim == d and q.kind == "likert":
                resp[q.id] = 5  # tout approuver, y compris les inverses
    b = detect_biases(resp)
    assert b["acquiescence"]["flag"] is True


def test_detection_desirabilite_sociale():
    sd_items = [q.id for q in QUESTION_BANK if q.sd]
    resp = {iid: 5 for iid in sd_items}
    b = detect_biases(resp)
    assert b["social_desirability"]["score"] == 1.0
    assert b["social_desirability"]["flag"] is True


def test_contexte_narratif_sans_verdict():
    # Profil contrasté : soutien émotionnel fort, cadeaux faible
    resp = {}
    for q in QUESTION_BANK:
        if q.dim == "soutien_emotionnel" and not q.reverse:
            resp[q.id] = 5
        elif q.dim == "cadeaux" and not q.reverse:
            resp[q.id] = 1
    ctx = build_narrative_context(resp)
    assert ctx["prompt_id"] == "PROD-PROF-001"
    assert ctx["dominantes"]
    assert all(0.0 <= d["score"] <= 1.0 for d in ctx["dominantes"])
    assert "diagnostic" not in ctx["consigne"].lower() or "jamais" in ctx["consigne"].lower()
