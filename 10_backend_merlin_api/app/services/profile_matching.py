"""Matching praticien↔client sur profils comportementaux multi-couches (MERLIN).

Couches : Big Five (OCEAN), Schwartz (valeurs), 8 Expressions de l'Amour,
Attachement (Bartholomew), VAD (état dynamique).

Principe :
- chaque couche est notée en [0,1] via **cosine similarity** + **euclidienne pondérée** ;
- chaque couche a un **mode** : SIMILARITÉ (proximité = bon) ou COMPLÉMENTARITÉ
  (différence/équilibre = bon — ex. attachement) ;
- pondérations par couche **configurables** ;
- score global **0–100** + **explication** des dimensions dominantes.

Posture (constitution IVIA) : ces scores sont des **observations/hypothèses** d'aide à
l'orientation, **jamais un diagnostic ni un verdict de compatibilité**. Le matcher est
découplé de l'ORM : il opère sur des dicts (testable sans base).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class LayerMode(str, Enum):
    similarity = "similarity"          # proximité = bon (valeurs, traits)
    complementarity = "complementarity"  # équilibre/différence = bon (attachement)


# Dimensions numériques par couche (miroir de app/models/behavioral_profile.py).
LAYER_DIMENSIONS: dict[str, list[str]] = {
    "ocean": ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"],
    "schwartz": ["self_direction", "stimulation", "hedonism", "achievement", "power",
                 "security", "conformity", "tradition", "benevolence", "universalism"],
    "love": ["paroles_valorisantes", "moments_qualite", "contact_physique", "services_rendus",
             "cadeaux", "soutien_emotionnel", "espace_autonomie", "engagement_fiabilite"],
    "attachment": ["secure_score", "preoccupied_score", "dismissing_score", "fearful_score",
                   "self_model_anxiety", "other_model_avoidance"],
    "vad": ["valence", "arousal", "dominance"],
}

# Étendue des dimensions par couche (pour normaliser l'euclidienne). VAD ∈ [-1,1].
LAYER_RANGE: dict[str, float] = {"ocean": 1.0, "schwartz": 1.0, "love": 1.0,
                                 "attachment": 1.0, "vad": 2.0}

# Libellés FR (explication non-diagnostique).
DIM_LABELS_FR: dict[str, str] = {
    "openness": "ouverture", "conscientiousness": "rigueur", "extraversion": "extraversion",
    "agreeableness": "amabilité", "neuroticism": "réactivité émotionnelle",
    "self_direction": "autonomie", "stimulation": "stimulation", "hedonism": "plaisir",
    "achievement": "accomplissement", "power": "pouvoir", "security": "sécurité",
    "conformity": "conformité", "tradition": "tradition", "benevolence": "bienveillance",
    "universalism": "universalisme",
    "paroles_valorisantes": "paroles valorisantes", "moments_qualite": "moments de qualité",
    "contact_physique": "contact", "services_rendus": "services", "cadeaux": "cadeaux",
    "soutien_emotionnel": "soutien émotionnel", "espace_autonomie": "espace/autonomie",
    "engagement_fiabilite": "engagement/fiabilité",
    "valence": "tonalité", "arousal": "activation", "dominance": "assurance",
}
LAYER_LABELS_FR: dict[str, str] = {
    "ocean": "Traits", "schwartz": "Valeurs", "love": "Expressions relationnelles",
    "attachment": "Attachement", "vad": "État du moment",
}


@dataclass(frozen=True)
class LayerConfig:
    weight: float
    mode: LayerMode
    dim_weights: dict[str, float] | None = None  # pondération intra-couche (défaut : uniforme)


# Configuration par défaut (modes alignés sur la consigne : attachement → complémentaire,
# valeurs → similaire). Poids sommés à 1 (renormalisés si une couche manque).
DEFAULT_CONFIG: dict[str, LayerConfig] = {
    "ocean":      LayerConfig(0.20, LayerMode.similarity),
    "schwartz":   LayerConfig(0.25, LayerMode.similarity),
    "love":       LayerConfig(0.20, LayerMode.similarity),
    "attachment": LayerConfig(0.25, LayerMode.complementarity),
    "vad":        LayerConfig(0.10, LayerMode.similarity),
}

# Compatibilité d'attachement (Bartholomew) — une présence sécure stabilise ; le piège
# anxieux↔évitant est pénalisé. Valeurs symétriques.
_ATTACH_COMPAT: dict[frozenset, float] = {
    frozenset({"secure"}): 0.92,
    frozenset({"secure", "preoccupe"}): 0.85,
    frozenset({"secure", "detache"}): 0.82,
    frozenset({"secure", "craintif"}): 0.80,
    frozenset({"preoccupe"}): 0.45,
    frozenset({"preoccupe", "detache"}): 0.30,   # piège anxieux-évitant
    frozenset({"preoccupe", "craintif"}): 0.38,
    frozenset({"detache"}): 0.42,
    frozenset({"detache", "craintif"}): 0.40,
    frozenset({"craintif"}): 0.35,
}


@dataclass
class MatchResult:
    score: int                                   # 0–100
    per_layer: dict[str, dict] = field(default_factory=dict)
    dominant_dimensions: list[str] = field(default_factory=list)
    explanation: list[str] = field(default_factory=list)


# ── Primitives vectorielles (NumPy) ───────────────────────────────────────────
def _shared_vectors(a: dict, b: dict, dims: list[str]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Retourne les vecteurs alignés sur les dimensions présentes (non None) DES DEUX côtés."""
    keys = [d for d in dims if a.get(d) is not None and b.get(d) is not None]
    va = np.array([float(a[d]) for d in keys], dtype=float)
    vb = np.array([float(b[d]) for d in keys], dtype=float)
    return va, vb, keys


def _cosine(va: np.ndarray, vb: np.ndarray) -> float:
    """Cosine similarity → mappée [0,1]. 0.5 si vecteur nul (indéterminé)."""
    na, nb = np.linalg.norm(va), np.linalg.norm(vb)
    if na == 0 or nb == 0:
        return 0.5
    cos = float(np.dot(va, vb) / (na * nb))   # [-1,1]
    return (max(-1.0, min(1.0, cos)) + 1.0) / 2.0


def _weighted_euclidean_similarity(va, vb, keys, dim_weights, value_range) -> float:
    """1 − distance euclidienne pondérée normalisée → [0,1]."""
    w = np.array([(dim_weights or {}).get(k, 1.0) for k in keys], dtype=float)
    if w.sum() == 0:
        return 0.5
    dist = float(np.sqrt(np.sum(w * (va - vb) ** 2)))
    max_dist = float(np.sqrt(np.sum(w * (value_range ** 2))))  # diff max par dim = value_range
    return 1.0 - (dist / max_dist if max_dist else 0.0)


def _similarity_layer(a, b, dims, cfg, value_range) -> tuple[float, list[str]]:
    """Score de SIMILARITÉ d'une couche = moyenne(cosine, euclidienne) ; + dims les plus proches."""
    va, vb, keys = _shared_vectors(a, b, dims)
    if not keys:
        return None, []
    score = 0.5 * _cosine(va, vb) + 0.5 * _weighted_euclidean_similarity(
        va, vb, keys, cfg.dim_weights, value_range)
    # dimensions « dominantes » = les plus proches (points d'accroche)
    closeness = [(k, 1.0 - abs(a[k] - b[k]) / value_range) for k in keys]
    closeness.sort(key=lambda x: x[1], reverse=True)
    top = [k for k, _ in closeness[:3]]
    return float(max(0.0, min(1.0, score))), top


def _attachment_complementarity(a: dict, b: dict) -> tuple[float, list[str]]:
    """Complémentarité d'attachement : présence sécure valorisée, piège anxieux-évitant pénalisé.

    Utilise `primary_style` si présent des deux côtés ; sinon repli sur les axes
    anxiété/évitement (un partenaire stable relève le score)."""
    sa, sb = a.get("primary_style"), b.get("primary_style")
    if sa and sb:
        score = _ATTACH_COMPAT.get(frozenset({sa, sb}), 0.5)
        return score, ["style d'attachement"]
    # Repli sur les axes d'insécurité (anxiété + évitement), moyennés.
    def insec(p):
        vals = [p.get("self_model_anxiety"), p.get("other_model_avoidance")]
        vals = [v for v in vals if v is not None]
        return float(np.mean(vals)) if vals else None
    ia, ib = insec(a), insec(b)
    if ia is None or ib is None:
        return None, []
    stability = 1.0 - (ia + ib) / 2.0
    if ia > 0.5 and ib > 0.5:        # deux profils insécures → moins porteur
        stability *= 0.6
    return float(max(0.0, min(1.0, stability))), ["équilibre anxiété/évitement"]


def _generic_complementarity(a, b, dims, cfg, value_range) -> tuple[float, list[str]]:
    """Complémentarité générique : la DIFFÉRENCE est valorisée (1 − similarité euclidienne)."""
    va, vb, keys = _shared_vectors(a, b, dims)
    if not keys:
        return None, []
    sim = _weighted_euclidean_similarity(va, vb, keys, cfg.dim_weights, value_range)
    diffs = [(k, abs(a[k] - b[k]) / value_range) for k in keys]
    diffs.sort(key=lambda x: x[1], reverse=True)
    return float(max(0.0, min(1.0, 1.0 - sim))), [k for k, _ in diffs[:3]]


# ── Entrée publique ───────────────────────────────────────────────────────────
def match_profiles(
    profile_a: dict[str, dict],
    profile_b: dict[str, dict],
    config: dict[str, LayerConfig] | None = None,
) -> MatchResult:
    """Calcule un score de matching 0–100 entre deux profils 5 couches.

    profile_x : { 'ocean': {dim: float|None, ...}, 'schwartz': {...}, 'love': {...},
                  'attachment': {..., 'primary_style': 'secure'|...}, 'vad': {...} }
    Les couches/dimensions manquantes sont ignorées (poids renormalisés).
    """
    cfg = config or DEFAULT_CONFIG
    layer_scores: dict[str, float] = {}
    layer_tops: dict[str, list[str]] = {}

    for layer, lc in cfg.items():
        a = (profile_a or {}).get(layer) or {}
        b = (profile_b or {}).get(layer) or {}
        dims = LAYER_DIMENSIONS.get(layer, [])
        vr = LAYER_RANGE.get(layer, 1.0)

        if lc.mode is LayerMode.complementarity:
            if layer == "attachment":
                s, top = _attachment_complementarity(a, b)
            else:
                s, top = _generic_complementarity(a, b, dims, lc, vr)
        else:
            s, top = _similarity_layer(a, b, dims, lc, vr)

        if s is not None:
            layer_scores[layer] = s
            layer_tops[layer] = top

    if not layer_scores:
        return MatchResult(score=0, explanation=["Profils insuffisants pour un matching."])

    # Renormalisation des poids sur les couches disponibles.
    total_w = sum(cfg[l].weight for l in layer_scores)
    global_score = sum(layer_scores[l] * cfg[l].weight for l in layer_scores) / total_w

    per_layer = {}
    contributions = []
    for l, s in layer_scores.items():
        w_norm = cfg[l].weight / total_w
        per_layer[l] = {
            "score": round(s, 4),
            "weight": round(w_norm, 4),
            "mode": cfg[l].mode.value,
            "contribution": round(s * w_norm, 4),
            "top_dimensions": layer_tops[l],
        }
        contributions.append((l, s * w_norm))

    contributions.sort(key=lambda x: x[1], reverse=True)
    dominant = [l for l, _ in contributions[:3]]

    return MatchResult(
        score=int(round(global_score * 100)),
        per_layer=per_layer,
        dominant_dimensions=dominant,
        explanation=_explain(per_layer, dominant, cfg),
    )


def _explain(per_layer: dict, dominant: list[str], cfg: dict) -> list[str]:
    """Explication FR neutre (Observation), jamais diagnostique."""
    out: list[str] = []
    for layer in dominant:
        info = per_layer[layer]
        lbl = LAYER_LABELS_FR.get(layer, layer)
        pct = int(round(info["score"] * 100))
        dims_fr = ", ".join(DIM_LABELS_FR.get(d, d) for d in info["top_dimensions"]) or "—"
        if cfg[layer].mode is LayerMode.complementarity:
            out.append(f"{lbl} — complémentarité observée ({pct}/100) ; repères : {dims_fr}.")
        else:
            out.append(f"{lbl} — proximité observée ({pct}/100) sur : {dims_fr}.")
    return out
