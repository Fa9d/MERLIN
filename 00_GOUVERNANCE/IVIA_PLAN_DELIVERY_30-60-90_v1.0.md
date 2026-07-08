# IVIA — Plan delivery 30/60/90 (qualité, fiabilité, sécurité, livraison)

**Version** : v1.0 — 2026-07-08
**Statut** : canon (backlog vivant — cocher/amender ici, bumper la version)
**Auteur** : Claude Code (Fable 5), validé par David Phaneuf
**Contexte** : produit à partir de l'audit du 2026-07-07/08 (voir
`05_JOURNAUX/JOURNAL_reunification_depot_20260708.md`) et du diagnostic repo réel.

---

## Décisions fondateur actées

- **M2 refusé (2026-07-08)** : `emotion_saas` **reste active par défaut** sur le profil
  client en phase test. La réévaluation avant mise en marché (commentaire de
  `capability_gate.py`) demeure le point de contrôle.

## Diagnostic (résumé)

- **Forces** : stack canonique actée, CI réelle (verte depuis 2026-07-08), souveraineté
  données (whisper/prosodie locaux, Matomo auto-hébergé, sauvegardes chiffrées),
  gouvernance IA outillée (vanne de capacités, évals, constitution), dépendances épinglées.
- **Risques** : bus factor 1 ; pas de protection de branche (plan GitHub gratuit) ;
  CI restée rouge 6 jours sans réaction ; restore de sauvegarde jamais prouvé ;
  divergence de branches déjà survenue (prod hors branche d'intégration, 2-7 juillet).

## Backlog priorisé (état au 2026-07-08)

| ID | Titre | Prio | Effort | Statut |
|----|-------|------|--------|--------|
| M0 | Redéployer prod sur branche d'intégration | P0 | S | **en attente David (VPS)** |
| M1 | Rétablir SSH poste → VPS | P0 | S | **en attente David** |
| M2 | Désactiver emotion_saas profil client | — | — | **REFUSÉ fondateur 2026-07-08** |
| M3 | gitleaks bloquant en CI (+ allowlist `_archives/`) | P0 | S | **livré 2026-07-08** |
| M4 | pip-audit bloquant nouvelles CVE (9 existantes = risque accepté, cf. ci.yml) | P0 | S | **livré 2026-07-08** |
| M5 | Test de restauration de sauvegarde (chrono + doc + journal) | P0 | M | à faire (dép. M1) |
| M6 | GitHub Pro + protection de branche (require PR + CI verte) | P1 | S | **en attente David (facturation)** |
| M7 | Template PR + issue | P1 | S | **livré 2026-07-08** |
| M8 | CONTRIBUTING.md | P1 | S | **livré 2026-07-08** |
| M9 | CODEOWNERS zones critiques | P1 | S | à faire (dép. M6) |
| M10 | Zéro commit checkpoint sur branches partagées | P1 | S | à faire |
| M11 | E2E happy path intake → activation → mon-espace | P1 | M | **livré 2026-07-08** (`tests/test_public_intake_e2e.py`) |
| M12 | Tests intégration paiement test + réservation | P1 | M | à faire |
| M13 | Couverture ≥ 60 % sur `app/services` + `app/api/routes` (gate CI) | P1 | M | à faire (dép. M11) |
| M14 | Smoke test post-déploiement dans `pull-deploy.sh` | P1 | S | **livré 2026-07-08** (première exécution réelle = M0) |
| M15 | Alertes Uptime Kuma (courriel) API/site/stats | P1 | S | à faire |
| M16 | `ruff format` + pre-commit hooks | P2 | S | à faire |
| M17 | Bump fastapi/starlette (ferme les 9 CVE acceptées) + Dependabot | P1 | M | à faire |
| M18 | Logs structurés routes sensibles (auth, paiements, analyses) | P2 | M | à faire |
| M19 | SemVer + CHANGELOG auto | P2 | S | à faire |
| M20 | Runbook incident/rollback répété à blanc (< 10 min) | P1 | M | à faire (dép. M0, M1) |
| M21 | README onboarding < 10 min | P2 | S | à faire |
| M22 | Safety evals bloquantes en CI si `11_PROMPTS/**` touché | P1 | L | à faire (secret ANTHROPIC_API_KEY requis) |

**Ordre strict restant** : M0 → M1 → M6 → M14 → M5 → M15 → M11 → M12 → M13 → M20 →
M9 → M10 → M17 → M16 → M22 → M18 → M21 → M19.

## Jalons

- **J+30 (verrouiller)** : M0-M8 fermés (hors M2 refusé) + M14 + M5. Mesure : CI verte
  30 jours, 0 push direct hors merge, 1 restore prouvé daté.
- **J+60 (prouver)** : M11-M13. Mesure : casser volontairement un parcours critique
  fait échouer un test.
- **J+90 (observer & livrer)** : M15, M17-M20 + étape 1 du chantier Analyses
  (`IVIA_CADRAGE_ANALYSES_JOURNAL_RESTITUTIONS`) livrée sous les nouveaux gates.
  Mesure : détection de panne simulée < 5 min ; rollback à blanc < 10 min.

## Gouvernance de delivery (résumé opposable)

- Toute modification non triviale = PR (self-merge si CI verte). Template PR obligatoire.
- Branches de travail < 5 jours, < 20 commits d'écart avec l'intégration.
- Gates CI : ruff · unit · full-suite · gitleaks · pip-audit (+ couverture à J+60,
  safety evals sur prompts à M22).
- Rituels : lecture/écriture `05_JOURNAUX/` par session ; review hebdo (vendredi) ;
  rétro mensuelle → **une seule** nouvelle règle max.
- Checklists release et incident : voir `CONTRIBUTING.md` et le template PR.
