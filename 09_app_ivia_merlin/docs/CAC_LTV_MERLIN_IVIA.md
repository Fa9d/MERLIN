# Modèle CAC / LTV — MERLIN × IVIA
**Version :** 1.0 — 26 juin 2026  
**Auteur :** Session de travail Perplexity × Fondateur  
**Statut :** Hypothèses fondatrices — à valider en Phase 0 (pilote 10 praticiens)

---

## 1. Contexte et périmètre

MERLIN est une plateforme SaaS B2B destinée aux praticiens en accompagnement (coachs, thérapeutes, psychopraticiens, praticiens en développement personnel) au Québec, avec une expansion Canada francophone envisagée. Le modèle économique est un abonnement mensuel récurrent par praticien, avec des add-ons modulaires (module analytique d'orientation, module de transcription, etc.).

Le présent document modélise trois métriques fondamentales :
- **CAC** — Coût d'Acquisition Client (par praticien actif)
- **LTV** — Lifetime Value (valeur nette sur la durée de vie du praticien)
- **LTV/CAC** — Ratio de santé du moteur de croissance

---

## 2. Hypothèses de pricing

Trois scénarios tarifaires sont modélisés. Le scénario central (B) est la base de référence pour les projections.

| Scénario | Abonnement mensuel | Positionnement |
|---|---|---|
| **A — Entrée** | 49 $/mois | Adoption rapide, volume |
| **B — Référence** | 79 $/mois | Valeur équilibrée (recommandé Phase 1) |
| **C — Premium** | 129 $/mois | Praticiens établis, add-ons inclus |

**Add-ons modulaires (optionnels) :**
- Module analytique d'orientation (IVIA) : +19 $/mois
- Module transcription : +15 $/mois
- Compte client autonome (portail client) : +9 $/mois

**ARPU cible (Annual Revenue Per User) en régime de croisière :**
- Scénario B seul : **948 $/an**
- Scénario B + 1 add-on moyen : **1 176 $/an** (~38 % des praticiens adoptent ≥1 add-on)

---

## 3. Modèle CAC

### 3.1 Définition retenue

> **CAC = Totalité des dépenses d'acquisition (marketing + ventes) sur une période ÷ Nombre de nouveaux praticiens actifs acquis sur cette même période.**

Un praticien est "actif" lorsqu'il a complété son onboarding ET créé au moins un dossier client.

### 3.2 Canaux d'acquisition et coûts estimés

| Canal | Phase 0 (Pilote) | Phase 1 (Lancement) | Phase 2 (Croissance) |
|---|---|---|---|
| **Bouche à oreille / Réseau fondateur** | 0–50 $ | 0–50 $ | 0–50 $ |
| **Contenu organique (LinkedIn, Substack, communautés)** | 200 $/mois (temps) | 400 $/mois | 600 $/mois |
| **Partenariats (associations, ordres, instituts de formation)** | 500 $ setup | 200 $/mois | 300 $/mois |
| **Pub payante Meta/Google** | — | 500–1 500 $/mois | 2 000–5 000 $/mois |
| **Démos / webinaires praticiens** | 150 $/événement | 300 $/événement | 500 $/événement |
| **Coût fondateur (temps alloué à la vente)** | 20 h/mois × 75 $/h | 15 h/mois × 75 $/h | 10 h/mois × 75 $/h |

### 3.3 CAC par phase (scénario central)

| Phase | Dépenses totales/mois | Acquisitions/mois | **CAC estimé** |
|---|---|---|---|
| **Phase 0 — Pilote (0–10 praticiens)** | ~1 650 $ | 2–3 | **~550–825 $** |
| **Phase 1 — Lancement (10–50 praticiens)** | ~3 500 $ | 8–12 | **~290–440 $** |
| **Phase 2 — Croissance (50–200 praticiens)** | ~8 000 $ | 20–30 | **~265–400 $** |

**CAC cible en régime stabilisé : 300–350 $**

> **Référence sectorielle SaaS B2B SMB :** CAC médian 300–800 $ pour des abonnements 50–150 $/mois. MERLIN se positionne bien si le bouche à oreille et les partenariats restent les canaux dominants.

### 3.4 Levier clé : le referral praticien

Un praticien satisfait qui réfère un collègue génère un CAC ≈ 50–100 $ (carte cadeau, mois offert). Avec un taux de referral de 20–25 % des praticiens actifs, le CAC blended descend à **200–250 $** en Phase 2. C'est le levier prioritaire à activer dès le pilote.

---

## 4. Modèle LTV

### 4.1 Composantes de la LTV

```
LTV = ARPU mensuel × Marge brute × (1 / Churn mensuel)
```

### 4.2 Hypothèses de churn

| Type de SaaS | Churn mensuel typique | Durée de vie implicite |
|---|---|---|
| SaaS horizontal générique | 3–5 % | 20–33 mois |
| SaaS vertical (outil métier spécialisé) | 1–2 % | 50–100 mois |
| Outil de pratique professionnelle (ancrage fort) | 0,5–1,5 % | 67–200 mois |

Hypothèse retenue : **churn mensuel de 1,5 % en Phase 1, cible 1 % en Phase 2**.

### 4.3 Calcul LTV par scénario

| Scénario | ARPU/mois | Marge | Churn | **LTV** |
|---|---|---|---|---|
| A — Entrée, Phase 1 | 49 $ | 75 % | 1,5 % | **2 450 $** |
| B — Référence, Phase 1 | 79 $ | 75 % | 1,5 % | **3 950 $** |
| B — Référence, Phase 2 | 89 $ (avec add-ons) | 78 % | 1,0 % | **6 942 $** |
| C — Premium, Phase 2 | 148 $ (129 + add-ons) | 80 % | 0,8 % | **14 800 $** |

---

## 5. Ratio LTV / CAC

| Ratio | Interprétation |
|---|---|
| < 1 | Modèle non viable |
| 1–3 | Marginal |
| **3–5** | **Zone saine** |
| > 5 | Excellent |

### 5.1 Ratios projetés pour MERLIN

| Phase | LTV | CAC | **LTV/CAC** | Verdict |
|---|---|---|---|---|
| Phase 0 — Pilote | 3 950 $ | 700 $ | **5,6** | ✅ Excellent |
| Phase 1 — Lancement | 3 950 $ | 380 $ | **10,4** | ✅ Très fort |
| Phase 2 — Croissance | 6 942 $ | 300 $ | **23,1** | ✅ Machine à croissance |
| Phase 2 + referral | 6 942 $ | 225 $ | **30,8** | ✅ Exceptionnel |

---

## 6. Payback Period

```
Payback = CAC / (ARPU mensuel × Marge brute)
```

| Phase | CAC | ARPU × Marge | **Payback** |
|---|---|---|---|
| Phase 0 | 700 $ | 59 $/mois | **~12 mois** |
| Phase 1 | 380 $ | 59 $/mois | **~6,5 mois** |
| Phase 2 | 300 $ | 69 $/mois | **~4,3 mois** |

---

## 7. Sensibilité — Variables critiques

### 7.1 Impact du churn sur la LTV (ARPU = 79 $, marge = 75 %)

| Churn mensuel | Durée de vie | LTV |
|---|---|---|
| 3,0 % | 33 mois | 1 975 $ |
| 2,0 % | 50 mois | 2 963 $ |
| 1,5 % | 67 mois | **3 950 $** |
| 1,0 % | 100 mois | 5 925 $ |
| 0,5 % | 200 mois | 11 850 $ |

> **Réduire le churn de 2 % à 1 % double la LTV.** C'est le levier le plus puissant disponible.

### 7.2 Impact de l'adoption des add-ons sur l'ARPU

| Taux d'adoption | ARPU moyen | LTV (churn 1 %) |
|---|---|---|
| 0 % | 79 $ | 5 925 $ |
| 25 % | 83 $ | 6 225 $ |
| 40 % | 88 $ | 6 600 $ |
| 60 % | 100 $ | 7 500 $ |

### 7.3 Impact du referral sur le CAC blended

| Taux de referral | CAC blended | LTV/CAC (Phase 2) |
|---|---|---|
| 0 % | 300 $ | 23,1 |
| 15 % | 265 $ | 26,2 |
| 25 % | 225 $ | 30,8 |
| 40 % | 190 $ | 36,5 |

---

## 8. MRR / ARR Projections (scénario central B)

| Mois | Praticiens actifs | MRR | ARR |
|---|---|---|---|
| M3 (fin pilote) | 10 | 790 $ | 9 480 $ |
| M6 | 25 | 1 975 $ | 23 700 $ |
| M12 | 60 | 5 280 $ | 63 360 $ |
| M18 | 120 | 10 800 $ | 129 600 $ |
| M24 | 220 | 21 120 $ | 253 440 $ |
| M36 | 500 | 52 500 $ | 630 000 $ |

---

## 9. Seuil de rentabilité opérationnelle

**Coûts fixes mensuels estimés (Phase 1–2) :** ~7 000–12 000 $/mois

```
Praticiens nécessaires = Coûts fixes / (ARPU × Marge brute)
= 9 500 $ / (79 $ × 0,75) ≈ 161 praticiens
```

**Point de rentabilité opérationnelle : ~160 praticiens actifs** (mois 15–18 selon projections).

---

## 10. Recommandations stratégiques

### Priorités Phase 0 (Pilote)

1. **Mesurer le churn dès M1** — Churn > 3 % = signal d'alarme produit, pas commercial
2. **Activer le referral dès M2** — 1 mois gratuit par praticien référé
3. **Surveiller le temps d'activation** — Praticien avec 5+ dossiers en J14 → churn 3× plus faible
4. **Ne pas lancer la pub payante avant M6** — Commencer organique

### KPIs à suivre dans le dashboard MERLIN

| KPI | Fréquence | Seuil d'alerte |
|---|---|---|
| Churn mensuel | Mensuel | > 2 % |
| CAC blended | Trimestriel | > 500 $ |
| LTV/CAC | Trimestriel | < 3 |
| Payback period | Trimestriel | > 9 mois |
| ARPU | Mensuel | < 79 $ |
| Taux d'activation J14 | Hebdomadaire | < 60 % |
| NPS praticien | Trimestriel | < 40 |

---

## 11. Impact du module analytique d'orientation (IVIA) sur la LTV

Le module analytique est un **levier LTV direct** :

- Augmente l'ARPU de +19 $/mois (+24 % sur l'abonnement de base)
- Crée un ancrage fort → réduction du churn estimée à -0,3 à -0,5 %
- Différencie MERLIN de tout outil généraliste

| | Sans module IVIA | Avec module IVIA (40 % adoption) |
|---|---|---|
| ARPU | 79 $ | 89 $ |
| Churn mensuel | 1,5 % | 1,2 % |
| LTV | 3 950 $ | 5 563 $ |
| **Uplift LTV** | — | **+41 %** |

---

*Document produit dans le cadre du cycle de conception MERLIN × IVIA — Juin 2026*  
*Hypothèses à réviser à chaque phase avec données réelles.*
