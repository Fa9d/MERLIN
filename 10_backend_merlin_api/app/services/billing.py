"""Facturation & comptabilité IVIA — source de vérité des prix et décomposition.

Tous les prix sont **TTC** (taxe incluse) en cents CAD. IVIA absorbe les frais Stripe.

Décomposition d'un encaissement :
    TTC = HT + TPS + TVQ           (taxes seulement si assujetti)
    HT  = revenu IVIA brut
    Marge IVIA = HT − frais_stripe − cout_ia − part_praticien

Tant que `settings.tax_registered` est False (sous le seuil de petit fournisseur
de 30 000 $), aucune taxe n'est perçue : HT = TTC, TPS = TVQ = 0. Le jour de
l'inscription, basculer `MERLIN_TAX_REGISTERED=true` active la décomposition —
aucune autre modification de code requise.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True)
class Offer:
    code: str
    label: str
    amount_ttc_cents: int   # prix affiché, taxe incluse
    live: bool              # True = temps praticien (séance), False = asynchrone


# Catalogue officiel (miroir des prix serveur ; voir config stripe_*_amount_cents).
# Les 3 offres IVIA : 35 = enregistrement + rappel 10 min ; 49 = séance live 30 min ;
# 75 = séance live 1 h. Toutes incluent transcription + analyse.
OFFERS: dict[str, Offer] = {
    "enr_rappel": Offer("enr_rappel", "Enregistrement + rappel 10 min", 3500, live=False),
    "seance_live": Offer("seance_live", "Séance live · 30 min / 1 h",    7500, live=True),
}

# Frais Stripe Canada (cartes domestiques) — pour estimation ; le montant réel
# vient de la balance transaction Stripe au webhook quand disponible.
STRIPE_PCT = 0.029
STRIPE_FIXED_CENTS = 30

# Coût IA indicatif par analyse (Sonnet 4.6 ; ~0,10–0,13 $). Affiné si on logge l'usage réel.
AI_COST_CENTS_ESTIMATE = 12

# --- Modèle praticien (voir docs/MODELE_PRATICIEN_IVIA.md) ------------------------
# Frais plateforme IVIA par séance live, selon la durée.
SESSION_PLATFORM_FEE_CENTS = {30: 300, 60: 500}   # 3 $ (30 min) / 5 $ (1 h)
INCLUDED_SESSIONS_PER_MONTH = 5                    # 5 premières séances/mois sans frais


def platform_fee_cents(duration_min: int, prior_sessions_this_month: int) -> int:
    """Frais plateforme IVIA pour une séance live (cents).

    `prior_sessions_this_month` = nombre de séances déjà encaissées ce mois-ci pour
    ce praticien AVANT celle-ci (index 0-based). Les 5 premières sont incluses (0 $).
    Au-delà, frais 3/5 $ avec réduction au volume sur les séances « payantes » :
    1–29 → plein · 30–79 → −20 % · 80+ → −40 %.
    """
    if prior_sessions_this_month < INCLUDED_SESSIONS_PER_MONTH:
        return 0
    base = SESSION_PLATFORM_FEE_CENTS[60] if duration_min > 30 else SESSION_PLATFORM_FEE_CENTS[30]
    payante_index = prior_sessions_this_month - INCLUDED_SESSIONS_PER_MONTH + 1  # 1-based
    if payante_index >= 80:
        factor = 0.60
    elif payante_index >= 30:
        factor = 0.80
    else:
        factor = 1.0
    return round(base * factor)


def offer_payant_key(code: str) -> str:
    return f"pay_{code}"


def is_offer_payant(db, code: str) -> bool:
    """Vrai si l'offre doit être facturée. Décochée côté admin → gratuite (mode test).

    Défaut : payant (True). Lit le réglage runtime `pay_<offre>` (table app_settings).
    """
    from app.services.app_settings import get_bool
    return get_bool(db, offer_payant_key(code), default=True)


def decompose(amount_ttc_cents: int) -> dict[str, int]:
    """Décompose un encaissement TTC en HT + TPS + TVQ (cents).

    Respecte `settings.tax_registered` : si False, HT = TTC et taxes = 0.
    """
    if not settings.tax_registered:
        return {"ttc": amount_ttc_cents, "ht": amount_ttc_cents, "tps": 0, "tvq": 0, "taxes": 0}
    combined = 1 + settings.tps_rate + settings.tvq_rate
    ht = round(amount_ttc_cents / combined)
    taxes = amount_ttc_cents - ht           # total taxe, exact au cent
    tps = round(ht * settings.tps_rate)
    tvq = taxes - tps                       # le reste va à la TVQ → TPS + TVQ == taxes pile
    return {"ttc": amount_ttc_cents, "ht": ht, "tps": tps, "tvq": tvq, "taxes": taxes}


def estimate_stripe_fee_cents(amount_ttc_cents: int) -> int:
    """Estimation du frais Stripe (le réel vient du webhook)."""
    return round(amount_ttc_cents * STRIPE_PCT) + STRIPE_FIXED_CENTS


def revenue_breakdown(
    amount_ttc_cents: int,
    *,
    stripe_fee_cents: int | None = None,
    ai_cost_cents: int | None = None,
    praticien_share_cents: int = 0,
) -> dict[str, int]:
    """Ventilation complète d'un encaissement, pour le grand livre / dashboard admin.

    Renvoie : ttc, ht, tps, tvq, taxes, frais_stripe, cout_ia, part_praticien, marge_ivia.
    """
    d = decompose(amount_ttc_cents)
    stripe_fee = stripe_fee_cents if stripe_fee_cents is not None else estimate_stripe_fee_cents(amount_ttc_cents)
    ai = ai_cost_cents if ai_cost_cents is not None else AI_COST_CENTS_ESTIMATE
    marge = d["ht"] - stripe_fee - ai - praticien_share_cents
    return {
        "ttc": d["ttc"],
        "ht": d["ht"],
        "tps": d["tps"],
        "tvq": d["tvq"],
        "taxes": d["taxes"],
        "frais_stripe": stripe_fee,
        "cout_ia": ai,
        "part_praticien": praticien_share_cents,
        "marge_ivia": marge,
    }
