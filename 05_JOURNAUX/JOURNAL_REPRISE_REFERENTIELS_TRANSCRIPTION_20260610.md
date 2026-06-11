# JOURNAL — Reprise : commits, Carte de Vie vivante, METH → registre, faster-whisper

**Date** : 2026-06-10 (seconde session du jour)
**Branche** : `refonte-ivia-site-unifie`
**Opérateur** : David Phaneuf + Claude Code (Fable 5)
**Référence amont** : `JOURNAL_REFERENTIELS_VIVANTS_20260610.md` (même jour — étapes #1 à #5)

---

## 1. Sécurisation du travail non commité

Tout le travail en suspens a été séparé en commits logiques (plus rien en attente) :

- `5fb551f` feat(referentiels) — 7 YAML doctrine + registry + route API `/referentiels` + tests
- `cbc8f28` chore(ci) — workflow GitHub Actions (lint ruff + tests sans DB bloquants ; full-suite
  Postgres informative ; safety suite scaffoldée), fix fixture DB autouse de `conftest.py`
- `91b604a` docs(claude-md) — HEAD migrations corrigé (`20260528_0027`)
- `8d7392b` feat(seance-pilote) — `pilot_book_slot`, `upload_session_audio`, séance client enrichie
- `08bc934` copy(hero) — « Quand tout se mélange, commencez par être entendu. »
- `4dc6827` feat(carte-de-vie) — première maquette `praticien/carte-de-vie-demo.html`
- `016f269` chore(claude) — modèle `claude-fable-5` + allowlist permissions

Nettoyage : diff parasite (BOM) de `reserver.html` annulé.

## 2. Carte de Vie — taxonomies vivantes (`6ec3c8a`)

La démo praticien suit désormais les référentiels (spec §6 « la carte suit les référentiels ») :
axes et tensions chargés depuis `GET /api/v1/referentiels/{axes,tensions}`, badge
« référentiels : vivants » dans la barre, repli silencieux sur les données embarquées
(page autonome hors-ligne), surcharge locale `?api=http://127.0.0.1:8000`.
**Prochain swap** : remplacer les lectures fictives par `GET /clients/{id}/carte-de-vie`
(endpoint de composition à créer — strate par strate selon spec §4).

## 3. Prompts METH consommateurs du registre (`f68df86`) — étape #4 soldée

- `session_note_cercle_v1.py` : `QUEBEC_CONTEXT_HYPOTHESES` / `QUEBEC_CONTEXT_SIGNALS`
  rendus depuis le registre (`pressions_societales`, `signaux_contextuels`) ; enums du schéma
  de sortie (`familles_contexte`, pressions, `tensions`, `vigilance`) construits via `get_codes()`.
- **METH-001 v1.1 / METH-002 v1.1** : le §7 délègue au référentiel YAML — fin de la duplication.
  La source d'autorité des données est désormais le YAML ; le prompt garde les règles d'usage.
- Tests `test_prompt_injection.py` réécrits contre le registre.

### Divergence à arbitrer (fondateur)

`next_step_type_code` **n'a pas été basculé** : les codes runtime sont en anglais
(`continue_to_structure`, …) alors que `prochaines_etapes.v1.yaml` porte des codes français
(`continuer_a_parler_et_structurer`, …). Aligner l'un sur l'autre = migration de données
(`SessionNote`) ou refonte du référentiel — décision fondateur requise.

## 4. Transcription locale faster-whisper (`6fbf3f2`) — étape #3 soldée

Bascule **AssemblyAI → faster-whisper** (open source, auto-hébergé, données Québec / Loi 25) :

- `app/services/transcription.py` : sélection `MERLIN_TRANSCRIPTION_PROVIDER`
  (`auto` | `faster_whisper` | `assemblyai`), modèle chargé une fois par process,
  rapatriement des audios distants, transcription CPU hors event loop.
- `auto` (défaut) = faster-whisper **si le package est installé**, sinon AssemblyAI →
  **aucun changement de comportement en prod** tant que `requirements-transcription.txt`
  n'est pas installé dans l'image Docker.
- 6 tests unitaires sans DB, ajoutés au job CI bloquant ; ruff vert ; smoke test blindé
  (provider legacy forcé là où la fonction AssemblyAI est mockée).

### Pour activer en prod (ops)

1. Ajouter `pip install -r requirements-transcription.txt` à l'image API.
2. Prévoir un volume persistant pour le cache modèle (`~/.cache/huggingface`).
3. Dimensionner : modèle `medium` int8 CPU par défaut (`MERLIN_WHISPER_MODEL` pour ajuster —
   `small` si le VPS souffre).
4. Une fois validé : retirer `ASSEMBLYAI_API_KEY` de `.env.prod` (sortie définitive du tiers).

## 5. État des tests

- Sans DB : 62 verts (référentiels 28, prompt/schema 28 dont réécrits, transcription 6).
- Full-suite Postgres : non exécutée localement (job CI informatif).

## 6. Reste ouvert

1. Endpoint `GET /clients/{id}/carte-de-vie` (composition 5 strates — spec §4).
2. Arbitrage codes `prochaines_etapes` (français YAML vs anglais runtime).
3. Activation faster-whisper en prod (image Docker + cache modèle).
4. Safety suite en gate CI dur (secret `ANTHROPIC_API_KEY` à fournir).
5. Modèle Claude codé en dur (`claude-sonnet-4-20250514`) → config (constat de la session 1).
