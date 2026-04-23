# MERLIN - Spec donnees V1 IVIA / MERLIN

Date: 2026-04-21
Statut: draft
Objet: definir les objets, champs, relations, statuts et contraintes applicatives du noyau V1

---

## 1) Role de cette spec

Cette spec est le contrat entre:
- la gouvernance;
- la BDD;
- l'API;
- l'interface;
- la couche IA;
- l'audit.

Elle couvre le noyau V1:
- adulte;
- non urgent;
- entree client;
- seance;
- note structuree;
- historique court;
- orientation simple;
- transcription optionnelle;
- documents derives.

Elle ne couvre pas encore en detail:
- mineurs / parents;
- multi-praticiens complexe;
- biometrie vocale;
- diagnostic reserve;
- portail pro avance;
- couche R&D theorique profonde.

---

## 2) Principes de modelisation

### Principe 1 - Faits, sources, derives et restitutions separes

On distingue:
- l'identite;
- la demande;
- la seance;
- la source brute;
- le derive;
- la restitution;
- l'audit.

### Principe 2 - Tout objet critique est versionnable et traçable

Tout objet critique doit pouvoir porter:
- un identifiant stable;
- un statut;
- un auteur;
- une date de creation;
- une date de mise a jour;
- un niveau de sensibilite;
- une classe de retention.

### Principe 3 - La production n'est pas la R&D

La spec distingue 3 couches de travail:
- `production`
- `supervision`
- `research`

La couche `research` ne doit jamais devenir visible en production par simple accident de schema.

---

## 3) Classes transversales obligatoires

Les objets critiques devront reutiliser, quand applicable, les classes suivantes.

### A. `record_status`

Valeurs recommandees:
- `draft`
- `active`
- `validated`
- `closed`
- `deprecated`
- `archived`

### B. `data_sensitivity_class`

Valeurs recommandees:
- `low`
- `moderate`
- `high`
- `restricted`

### C. `retention_class`

Valeurs recommandees:
- `ephemeral`
- `short_term`
- `standard`
- `extended`
- `archival`

### D. `human_validation_status`

Valeurs recommandees:
- `not_required`
- `pending`
- `validated`
- `rejected`
- `superseded`

### E. `workspace_scope`

Valeurs recommandees:
- `production`
- `supervision`
- `research`

### F. `source_type`

Valeurs recommandees:
- `human_input`
- `audio_source`
- `transcript_source`
- `derived_by_rule`
- `derived_by_ai`
- `manual_summary`
- `system_event`

---

## 4) Objets coeur V1

## 4.1 `client`

Role:
- identite minimale de la personne prise en charge ou suivie.

Champs minimum:
- `id`
- `public_client_code`
- `first_name_or_alias`
- `last_name` nullable
- `email` nullable
- `phone` nullable
- `language_code`
- `timezone`
- `territory_code`
- `is_adult_confirmed`
- `created_at`
- `updated_at`
- `record_status`
- `data_sensitivity_class`

Contraintes:
- pas de creation de seance sans `client`
- `is_adult_confirmed = true` requis pour V1 standard

Notes:
- `public_client_code` peut servir a l'affichage ou a la reference humaine sans exposer l'ID interne.

## 4.2 `intake_request`

Role:
- enregistrer la demande initiale et la qualification d'entree.

Champs minimum:
- `id`
- `client_id`
- `request_channel_code`
- `request_for_code` (`self`, `relative`, `other`)
- `primary_need_code`
- `perceived_urgency_code`
- `support_already_in_place` boolean
- `requested_outcome_text` nullable
- `entry_summary_text` nullable
- `created_at`
- `updated_at`
- `record_status`
- `referential_version`

Contraintes:
- une `intake_request` doit preceder la premiere `session`, sauf creation interne documentee

## 4.3 `consent`

Role:
- enregistrer chaque consentement distinct.

Champs minimum:
- `id`
- `client_id`
- `session_id` nullable
- `consent_type_code`
- `consent_value` boolean
- `consent_version_code`
- `granted_by_actor_code`
- `granted_at`
- `revoked_at` nullable
- `revocation_scope_code` nullable
- `notes` nullable
- `record_status`

Types minimum V1:
- `consent_session`
- `consent_session_note`
- `consent_history`
- `consent_recording`
- `consent_transcription`
- `consent_client_delivery`
- `consent_third_party_transmission`

Contraintes:
- pas de `audio_source` sans `consent_recording = true`
- pas de `transcript_source` sans `consent_transcription = true`
- pas de `third_party_transmission` sans consentement compatible ou base imperative documentee

## 4.4 `session`

Role:
- objet central d'une interaction tenue.

Champs minimum:
- `id`
- `client_id`
- `intake_request_id` nullable
- `session_sequence_number`
- `session_mode_code`
- `session_channel_code`
- `scheduled_start_at` nullable
- `actual_start_at` nullable
- `actual_end_at` nullable
- `duration_minutes` nullable
- `operator_user_id`
- `session_status_code`
- `record_status`
- `data_sensitivity_class`
- `retention_class`
- `created_at`
- `updated_at`

Valeurs de `session_status_code` recommandees:
- `scheduled`
- `in_progress`
- `completed`
- `cancelled`
- `no_show`
- `escalated`

## 4.5 `session_note`

Role:
- note structuree principale de la seance.

Champs minimum:
- `id`
- `session_id`
- `client_id`
- `note_template_version`
- `presenting_need_text`
- `key_elements_text`
- `vigilance_summary_text`
- `next_step_summary_text`
- `operator_summary_text`
- `human_validation_status`
- `created_by_user_id`
- `created_at`
- `updated_at`
- `record_status`
- `retention_class`

Contraintes:
- une `session_note` est obligatoire pour une `session.completed` en V1 standard

## 4.6 `audio_source`

Role:
- tracer l'existence et le regime d'un fichier audio, qu'il reste en hot storage ou archive froide.

Champs minimum:
- `id`
- `client_id`
- `session_id`
- `storage_provider_code`
- `storage_class_code` (`hot`, `cold`, `offline_archive`)
- `storage_object_path`
- `file_format_code`
- `file_size_bytes`
- `checksum_sha256`
- `recorded_at`
- `uploaded_at`
- `archived_at` nullable
- `deleted_at` nullable
- `retention_until` nullable
- `consent_snapshot_id`
- `record_status`
- `data_sensitivity_class`
- `retention_class`

Contraintes:
- `data_sensitivity_class` doit etre `restricted`
- si `deleted_at` non null, le chemin ne doit plus etre considere disponible en production

Notes:
- le nom de fichier ne doit pas contenir le nom civil du client
- la BDD garde le lien meme si le fichier sort du stockage actif

## 4.7 `transcript_source`

Role:
- transcription complete source d'une seance.

Champs minimum:
- `id`
- `client_id`
- `session_id`
- `audio_source_id` nullable
- `transcription_provider_code`
- `transcript_text`
- `language_code`
- `quality_score` nullable
- `generation_started_at`
- `generation_completed_at`
- `human_validation_status`
- `record_status`
- `data_sensitivity_class`
- `retention_class`
- `source_type`

Contraintes:
- `source_type = transcript_source`
- acces restreint par defaut

## 4.8 `derived_fact`

Role:
- stocker un fait derive de la seance ou du transcript, sans le confondre avec une conclusion.

Champs minimum:
- `id`
- `client_id`
- `session_id`
- `source_origin_code`
- `fact_type_code`
- `fact_text`
- `fact_json` nullable
- `confidence_score` nullable
- `human_validation_status`
- `generated_by_code`
- `prompt_or_rule_version` nullable
- `created_at`
- `record_status`
- `workspace_scope`

Valeurs de `fact_type_code` possibles en V1:
- `reported_need`
- `reported_attempt`
- `reported_blocker`
- `reported_resource`
- `red_flag_signal`
- `theme`

Contraintes:
- pas de `diagnosis` ou equivalent en V1

## 4.9 `risk_assessment`

Role:
- qualifier le niveau de vigilance et sa base.

Champs minimum:
- `id`
- `client_id`
- `session_id`
- `risk_level_code`
- `risk_reason_summary_text`
- `confidence_level_code`
- `requires_escalation` boolean
- `human_validation_status`
- `validated_by_user_id` nullable
- `created_at`
- `record_status`
- `workspace_scope`

Valeurs minimum de `risk_level_code`:
- `non_urgent`
- `watch`
- `priority`
- `urgent`

Contraintes:
- tout `urgent` doit laisser une trace minimale d'escalade ou de justification

## 4.10 `orientation`

Role:
- enregistrer une orientation ou suggestion de prochaine etape.

Champs minimum:
- `id`
- `client_id`
- `session_id`
- `orientation_target_code`
- `orientation_reason_text`
- `orientation_confidence_code`
- `orientation_priority_code`
- `human_validation_status`
- `validated_by_user_id` nullable
- `created_at`
- `record_status`

Valeurs minimum de `orientation_confidence_code`:
- `exploratory`
- `recommended`
- `priority`
- `urgent_escalation`

## 4.11 `document_derived`

Role:
- document remis ou generé a partir des objets de seance.

Champs minimum:
- `id`
- `client_id`
- `session_id` nullable
- `document_type_code`
- `document_title`
- `document_body_text` or `document_payload_json`
- `generation_mode_code`
- `generated_from_scope_code`
- `human_validation_status`
- `delivered_to_client` boolean
- `delivered_at` nullable
- `record_status`
- `retention_class`
- `created_at`

Champ recommande a ajouter ensuite:
- `client_delivery_status_code` nullable

Types minimum V1:
- `entry_summary`
- `session_summary`
- `care_journal_entry`
- `relay_note`

Logique de diffusion recommandee:
- `internal_only`
- `prepared_for_client`
- `validated_for_client`
- `delivered_to_client`

## 4.12 `third_party_transmission`

Role:
- tracer toute transmission a un tiers.

Champs minimum:
- `id`
- `client_id`
- `session_id` nullable
- `document_derived_id`
- `recipient_type_code`
- `recipient_name_text`
- `transmission_basis_code`
- `transmission_reason_text`
- `transmitted_at`
- `transmitted_by_user_id`
- `record_status`

Contraintes:
- pas de transmission sans document derive ou objet proportionne trace

## 4.13 `client_timeline_event`

Role:
- objet simple de continuité, relisant le parcours sans recalcul lourd.

Champs minimum:
- `id`
- `client_id`
- `related_session_id` nullable
- `event_type_code`
- `event_summary_text`
- `event_date`
- `created_at`
- `record_status`

Types possibles:
- `intake_created`
- `session_completed`
- `orientation_added`
- `document_delivered`
- `transmission_done`

## 4.14 `referential_version`

Role:
- version de referentiel utilisee au moment d'un traitement.

Champs minimum:
- `id`
- `referential_family_code`
- `version_code`
- `effective_from`
- `effective_to` nullable
- `compatibility_notes` nullable
- `record_status`

## 4.15 `audit_event`

Role:
- journaliser actions critiques, traitements IA et acces sensibles.

Champs minimum:
- `id`
- `actor_type_code`
- `actor_user_id` nullable
- `target_object_type_code`
- `target_object_id`
- `action_code`
- `reason_text` nullable
- `metadata_json` nullable
- `created_at`
- `record_status`

Actions minimum:
- `create`
- `update`
- `validate`
- `reject`
- `deliver`
- `transmit`
- `archive`
- `delete_logical`
- `view_restricted`
- `generate_ai_output`

---

## 5) Relations principales

- `client 1 -> n intake_request`
- `client 1 -> n consent`
- `client 1 -> n session`
- `session 1 -> 1 session_note` minimum en V1 standard
- `session 1 -> 0..n audio_source`
- `session 1 -> 0..n transcript_source`
- `session 1 -> 0..n derived_fact`
- `session 1 -> 0..n risk_assessment`
- `session 1 -> 0..n orientation`
- `session 1 -> 0..n document_derived`
- `document_derived 1 -> 0..n third_party_transmission`
- `client 1 -> n client_timeline_event`

---

## 6) Separation production / supervision / research

Cette separation doit etre explicite dans le schema.

### Production

Objets admissibles:
- `client`
- `intake_request`
- `consent`
- `session`
- `session_note`
- `audio_source`
- `transcript_source`
- `derived_fact`
- `risk_assessment`
- `orientation`
- `document_derived`
- `third_party_transmission`

Regle:
- seuls les objets production peuvent alimenter directement le dossier actif et les sorties client.

### Supervision

Objets admissibles:
- evaluation de qualite;
- relecture des sorties IA;
- commentaires de supervision;
- validations ou rejections.

Regle:
- les objets de supervision peuvent commenter ou valider la production, mais pas muter silencieusement les faits passes.

### Research

Objets admissibles:
- hypotheses riches;
- tests de prompts;
- grilles experimentales;
- analyses non autorisees en production.

Regle:
- jamais de diffusion automatique;
- jamais de confusion avec le dossier de production;
- idealement sur corpus pseudonymise, anonymise ou synthetique selon le cas.

---

## 7) Contraintes applicatives critiques

### C-01

Pas de `session.completed` sans:
- consentement seance compatible;
- note structuree;
- trace minimale operateur.

### C-02

Pas de `audio_source` sans consentement enregistrement compatible.

### C-03

Pas de `transcript_source` sans consentement transcription compatible.

### C-04

Pas de `third_party_transmission` sans:
- base de transmission;
- objet transmis;
- trace auteur;
- date.

### C-05

Pas de sortie IA critique visible au client ou utilisee operatoirement sans statut de validation si le type le requiert.

### C-06

Les logs applicatifs ne doivent pas contenir le verbatim complet par defaut.

### C-07

Les objets `research` ne doivent pas remonter dans l'UI production sans filtre explicite.

---

## 8) Referentiels minimum a fermer apres cette spec

Cette spec suppose l'existence rapide des referentiels suivants:

- `need_codes`
- `risk_level_codes`
- `orientation_target_codes`
- `consent_type_codes`
- `session_status_codes`
- `document_type_codes`
- `retention_classes`
- `data_sensitivity_classes`
- `workspace_scope_codes`

Sans eux, l'API et l'UI resteront trop textuelles.

---

## 9) Indexation et performance

Indexes minimum recommandes:
- `client(public_client_code)`
- `session(client_id, actual_start_at desc)`
- `consent(client_id, consent_type_code, granted_at desc)`
- `audio_source(session_id)`
- `transcript_source(session_id)`
- `document_derived(client_id, created_at desc)`
- `audit_event(target_object_type_code, target_object_id, created_at desc)`

Principe:
- les recherches courantes doivent porter sur identifiants, sessions, consentements et documents;
- les textes longs ne doivent pas etre le seul moyen de retrouver l'information.

---

## 10) Strategie d'implementation par ordre

Ordre recommande de build BDD / API:

1. `client`
2. `intake_request`
3. `consent`
4. `session`
5. `session_note`
6. `document_derived`
7. `client_timeline_event`
8. `audio_source`
9. `transcript_source`
10. `derived_fact`
11. `risk_assessment`
12. `orientation`
13. `third_party_transmission`
14. `audit_event`
15. `referential_version`

Logique:
- faire exister le service sans attendre toute la sophistication IA;
- brancher l'IA ensuite sur des objets deja stables.

---

## 11) Ce que cette spec ferme

Cette spec ferme:
- les objets coeur du noyau V1;
- la separation source / derive / restitution;
- la place de l'audio et de la transcription;
- la separation production / supervision / research;
- les champs transversaux indispensables;
- les contraintes applicatives minimum.

Cette spec n'enterre pas l'evolution.
Elle la rend construisible sans casser la base.

---

## 12) Decision active

IVIA / MERLIN adopte ce schema logique V1 comme base de travail pour:
- la spec ecrans V1;
- le choix de stack;
- le modele BDD initial;
- les routes API initiales;
- la pipeline IA gouvernee.

Prochaine etape recommandee:
- rediger la `spec ecrans V1 du parcours client`.

References:
- [MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md)
- [MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md)
- [MERLIN_GOUV_CADRAGE_ANALYSE_IA_TEMPS_REEL_ORIENTATION_PRUDENTE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CADRAGE_ANALYSE_IA_TEMPS_REEL_ORIENTATION_PRUDENTE_v1.0.md)
- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)
- [MERLIN_GOUV_SPEC_WORKFLOW_DIFFUSION_CLIENT_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_WORKFLOW_DIFFUSION_CLIENT_V1.md)
