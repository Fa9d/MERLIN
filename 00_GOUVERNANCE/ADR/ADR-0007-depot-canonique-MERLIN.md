---
titre: Dépôt ET branche canoniques — Fa9d/MERLIN @ refonte-ivia-site-unifie
id: ADR-0007
statut: validated
couche: PROD
type: ADR
auteur: fondateur
date: 2026-06-29
décideurs: David Phaneuf (Fa9d)
dépend_de: [ADR-0006]
remplace: []
source_canonique: 00_GOUVERNANCE/ADR/ADR-0007-depot-canonique-MERLIN.md
---

# ADR-0007 — Dépôt ET branche canoniques

> Corrige et complète la 1ʳᵉ rédaction (Perplexity, sur `master`) qui contenait des
> erreurs factuelles (head 0017, « frontend Next.js ») et **omettait le vrai problème :
> la branche canonique**.

---

## Contexte

Deux dépôts coexistaient :
- `Fa9d/MERLIN` — monorepo complet (doctrine, backend FastAPI `10_backend_merlin_api/`,
  frontend **statique `ivia_site_v2/`** servi par nginx, corpus, design, infra). **En production.**
- `Fa9d/ivia` — prototype initial (autre stack). Activité récente = commits erronés de
  Perplexity (revertés le 2026-06-29).

**Cause racine identifiée** : plusieurs **agents** (Claude Code, Perplexity, Copilot) que le
fondateur orchestre travaillent sans coordination. Chacun lit la **branche par défaut** du
repo. Or cette default = **`master`** (head `0017`, **périmé**), alors que tout le travail réel
et la **production** sont sur **`refonte-ivia-site-unifie`** (head `0039`). → chaque agent qui
arrive repart d'un état mort. Ce n'est pas un bug d'agent, c'est **structurel** (mauvais pointeur).

## Décision

1. **Dépôt canonique unique : `Fa9d/MERLIN`.** `Fa9d/ivia` → **archivé** (lecture seule,
   historique conservé), README pointant vers MERLIN. Aucun merge de code.
2. **Branche canonique unique : `refonte-ivia-site-unifie`** (head Alembic **`20260625_0039`**,
   stack ADR-0006, = la production). Toute nouvelle migration part de **`0039`**, pas de `0017`.
3. **La branche par défaut GitHub doit pointer vers la branche canonique** (changer
   `master` → `refonte-ivia-site-unifie`, ou y amener le contenu de refonte) — **action
   sensible, exécutée par le fondateur**. C'est le seul fix qui ferme la source de divergence.
4. **Tous les agents (Claude Code, Perplexity, Copilot) travaillent sur la branche canonique**
   (ou via PR vers elle). Les briefs/specs vont dans `00_GOUVERNANCE/COMPORTEMENTAL/`.
5. **Frontend = statique `ivia_site_v2/`** (ADR-0006). Le Next.js `09_app_ivia_merlin/` est
   **archivé** — corrige la mention erronée « frontend Next.js » de la 1ʳᵉ rédaction.

## Conséquences

- Source unique de vérité (dépôt + branche) → fin de la double vérité qui désoriente les agents.
- Les branches d'agents existantes (`copilot/fix-…`, `feat/module-analytique-orientation`,
  `master`) ne sont **pas supprimées** : à auditer puis rapatrier le bon / archiver.
- Changer la default branch est **non destructif** (aucun commit perdu).

## Dépôts / branches

| Élément | Statut |
|---|---|
| `Fa9d/MERLIN` | ✅ Canonique — actif |
| `Fa9d/ivia` | 🗄️ Archivé — lecture seule |
| branche `refonte-ivia-site-unifie` | ✅ Canonique (head 0039, prod) |
| branche `master` | ⚠️ Périmée (head 0017) — à réconcilier puis retirer du flux |
| branches agents (`copilot/*`, `feat/*`) | 🔎 À auditer (travail unique possible) |

---

## Entrée registre associée
> DEC-022 | 2026-06-29 | gouvernance | Dépôt + branche canoniques (MERLIN @ refonte) ; ivia archivé | validated | ADR-0007

## Historique
| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-06-29 | fondateur | Création corrigée (head 0039, frontend statique, clause branche canonique) |
