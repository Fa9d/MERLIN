---
titre: Prompt de reference — hypotheses contextuelles Quebec
id: MERLIN-PROMPT-FOND-QUEBEC_CONTEXT_HYPOTHESES-V1
statut: active
type: prompt
couche: FOND
périmètre: backend
auteur: fondateur
date: 2026-05-05
version: 1.1
modèle_cible: claude-sonnet-4-20250514
dépend_de: [ADR-0002, ADR-0003]
utilisé_par: [app/ai/prompts/session_note_cercle_v1.py]
test_associe: test_prompt_injection.py::test_meth001_no_diagnosis
impact_attendu: "À documenter lors de la prochaine modification"
remplace: []
arbitrage_requis: oui — tout ajout ou retrait d'hypothese contextuelle
validation_requise: fondateur
données_sensibles: non
---

# MERLIN — Hypothèses contextuelles Québec V1

## 1. Contexte et usage

Données de référence injectées dans le prompt système METH-003 (note de séance Cercle V1).
Représentent 9 hypothèses de pression contextuelle québécoise observables dans les séances.
Ces hypothèses alimentent l'enrichissement contextuel optionnel, séparément de l'analyse individuelle du Cercle.
Chargées dynamiquement via `app/ai/prompt_loader.py` avec l'identifiant `METH-001`.

## 2. Persona / Rôle

Document de données de référence — pas de persona. Ce fichier est lu et injecté par le loader dans METH-003 ; il n'est pas exécuté directement comme prompt système.

## 3. Instructions

Règle d'usage dans METH-003 : ces hypothèses ne sont mobilisées que si des indices observables apparaissent dans la transcription. Elles forment une couche contextuelle distincte de l'analyse individuelle du Cercle et ne la remplacent jamais.

## 4. Contraintes absolues

- Ne jamais présenter une hypothèse contextuelle comme une vérité imposée — toujours comme hypothèse prudente.
- Ne jamais utiliser ces hypothèses dans `client_delivery`.
- Ne jamais remplacer l'analyse individuelle du Cercle par cette couche contextuelle.
- Ne jamais produire de thèse anti-médicalisation ni de référence aux Peuples Premiers sans cadre formel établi.
- Limiter à 0-3 hypothèses utiles par séance, distinctes des tensions du Cercle.

## 5. Format de sortie

Liste de couples `[clé]: [signaux observables] -> hypothèse prudente; dimension(s) Cercle`. Injectée telle quelle dans METH-003.

## 6. Entrée attendue

Transcription ou résumé de séance — passé via METH-003. Ce fichier n'est pas appelé directement par les routes API.

## 7. Données de référence

**Source d'autorité unique** : référentiel vivant `00_DOCTRINE/referentiels/pressions_societales.v1.yaml`
(9 hypothèses de pression), chargé à l'exécution par `app/referentiels/registry.py` et rendu au
format du §5 par `app/ai/prompts/session_note_cercle_v1.py` (`QUEBEC_CONTEXT_HYPOTHESES`).

Ce fichier ne duplique plus la liste : tout ajout, retrait ou reformulation d'hypothèse se fait
dans le référentiel YAML (arbitrage fondateur requis, voir frontmatter), jamais ici.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 3 Phase A, externalisation depuis `session_note_cercle_v1.py` |
| 1.1 | 2026-06-10 | fondateur + Claude Code | §7 délégué au référentiel vivant `pressions_societales.v1.yaml` — fin de la duplication (redéploiement modulaire) |
