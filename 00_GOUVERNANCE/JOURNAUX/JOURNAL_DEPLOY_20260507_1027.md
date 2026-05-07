# Journal de déploiement — Vague 7

**Date** : 7 mai 2026
**Heure début** : 10:27 EDT
**Heure fin smoke tests verts** : 13:08 EDT
**Durée totale** : ~2h40
**Stamp de référence** : `20260507_1027`
**Opérateur** : David Phaneuf (VSCode + Claude Code + Perplexity Computer)
**VPS** : `ubuntu@137.74.42.121` → `https://ivia.quebec` + `https://api.ivia.quebec`

---

## 1. Périmètre déployé

### Tickets livrés en prod

- **MATCH-001** — `PractitionerProfile` enrichi avec champs de matching (commit `abf2252`)
- **MATCH-002** — Page `/demarche` formulaire 3 étapes sans auth, urgence 811 (commit `01fe8a7`)
- **Migration 0018** — `add_match_fields_to_practitioner_profile` + 4 migrations en cascade jamais appliquées en prod

### Migrations appliquées en cascade

```
20260504_0017 (état initial prod)
    ↓
69a1d763d644  add_practitioner_profiles
    ↓
cfe9090adc2f  add_practitioner_profiles
    ↓
b5bac8044496  add_display_fields_to_practitioner_profile
    ↓
072fa69b58e4  rename_session_channel_codes_add_pending_review
    ↓
20260507_0018  add_match_fields_to_practitioner_profile  ← HEAD final
```

Les 4 migrations intermédiaires existaient en dev depuis fin avril mais n'avaient jamais atteint la prod (qui était bloquée à 0017). Toutes appliquées de manière atomique via DDL transactionnel PostgreSQL.

---

## 2. Modifications structurelles

### Volume mount ajouté à `docker-compose.prod.yml`

Sous le service `api`, section `volumes` :

```yaml
- /opt/merlin/11_PROMPTS:/11_PROMPTS:ro
```

**Raison** : le module `app/ai/prompt_loader.py` calcule le chemin canonique des prompts via `Path(__file__).resolve().parents[3] / "11_PROMPTS"`, ce qui résout en `/11_PROMPTS` dans le container Docker. Le dossier n'était pas présent — fix par mount read-only depuis l'hôte.

**Backup du fichier original** : `/opt/merlin/docker-compose.prod.yml.bak_20260507_1247`

### Nouveau dossier sur le VPS

```
/opt/merlin/11_PROMPTS/
├── 02_METH/
│   ├── METH-001-quebec-context-hypotheses-v1.md
│   ├── METH-002-quebec-context-signals-v1.md
│   ├── METH-003-session-note-cercle-system-prompt-v1.md
│   └── METH-004-triage-signaux-urgence-v1.md
└── (autres sous-dossiers selon arborescence repo)
```

Total : 21 fichiers Markdown, 40 Ko.

---

## 3. Backups conservés (rollback possible)

```
/opt/merlin/10_backend_merlin_api.OLD_20260507_1153   (ancien backend prod)
/opt/merlin/10_backend_merlin_api.bak_20260507_1027   (snapshot étape 5)
/opt/merlin/09_app_ivia_merlin.OLD_20260507_1153      (ancien frontend prod)
/opt/merlin/09_app_ivia_merlin.bak_20260507_1027      (snapshot étape 5)
/opt/merlin/docker-compose.prod.yml.bak_20260507_1247 (compose avant volume mount)
```

**Rollback en 30 secondes possible** si une régression apparaît sous 24-48h. À archiver dans `/opt/merlin/_archives/` après J+7 stable.

---

## 4. Smoke tests post-déploiement

Exécutés à **13:08 EDT** depuis le VPS lui-même :

| Test | Cible | Résultat | Latence |
|---|---|---|---|
| Frontend public | `https://ivia.quebec` | **HTTP 200** | 324 ms |
| API auth gate | `https://api.ivia.quebec/api/v1/auth/me` | **HTTP 401** (attendu, exige token) | 102 ms |
| Migration head DB | `alembic current` | **20260507_0018 (head)** | < 50 ms |

### État Docker final (7/7 services)

| Container | Status |
|---|---|
| `merlin-api-1` | Up healthy |
| `merlin-frontend-1` | Up |
| `merlin-nginx-1` | Up 2 days (non recréé, OK) |
| `merlin-db-1` | Up healthy |
| `merlin-livekit-1` | Up 2 days |
| `merlin-livekit-egress-1` | Up healthy |
| `merlin-redis-1` | Up healthy |

---

## 5. Incidents et leçons apprises

### Incident 1 — `scp -r` non filtré

À 10h27, premier `scp -r` lancé sans exclusions → 45 minutes à copier `venv/`, `node_modules/` et autres dossiers lourds vers `/tmp/merlin_deploy_20260507_1027/`. Interrompu manuellement par `^C` à 11h12.

**Mitigation** : cleanup intégral de `/tmp/merlin_deploy_*` (487 Mo libérés). Aucun impact sur `/opt/merlin/` (la bascule n'avait pas eu lieu).

**Leçon** : toujours utiliser un fichier d'exclusions `tar -X` avec patterns explicites (`venv`, `.next`, `node_modules`, `__pycache__`, `*.db`, `.env`).

### Incident 2 — PowerShell encoding UTF-16 pour fichier d'exclusions

Premier `Set-Content deploy_excludes.txt` produit un fichier UTF-16 LE avec BOM, illisible par `tar -X`. Tarball résultant à 0,07 Mo (vide).

**Mitigation** : régénération avec `Set-Content -Encoding ascii`.

**Leçon** : sur PowerShell 5.1, **toujours** spécifier `-Encoding ascii` ou `-Encoding utf8` (qui ajoute un BOM mais reste lisible) pour les fichiers consommés par des outils Unix.

### Incident 3 — Wildcards PowerShell expandés dans args natifs

`tar.exe --exclude="*.pyc"` interprété par PowerShell qui remplace `*` par des fragments du PATH. Tarball corrompu.

**Mitigation** : usage du fichier d'exclusions (`-X deploy_excludes.txt`) au lieu d'arguments inline.

**Leçon** : pour exécutables natifs sous PowerShell, soit utiliser `--%` (stop-parsing token), soit array `@args`, soit fichier de configuration externe (le plus fiable).

### Incident 4 — `merlin-api` plante sur `PromptNotFoundError`

Au premier restart avec la nouvelle image, l'API entre en boucle de redémarrage. Stack trace pointe vers `prompt_loader.py` → fichier `/11_PROMPTS/02_METH/METH-001-quebec-context-hypotheses-v1.md` introuvable.

**Cause racine** : le module `ai/prompts/` (introduit par MATCH-001/002) suppose une structure monorepo avec `11_PROMPTS/` à la racine du repo, mais l'image Docker ne contient que `/app/` (le sous-dossier backend renommé).

**Mitigation** : volume mount `/opt/merlin/11_PROMPTS:/11_PROMPTS:ro` ajouté à `docker-compose.prod.yml`.

**Leçon** : avant tout déploiement, scanner les chemins en dur dans le code Python (`grep -r "11_PROMPTS"` ou équivalent) pour identifier toutes les dépendances filesystem hors du dossier de service.

### Incident 5 — Docker Compose sans `--env-file`

Premier build a échoué avec `invalid containerPort: -` parce que toutes les variables d'env étaient blank.

**Cause racine** : Docker Compose ne charge pas automatiquement `.env.prod` (uniquement `.env`).

**Mitigation** : commande corrigée avec `docker compose --env-file .env.prod -f docker-compose.prod.yml ...`.

**Leçon** : documenter dans le runbook que **toutes** les commandes `docker compose` en prod doivent inclure `--env-file .env.prod`.

---

## 6. Backlog généré par cette Vague 7

### Ticket nouveau identifié — `BACK-010` (suggestion)

**Titre** : Refactor `prompt_loader.py` pour respecter une variable d'environnement
**Priorité** : Moyenne
**Description** : Modifier `_prompts_root()` pour utiliser `os.getenv("MERLIN_PROMPTS_DIR")` en priorité, avec fallback sur le calcul `parents[3]` actuel. Permet de découpler le code de la structure filesystem du repo.

### Ticket nouveau identifié — `OPS-001` (suggestion)

**Titre** : Documenter la procédure de déploiement standard
**Priorité** : Haute
**Description** : Créer un runbook `OPS_DEPLOY_RUNBOOK_v1.md` avec les 7 étapes validées aujourd'hui (tarballs, scp, bascule, build, alembic, restart, smoke). Inclure le fichier `deploy_excludes.txt` à committer.

### BACK-009 (déjà existant)

Renommage des 4 fichiers Alembic au slug menteur. **Non urgent** — les migrations sont passées en cascade sans souci grâce aux revision_id (qui ne dépendent pas du nom de fichier).

---

## 7. Métriques

| Métrique | Valeur |
|---|---|
| Durée totale opération | 2h40 |
| Fenêtre d'indisponibilité prod | ~5 minutes (entre stop des containers et restart healthy) |
| Données transférées hôte → VPS | ~480 Ko (vs ~487 Mo écrasés au premier scp) |
| Ratio efficacité tarballs | ~1 000:1 |
| Migrations Alembic appliquées | 5 (4 intermédiaires + 1 cible) |
| Backups conservés | 5 dossiers/fichiers |
| Smoke tests verts | 3/3 |

---

## 8. Prochaines vagues

- **Vague 8** — Analyse stack outils MERLIN/IVIA (livré : `IVIA_ANALYSE_STACK_OUTILS_v1.md`). Décisions à prendre : Linear, Dozzle, Uptime Kuma, GlitchTip.
- **Vague 9** — Setup Umami + Infisical + v0.app (selon validation Vague 8).
- **Vague 10** — Onboarding praticien pilote (cible 31 mai 2026).

---

## 9. Validation

- ✅ DB en `20260507_0018 (head)`
- ✅ 7 containers Up, dont API et DB healthy
- ✅ Frontend `https://ivia.quebec` répond 200
- ✅ API `https://api.ivia.quebec/api/v1/auth/me` répond 401 (auth gate fonctionne)
- ✅ Backups multiples conservés pour rollback
- ✅ Aucune perte de données
- ✅ Aucune dégradation services tiers (LiveKit, Redis, Nginx intacts)

**Statut Vague 7** : ✅ **DÉPLOYÉE ET VALIDÉE**

---

**Devise IVIA : Au sein de l'être — En actes**

*Journal généré le 7 mai 2026 à 13:08 EDT par Perplexity Computer en collaboration avec Claude Code (VSCode) sous direction de David Phaneuf.*
