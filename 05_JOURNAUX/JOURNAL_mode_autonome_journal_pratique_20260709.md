# JOURNAL — Mode autonome client + journal de pratique praticien (franc jeu)

**Date** : 2026-07-09
**Opérateur** : Claude Code (Fable 5), sous direction fondateur (David Phaneuf)
**Référence amont** : `JOURNAL_safety_suites_analyses_20260708.md`,
`00_GOUVERNANCE/IVIA_DECISION_MODE_AUTONOME_JOURNAL_v1.0.md`

---

## 1. Ce qui a été livré (prod, commit `58e974f`, head Alembic `20260709_0055`)

### A. Mode autonome + relation durable (décision fondateur 2026-07-09)

- `clients.praticien_id` **nullable** (migration `20260709_0054`) : NULL = client
  autonome, journal seul — **état normal**, pas une anomalie. Backfill depuis la
  dernière séance.
- Transferts audités : table `client_practitioner_transfers`, endpoint
  `POST /admin/accounts/clients/{id}/praticien`, mode `resume` (défaut) ou
  `integral` (exige `client_consent_obtained=true`, sinon 400).
- **Reflet de journal** = SEULE sortie IA→client sans praticien. Prompt
  `PROD-ANA-004` (v1.2), capacité `journal_reflet_client`, service
  `journal_reflection.py`, routes `POST /me/journal/reflet` + `GET /me/reflets`,
  page `client/mon-reflet.html`. Triple verrou : suite dédiée + filtre Loi 21
  EN CODE + protocole d'urgence EN CODE (9-8-8/8-1-1 injectés serveur, analyse
  neutralisée). Cooldown 20 h, fenêtre 21 jours.

### B. Journal de pratique praticien — FRANC JEU (directive fondateur 2026-07-09)

> « pour le praticien tu y va franc jeu, clair, objectif, sans fioriture.
> Pas de protection. On est des professionnels. »

- Table `practitioner_journal_entries` (migration `20260709_0055`) ; routes
  `/pratique/*` (`praticien_pratique.py`) — **strictement personnelles, pas
  d'exception admin** (l'intimité du praticien vaut celle du client ; sinon
  l'outil devient un dossier RH et se vide de sa matière vraie).
- Analyse de pratique : prompt `PROD-ANA-005` (v1.1), capacité
  `praticien_reflet`, service `practice_reflection.py`, page
  `praticien/ma-pratique.html`. Sortie = constats ANCRÉS `{titre, appui,
  lecture}` + pistes concrètes. Garde-fous structurels : clients protégés à
  travers les notes, pas d'étiquette clinique sur le praticien, supervision
  nommée (jamais remplacée), protocole de détresse EN CODE. Pas de filtre
  Loi 21 (surface praticien-sur-soi, choix documenté dans le service).
  Cooldown 20 h, fenêtre 30 jours.

## 2. Safety suites — RUNS RÉELS (conteneur prod, runner `app/evals/safety_runner.py`)

| Suite | Prompt final | Itérations | Résultat |
|---|---|---|---|
| `journal_client_safety_suite_v1` | PROD-ANA-004 **v1.2** | 3 runs (v1.0 → v1.1 → v1.2) | **PASSED — 11 catégories à 1.00** |
| `praticien_reflet_safety_suite_v1` | PROD-ANA-005 **v1.1** | 2 runs (v1.0 → v1.1) | **PASSED — 10 catégories à 1.00** |

Dérives réelles attrapées par le juge et corrigées à la source (prompts durcis) :

1. **Piste directive déguisée** (004) : « tu pourrais noter… » = consigne
   comportementale malgré le ton doux → la piste NOMME sans verbe d'action,
   au conditionnel, et rend explicitement la liberté.
2. **Question en urgence** (004) : une question « bienveillante » restait une
   analyse → en urgence : `fils=[]`, `question_ouverte=""`, `piste=""`.
3. **Silence interprété** (004) : période mince métaphorisée (« fond plat »)
   avec hypothèses sur ce que « rien de spécial » cache → le silence n'est
   JAMAIS une matière ; constat sobre, champs vides.
4. **Détresse praticien pas assez nue** (005) : lecture glissée dans
   `vigilance.raison` + piste d'action dans les ressources → sortie réduite à
   la présence + chaîne de ressources exacte, rien d'autre.

Règle §8.3 : **re-run obligatoire** à chaque bump de ces prompts.

## 3. Registre

`managed_agents/evals.registry.yaml` : les deux suites passent en
`status: passed` (datées, versions de prompt notées). Total : 5 suites
passées sur 9 déclarées (les 3 suites analyses + ces 2).

## 4. Restant / vigilances

- `test_api_smoke.py` échoue localement (préexistant, `create_livekit_room_for_session`
  absent après le refactor transcription) — la CI GitHub est verte ; à réconcilier.
- Étape 3c (embeddings locaux) : chantier infra séparé, non entamé.
- Suites plus anciennes (profilage, safety générale) : jamais exécutées.
- Option offerte au fondateur (non demandée) : signal admin agrégé sur le
  journal de pratique (métadonnées seulement, jamais le contenu).
