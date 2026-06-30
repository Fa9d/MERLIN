# MERLIN - Schema analyse assistee de seance (v1)

Date: 2026-04-20
Statut: draft
Type: schema

---

## Finalite

Ce schema sert a stocker la couche d'analyse assistee issue d'une seance MERLIN.

Il ne sert pas a:
- poser un diagnostic;
- decrire la personne dans son entier;
- stocker une theorie speculative comme verite.

---

## Principe

Chaque objet `analyse_assistee_seance` doit distinguer:
- les faits issus de la seance;
- les suggestions de l'IA;
- la validation humaine;
- l'incertitude;
- la version des referentiels utilises.

---

## Champs recommandes

- `analysis_id`
- `client_id`
- `session_id`
- `created_at`
- `source_mode`
- `consent_transcription`
- `consent_analyse_assistee`
- `transcript_exists`
- `summary_exists`
- `faits_principaux`
- `maux_exprimes`
- `besoins_exprimes`
- `actions_deja_tentees`
- `ressources_disponibles`
- `blocages_exprimes`
- `drapeaux_rouges_detectes`
- `dimension_active_principale`
- `dimension_secondaire`
- `besoin_dominant`
- `blocage_principal`
- `niveau_risque_suggere`
- `niveau_risque_valide`
- `orientation_suggeree`
- `orientation_validee`
- `prochaine_action_suggeree`
- `prochaine_action_validee`
- `delta_depuis_derniere_seance`
- `incertitudes`
- `ai_confidence`
- `human_review_status`
- `reviewed_by`
- `reviewed_at`
- `referentiel_orientation_version`
- `referentiel_triage_version`
- `schema_version`
- `notes_revision`

---

## Valeurs conseillees

### `source_mode`

- `note_only`
- `transcript_post_session`
- `temps_reel`

### `dimension_active_principale`

- `affectif_relationnel`
- `corporel_rythme`
- `mental_cognitif`
- `sens_identite`
- `contexte_social`
- `mixte`

### `besoin_dominant`

- `ecoute_structurante`
- `stabilisation`
- `clarification`
- `soutien_communautaire`
- `orientation_professionnelle`
- `orientation_medicale`
- `orientation_psychosociale`
- `repos_rythme`
- `a_verifier`

### `niveau_risque_suggere`

- `non_urgent`
- `vigilance`
- `subaigu`
- `urgence_sociale`
- `urgent`
- `critique`

### `human_review_status`

- `non_revu`
- `revu_sans_modification`
- `revu_avec_correction`
- `escalade`
- `rejete`

### `ai_confidence`

- `faible`
- `moyenne`
- `elevee`

---

## Champs interdits en V1

Les champs suivants ne doivent pas etre crees dans ce schema:

- `diagnostic_probable`
- `trouble_probable`
- `score_leary`
- `niveau_evolutif_client`
- `loi_du_vivant_violee`
- `indice_transgenerationnel`
- `indice_spirituel`
- `verite_profonde_client`

---

## Regles critiques

### Regle 1 - Pas d'orientation critique sans validation

Si `niveau_risque_suggere` vaut `urgent` ou `critique`, alors:
- `human_review_status` ne peut pas rester `non_revu` si l'objet est utilise operatoirement;
- l'action finale doit etre tracee;
- la regle de triage applicable doit pouvoir etre reliee.

### Regle 2 - Les suggestions IA ne sont pas des faits

Tout element dans:
- `orientation_suggeree`
- `prochaine_action_suggeree`
- `niveau_risque_suggere`
- `delta_depuis_derniere_seance`

doit pouvoir etre corrige sans modifier les faits sources.

### Regle 3 - Consentement explicite

Si `transcript_exists` vaut `true`, alors:
- `consent_transcription` doit valoir `true`;
- `source_mode` ne peut pas etre `note_only`.

### Regle 4 - Versionnage obligatoire

Tout objet doit conserver:
- la version du schema;
- la version des referentiels critiques de triage et d'orientation.

---

## Exemple minimal

```yaml
analysis_id: ana_2026_04_20_001
client_id: cli_0001
session_id: ses_2026_04_20_001
created_at: 2026-04-20T15:30:00-04:00
source_mode: transcript_post_session
consent_transcription: true
consent_analyse_assistee: true
transcript_exists: true
summary_exists: true
faits_principaux:
  - fatigue persistante
  - conflit familial recurrent
  - sentiment de perte de controle
maux_exprimes:
  - anxiete
  - epuisement
besoins_exprimes:
  - etre ecoute
  - retrouver un cadre
actions_deja_tentees:
  - parler a un proche
  - reduction temporaire du travail
ressources_disponibles:
  - proche soutenant
blocages_exprimes:
  - peur de demander de l aide
drapeaux_rouges_detectes: []
dimension_active_principale: affectif_relationnel
dimension_secondaire: contexte_social
besoin_dominant: clarification
blocage_principal: difficulte a demander un soutien formel
niveau_risque_suggere: vigilance
niveau_risque_valide: vigilance
orientation_suggeree:
  - svc_ligne_ecoute
  - svc_travailleur_social_public_qc
orientation_validee:
  - svc_ligne_ecoute
prochaine_action_suggeree: verifier ressources de soutien et reprendre contact sous 7 jours
prochaine_action_validee: transmettre une synthese client et reevaluation sous 7 jours
delta_depuis_derniere_seance: aggravation moderee de la fatigue, meilleure capacite a nommer les besoins
incertitudes:
  - niveau exact d isolement
ai_confidence: moyenne
human_review_status: revu_avec_correction
reviewed_by: op_001
reviewed_at: 2026-04-20T15:45:00-04:00
referentiel_orientation_version: 1.0
referentiel_triage_version: 1.0
schema_version: 1.0
notes_revision: orientation medicale non retenue a ce stade, absence de drapeaux rouges critiques
```

---

## Usage recommande

Cet objet peut alimenter:
- la note de seance;
- l'historique client;
- le journal de parcours;
- les rapports d'evolution;
- les tableaux de bord praticiens.

Il ne doit pas etre remis tel quel au client sans transformation lisible.
