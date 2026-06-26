"""Quiz adaptatif — 8 Expressions de l'Amour (MERLIN).

- Banque de 40 items (Likert 1–5 + scénarios situationnels), 5 par dimension.
- Sélection **adaptative IRT-inspirée** (Rasch 1PL) : on mesure d'abord les
  dimensions les moins couvertes, puis l'item le plus informatif (Fisher) au
  niveau estimé.
- Scoring : vecteur normalisé **[0,1]** par dimension (moyenne pondérée par la
  discrimination, items inverses corrigés).
- Détection de **biais** : acquiescence (paires item/inverse) + désirabilité sociale.
- Contexte narratif prêt pour le LLM (le texte est généré par le prompt
  `11_PROMPTS/06_profilage/PROMPT_quiz_amour_narratif_v1.md`, id `PROD-PROF-001`).

Posture (constitution IVIA) : il s'agit de **préférences relationnelles**, pas d'un
test clinique ni d'un diagnostic. Vocabulaire Loi 21 ; restitution Observation/
Hypothèse/Orientation (jamais de verdict).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

DIMENSIONS = [
    "paroles_valorisantes", "moments_qualite", "contact_physique", "services_rendus",
    "cadeaux", "soutien_emotionnel", "espace_autonomie", "engagement_fiabilite",
]
DIM_LABELS_FR = {
    "paroles_valorisantes": "Paroles valorisantes", "moments_qualite": "Moments de qualité",
    "contact_physique": "Contact physique", "services_rendus": "Services rendus",
    "cadeaux": "Cadeaux", "soutien_emotionnel": "Soutien émotionnel",
    "espace_autonomie": "Espace et autonomie", "engagement_fiabilite": "Engagement et fiabilité",
}

NARRATIVE_PROMPT_ID = "PROD-PROF-001"


@dataclass(frozen=True)
class QItem:
    id: str
    dim: str
    text: str
    kind: str = "likert"          # 'likert' (1–5) | 'scenario'
    a: float = 1.0                # discrimination (IRT)
    b: float = 0.0               # difficulté (IRT), ~[-1,1]
    reverse: bool = False         # item inversé (sert aussi à l'acquiescence)
    sd: bool = False              # marqueur de désirabilité sociale
    options: tuple[str, ...] = ()  # libellés (scénario)


# ── Banque de 40 items (5 par dimension : 3 likert + 1 inverse + 1 scénario) ──
def _bank() -> list[QItem]:
    raw = [
        # dim, suffixe, texte, kind, a, b, reverse, sd
        ("paroles_valorisantes", "1", "Entendre « je suis fier·ère de toi » me touche profondément.", "likert", 1.2, -0.3, False, False),
        ("paroles_valorisantes", "2", "Les encouragements sincères me donnent de l'élan.", "likert", 1.0, 0.0, False, False),
        ("paroles_valorisantes", "3", "Un compliment précis vaut mieux qu'un grand geste.", "likert", 0.9, 0.4, False, False),
        ("paroles_valorisantes", "R", "Les mots comptent peu pour moi, seuls les actes parlent.", "likert", 1.1, 0.1, True, False),
        ("paroles_valorisantes", "S", "Quand on me valorise, je préfère répondre une parole bienveillante plutôt qu'un service.", "scenario", 1.0, 0.0, False, False),

        ("moments_qualite", "1", "Du temps ensemble, sans distraction, me ressource.", "likert", 1.3, -0.4, False, False),
        ("moments_qualite", "2", "Je me sens proche quand on partage une activité à deux.", "likert", 1.0, 0.0, False, False),
        ("moments_qualite", "3", "Une conversation attentive me nourrit plus qu'un cadeau.", "likert", 0.9, 0.3, False, False),
        ("moments_qualite", "R", "Passer beaucoup de temps ensemble n'est pas important pour moi.", "likert", 1.1, 0.1, True, False),
        ("moments_qualite", "S", "Pour me sentir relié·e, je choisis d'abord un moment partagé sans écran.", "scenario", 1.0, -0.1, False, False),

        ("contact_physique", "1", "Un contact rassurant (main, épaule) m'apaise.", "likert", 1.2, -0.2, False, False),
        ("contact_physique", "2", "La présence physique me sécurise plus que les mots.", "likert", 1.0, 0.1, False, False),
        ("contact_physique", "3", "Je remarque vite l'absence de contact chaleureux.", "likert", 0.9, 0.4, False, False),
        ("contact_physique", "R", "Le contact physique m'est plutôt indifférent.", "likert", 1.1, 0.0, True, False),
        ("contact_physique", "S", "Dans un moment difficile, une présence proche me réconforte plus qu'un conseil.", "scenario", 1.0, -0.1, False, False),

        ("services_rendus", "1", "Quand on m'aide concrètement, je me sens aimé·e.", "likert", 1.2, -0.3, False, False),
        ("services_rendus", "2", "Un coup de main vaut mille mots pour moi.", "likert", 1.0, 0.0, False, False),
        ("services_rendus", "3", "J'apprécie qu'on anticipe mes besoins pratiques.", "likert", 0.9, 0.3, False, False),
        ("services_rendus", "R", "Qu'on me rende service ne change pas grand-chose à ce que je ressens.", "likert", 1.1, 0.1, True, False),
        ("services_rendus", "S", "Quand je suis débordé·e, qu'on m'enlève une tâche me touche plus qu'un mot doux.", "scenario", 1.0, 0.0, False, False),

        ("cadeaux", "1", "Un présent réfléchi me fait sentir pensé·e.", "likert", 1.1, 0.0, False, False),
        ("cadeaux", "2", "Recevoir un objet symbolique me touche.", "likert", 1.0, 0.2, False, False),
        ("cadeaux", "3", "Je garde longtemps les petites attentions matérielles.", "likert", 0.9, 0.4, False, False),
        ("cadeaux", "R", "Les cadeaux n'ont pas vraiment d'importance pour moi.", "likert", 1.1, 0.0, True, False),
        ("cadeaux", "S", "Un petit présent inattendu me marque autant qu'une longue conversation.", "scenario", 0.9, 0.3, False, False),

        ("soutien_emotionnel", "1", "Me sentir écouté·e dans mes émotions est essentiel.", "likert", 1.3, -0.5, False, True),
        ("soutien_emotionnel", "2", "Qu'on accueille ma peine sans la juger me soulage.", "likert", 1.1, -0.2, False, False),
        ("soutien_emotionnel", "3", "J'ai besoin qu'on reconnaisse ce que je traverse.", "likert", 1.0, 0.0, False, False),
        ("soutien_emotionnel", "R", "Je préfère gérer mes émotions seul·e, sans soutien.", "likert", 1.0, 0.2, True, False),
        ("soutien_emotionnel", "S", "Dans l'épreuve, être entendu·e compte plus pour moi que recevoir des solutions.", "scenario", 1.1, -0.2, False, False),

        ("espace_autonomie", "1", "J'ai besoin de moments à moi pour me sentir bien.", "likert", 1.1, -0.1, False, False),
        ("espace_autonomie", "2", "Qu'on respecte mon indépendance est une marque d'amour.", "likert", 1.0, 0.1, False, False),
        ("espace_autonomie", "3", "Trop de sollicitation m'étouffe.", "likert", 0.9, 0.3, False, False),
        ("espace_autonomie", "R", "J'aime être entouré·e en permanence.", "likert", 1.0, 0.0, True, False),
        ("espace_autonomie", "S", "Après une journée intense, j'ai d'abord besoin de souffler seul·e avant de partager.", "scenario", 1.0, 0.0, False, False),

        ("engagement_fiabilite", "1", "La constance et la fiabilité me rassurent profondément.", "likert", 1.2, -0.3, False, True),
        ("engagement_fiabilite", "2", "Tenir ses promesses est, pour moi, une preuve d'amour.", "likert", 1.1, -0.1, False, True),
        ("engagement_fiabilite", "3", "Je me sens en sécurité quand je peux compter sur quelqu'un.", "likert", 1.0, 0.0, False, False),
        ("engagement_fiabilite", "R", "L'imprévu me convient mieux que la régularité d'un engagement.", "likert", 1.0, 0.2, True, False),
        ("engagement_fiabilite", "S", "Savoir qu'une personne sera là demain comme promis me touche plus qu'un grand geste ponctuel.", "scenario", 1.1, -0.1, False, False),
    ]
    items = []
    for dim, suf, text, kind, a, b, rev, sd in raw:
        opts = ("Plutôt cette option", "Plutôt l'autre") if kind == "scenario" else ()
        items.append(QItem(id=f"{dim}_{suf}", dim=dim, text=text, kind=kind,
                            a=a, b=b, reverse=rev, sd=sd, options=opts))
    return items


QUESTION_BANK: list[QItem] = _bank()
_BY_ID = {q.id: q for q in QUESTION_BANK}


# ── Session adaptative ────────────────────────────────────────────────────────
@dataclass
class QuizSession:
    responses: dict[str, int] = field(default_factory=dict)  # item_id -> 1..5
    max_items: int = 18
    min_per_dim: int = 2

    def _count_by_dim(self) -> dict[str, int]:
        c = {d: 0 for d in DIMENSIONS}
        for iid in self.responses:
            c[_BY_ID[iid].dim] += 1
        return c

    def _theta(self, dim: str) -> float:
        """Estimation logit du niveau courant sur une dimension (à partir des réponses)."""
        vals = []
        for iid, r in self.responses.items():
            q = _BY_ID[iid]
            if q.dim != dim:
                continue
            n = (r - 1) / 4.0
            if q.reverse:
                n = 1.0 - n
            vals.append(n)
        if not vals:
            return 0.0
        p = min(0.98, max(0.02, sum(vals) / len(vals)))
        return math.log(p / (1 - p))

    @staticmethod
    def _info(q: QItem, theta: float) -> float:
        """Information de Fisher (Rasch) de l'item au niveau theta."""
        p = 1.0 / (1.0 + math.exp(-q.a * (theta - q.b)))
        return q.a * q.a * p * (1 - p)

    def is_complete(self) -> bool:
        if len(self.responses) >= self.max_items:
            return True
        return all(c >= self.min_per_dim for c in self._count_by_dim().values()) and \
            len(self.responses) >= len(DIMENSIONS) * self.min_per_dim

    def next_item(self) -> QItem | None:
        """Item suivant : dimension la moins couverte, puis item le plus informatif."""
        if self.is_complete():
            return None
        counts = self._count_by_dim()
        target_dim = min(DIMENSIONS, key=lambda d: counts[d])
        theta = self._theta(target_dim)
        candidates = [q for q in QUESTION_BANK if q.dim == target_dim and q.id not in self.responses]
        if not candidates:  # dimension épuisée → n'importe quel item restant
            candidates = [q for q in QUESTION_BANK if q.id not in self.responses]
            if not candidates:
                return None
        return max(candidates, key=lambda q: self._info(q, theta))

    def answer(self, item_id: str, value: int) -> None:
        if item_id not in _BY_ID:
            raise KeyError(f"Item inconnu : {item_id}")
        if not 1 <= value <= 5:
            raise ValueError("La réponse Likert doit être entre 1 et 5.")
        self.responses[item_id] = value


# ── Scoring + biais ───────────────────────────────────────────────────────────
def score(responses: dict[str, int]) -> dict[str, float]:
    """Vecteur normalisé [0,1] par dimension (moyenne pondérée par la discrimination)."""
    out = {}
    for dim in DIMENSIONS:
        num = den = 0.0
        for iid, r in responses.items():
            q = _BY_ID.get(iid)
            if not q or q.dim != dim:
                continue
            n = (r - 1) / 4.0
            if q.reverse:
                n = 1.0 - n
            num += q.a * n
            den += q.a
        out[dim] = round(num / den, 4) if den else None
    return out


def detect_biases(responses: dict[str, int]) -> dict[str, dict]:
    """Acquiescence (paires item/inverse) + désirabilité sociale (items marqueurs)."""
    # Acquiescence : tendance à approuver un item ET son inverse (brut, non corrigé).
    pair_scores = []
    by_dim_fwd: dict[str, list[int]] = {}
    by_dim_rev: dict[str, list[int]] = {}
    for iid, r in responses.items():
        q = _BY_ID[iid]
        (by_dim_rev if q.reverse else by_dim_fwd).setdefault(q.dim, []).append(r)
    for dim in DIMENSIONS:
        fwd, rev = by_dim_fwd.get(dim), by_dim_rev.get(dim)
        if fwd and rev:
            f, v = sum(fwd) / len(fwd), sum(rev) / len(rev)
            pair_scores.append(max(0.0, (f + v - 6.0) / 4.0))  # 0 si cohérent, 1 si tout approuvé
    acq = round(sum(pair_scores) / len(pair_scores), 4) if pair_scores else 0.0

    # Désirabilité sociale : sur-approbation des items marqueurs.
    sd_vals = [(r - 1) / 4.0 for iid, r in responses.items() if _BY_ID[iid].sd]
    sd = round(sum(sd_vals) / len(sd_vals), 4) if sd_vals else 0.0

    return {
        "acquiescence": {"score": acq, "flag": acq > 0.40},
        "social_desirability": {"score": sd, "flag": sd > 0.85},
    }


def build_narrative_context(responses: dict[str, int]) -> dict:
    """Contexte structuré prêt pour le prompt LLM (id PROD-PROF-001).

    Ne contient AUCUN verdict : scores + dominantes + tensions + fiabilité.
    Le texte narratif est produit par le LLM via le template `11_PROMPTS`.
    """
    sc = {d: v for d, v in score(responses).items() if v is not None}
    biases = detect_biases(responses)
    ordered = sorted(sc.items(), key=lambda x: x[1], reverse=True)
    dominantes = [{"dimension": d, "label": DIM_LABELS_FR[d], "score": v} for d, v in ordered[:3]]
    secondaires = [{"dimension": d, "label": DIM_LABELS_FR[d], "score": v} for d, v in ordered[-2:]]

    # Tensions internes : une dominante forte qui contraste avec une secondaire faible.
    tensions = []
    if ordered and ordered[0][1] - ordered[-1][1] >= 0.4:
        tensions.append({
            "fort": DIM_LABELS_FR[ordered[0][0]],
            "faible": DIM_LABELS_FR[ordered[-1][0]],
        })

    fiabilite = "bonne"
    if biases["acquiescence"]["flag"] or biases["social_desirability"]["flag"]:
        fiabilite = "à nuancer"

    return {
        "prompt_id": NARRATIVE_PROMPT_ID,
        "scores": sc,
        "dominantes": dominantes,
        "secondaires": secondaires,
        "tensions": tensions,
        "biais": biases,
        "fiabilite": fiabilite,
        "n_items": len(responses),
        "consigne": (
            "Restituer en français, ton bienveillant, registre Observation/Hypothèse/"
            "Orientation. Préférences relationnelles, jamais un diagnostic ni un verdict."
        ),
    }


def compose_client_view(context: dict) -> dict:
    """Restitution CLIENT déterministe (hors LLM) — B3 : aucun score, aucune étiquette.

    Construit une triade Observation/Hypothèse/Orientation à partir du contexte, puis
    la passe au pare-feu Loi 21. Utilisable sans appel Anthropic. Forme alignée sur
    `ClientFacingProfileView` (app/schemas/behavioral_profile.py).
    """
    from app.services.loi21_filter import assert_client_safe  # import local (évite cycle)

    doms = [d["label"].lower() for d in context.get("dominantes", [])][:2]
    if doms:
        liste = " et ".join(doms)
        observation = (
            f"Ce que vous avez partagé met en lumière l'importance, pour vous, de {liste}."
        )
    else:
        observation = "Vos réponses donnent un premier éclairage sur ce qui vous fait du bien."

    hypothese = (
        "Il se pourrait que ces préférences éclairent ce qui vous aide à vous sentir "
        "considéré·e et relié·e — c'est un repère, pas une étiquette."
    )
    if context.get("fiabilite") == "à nuancer":
        hypothese += " On pourra y revenir : ce premier passage reste à confirmer."

    orientation = (
        "Gardez cela comme un point de départ. Si vous le souhaitez, vous pourrez en "
        "parler avec un·e praticien·ne pour l'explorer à votre rythme."
    )

    return {
        "observation": assert_client_safe(observation),
        "hypothese": assert_client_safe(hypothese),
        "orientation": assert_client_safe(orientation),
    }
