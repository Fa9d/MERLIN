# Planning Vague 8 — Analyse stack outils + Intégration plan d'affaires

**Date prévue** : Jeudi 7 mai 2026 (suite immédiate Vague 7)
**Auteur** : David Phaneuf + Perplexity Computer
**Statut** : 🟡 PLANIFIÉ
**Branche cible** : `master` (docs only, pas de code)

---

## Objectif de la vague

Verrouiller le **stack outils** MERLIN/IVIA pour les 12 prochains mois en arbitrant SaaS vs self-hosted, puis **intégrer la décision au plan d'affaires** pour J-24 (pilote praticien 31 mai 2026).

---

## Critères de succès (Definition of Done)

- [ ] `IVIA_ANALYSE_STACK_OUTILS_v1.md` relue, validée, commitée sur master
- [ ] Décision arbitrée pour chaque outil Tier 1-4 (SaaS vs self-hosted)
- [ ] Section "Stack technique & coûts opérationnels" intégrée au plan d'affaires MERLIN
- [ ] P&L 12 mois mis à jour avec ligne OPEX outils (~684 $/an reco vs 3 276 $/an SaaS)
- [ ] Tickets OPS créés pour les self-hosted retenus (déploiement + maintenance)

---

## Découpage des tâches

| # | Tâche | Estimé | Dépendance | Risque |
|---|---|---:|---|---|
| 1 | Relecture conjointe `IVIA_ANALYSE_STACK_OUTILS_v1.md` (356 lignes) | 20 min | — | 🟢 |
| 2 | Arbitrage par tier (décisions go/no-go par outil) | 30 min | #1 | 🟡 |
| 3 | Mise à jour de l'analyse avec décisions finales (v2) | 15 min | #2 | 🟢 |
| 4 | Rédaction section "Stack & OPEX" pour plan d'affaires MERLIN | 25 min | #3 | 🟢 |
| 5 | Mise à jour P&L 12 mois (intégration OPEX outils) | 20 min | #4 | 🟡 |
| 6 | Création tickets backlog OPS (déploiement self-hosted) | 15 min | #2 | 🟢 |
| 7 | Commit + push docs sur master | 5 min | #3,4,5 | 🟢 |
| | **TOTAL ESTIMÉ** | **2 h 10** | | |

**Coefficient correcteur** : × 1,3 (vague docs only, friction shell limitée)
**Temps réaliste attendu** : **~2 h 50**

---

## Risques identifiés

| Risque | Impact | Mitigation |
|---|---|---|
| Arbitrage SaaS/self-hosted bloqué par incertitude techno | Moyen | Décider avec critère unique : "peut-on tenir 12 mois sans recruter ?" |
| P&L existant introuvable ou daté | Moyen | Si absent, créer v1 minimal (3 lignes : revenus pilote, OPEX, marge) |
| Tickets OPS trop vagues | Faible | Réutiliser modèle BACK-009/010 de Vague 7 |
| Scope creep vers Vague 9 (déploiement effectif) | Élevé | **Stop strict** : Vague 8 = décision + docs, pas d'install |

---

## Tickets backlog anticipés

| Ticket | Description | Priorité |
|---|---|---|
| **OPS-002** | Déployer Plausible Analytics self-hosted sur VPS | P2 |
| **OPS-003** | Setup n8n self-hosted (alternative Make.com) | P2 |
| **OPS-004** | Migration vers Listmonk (alternative Mailchimp) | P3 |

(Liste indicative — sera ajustée après tâche #2)

---

## Bilan post-vague (à remplir en fin)

| # | Tâche | Estimé | Réel | Écart | Note |
|---|---|---:|---:|---:|---|
| 1 | Relecture analyse | 20 min | | | |
| 2 | Arbitrage par tier | 30 min | | | |
| 3 | Mise à jour v2 | 15 min | | | |
| 4 | Section plan d'affaires | 25 min | | | |
| 5 | P&L 12 mois | 20 min | | | |
| 6 | Tickets OPS | 15 min | | | |
| 7 | Commit + push | 5 min | | | |

**Total estimé** : 2 h 10 (réaliste : 2 h 50)
**Total réel** : à remplir
**Écart** : à calculer

### Leçons apprises

-

---

*Planning créé 7 mai 2026, 13h32 EDT — avant démarrage Vague 8*
