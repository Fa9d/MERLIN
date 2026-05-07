# Tickets backlog — issus de la Vague 8 (analyse stack outils)

**Date** : 7 mai 2026
**Source** : décisions arbitrées dans `IVIA_ANALYSE_STACK_OUTILS_v1.md`
**Cible** : à créer dans Linear (une fois Linear setup) ou GitHub Issues en attendant

---

## Tickets à créer

### OPS-002 — Déployer Dozzle (UI logs Docker) sur VPS

**Priorité** : P1 — quick win, signal pro immédiat
**Effort** : 10 min
**Vague** : 8 (cette semaine)

**Description** :
Déployer Dozzle (MIT) en conteneur Docker sur le VPS OVH pour avoir une UI web propre des logs des 7 conteneurs MERLIN.

**Acceptance criteria** :
- [ ] Conteneur `dozzle` lancé via `docker-compose.prod.yml`
- [ ] UI accessible via `https://logs.ivia.quebec` (reverse proxy nginx)
- [ ] Authentification basique activée
- [ ] Documenté dans `deploy/README.md`

**Référence** : [Dozzle GitHub](https://github.com/amir20/dozzle)

---

### OPS-003 — Déployer Uptime Kuma + status.ivia.quebec

**Priorité** : P1 — signal pro fort pour pilote praticien (J-24)
**Effort** : 30 min
**Vague** : 8 (cette semaine)

**Description** :
Déployer Uptime Kuma (MIT) pour monitorer uptime des services IVIA/MERLIN et publier une page de statut publique.

**Acceptance criteria** :
- [ ] Conteneur `uptime-kuma` opérationnel
- [ ] Monitors configurés : ivia.quebec, api.ivia.quebec, db Postgres
- [ ] Status page publique sur `https://status.ivia.quebec`
- [ ] Notifications email vers `bonjour@ivia.quebec` en cas d'incident
- [ ] DNS A record `status.ivia.quebec` créé chez OVH

**Référence** : [Uptime Kuma GitHub](https://github.com/louislam/uptime-kuma)

---

### OPS-004 — Déployer GlitchTip (monitoring erreurs Sentry-compatible)

**Priorité** : P2 — important mais peut attendre fin de Vague 8
**Effort** : 1 h 30 (déploiement + intégration SDK FastAPI/React)
**Vague** : 8

**Description** :
Remplacer les `print()` errors actuels par un vrai monitoring d'erreurs via GlitchTip self-hosted (AGPL, API-compatible Sentry).

**Acceptance criteria** :
- [ ] Conteneur `glitchtip` + worker Celery + Redis
- [ ] UI accessible via `https://errors.ivia.quebec` (interne, accès restreint)
- [ ] SDK Sentry installé dans `10_backend_merlin_api` (Python) → DSN GlitchTip
- [ ] SDK Sentry installé dans `09_app_ivia_merlin` (Next.js) → DSN GlitchTip
- [ ] Test : exception levée volontairement → apparaît dans GlitchTip
- [ ] Alertes email vers `bonjour@ivia.quebec` sur erreurs critiques

**Référence** : [GlitchTip Docs](https://glitchtip.com/documentation)

---

### OPS-005 — Migration tickets vers Linear Free

**Priorité** : P2
**Effort** : 2 h
**Vague** : 8

**Description** :
Migrer les tickets backlog actuels (MES-, MATCH-, INFRA-, BACK-, OPS-, GOUV-) depuis les fichiers MD `00_GOUVERNANCE/` vers Linear Free.

**Acceptance criteria** :
- [ ] Compte Linear créé (workspace IVIA)
- [ ] 4 teams créées : Backend, Frontend, Ops, Gouvernance
- [ ] Tous les tickets actifs (~30 estimé) migrés avec labels et priorités
- [ ] Tickets fermés marqués comme tels avec référence commit
- [ ] Intégration GitHub activée (auto-link PR ↔ ticket)

**Note** : conserver les fichiers MD de référence dans `00_GOUVERNANCE/`, Linear devient la source de vérité opérationnelle.

---

### OPS-006 — Déployer Umami Analytics (conformité Loi 25)

**Priorité** : P2
**Effort** : 30 min
**Vague** : 9 (semaine 14 mai)

**Description** :
Déployer Umami (MIT) pour tracking analytics conforme Loi 25 (pas de cookies, données sur VPS Beauharnois).

**Acceptance criteria** :
- [ ] Conteneur `umami` + Postgres dédié
- [ ] UI accessible via `https://analytics.ivia.quebec` (privé)
- [ ] Script tracking installé sur ivia.quebec (landing + onboarding)
- [ ] Mention dans la politique de confidentialité v0.1 mise à jour

---

### OPS-007 — Déployer Infisical (gestion secrets)

**Priorité** : P3
**Effort** : 2 h
**Vague** : 9-10

**Description** :
Migrer les `.env` critiques vers Infisical self-hosted (MIT, end-to-end encryption).

**Acceptance criteria** :
- [ ] Conteneur `infisical` + Postgres + Redis
- [ ] UI accessible via `https://secrets.ivia.quebec` (privé)
- [ ] Migration de `.env.prod` (variables non-publiques)
- [ ] Intégration CI/CD GitHub Actions (si activé)
- [ ] Documentation rotation secrets

---

### OPS-008 — Souscription v0.app Premium (3 mois ciblés)

**Priorité** : P2 — accélère landing + onboarding praticien
**Effort** : 5 min admin + usage continu
**Vague** : 9

**Description** :
Souscrire v0.app Premium (28 $/mois) pour 3 mois (mai-juin-juillet 2026), refonte landing IVIA + écrans onboarding praticien.

**Acceptance criteria** :
- [ ] Compte v0.app Premium actif
- [ ] Carte de crédit business utilisée (pas perso)
- [ ] Reminder pour évaluer renouvellement le 31 juillet 2026
- [ ] Templates générés exportés vers `09_app_ivia_merlin/components/`

---

## Tickets reportés (Vague 10+)

### OPS-009 — Grafana + Loki + Prometheus
**Vague** : 10 (post-pilote 31 mai)
**Effort** : 3 h
**Justification report** : pas critique avant le pilote, libère du temps J-24

### OPS-010 — PostHog self-hosted
**Vague** : 12+
**Effort** : 4 h
**Justification** : utile quand 50+ praticiens et besoin analyse comportementale

### OPS-011 — Évaluation migration Cursor
**Vague** : 11+
**Effort** : 1 semaine d'usage
**Justification** : seulement si productivité Claude Code/Codex/Copilot stagne

---

## Synthèse priorisation

| Vague | Tickets | Effort total | Bénéfice principal |
|---|---|---:|---|
| **Vague 8** (cette semaine) | OPS-002, 003, 004, 005 | ~4 h | Observabilité + ticketing pro |
| **Vague 9** (sem. 14 mai) | OPS-006, 007, 008 | ~3 h | Analytics Loi 25 + secrets + design |
| **Vague 10** (sem. 21 mai) | OPS-009 | ~3 h | Métriques applicatives |
| **Post-pilote** | OPS-010, 011 | ~5 h | Évolutions long-terme |

---

*Généré par Perplexity Computer — 7 mai 2026, 14h00 EDT*
*À intégrer dans Linear une fois OPS-005 terminé.*
