# JOURNAL — PRD canonique Option 1 + alignement doc

**Date** : 2026-06-26
**Opérateur** : David Phaneuf + Claude Code
**Statut** : PRD créé ; alignement doc amorcé. Aucun déploiement.

## Contexte
Décision ADR-0006 actée (Option 1). Réécriture de la documentation produit pour l'aligner.
Tracking git corrigé : local `master` suit désormais `origin/refonte-ivia-site-unifie`
(fin de l'ambiguïté « ahead/behind origin/master »).

## Fait
- `00_GOUVERNANCE/IVIA_PRD_CANONIQUE_v1.0.md` (nouveau) — PRD source de vérité, Option 1 :
  backend Python/FastAPI, frontend statique `ivia_site_v2`, Next.js archivé, IA en Python,
  pilote **juillet 2026**, **Praticienne A / Praticienne B à confirmer** (pas de Mylène/Émilie).
- `.claude/rules/frontend.md` — bannière **ARCHIVÉ** : ces règles ne valent que pour le legacy
  `09_app_ivia_merlin`; frontend prod = statique `ivia_site_v2`.

## Reste à aligner (stack obsolète dans la doc — non bloquant)
- `00_GOUVERNANCE/MERLIN_GOUV_CHOIX_STACK_TECHNIQUE_V1.md`
- `04_METHODES/IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.0.md`
- `07_EXPORTS/IVIA_BRIEF_PERPLEXITY_INTEGRATION_v1.md`
- `04_METHODES/IVIA_SPEC_PAGE_PRATICIENS_v2.0.md`
→ à mettre à jour (référencer ADR-0006) ou marquer périmés.
- Doc de **specs techniques** : s'appuyer sur `ARCHITECTURE.md` (déjà canonique).

## Non fait (volontaire)
- Aucun déploiement / migration. Paiement (`bookings.py /checkout`) non touché (déjà restauré).
