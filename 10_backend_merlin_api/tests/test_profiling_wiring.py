"""Tests du câblage profilage — DB-free (les tests touchant les tables 0039 sont
listés dans la security review et à exécuter après migration)."""
import pytest

# Charge tous les modèles pour que configure_mappers() résolve les relations
# (ex. PractitionerProfile) lors de la construction d'instances ORM.
from app.db.base import load_models

load_models()

from app.models.behavioral_profile import AttachmentProfileBartholomew, TraitProfileOcean
from app.models.enums import AttachmentStyle, ProfileSubjectKind
from app.services import behavioral_profile_service as svc
from app.services import love_quiz
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe, find_violations


# ── B4 : garde d'urgence déterministe ─────────────────────────────────────────
def test_garde_urgence_bloque_detresse():
    with pytest.raises(svc.EmergencyDetectedError):
        svc.guard_free_text("j'ai envie de me suicider, j'en peux plus")


def test_garde_urgence_laisse_passer_texte_neutre():
    svc.guard_free_text("j'aime les longues marches et le silence")  # ne lève rien


# ── B2 : consentement obligatoire à l'écriture (avant tout accès DB) ──────────
def test_record_layer_refuse_sans_consentement():
    with pytest.raises(svc.ConsentRequiredError):
        svc.record_layer(
            None, layer="love", scores={"cadeaux": 0.5},
            subject_kind=ProfileSubjectKind.client, client_id="c1", consent_id=None,
        )


def test_record_layer_refuse_sujet_ambigu():
    with pytest.raises(ValueError):
        svc.record_layer(
            None, layer="love", scores={}, subject_kind=ProfileSubjectKind.client,
            consent_id="k1", client_id="c1", practitioner_user_id="p1",
        )


# ── Adaptateurs ORM → dict (sans session) ─────────────────────────────────────
def test_row_to_scores_ocean():
    row = TraitProfileOcean(openness=0.8, conscientiousness=0.6, extraversion=0.5,
                            agreeableness=0.7, neuroticism=0.3)
    d = svc.row_to_scores("ocean", row)
    assert d["openness"] == 0.8 and d["neuroticism"] == 0.3


def test_row_to_scores_attachment_primary_style_serialise():
    row = AttachmentProfileBartholomew(secure_score=0.8, primary_style=AttachmentStyle.secure)
    d = svc.row_to_scores("attachment", row)
    assert d["primary_style"] == "secure"   # valeur d'enum sérialisée


# ── B3 + Loi 21 : la vue client ne contient ni score ni terme interdit ───────
def test_compose_client_view_sans_score_ni_chiffre():
    ctx = love_quiz.build_narrative_context({
        q.id: 5 for q in love_quiz.QUESTION_BANK
        if q.dim == "soutien_emotionnel" and not q.reverse
    })
    view = love_quiz.compose_client_view(ctx)
    assert set(view) == {"observation", "hypothese", "orientation"}
    blob = " ".join(view.values())
    assert not any(ch.isdigit() for ch in blob)             # aucun chiffre/score
    assert find_violations(blob) == []                       # aucun terme Loi 21


def test_loi21_filter_bloque_diagnostic():
    assert_client_safe("Vous avez beaucoup de douceur.")     # ok
    for bad in ("Vous avez un trouble de l'attachement.", "C'est une pathologie.",
                "Je propose une thérapie."):
        with pytest.raises(Loi21ViolationError):
            assert_client_safe(bad)


# ── Câblage : le routeur expose les 3 routes ─────────────────────────────────
# (on importe le routeur directement, pas app.main — celui-ci tire sessions.py qui
#  porte un bug pré-existant `BaseModel` non importé, hors périmètre de ce câblage.)
def test_routes_profiling_enregistrees():
    from app.api.routes.profiling import router
    paths = {r.path for r in router.routes}
    assert "/profiling/me/quiz/love" in paths
    assert "/profiling/matching/compute" in paths
    assert "/profiling/insights/generate" in paths
