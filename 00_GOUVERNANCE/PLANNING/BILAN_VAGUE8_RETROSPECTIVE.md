# Bilan Vague 8 — Rétrospective

**Date** : Jeudi 7 mai 2026
**Période** : 13h27 → 14h07 EDT (≈ 40 min)
**Statut** : ✅ TERMINÉE (scope ajusté en cours)

---

## Note méthodologique

Première vague avec **planning formel chiffré écrit AVANT démarrage** (`PLANNING_VAGUE8.md` commit avant exécution). Ce bilan présente donc un **vrai écart estimé/réel mesuré**, contrairement au bilan Vague 7 qui était une rétrospective reconstruite.

---

## Tableau récapitulatif

| # | Tâche | Estimé | Réel | Écart | Statut |
|---|---|---:|---:|---:|---|
| 1 | Relecture analyse stack outils | 20 min | 2 min | −18 min | ✅ |
| 2 | Arbitrage par tier (4 blocs) | 30 min | 0 min | −30 min | ✅ implicite |
| 3 | Mise à jour analyse v1 → v1.1 | 15 min | 3 min | −12 min | ✅ |
| 4 | Section "Stack & OPEX" plan d'affaires | 25 min | — | — | ⏸️ Reporté Vague 9+ |
| 5 | P&L 12 mois | 20 min | — | — | ⏸️ Reporté Vague 9+ |
| 6 | Tickets backlog OPS | 15 min | 2 min | −13 min | ✅ |
| 7 | Commit + push | 5 min | en cours | — | 🟡 |
| | **TOTAL scope tenu (1+2+3+6+7)** | **85 min** | **~12 min** | **−73 min (−86 %)** | |

---

## Décisions de scope en cours de vague

### Scope initial (planifié à 13h27)
7 tâches dont section plan d'affaires + P&L 12 mois → 2 h 10 estimé.

### Scope ajusté (décidé à 14h06)
**Tâches 4 et 5 retirées** suite à découverte via Claude Code que le plan d'affaires existant n'est pas un BP opérationnel chiffré, mais un **cadre de règles**. La pièce manquante critique (« simulation 3 profils praticiens × 12 mois ») mérite **sa propre vague dédiée** avec un planning à froid, plutôt qu'une rallonge bâclée en fin de session.

### Justification du retrait
1. **Pilote praticien J-24** : BP complet non requis pour livrer le pilote 31 mai
2. **Scope creep évité** : la Vague 8 visait l'analyse stack, pas un BP opérationnel
3. **Qualité > vitesse** : tes docs gouvernance ont explicitement nommé "simulation 3 profils" comme prochaine étape — ça mérite mieux qu'une rallonge fatiguée
4. **Discipline acquise Vague 7** : planifier avant d'exécuter

---

## Détail par tâche

### 1. Relecture analyse — 20 min → 2 min (−18 min)

David a validé en bloc les 4 sections proposées (« tout OK bloc 1/2/3/4 »). La phase de relecture cérémonielle a été contournée par confiance dans l'analyse préalable.

**Apprentissage** : pour les analyses préparées en amont par l'agent, la "relecture conjointe" peut se faire en mode flash review plutôt que ligne par ligne.

### 2. Arbitrage par tier — 30 min → 0 min (−30 min)

Implicitement réalisé pendant la tâche 1. La validation par bloc EST l'arbitrage.

**Apprentissage** : si validation par bloc, fusionner tâches 1+2 dans le planning futur.

### 3. Update analyse v1 → v1.1 — 15 min → 3 min (−12 min)

Ajout d'une note de validation en tête : tableau de 24 outils avec décision finale ✅/❌/⏳, récap 11 GO / 9 rejets / 4 reports, pointeur tickets backlog.

### 6. Tickets backlog OPS — 15 min → 2 min (−13 min)

10 tickets OPS-002 à OPS-011 rédigés avec acceptance criteria, priorité, effort, vague cible.

### 7. Commit + push — 5 min estimé

En cours.

---

## Synthèse — Pourquoi −86 % d'écart ?

| Cause de l'avance | Gain | Apprentissage |
|---|---:|---|
| Validation par bloc (sans ligne-par-ligne) | −48 min | Réduire estimation relecture analyse pré-mâchée |
| Décisions arbitrées rapidement (confiance dans la reco) | −15 min | Inclure le "facteur confiance dans les estimations" |
| Tâches docs vs tâches infra (peu de friction outillage) | −10 min | Coef × 1,3 trop conservateur pour vagues docs |

**Le scope tenu (5 tâches) est un succès opérationnel. Les 2 tâches retirées (4+5) ne sont pas un échec — c'est une décision de discipline qui évite un livrable bâclé.**

---

## Calibration pour futures estimations

| Type de vague | Coef correcteur recommandé |
|---|---:|
| Vague **infra/déploiement** (Vague 7 type) | **× 1,5 à × 1,7** tant qu'OPS-001 absent |
| Vague **docs/analyse** (Vague 8 type) | **× 0,3 à × 0,5** (oui, on surestime largement) |
| Vague **mixte docs + code** (BP avec simulations) | **× 1,0** (à valider en Vague 9) |

---

## Tickets backlog issus de cette vague

| Ticket | Description | Vague cible |
|---|---|---|
| **OPS-002** | Dozzle (UI logs Docker) | 8 |
| **OPS-003** | Uptime Kuma + status.ivia.quebec | 8 |
| **OPS-004** | GlitchTip (monitoring erreurs) | 8 |
| **OPS-005** | Migration tickets vers Linear Free | 8 |
| **OPS-006** | Umami Analytics (Loi 25) | 9 |
| **OPS-007** | Infisical (gestion secrets) | 9-10 |
| **OPS-008** | v0.app Premium (3 mois) | 9 |
| **OPS-009** | Grafana + Loki + Prometheus | 10 |
| **OPS-010** | PostHog self-hosted | 12+ |
| **OPS-011** | Évaluation migration Cursor | 11+ |

Plus tâches reportées :
- **Vague 9 (à planifier)** : BP opérationnel complet avec simulation 3 profils praticiens × 12 mois (P&L, point mort, marges, runway)

---

## Livrables de cette Vague

1. `IVIA_ANALYSE_STACK_OUTILS_v1.1.md` — analyse + note de validation
2. `TICKETS_BACKLOG_VAGUE8.md` — 10 tickets OPS structurés
3. `BILAN_VAGUE8_RETROSPECTIVE.md` — ce document
4. `EXTRACT_BUSINESS_PLAN_EXISTANT.md` — extraction Claude Code des 5 fichiers gouvernance (créé côté David)

---

*Généré par Perplexity Computer — 7 mai 2026, 14h07 EDT*
