---
titre: Journal — Ajout de la 6ᵉ couche de profilage (types jungiens)
id: JOURNAL-PROFILAGE-JUNG-20260701
type: journal
couche: SYSTEME
date: 2026-07-01
auteur: fondateur + Claude Code
dépend_de: [INDIVIDUATION_cadre_jungien_v0.1, CARTE_DE_VIE_modele_v0.1]
---

# Journal — 6ᵉ couche de profilage : types jungiens (2026-07-01)

## Contexte
Suite à la formalisation du cadre jungien (`00_DOCTRINE/INDIVIDUATION_cadre_jungien_v0.1.md`),
décision du fondateur de **relier Jung au profilage comportemental** (jusqu'ici 5 couches :
OCEAN, Schwartz, Amour×8, Bartholomew, VAD). Jung était noté **P1** dans l'étude des modèles
comportementaux mais jamais implémenté.

## Ce qui a été fait (ajout de code, additif, non destructif)
- **Enum** `JungianFunction` (pensée/sentiment/sensation/intuition) — `app/models/enums.py`.
- **Modèle** `TypeProfileJungian` (table `profile_types_jungian`) — `app/models/behavioral_profile.py` :
  attitude `introversion` [0,1] + 4 fonctions [0,1] + `dominant_function`. Suit **exactement** le
  pattern des 5 autres couches (`ProfileLayerMixin`, `_common_table_args`, append-only, index de matching).
- **Schémas** `JungianScores/Create/Read` — `app/schemas/behavioral_profile.py`.
- **CLAUDE.md** mis à jour (5 → 6 couches ; règle §11).
- Syntaxe des 3 fichiers Python **validée** (`py_compile` OK).

## NON fait (volontairement — prudence backend)
- **Pas de migration Alembic écrite à la main** : la chaîne de révisions mélange deux styles de
  nommage (datés + hash) → head ambigu, et impossible de tester `alembic upgrade` hors environnement.
  → **À générer par `alembic revision --autogenerate -m "profile_types_jungian"` puis tester** dans
  l'environnement (la nouvelle table sera détectée automatiquement).

## Garde-fous (opposables)
- `status` défaut `hypothese` — **jamais un diagnostic**.
- **Scores/étiquettes jamais exposés au client** (`ClientFacingProfileView` uniquement).
- Écriture conditionnée à un **consentement** (N2/N3) ; sensibilité `high`.
- Les types = **repères, pas des cases** (cf. doctrine individuation §6).
- **security-review + safety evals requises avant toute exposition** (constitution §8, CLAUDE.md).

## Reste à faire
- [ ] Générer + tester la migration `profile_types_jungian`.
- [ ] Décider si la fonction dominante alimente le `profile_matching` (mode complémentarité/similarité).
- [ ] security-review avant toute restitution client.
- [ ] (optionnel) relier à la Carte de Vie (les types comme lentille de lecture des 11 axes).

## Historique
| Date | Auteur | Nature |
|---|---|---|
| 2026-07-01 | fondateur + Claude Code | Ajout couche Jung (modèle/enum/schéma) — migration en attente |
