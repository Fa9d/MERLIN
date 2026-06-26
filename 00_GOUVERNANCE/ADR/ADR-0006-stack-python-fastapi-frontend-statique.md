---
titre: Stack canonique — Backend Python/FastAPI + frontend statique (Next.js archivé)
id: ADR-0006
statut: validated
couche: PROD
type: ADR
auteur: fondateur
date: 2026-06-26
version: 1.0
décideurs: fondateur
dépend_de: [ADR-0003]
remplace: []
remplacé_par: []
arbitrage_requis: non — décision actée
source_canonique: 00_GOUVERNANCE/ADR/ADR-0006-stack-python-fastapi-frontend-statique.md
---

# ADR-0006 — Stack canonique : Backend Python/FastAPI + frontend statique (Next.js archivé)

> **Statut** : validated — 2026-06-26
> **Couche concernée** : PROD
> **Document de référence** : `CLAUDE.md` §2 · `ARCHITECTURE.md`

---

## Contexte

Une ambiguïté d'architecture persistait : deux frontends coexistaient dans le repo
(`ivia_site_v2/` statique servi en prod, `09_app_ivia_merlin/` Next.js legacy retiré
de la prod le 2026-06-23), et la question d'une migration vers un monorepo Node.js /
Prisma / Next.js était posée. Cette ambiguïté produisait des erreurs d'assistants
(PRD flou, suggestions incohérentes).

Faits au moment de la décision :
- Backend **Python / FastAPI / SQLAlchemy / Alembic** en production, **41 migrations**
  versionnées, suite de tests verte.
- Pipeline IA **Python-natif** : transcription **faster-whisper en local** (données
  hébergées au Québec — Loi 25), analyse Anthropic, profilage/matching/insights.
- Frontend de prod = **site statique `ivia_site_v2`** servi par nginx
  (`root /opt/merlin/ivia_site_v2`). Le Next.js n'est **pas** servi en prod.

---

## Options considérées

**Option A — Migrer vers Node.js / Prisma / Next.js (monorepo)**
Tout réécrire dans un seul repo TypeScript.
*Rejeté* : impose la **réécriture du pipeline IA en TypeScript**, ce qui ferait
**perdre faster-whisper local** et introduirait un **risque de résidence des données**
(Loi 25). 2–3 semaines+ de migration d'un système déjà en prod, à l'approche du pilote.

**Option B — Garder les deux, décider après le pilote**
*Rejeté* : entretient exactement l'**ambiguïté** qui cause les erreurs d'assistants ;
accumule de la dette. Le remède à l'ambiguïté est de décider, pas de reporter.

**Option C — Rester Python/FastAPI + frontend statique ; archiver le Next.js**
*Retenu* : zéro réécriture, pipeline IA préservé (Loi 25), prod stable, ambiguïté levée.

---

## Décision

1. La **stack canonique** est : **backend Python / FastAPI / SQLAlchemy / Alembic**.
2. Le **frontend de production** est le **site statique `ivia_site_v2/`** (HTML + Tailwind),
   servi par nginx, qui consomme l'API FastAPI (`https://api.ivia.quebec`).
3. Le **pipeline IA reste en Python** (faster-whisper local, Anthropic) — il ne migre pas
   hors Python, pour préserver la résidence des données (Loi 25).
4. **Aucune migration** vers Node.js / Prisma / Next.js.
5. Le frontend **`09_app_ivia_merlin/` (Next.js) est ARCHIVÉ** : gelé, conservé pour
   référence, **non développé**, **non servi**. Aucune nouvelle fonctionnalité n'y est ajoutée.

---

## Conséquences

### Avantages
- Décision unique et sans ambiguïté → PRD et assistants alignés.
- Pipeline IA et résidence des données (Loi 25) préservés.
- Aucun risque de migration à l'approche du pilote.

### Inconvénients ou risques
- Le frontend statique appelle l'API séparément (séparation assumée, déjà documentée).
- *Mitigation* : la séparation statique↔API est nette et versionnée ; pas un défaut.

### Actions requises
- [x] Marquer `09_app_ivia_merlin/` comme archivé (bannière `ARCHIVED`).
- [x] Mettre `CLAUDE.md` §2 à jour (stack canonique + Next.js archivé).
- [ ] (PRD/specs externes) Réaligner toute documentation sur Option 1.

---

## Entrée registre associée

> DEC-021 | 2026-06-26 | architecture | Stack canonique Python/FastAPI + frontend statique, Next.js archivé | validated | ADR-0006

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-06-26 | fondateur | Création — décision actée |
