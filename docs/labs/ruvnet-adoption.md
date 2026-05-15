# Ruvnet — Notes laboratoire et politique d'adoption

**Statut** : v0.1 — 2026-05-15 — scaffolding doctrinal, AUCUNE installation en cours.
**Référence opposable** : `CLAUDE.md` §7 (politique laboratoire Ruvnet).

> Ce document est un **journal de positionnement**. Il décrit ce que MERLIN
> regarde dans l'écosystème ruvnet, ce qu'on autorise à expérimenter, et
> ce qui est interdit en production. Toute déviation doit être justifiée
> par PR référencée à ce document.

---

## 1. Pourquoi ce document existe

L'écosystème **ruvnet** (autour de `ruflo`, `open-claude-code`, `marketing`,
`tribe-knowledgegraph`, etc.) propose des patterns intéressants d'orchestration
d'agents, d'expérience CLI, et d'écologie de contenu. Plusieurs de ces idées
**résonnent** avec ce qu'on construit côté MERLIN/IVIA.

Mais ce sont des **projets externes**, en évolution rapide, parfois en
zone grise sur le plan juridique (rétro-ingénierie de Claude Code), parfois
minimaux / non maintenus. On ne peut pas s'y appuyer comme on s'appuie sur
FastAPI ou Next.js.

D'où une politique **sandbox-only** : on étudie, on s'inspire, on ne dépend pas.

---

## 2. Règles dures (rappel)

- ❌ **Ne pas installer** un package `ruvnet/*` dans `package.json`, `requirements.txt`,
  `pyproject.toml`, ou tout autre manifeste de production.
- ❌ **Ne pas exécuter** `ruflo init` à la racine du repo MERLIN.
- ❌ **Ne pas intégrer** `open-claude-code` comme dépendance — risques juridiques
  (rétro-ingénierie de Claude Code), risques de confiance pour les utilisateurs.
- ❌ **Ne pas wrapper** un agent ruvnet derrière une API publique IVIA.
- ✅ **Lire** le code, les README, les ADR — pour comprendre les choix.
- ✅ **Reproduire** des idées **dans nos propres briques**, avec nos conventions,
  notre constitution, nos evals.

Toute exception à ces règles passe par une décision documentée dans
`00_GOUVERNANCE/`, validée par David, et journalisée dans `05_JOURNAUX/`.

---

## 3. Cartographie projet par projet

### 3.1 `ruflo` — orchestration d'agents

- **Lecture qu'on en fait** : framework d'orchestration multi-agents, intéressant
  pour explorer des patterns de coordination (planner / executor / critic).
- **Décision MERLIN** : **POC en sandbox uniquement**.
  - Sandbox = worktree isolé hors `master` et hors `refonte-ivia-site-unifie`,
    ou container/VM séparée.
  - Aucun appel réseau vers nos APIs de production depuis le POC.
  - Aucune donnée client réelle ou pseudo-réelle.
- **Ce qu'on cherche à apprendre** :
  - Comment ruflo découpe planner/executor.
  - Quels signaux il remonte (logs, traces) et comment on pourrait s'inspirer
    pour notre `managed_agents/`.
  - Limites observées en pratique (latence, fiabilité, coût).
- **Ce qu'on ne fera pas** :
  - Pas d'intégration en prod, même expérimentale.
  - Pas de `ruflo init` à la racine du repo.
  - Pas d'adoption de leur schéma de config tel quel — on reste sur
    `managed_agents/evals.registry.yaml` comme source de vérité.

### 3.2 `open-claude-code` — clone open-source de Claude Code

- **Lecture qu'on en fait** : tentative de rebuild de l'expérience Claude Code
  en open-source. Intéressant pour comprendre quelle UX agent est valorisée.
- **Décision MERLIN** : **lecture seule, inspiration architecturale uniquement**.
  - On peut lire le code et les issues.
  - On **ne** copie **pas** de code source.
  - On **ne** wrappe **pas** ce projet.
  - On **ne** propose **pas** à nos utilisateurs un outil dérivé.
- **Pourquoi** :
  - Rétro-ingénierie d'un produit Anthropic — risque juridique réel.
  - Risque de confiance : nos utilisateurs s'attendent à un canal Anthropic
    encadré, pas à un fork communautaire non audité.
  - Notre constitution (CLAUDE.md §6.4) est plus stricte que ce que le projet
    impose ; un fork rendrait nos garanties non vérifiables.

### 3.3 `marketing` (ruvnet) — automation marketing agentique

- **Lecture qu'on en fait** : patterns d'écologie de contenu, génération
  d'articles, séquencement de diffusion.
- **Décision MERLIN** : **adaptation conceptuelle uniquement, pas d'adoption**.
  - On en tire la notion d'**écologie de diffusion IVIA** :
    - articles fondateurs (`04_METHODES/articles/`),
    - voix MÉSANGES, présence longue, retour au calme,
    - pas de campagnes payantes, pas d'A/B testing à grande échelle.
  - On ne fait **pas** d'ads automation, pas d'enrichissement froid de leads,
    pas de scraping de réseaux sociaux.
- **Pourquoi** :
  - L'éthique IVIA (maison du vivant) est incompatible avec le marketing
    comportemental.
  - Loi 25 — toute personnalisation publicitaire doit être consentie, ce qui
    sort du périmètre actuel.

### 3.4 `tribe-knowledgegraph` — knowledge graph communautaire

- **Lecture qu'on en fait** : projet d'amont, repo minimal / quasi vide à l'observation.
  Idée séduisante : graphe de connaissance partagé, vivant, par communauté.
- **Décision MERLIN** : **inspiration uniquement**.
  - On s'en inspire pour construire **notre propre knowledge graph interne**,
    qui relie :
    - Correspondances vivantes (expressions ↔ axes MERLIN),
    - prompts (`11_PROMPTS/`),
    - preuves et sources (`05_PREUVES_SOURCES/`),
    - décisions de gouvernance (`00_GOUVERNANCE/`),
    - praticiens et leurs voies.
  - L'implémentation est interne, dans MERLIN, sur stack maîtrisée
    (PostgreSQL + éventuellement vues YAML/Markdown pour la lecture humaine).
- **Pourquoi pas d'adoption directe** :
  - Repo amont insuffisamment mature à l'observation.
  - Couplage à un schéma externe nous priverait de la flexibilité dont on a
    besoin sur le terrain clinique / culturel québécois.

---

## 4. Plan de POC ruflo (sandbox)

> À déclencher seulement quand David donne le go explicite.

1. **Worktree dédié** : `claude-code-worktree-ruflo-lab` ou équivalent, **hors**
   `master` et **hors** `refonte-ivia-site-unifie`.
2. **Environnement isolé** : venv ou container Docker dédié, sans accès aux
   secrets prod (`.env.prod`).
3. **Données** : fixtures factices uniquement (cf. `managed_agents/evals/fixtures/`).
4. **Critères de succès** :
   - Comprendre l'API de planning de ruflo.
   - Identifier 1 à 3 patterns potentiellement réutilisables dans
     `managed_agents/`.
   - Mesurer le coût (latence, tokens) sur 5 cas simples.
5. **Critères d'arrêt** :
   - Toute tentative d'écriture hors du worktree de sandbox.
   - Toute fuite de données vers un service tiers hors Canada.
   - Toute incompatibilité bloquante avec la constitution MERLIN.
6. **Livrable** : note `docs/labs/ruflo-poc-<date>.md` avec observations,
   verdict (continuer / arrêter), et propositions pour MERLIN.
7. **Rollback** : suppression du worktree, aucun artefact en `master`.

---

## 5. Stratégie de rollback

Si, par erreur, un élément ruvnet venait à apparaître en branche d'intégration :

1. **Détecter** :
   - `grep -r "ruvnet" .` dans le repo.
   - Vérifier `package.json` et `requirements.txt`.
2. **Annuler** :
   - Préférer `git revert` au `git reset --hard`.
   - Journaliser dans `05_JOURNAUX/JOURNAL_ruvnet_rollback_<date>.md`.
3. **Auditer** :
   - Comprendre comment c'est passé (skill manquant ? règle pas claire ?).
   - Mettre à jour `CLAUDE.md` si la règle doit être renforcée.
4. **Communiquer** :
   - Ticket gouvernance dans `00_GOUVERNANCE/`.

---

## 6. Veille et mise à jour

Cette note est **vivante**. Elle doit être relue chaque fois que :

- un projet ruvnet majeur est mis à jour ;
- un membre de l'équipe rapporte une nouvelle observation pertinente ;
- une décision de gouvernance change la politique laboratoire.

Toute mise à jour incrémente la version dans l'en-tête.
