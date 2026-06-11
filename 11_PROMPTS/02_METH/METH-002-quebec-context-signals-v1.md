---
titre: Prompt de reference — signaux contextuels Quebec
id: MERLIN-PROMPT-FOND-QUEBEC_CONTEXT_SIGNALS-V1
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
test_associe: test_json_schema_validation.py::test_meth002_schema_structure
impact_attendu: "À documenter lors de la prochaine modification"
remplace: []
arbitrage_requis: oui — tout ajout ou retrait de signal contextuel
validation_requise: fondateur
données_sensibles: non
---

# MERLIN — Signaux contextuels Québec V1

## 1. Contexte et usage

Données de référence injectées dans le prompt système METH-003 (note de séance Cercle V1).
Représentent 12 signaux d'entretien québécois à détecter dans les transcriptions.
Ces signaux alimentent `supervision.detected_context_signals` et ne sont jamais inclus dans `client_delivery`.
Chargés dynamiquement via `app/ai/prompt_loader.py` avec l'identifiant `METH-002`.

## 2. Persona / Rôle

Document de données de référence — pas de persona. Ce fichier est lu et injecté par le loader dans METH-003 ; il n'est pas exécuté directement comme prompt système.

## 3. Instructions

Règle d'usage dans METH-003 : ces signaux sont détectés si présents dans la transcription et reportés uniquement dans `supervision.detected_context_signals`. Ils ne déclenchent pas d'hypothèse automatique — l'analyste les évalue comme indices contextuels, pas comme diagnostics.

## 4. Contraintes absolues

- Ne jamais inclure ces signaux dans `client_delivery`. Surface supervision uniquement.
- Ne jamais interpréter un signal comme une vérité clinique — c'est un indice d'entretien.
- Ne jamais utiliser ces signaux pour remplacer l'analyse individuelle du Cercle.
- Si aucun signal n'est présent dans la transcription, ne pas forcer leur détection.

## 5. Format de sortie

Liste de couples `[clé]: [expressions types]`. Injectée telle quelle dans METH-003 ; les signaux détectés sont rapportés comme liste dans `supervision.detected_context_signals`.

## 6. Entrée attendue

Transcription ou résumé de séance — passé via METH-003. Ce fichier n'est pas appelé directement par les routes API.

## 7. Données de référence

**Source d'autorité unique** : référentiel vivant `00_DOCTRINE/referentiels/signaux_contextuels.v1.yaml`
(12 signaux d'entretien), chargé à l'exécution par `app/referentiels/registry.py` et rendu au
format du §5 par `app/ai/prompts/session_note_cercle_v1.py` (`QUEBEC_CONTEXT_SIGNALS`).

Ce fichier ne duplique plus la liste : tout ajout ou retrait de signal se fait dans le
référentiel YAML (arbitrage fondateur requis, voir frontmatter), jamais ici.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 3 Phase A, externalisation depuis `session_note_cercle_v1.py` |
| 1.1 | 2026-06-10 | fondateur + Claude Code | §7 délégué au référentiel vivant `signaux_contextuels.v1.yaml` — fin de la duplication (redéploiement modulaire) |
