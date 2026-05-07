# EXTRACT — Business plan existant (synthèse)

Date : 2026-05-07
Sources : 5 docs `00_GOUVERNANCE/` (modèle éco praticiens, grille commerciale, frais/volume/coûts/seuils, étude marché MESANGE, pilotage MESANGE)
Statut sources : tous **draft** (avril 2026)

> **TL;DR** — La grille commerciale MERLIN praticiens est posée (15 prix unitaires). Tout le reste — coûts unitaires, point mort, marges chiffrées, runway, P&L — est **structuré mais non chiffré**. Aucun P&L consolidé n'existe.

---

## 1) Modèle de revenus

### MERLIN — praticiens (chiffré)

Hypothèse active : *Stripe à la charge du praticien ; MERLIN facture à la séance ; prix dégressifs au volume.*

**Paliers volume / mois** : Petit `0–30` · Régulier `31–80` · Gros `81–200` · Institutionnel `200+` (négocié).

| Offre | Inclus | Petit | Régulier | Gros |
|---|---|---:|---:|---:|
| **Essentiel** | rdv + rappels + revue email | 4,90 | 4,40 | 3,90 |
| **Standard** | transcription + résumé simple | 7,90 | 7,40 | 6,90 |
| **Premium** | résumé historique + préconisations | 12,90 | 11,90 | 10,90 |
| Module Trace | transcription seule (upsell Essentiel) | 5,90 | 5,40 | 4,90 |
| Module Orientation | préconisations prudentes (upsell Standard) | 9,90 | 9,40 | 8,90 |

*Tarifs en CAD par séance.* Revenu par praticien/mois **non simulé** dans les docs (aucun scénario `prix × volume`).

### MESANGE (ordres de grandeur, non engagés)

| Modèle | Fourchette | Récurrent ? |
|---|---|---|
| Mandats d'analyse | 1 500 – 8 000 CAD | non |
| Veille récurrente client | 1 000 – 5 000 CAD/mois | oui |
| Observatoire financé | 15 000 – 60 000 CAD/an | oui |
| Formation / atelier | 750 – 3 000 CAD | non |
| Premium citoyen | 12 – 29 CAD/mois | oui |
| Premium pro léger | 49 – 149 CAD/mois | oui |
| Outil / licence | 250 – 1 500 CAD/mois | oui |

Hypothèse stratégique : *au lancement, payeurs = organisations/pros, pas le grand public.*

---

## 2) OPEX / coûts documentés

### MERLIN — 5 blocs identifiés (variables nommées, **non chiffrées**)

| Bloc | Variables clés | Statut |
|---|---|---|
| Paiement | `cout_paiement_par_transaction` | à mesurer |
| IA / transcription | `cout_transcription_par_minute`, `cout_resume_par_seance`, `cout_reporting_par_rapport` | à mesurer |
| Mémoire / stockage | `cout_stockage_par_go`, `cout_retention_par_client_actif` | à mesurer |
| Applicatif / opération | `cout_operation_par_seance`, `cout_support_par_praticien` | à mesurer |
| Commercial / impayés | `cout_acquisition_amorti`, `taux_impayes_prevu` | à mesurer |

### MESANGE — exemples budgétaires (seuls chiffres concrets)

**Budget mensuel par axe** (Tableau A) :

| Axe | Budget /mois (CAD) |
|---|---:|
| veille politique QC | 2 500 |
| vérification publique | 1 800 |
| diffusion éditoriale | 900 |
| doctrine / cadre MESANGE | 600 |
| **Total axes** | **5 800** |

**Budget mensuel outils** (Tableau C) :

| Outil | Budget /mois (CAD) |
|---|---:|
| LLM | 300 |
| transcription | 180 |
| scraping | 120 |
| hébergement | 80 |
| **Total outils** | **680** |

**Coût-exemple d'un dossier MESANGE** (S-001 / D-014) :
- LLM (180k tokens × 0,000002) → 0,36
- Vérification (2,5 h × 65 CAD) → 162,50
- Rédaction (1,5 h × 55 CAD) → 82,50
- **Total dossier** ≈ **245 CAD**

> Tarif horaire interne implicite : analyste senior 65 CAD/h, rédacteur 55 CAD/h.

---

## 3) Hypothèses de rentabilité

**Aucun chiffre** de point mort, marge cible (%), ni runway dans les 5 docs. Uniquement des **règles structurelles** :

- Marge minimale **absolue** par séance/opération (plancher fixe — non chiffré).
- Marge minimale **relative** cible (% — non chiffré).
- `prix_unitaire_minimum = cout_revient_unitaire + marge_minimale`
- Dégressivité au volume **uniquement si économies d'échelle réelles**, jamais sous coût de revient + marge plancher.
- Revue **trimestrielle** des coûts réels.
- Garde-fou : si marge brute par praticien passe sous plancher → ajustement automatique du palier ou minimum facturé.

**Formules de pilotage MESANGE** (cadres prêts, valeurs absentes) :

```
cout_direct_dossier   = couts_outils + couts_humains + couts_diffusion + couts_risque
cout_complet_dossier  = cout_direct_dossier + quote_part_couts_fixes
marge_dossier         = revenus_associes_dossier - cout_complet_dossier
cout_par_sujet_resolu = cout_total_periode / nombre_de_sujets_resolus
```

---

## 4) Chiffres P&L existants

**Inventaire complet des nombres trouvés** :

| Élément | Source | Valeur |
|---|---|---|
| 15 prix unitaires séance MERLIN | grille commerciale | 3,90 → 12,90 CAD |
| Paliers volume MERLIN | grille commerciale | 30 / 80 / 200 séances/mois |
| 7 fourchettes revenus MESANGE | étude marché | 12 CAD/mois → 60 000 CAD/an |
| 4 budgets axes MESANGE | pilotage | 600 → 2 500 CAD/mois (Σ 5 800) |
| 4 budgets outils MESANGE | pilotage | 80 → 300 CAD/mois (Σ 680) |
| Exemple dossier MESANGE | pilotage | ≈ 245 CAD (3 lignes) |
| Taux horaires internes | pilotage (exemple) | 55 / 65 CAD/h |

**Manques critiques pour un BP opérationnel** :
- Aucun coût unitaire MERLIN mesuré (les 5 blocs restent en variables).
- Aucune simulation `revenu × coût × volume` pour les 3 profils praticiens (faible/régulier/gros) pourtant explicitement demandée comme prochaine étape.
- Pas d'hypothèses CAC, churn, LTV, conversion.
- Pas de runway ni de besoin de financement chiffré.
- Pas de P&L consolidé MERLIN+MESANGE.

---

## 5) Prochaines étapes déjà identifiées dans les docs

1. **Feuille de calcul des coûts unitaires** MERLIN (5 blocs → valeurs réelles).
2. **Simulation 3 profils praticiens** (faible / régulier / gros) avant de figer les prix publics.
3. Spec d'offres MESANGE en 3–5 packages vendables.
4. Simulation économique MESANGE 12 mois, plusieurs scénarios.

## 6) Sources

- [MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md](../MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md)
- [MERLIN_GOUV_MODELE_ECO_PRATICIENS_APPLICATION_v1.0.md](../MERLIN_GOUV_MODELE_ECO_PRATICIENS_APPLICATION_v1.0.md)
- [MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md](../MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md)
- [MERLIN_GOUV_ETUDE_MARCHE_MESANGE_QUEBEC_REVENUS_MODELES_V1.md](../MERLIN_GOUV_ETUDE_MARCHE_MESANGE_QUEBEC_REVENUS_MODELES_V1.md)
- [MERLIN_GOUV_MODELE_ECO_MESANGE_PILOTAGE_COUTS_BUDGETS_RENTABILISATION_v1.0.md](../MERLIN_GOUV_MODELE_ECO_MESANGE_PILOTAGE_COUTS_BUDGETS_RENTABILISATION_v1.0.md)
