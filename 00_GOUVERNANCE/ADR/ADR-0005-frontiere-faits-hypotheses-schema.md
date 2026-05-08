---
titre: Frontière fait / hypothèse / recommandation dans le schéma JSON des notes cliniques
id: ADR-0005
statut: validated
couche: PROD
type: ADR
auteur: fondateur
date: 2026-05-08
version: 1.0
décideurs: fondateur
dépend_de: [ADR-0002]
remplace: []
remplacé_par: []
arbitrage_requis: non
source_canonique: 00_GOUVERNANCE/ADR/ADR-0005-frontiere-faits-hypotheses-schema.md
---

# ADR-0005 — Frontière fait / hypothèse / recommandation dans le schéma JSON des notes cliniques

> **Statut** : validated — 2026-05-08
> **Couche concernée** : PROD
> **Document de référence** : `10_backend_merlin_api/app/ai/prompts/session_note_cercle_v1.py`

---

## Contexte

Le **Contrat Prompt V1** (DEC-039) impose, en §3 et §5.1, une distinction explicite entre trois niveaux de preuve dans toute sortie IA :

1. **Fait observable** — extrait verbatim ou paraphrase directe du transcript
2. **Hypothèse** — inférence raisonnée, non confirmée
3. **Recommandation** — action suggérée, sous réserve de validation

La structure JSON minimale du Contrat Prompt §5.1 contient explicitement les clés `faits`, `hypotheses`, `recommandations`.

**Problème observé** : le schéma actuel `SESSION_NOTE_CERCLE_OUTPUT_SCHEMA` (fichier `session_note_cercle_v1.py`) ne contient **pas ces trois clés au premier niveau**. Il propose à la place :

- `production_note.summary_text`, `observations_text`, `coeur_summary_text`, etc. — texte libre mélangeant potentiellement les trois niveaux
- `context_hypotheses_json` — bonne séparation pour les hypothèses contextuelles
- `identified_tensions_json` — taxonomie des tensions (mélange faits + interprétation)
- Aucun champ explicitement nommé `faits` ni `recommandations`

Conséquence : la **GRILLE-QUALITE-NOTE-V1** critère `tracabilite_sources` ne peut pas être appliquée mécaniquement, car la frontière n'est pas encodée dans la structure de la sortie. Un évaluateur doit lire chaque phrase de `summary_text` pour décider si c'est un fait, une hypothèse ou une recommandation. Cela viole le principe « la frontière doit être structurelle, pas littéraire » du Contrat Prompt §3.

---

## Options considérées

**Option A — Statu quo : laisser le prompt produire du texte libre dans `summary_text`**
*Rejeté* : viole le Contrat Prompt §3, rend la GRILLE-QUALITE-NOTE non automatisable, augmente la charge cognitive du praticien validant.

**Option B — Refonte complète du schéma : remplacer toute la structure actuelle par `{faits, hypotheses, recommandations}` plat**
*Rejeté* : breaking change majeur, casse les 18 sessions déjà créées (champs `coeur_summary_text` etc. utilisés en frontend), perd la richesse axes (cœur/corps/esprit/être) déjà acceptée doctrinalement.

**Option C — Extension additive : ajouter au schéma existant les trois clés `faits`, `hypotheses`, `recommandations` au niveau `production_note`, garder le reste**
*Retenu* : compatibilité ascendante (G7 GO/NO-GO PASS), respect du Contrat Prompt §5.1 lettrement, GRILLE-QUALITE-NOTE applicable, migration progressive (les champs existants deviennent des projections de `faits`/`hypotheses` par axe et par dimension).

---

## Décision

Patch **MINOR** (selon SemVer du Contrat Prompt §8) sur `SESSION_NOTE_CERCLE_OUTPUT_SCHEMA` — version `v1.1` :

### 1. Ajout au niveau `production_note` de trois clés obligatoires

```python
"faits": [
    {
        "id": "F-001",
        "texte": "string",                  # paraphrase ou citation
        "citation_directe": "string|null",  # extrait verbatim si disponible
        "timestamp": "string|null",         # ex "00:04:32"
        "axe_primaire": "coeur|corps|esprit|etre",
        "source": "transcript|brief_verbal",
    }
],
"hypotheses": [
    {
        "id": "H-001",
        "texte": "string",
        "faits_supports": ["F-001", "F-003"],   # IDs des faits qui soutiennent
        "axe_primaire": "coeur|corps|esprit|etre",
        "confidence_code": "faible|moyen|eleve",
    }
],
"recommandations": [
    {
        "id": "R-001",
        "texte": "string",
        "type": "exploration|stabilisation|orientation|escalade|suivi",
        "fonde_sur": ["F-001", "H-002"],   # IDs faits + hypothèses
        "specificite_code": "specifique_au_cas|generique",
    }
],
```

### 2. Règles d'intégrité

- **R1** : Toute hypothèse doit référencer ≥ 1 fait dans `faits_supports` (sinon REJET via critère B4).
- **R2** : Toute recommandation doit référencer ≥ 1 élément dans `fonde_sur` (fait ou hypothèse).
- **R3** : Les IDs `F-XXX`, `H-XXX`, `R-XXX` sont uniques au sein d'une note, séquentiels.
- **R4** : Les champs `summary_text`, `observations_text`, `coeur_summary_text` etc. **restent** mais deviennent **dérivés** : ils peuvent référencer les IDs de `faits`/`hypotheses` au format `[F-001]` pour traçabilité.

### 3. Validation

- Pydantic schema mis à jour dans `app/schemas/session_note.py` avec les 3 nouveaux champs
- Test unitaire `tests/test_json_schema_validation.py::test_v11_faits_hypotheses_recommandations` ajouté
- Test prompt injection `tests/test_prompt_injection.py::test_v11_no_orphan_hypothesis` (vérifier R1)

### 4. Migration des notes existantes

- Migration Alembic `0019_add_faits_hypotheses_recommandations_jsonb` — ajoute 3 colonnes JSONB nullable sur `session_notes`
- Pas de backfill rétroactif des notes pré-v1.1 (elles restent valides en v1.0)
- Champ `metadata.prompt_version` permet de distinguer

---

## Conséquences

### Avantages

- Application mécanique de la `GRILLE-QUALITE-NOTE` (critère `tracabilite_sources` automatisable)
- Frontière fait/hypothèse devient **structurelle**, plus seulement littéraire
- Permet construction d'un graphe de traçabilité fait → hypothèse → recommandation
- Lit le Contrat Prompt §5.1 à la lettre (clé `faits`, `hypotheses`, `recommandations` enfin présentes)
- Compatible avec l'évaluation inter-praticien (Mylène vs Émilie peuvent désigner précisément quel fait soutient quelle hypothèse, plutôt que débattre sur du texte fluent)

### Inconvénients ou risques

- Charge prompt augmente (modèle doit générer ~30 % de tokens en plus pour les IDs et liens)
- Premières sorties v1.1 risquent de produire des `faits_supports: []` (modèle pas encore calibré) — d'où la règle R1 qui enverra ces notes en `RETOUCHE_REQUISE`
- Migration Alembic à exécuter en prod (suppose une fenêtre de maintenance ou hot migration)
- Frontend devra évoluer pour afficher les liens IDs (cliquer sur `[F-001]` dans `summary_text` doit ouvrir le fait)

### Actions requises

- [ ] Mettre à jour `session_note_cercle_v1.py` → version `v1.1` (frontmatter Contrat Prompt + bump version dans constante `SESSION_NOTE_CERCLE_PROMPT_VERSION`)
- [ ] Étendre `SESSION_NOTE_CERCLE_OUTPUT_SCHEMA` avec les 3 clés (production_note → faits, hypotheses, recommandations)
- [ ] Mettre à jour `app/schemas/session_note.py` (Pydantic) avec les nouveaux champs
- [ ] Créer migration Alembic `0019_add_faits_hypotheses_recommandations_jsonb`
- [ ] Ajouter tests `test_json_schema_validation.py::test_v11_faits_hypotheses_recommandations` et `test_prompt_injection.py::test_v11_no_orphan_hypothesis`
- [ ] Annoncer dans `JOURNAL_PILOTE_MERLIN.md` (G10 GO/NO-GO) le passage v1.0 → v1.1 avant merge
- [ ] Re-baseliner 5 notes du pilote v1.0 sous v1.1 pour validation visuelle (1 semaine après déploiement)

---

## Entrée registre associée

> DEC-044 | 2026-05-08 | qualite-ia | Schéma session_note v1.1 — frontière faits/hypotheses/recommandations explicite | validated | ADR-0005

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-08 | fondateur | Création initiale (QIA-007 backlog) |
