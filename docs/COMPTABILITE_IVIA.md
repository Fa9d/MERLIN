# Comptabilité IVIA — structure des argents

> Référence pour la facturation et le dashboard admin. Source de vérité des prix :
> `10_backend_merlin_api/app/services/billing.py` + `app/core/config.py`.

## Principe : prix TTC, frais Stripe absorbés

Le client paie un **prix tout compris** (taxe incluse). IVIA **absorbe les frais Stripe**.
Trois natures d'argent à ne jamais confondre :

- **HT** — le revenu réel d'IVIA.
- **TPS + TVQ** — argent qui **transite** vers les gouvernements (passif, pas un revenu).
- **Coûts** — frais Stripe + IA + part praticien.

```
TTC = HT + TPS + TVQ
Marge IVIA = HT − frais_stripe − coût_IA − part_praticien
```

## Statut taxes : NON inscrit pour l'instant

David (et des praticiens qui démarreraient sous IVIA) sont **sous le seuil de petit
fournisseur (30 000 $)** → **aucune taxe perçue**. Donc, tant que
`MERLIN_TAX_REGISTERED=false` : **HT = TTC, TPS = TVQ = 0** (le prix est 100 % revenu).

Le jour de l'inscription : passer `MERLIN_TAX_REGISTERED=true` → la décomposition
TTC → HT + TPS + TVQ s'active automatiquement, **aucun autre changement de code**.
Avant ce jour : faire valider l'assujettissement par un·e comptable (statut non
clinique ⇒ services vraisemblablement taxables, pas d'exemption santé).

## Grille (TTC, cents) — `OFFERS` dans billing.py

| Offre | Prix TTC | Code | Type |
|------|----------|------|------|
| Enregistrement seul | 35 $ | `enr_seul` | asynchrone |
| Enregistrement + rappel (compte-rendu + rappel 10 min) | 49 $ | `enr_rappel` | asynchrone |
| Séance live 1 h | 75 $ | `seance_live` | temps praticien |

Prix serveur (anti-manipulation) : `stripe_audio_async_amount_cents=4900`,
`stripe_seance_amount_cents=7500` (config). Tous les chemins de paiement lisent ces réglages.

## Décomposition par offre

**Aujourd'hui (taxe OFF)** — tout est revenu :

| Offre | Encaissé | Revenu (HT) | Frais Stripe | IA | Marge avant praticien |
|------|----------|-------------|--------------|-----|----------------------|
| 35 $ | 35,00 | 35,00 | 1,32 | 0,12 | **33,56** |
| 49 $ | 49,00 | 49,00 | 1,72 | 0,12 | **47,16** (− ~10 min praticien) |
| 75 $ | 75,00 | 75,00 | 2,48 | 0,13 | **72,39** (− 1 h praticien) |

**Après inscription (taxe ON, ~14,975 %)** — le revenu baisse, la taxe est à remettre :

| Offre | TTC | HT | TPS | TVQ | Frais Stripe |
|------|-----|-----|-----|-----|--------------|
| 35 $ | 35,00 | 30,44 | 1,52 | 3,04 | 1,32 |
| 49 $ | 49,00 | 42,62 | 2,13 | 4,25 | 1,72 |
| 75 $ | 75,00 | 65,23 | 3,26 | 6,51 | 2,48 |

## Grand livre (à construire) — une ligne par encaissement

Champs (cents) : `montant_ttc · ht · tps · tvq · taxes · frais_stripe · cout_ia · part_praticien · marge_ivia · offre · session_id · payé_le`.
Le **frais Stripe réel** vient de la *balance transaction* au webhook ; sinon estimation (`billing.estimate_stripe_fee_cents`).
Helper prêt : `billing.revenue_breakdown(amount_ttc_cents, stripe_fee_cents=..., praticien_share_cents=...)`.

## Dashboard admin (à construire)

Sur une période : **encaissé** · **TPS et TVQ à remettre** (séparées, pour les déclarations) ·
**frais Stripe absorbés** · **coûts IA** · **versements praticiens** · **marge nette** ;
répartition par offre et par mois.

## Idée connexe — garde-fou praticiens

L'outil peut **rappeler** à chaque praticien son statut (inscrit taxes ou non, approche
du seuil 30 000 $) et **guider sa conduite** sous le modèle IVIA. À cadrer plus tard.

## Reste à faire (séquencé)

1. ✅ Grille 35/49/75 en config + module `billing.py` (décomposition, interrupteur taxes).
2. Grand livre par encaissement (table + écriture au `_fulfill_paid_order`).
3. Page compta du dashboard admin.
4. Paiement des offres d'enregistrement si pas déjà couvert par le parcours `audio_async`.
5. Stripe Tax (mode prix-inclusif) le jour de l'inscription.
