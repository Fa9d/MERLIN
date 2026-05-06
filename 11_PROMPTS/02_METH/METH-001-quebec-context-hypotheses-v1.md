---
titre: Prompt de reference — hypotheses contextuelles Quebec
id: MERLIN-PROMPT-FOND-QUEBEC_CONTEXT_HYPOTHESES-V1
statut: active
type: prompt
couche: FOND
périmètre: backend
auteur: fondateur
date: 2026-05-05
version: 1.0
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

- pression_silence_et_minimisation: minimisation repetee, consultation tardive, decalage ton/gravite -> hypothese prudente de retenue ou souffrance sous-declaree; dimension coeur/corps.
- pression_performance_travail: surmenage valorise, honte du repos, productivite comme valeur -> hypothese prudente de charge normalisee; dimension esprit/corps/etre.
- pression_isolement_relationnel: peu de reseau mobilisable, un seul filet relationnel, peur de deranger -> hypothese prudente d'isolement peu nomme; dimension coeur/etre.
- pression_honte_ambition_ou_reussite: gene a reussir, negocier, parler d'argent -> hypothese prudente de tension entre elan et permission; dimension etre/esprit.
- pression_identite_collective_fragile: hypersensibilite a la critique, fragilite de legitimite -> hypothese prudente de tension d'appartenance; dimension etre.
- pression_medicalisation_du_sens: recit colle au diagnostic, attente d'une solution externe -> hypothese prudente de langage de souffrance centre sur l'etiquette; dimension esprit/corps.
- pression_deconnexion_somatique: fatigue, douleurs, insomnie, regulation par evitement ou substances -> hypothese prudente de charge surtout portee par le corps; dimension corps.
- pression_vide_de_sens_ou_de_cadre: vide, perte de reperes, gene a parler de sens -> hypothese prudente de manque de cadre existentiel; dimension etre/esprit.
- pression_rapport_aux_institutions: mefiance, fatigue administrative, sentiment d'etre mal recu -> hypothese prudente de charge contextuelle institutionnelle; dimension esprit/etre.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 3 Phase A, externalisation depuis `session_note_cercle_v1.py` |
