---
titre: Index des agents C-suite — MERLIN
id: MERLIN-INDEX-CSUITE-V1
statut: active
type: charte
couche: SYSTEME
périmètre: admin
auteur: fondateur
date: 2026-06-29
version: 1.0
dépend_de: [ADR-0006, ADR-0007, MERLIN-INDEX-PROMPTS-V1, MERLIN-PROMPTS-CONV-NOMMAGE-V1]
remplace: []
arbitrage_requis: non — index de référence
source_canonique: 11_PROMPTS/06_CSUITE/INDEX_CSUITE_V1.md
---

# MERLIN — Index des agents C-suite V1.0

> **Statut** : active — 2026-06-29  
> **Vague** : 6 — Agents C-suite stratégiques  
> **Dossier** : `11_PROMPTS/06_CSUITE/`

---

## Principe de la couche C-suite

Les agents C-suite sont des **prompts de coordination stratégique et opérationnelle**.
Ils ne remplacent pas les prompts de couche METH, FOND, EDIT ou PROD — ils les orchestrent.

Chaque agent C-suite représente un rôle de direction :

| Agent | Rôle | Analogie |
|---|---|---|
| MERLIN-STRAT | Stratégie, roadmap, arbitrages | CEO |
| MERLIN-ARCH | Architecture technique, migrations, stack | CTO |
| MERLIN-COMM | Communications, contenu, financement | CCO |
| MERLIN-UX | Expérience utilisateur, design, interfaces | CXO |
| MERLIN-FIN | Finances, ROI, métriques, tarification | CFO |
| MERLIN-QA | Qualité, DevOps, tests, monitoring | VP QA / DevOps |

---

## Registre complet

| ID | Fichier | Version | Couche | Périmètre | Trigger principal | Statut |
|---|---|---|---|---|---|---|
| `MERLIN-PROMPT-CSUITE-STRAT-V1` | `MERLIN_PROMPT_CSUITE-STRAT_v1.0.md` | 1.0 | SYSTEME | admin | Décision structurante, ADR, roadmap | active |
| `MERLIN-PROMPT-CSUITE-ARCH-V1` | `MERLIN_PROMPT_CSUITE-ARCH_v1.0.md` | 1.0 | SYSTEME | backend | Choix d'implémentation, migration Alembic | active |
| `MERLIN-PROMPT-CSUITE-COMM-V1` | `MERLIN_PROMPT_CSUITE-COMM_v1.0.md` | 1.0 | SYSTEME | admin | Contenu externe, dossier financement | active |
| `MERLIN-PROMPT-CSUITE-UX-V1` | `MERLIN_PROMPT_CSUITE-UX_v1.0.md` | 1.0 | SYSTEME | frontend | Nouveau composant, parcours utilisateur | active |
| `MERLIN-PROMPT-CSUITE-FIN-V1` | `MERLIN_PROMPT_CSUITE-FIN_v1.0.md` | 1.0 | SYSTEME | admin | ROI module, revue mensuelle, tarification | active |
| `MERLIN-PROMPT-CSUITE-QA-V1` | `MERLIN_PROMPT_CSUITE-QA_v1.0.md` | 1.0 | SYSTEME | backend | Revue PR, validation migration, monitoring | active |

---

## Matrice de collaboration inter-agents

Certaines décisions nécessitent la consultation de plusieurs agents C-suite.

| Situation | Agent principal | Agents consultés |
|---|---|---|
| Nouvelle strate ou nouveau module | STRAT | ARCH (faisabilité), FIN (ROI), QA (tests) |
| Implémentation d'un composant | ARCH | QA (revue), UX (spécification) |
| Contenu client ou externe | COMM | UX (conformité non-clinique), QA (validation contenu) |
| Nouveau parcours utilisateur | UX | ARCH (faisabilité), QA (tests) |
| Dossier de financement | COMM | FIN (section financière), STRAT (mission et impact) |
| Tarification ou plan praticien | FIN | STRAT (positionnement), COMM (communication) |
| Incident de production | QA | ARCH (cause technique), FIN (impact financier) |
| Décision de migration Alembic | ARCH | QA (validation), STRAT (si impact roadmap) |

---

## Règles d'utilisation

1. **Un agent = un rôle** — ne pas combiner deux agents C-suite dans une même session. Changer d'agent explicitement quand le rôle change.
2. **Toujours valider avec le fondateur** — aucun agent C-suite ne produit de décision finale. Il formule des recommandations que le fondateur valide.
3. **Produire un artefact** — chaque session C-suite produit un artefact : ADR, mise à jour de CLAUDE.md, section de document, ou ticket d'implémentation.
4. **Respecter la séquence** — pour une décision d'implémentation : STRAT (direction) → ARCH (faisabilité) → UX (design si pertinent) → FIN (ROI) → QA (validation avant merge).
5. **Pas de dérivation clinique** — aucun agent C-suite ne produit de contenu clinique, de diagnostic, ou de recommandation thérapeutique.

---

## Intégration avec la bibliothèque de prompts existante

Les agents C-suite s'appuient sur les prompts de couches inférieures sans les remplacer :

| Agent C-suite | Prompts de couche opérationnelle liés |
|---|---|
| MERLIN-ARCH | `02_METH/METH-003` (pipeline note de séance) |
| MERLIN-QA | `05_PROD/` (tous les prompts de validation) |
| MERLIN-COMM | `03_EDIT/` (prompts de contenu public) |
| MERLIN-UX | `04_ADMIN/` (onboarding, routage client) |
| MERLIN-FIN | `04_ADMIN/PROMPT_audit_dossier.md` |

---

## Mots-clés d'activation recommandés

Pour activer un agent C-suite dans une session, utiliser l'un de ces préfixes :

| Préfixe | Agent activé |
|---|---|
| « En tant que MERLIN-STRAT... » | MERLIN-STRAT |
| « Revue architecturale... » ou « MERLIN-ARCH... » | MERLIN-ARCH |
| « Communications IVIA... » ou « MERLIN-COMM... » | MERLIN-COMM |
| « Conception UX... » ou « MERLIN-UX... » | MERLIN-UX |
| « Analyse financière... » ou « MERLIN-FIN... » | MERLIN-FIN |
| « Revue QA... » ou « MERLIN-QA... » | MERLIN-QA |

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-06-29 | fondateur | Création initiale — Vague 6 agents C-suite |
