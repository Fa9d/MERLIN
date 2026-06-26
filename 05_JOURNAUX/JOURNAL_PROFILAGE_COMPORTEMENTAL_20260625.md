# JOURNAL — Profilage comportemental à 5 couches

**Date** : 2026-06-25
**Opérateur** : David Phaneuf + Claude Code
**Statut** : ✅ Code écrit, mappers vérifiés, migration créée — ⏳ **NON appliquée en prod** (en attente security-review)

---

## Objet
Schéma de données pour un profilage comportemental à 5 couches (matching praticien↔client) :
1. Traits stables — Big Five **OCEAN**
2. Valeurs profondes — **Schwartz** (10 valeurs)
3. Style relationnel — **8 Expressions de l'Amour**
4. Style d'attachement — **Bartholomew** (4 quadrants)
5. État dynamique — **Circumplex VAD** (Valence/Arousal/Dominance)

## Fichiers créés / modifiés
- `app/models/behavioral_profile.py` (nouveau) — mixin `ProfileLayerMixin` + 5 modèles.
- `app/schemas/behavioral_profile.py` (nouveau) — Create/Read par couche + `ClientFacingProfileView` (garde-fou).
- `app/models/enums.py` — +4 enums (`ProfileSubjectKind`, `ProfileSource`, `ProfileStatus`, `AttachmentStyle`).
- `app/db/base.py` — enregistrement du module dans `load_models()`.
- `alembic/versions/20260625_0039_add_behavioral_profile_layers.py` (nouveau) — head `0039`, down `0038`.
- `CLAUDE.md` (§13) + `.claude/rules/backend.md` — head migration `0038` → `0039` + note posture.

## Conception
- **Append-only versionné** : 1 layer = 1 table ; chaque ré-évaluation = nouvelle ligne (`version`+1, `is_current=True`). Historique = toutes les lignes ; score courant = `is_current`. **Index UNIQUE partiel** `uq_*_current` garantit un seul courant par sujet.
- **Sujet polymorphe** : `subject_kind` (client/praticien) + `client_id`→`clients.id` OU `practitioner_user_id`→`app_users.id` (CheckConstraint d'exclusivité). Permet le matching.
- **Index de matching** : index partiels `WHERE is_current` sur les dimensions clés par couche + `ix_*_subject_current`.
- **Provenance/validation** : `source`, `assessed_by_user_id`, `validated_by_user_id`/`validated_at`, `confidence`.

## Garde-fous (constitution IVIA — Loi 21 / Loi 25)
- `status` défaut **`hypothese`** — **jamais un diagnostic**.
- `consent_id`→`consents.id` : toute écriture rattachable à un consentement (N2/N3).
- `data_sensitivity_class` défaut **`high`**.
- **Client jamais exposé aux scores bruts** ni à une étiquette : seule `ClientFacingProfileView` (Observation/Hypothèse/Orientation) lui est destinée.
- `ondelete=CASCADE` sur le sujet (droit à l'effacement Loi 25).

## Vérifications
- `py_compile` : OK (5 fichiers).
- Construction des mappers SQLAlchemy (`configure_mappers`) : OK — 5 tables, colonnes/index conformes.
- Chaîne Alembic linéaire : seul `0039` référence `0038` (head propre).

## À faire avant exposition / déploiement (NON fait ici)
1. **security-review** (modèle de données client sensible).
2. **Safety evals** : garantir qu'aucune sortie client ne ressort en diagnostic/étiquette.
3. Décision produit + **services/routes** (création, passage de l'ancien courant à `is_current=False`, matching).
4. Application migration : `alembic upgrade head` (via `make migrate`) — non lancée en prod.
5. Option `pgvector` pour le matching à grande échelle (discuté, non implémenté).

## Références
- Conventions : `CLAUDE.md` §13, `.claude/rules/backend.md`
- Modèles voisins : `app/models/client.py`, `app/models/consent.py`, `app/models/enums.py`
