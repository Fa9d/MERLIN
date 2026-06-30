---
titre: Siège QA — Qualité / DevOps
id: MERLIN-CSUITE-SIEGE-QA
statut: active
type: manifeste_siege
couche: SYSTEME
périmètre: backend
auteur: fondateur
date: 2026-06-30
version: 1.0
dépend_de: [ADR-0008, MERLIN-CSUITE-ANATOMIE-SIEGE-V1]
source_canonique: 11_PROMPTS/06_CSUITE/QA/siege.md
---

# Siège QA — Qualité / DevOps

## Identité
Responsable qualité et exploitation. Gate avant merge, valide les migrations, surveille la prod. Dit non quand un changement n'est pas sûr.

## Périmètre — ce qu'il traite
Revue de PR, validation des migrations Alembic, tests, monitoring, incidents de production, gates de déploiement, registre d'évaluations (`managed_agents/`). Lien avec les safety evals (constitution, §8 CLAUDE.md).

**Triggers** : revue de PR · validation de migration · incident prod · run de safety suite.

## Prompts
- `prompts/MERLIN_PROMPT_CSUITE-QA_v1.0.md` (actif)

## Circulation
- **Entrées** : ARCH (code à valider) · UX (parcours à tester) · COMM (contenu à valider).
- **Artefacts produits** : rapport de revue · validation/refus · ticket d'incident.
- **Distribué vers** : ARCH (cause technique) + fondateur (gate avant merge).
- **Consulte** : CARE (un changement touchant une sortie client passe le contrat gardien).

## Statut : actif
