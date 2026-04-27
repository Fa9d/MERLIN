# MERLIN - Tableau donnees MESANGE sources dossiers claims budgets V1

Date: 2026-04-25
Statut: draft
Objet: fixer les objets de donnees canoniques de MESANGE pour la gestion des sources, des sujets, des dossiers, des affirmations, des analyses, des budgets, des couts et des revenus

---

## 1) Principe directeur

MESANGE ne doit pas seulement stocker de l'information.

Il doit permettre de suivre:

1. `ce qui entre`
2. `ce qui est retenu`
3. `ce qui est analyse`
4. `ce qui est classe en dossier`
5. `ce qui est verifie`
6. `ce qui est publie`
7. `ce qui coute`
8. `ce qui rapporte`
9. `ce qui est resolu`

Doctrine:

`Tout sujet suivi dans MESANGE doit pouvoir etre rattache a une source, a un dossier, a une chronologie, a un statut de verification et a une trace economique.`

---

## 2) Les 6 couches de donnees

MESANGE doit distinguer au minimum:

1. `sources`
2. `contenus ingeres`
3. `objets analytiques`
4. `dossiers et suivi`
5. `livrables et diffusion`
6. `pilotage economique`

Cette separation est centrale.

Elle evite de melanger:

- la matiere brute;
- les interpretations;
- les claims;
- les decisions editoriales;
- les calculs economiques.

---

## 3) Classes transversales recommandees

### A. `record_status`

Valeurs recommandees:

- `draft`
- `active`
- `validated`
- `closed`
- `deprecated`
- `archived`

### B. `review_status`

Valeurs recommandees:

- `not_reviewed`
- `in_review`
- `validated`
- `rejected`
- `superseded`

### C. `dossier_status`

Valeurs recommandees:

- `a_trier`
- `ouvert`
- `en_analyse`
- `a_valider`
- `en_action`
- `en_surveillance`
- `resolu`
- `archive`
- `reouvert`

### D. `claim_verification_status`

Valeurs recommandees:

- `non_verifie`
- `partiellement_etabli`
- `etabli`
- `trompeur`
- `contredit_par_les_faits`
- `non_documente`
- `obsolete`
- `en_attente_de_reponse`

### E. `source_status`

Valeurs recommandees:

- `active`
- `paused`
- `deprecated`
- `blocked`

### F. `priority_level`

Valeurs recommandees:

- `low`
- `normal`
- `high`
- `critical`

### G. `economic_value_type`

Valeurs recommandees:

- `revenu_direct`
- `valeur_strategique`
- `mixte`
- `non_rentabilise`

---

## 4) Tableau principal des objets

| Objet | Role | Cree par | Relation cle | Statuts critiques | Decision active |
|---|---|---|---|---|---|
| `source` | decrire une source suivie | admin / analyste | produit plusieurs `source_item` | `source_status`, `record_status` | requis |
| `source_item` | representer une unite ingeree | systeme / import / manuel | appartient a `source` | `record_status`, `review_status` | requis |
| `document` | version normalisee exploitable d'un contenu | systeme / analyste | derive de `source_item` | `record_status` | requis |
| `analysis_run` | tracer une execution analytique | systeme / analyste | porte sur `document` ou `dossier` | `record_status` | requis |
| `concept` | definir un theme, signal, categorie ou principe | admin / gouvernance | relie a `claim`, `signal`, `dossier` | `record_status` | requis |
| `claim` | isoler une affirmation verifiable | systeme / analyste | issue d'un `document` | `claim_verification_status`, `review_status` | coeur MESANGE |
| `evidence` | rattacher une piece probante ou contradictoire | analyste | rattachee a `claim` | `review_status`, `record_status` | requis |
| `signal` | noter un indicateur analytique utile | systeme / analyste | issu d'un `analysis_run` | `review_status`, `record_status` | utile |
| `topic` | regrouper un enjeu general | admin / analyste | contient plusieurs `dossier` | `record_status` | requis |
| `dossier` | suivre un sujet de bout en bout | analyste / systeme | relie sources, claims, livrables, couts | `dossier_status`, `priority_level` | coeur MESANGE |
| `dossier_event` | historiser la vie du dossier | systeme / analyste | appartient a `dossier` | `record_status` | requis |
| `actor` | representer une personne, institution ou mouvement | systeme / analyste | lie a `claim`, `dossier`, `position` | `record_status` | requis |
| `position` | decrire une position publique d'acteur | analyste | appartient a `actor` et `topic` | `review_status` | utile |
| `report` | produire un livrable ou une chronique | analyste / systeme | derive de `dossier` ou `topic` | `review_status`, `record_status` | requis |
| `budget` | fixer une enveloppe de pilotage | admin | relie a axe, sujet ou dossier | `record_status` | requis |
| `cost_entry` | journaliser un cout | systeme / admin / analyste | rattache a `dossier`, `topic`, `report` | `record_status` | requis |
| `revenue_entry` | journaliser un revenu ou soutien | admin | rattache a axe, client, dossier ou report | `record_status` | requis |
| `value_assessment` | qualifier la valeur economique ou strategique | analyste / admin | rattache a `dossier` ou `topic` | `review_status` | recommande |

---

## 5) Detail par objet

## 5.1 `source`

Role:

- declarer une source exploitable.

Champs minimum:

- `id`
- `name`
- `source_type_code`
- `source_url`
- `owner_user_id`
- `source_status`
- `default_priority_level`
- `trust_level_code`
- `refresh_frequency_code`
- `cost_profile_code`
- `created_at`
- `updated_at`
- `record_status`

Exemples de `source_type_code`:

- `rss`
- `website`
- `pdf`
- `social_account`
- `manual_import`
- `newsletter`
- `video`
- `audio`
- `internal_note`

## 5.2 `source_item`

Role:

- tracer chaque unite ingeree.

Champs minimum:

- `id`
- `source_id`
- `external_reference`
- `published_at`
- `captured_at`
- `title`
- `raw_text_excerpt`
- `language_code`
- `item_hash`
- `ingestion_status_code`
- `review_status`
- `record_status`

Contraintes:

- un `source_item` peut etre ignore, classe, rattache ou rejete;
- il ne doit pas etre confondu avec un dossier.

## 5.3 `document`

Role:

- produire une version normalisee, exploitable et versionnee.

Champs minimum:

- `id`
- `source_item_id`
- `document_type_code`
- `normalized_text`
- `summary_text`
- `document_version`
- `processing_notes`
- `record_status`
- `created_at`
- `updated_at`

## 5.4 `concept`

Role:

- structurer la grille d'analyse.

Champs minimum:

- `id`
- `concept_code`
- `label`
- `concept_family_code`
- `definition_text`
- `is_active`
- `version_code`
- `record_status`

Exemples de `concept_family_code`:

- `enjeu`
- `signal`
- `technique_discursive`
- `sophisme`
- `principe_mesange`
- `type_de_resolution`
- `categorie_budgetaire`

## 5.5 `claim`

Role:

- isoler une affirmation verifiable.

Champs minimum:

- `id`
- `document_id`
- `actor_id` nullable
- `claim_text`
- `claim_short_label`
- `claim_type_code`
- `claim_verification_status`
- `confidence_level_code`
- `verification_notes`
- `first_seen_at`
- `last_reviewed_at`
- `review_status`
- `record_status`

Exemples de `claim_type_code`:

- `factuel`
- `promesse`
- `causal`
- `chiffre`
- `interpretatif`
- `normatif`

## 5.6 `evidence`

Role:

- rattacher une piece probante, contradictoire ou incomplete.

Champs minimum:

- `id`
- `claim_id`
- `evidence_type_code`
- `source_item_id` nullable
- `document_id` nullable
- `evidence_summary_text`
- `supports_claim` boolean nullable
- `strength_level_code`
- `review_status`
- `record_status`

Exemples de `evidence_type_code`:

- `source_primaire`
- `source_secondaire`
- `document_officiel`
- `donnee_statistique`
- `citation`
- `contradiction`
- `absence_de_preuve`

## 5.7 `signal`

Role:

- stocker un signal analytique utile mais non encore transforme en claim ou decision.

Champs minimum:

- `id`
- `analysis_run_id`
- `signal_code`
- `signal_family_code`
- `signal_text`
- `severity_level_code`
- `review_status`
- `record_status`

## 5.8 `topic`

Role:

- regrouper un enjeu ou domaine de suivi.

Champs minimum:

- `id`
- `topic_code`
- `label`
- `description_text`
- `topic_family_code`
- `owner_user_id`
- `record_status`

## 5.9 `dossier`

Role:

- suivre un sujet du signal initial jusqu'a la resolution.

Champs minimum:

- `id`
- `topic_id`
- `dossier_code`
- `title`
- `summary_current_text`
- `dossier_status`
- `priority_level`
- `owner_user_id`
- `opened_at`
- `last_activity_at`
- `resolution_due_at` nullable
- `resolution_summary_text` nullable
- `record_status`

Champs fortement recommandes:

- `citizen_impact_text`
- `questions_open_text`
- `decision_log_summary`
- `economic_value_type`

## 5.10 `dossier_event`

Role:

- conserver la timeline du dossier.

Champs minimum:

- `id`
- `dossier_id`
- `event_type_code`
- `event_at`
- `actor_user_id`
- `event_text`
- `record_status`

Exemples de `event_type_code`:

- `opened`
- `claim_added`
- `status_changed`
- `report_published`
- `actor_contacted`
- `response_received`
- `resolution_recorded`
- `reopened`

## 5.11 `actor`

Role:

- representer un acteur public ou collectif.

Champs minimum:

- `id`
- `actor_type_code`
- `display_name`
- `organization_name` nullable
- `territory_code`
- `notes`
- `record_status`

Exemples de `actor_type_code`:

- `personne_publique`
- `media`
- `parti`
- `institution`
- `mouvement_citoyen`
- `organisme`

## 5.12 `position`

Role:

- decrire la position soutenue publiquement par un acteur sur un sujet.

Champs minimum:

- `id`
- `actor_id`
- `topic_id`
- `position_text`
- `position_date`
- `source_item_id`
- `review_status`
- `record_status`

## 5.13 `report`

Role:

- produire une restitution diffusable.

Champs minimum:

- `id`
- `report_type_code`
- `topic_id` nullable
- `dossier_id` nullable
- `title`
- `summary_text`
- `body_text`
- `audience_code`
- `publication_status_code`
- `published_at` nullable
- `review_status`
- `record_status`

Exemples de `report_type_code`:

- `briefing`
- `fiche_verification`
- `chronologie`
- `chronique`
- `note_strategique`
- `synthese_executive`

## 5.14 `budget`

Role:

- definir une enveloppe financiere.

Champs minimum:

- `id`
- `budget_scope_code`
- `label`
- `period_start`
- `period_end`
- `budget_amount`
- `warning_threshold_amount`
- `hard_limit_amount` nullable
- `owner_user_id`
- `record_status`

Exemples de `budget_scope_code`:

- `global`
- `axe`
- `topic`
- `dossier`
- `outil`

## 5.15 `cost_entry`

Role:

- tracer un cout reel.

Champs minimum:

- `id`
- `cost_type_code`
- `cost_date`
- `topic_id` nullable
- `dossier_id` nullable
- `report_id` nullable
- `tool_name` nullable
- `quantity`
- `unit_code`
- `unit_cost`
- `total_cost`
- `budget_id` nullable
- `notes`
- `record_status`

Exemples de `cost_type_code`:

- `outil_llm`
- `outil_transcription`
- `outil_recherche`
- `temps_tri`
- `temps_verification`
- `temps_redaction`
- `temps_validation`
- `cout_diffusion`
- `cout_fixe_reparti`
- `cout_reprise`

## 5.16 `revenue_entry`

Role:

- tracer un revenu ou financement associe.

Champs minimum:

- `id`
- `revenue_type_code`
- `revenue_date`
- `client_name` nullable
- `topic_id` nullable
- `dossier_id` nullable
- `report_id` nullable
- `amount`
- `notes`
- `record_status`

Exemples de `revenue_type_code`:

- `abonnement`
- `mandat`
- `sponsorship`
- `subvention`
- `formation`
- `vente_note`
- `licence`

## 5.17 `value_assessment`

Role:

- rendre explicite la valeur non purement comptable.

Champs minimum:

- `id`
- `topic_id` nullable
- `dossier_id` nullable
- `value_type_code`
- `assessment_text`
- `reviewed_at`
- `review_status`
- `record_status`

Exemples de `value_type_code`:

- `revenu_direct`
- `acquisition_audience`
- `credibilite`
- `corpus_strategique`
- `ouverture_mandat`
- `service_public`

---

## 6) Relations critiques

### Relation A

Une `source` produit plusieurs `source_item`.

### Relation B

Un `source_item` peut produire un `document`, puis plusieurs `claim`.

### Relation C

Une `claim` peut recevoir plusieurs `evidence`.

### Relation D

Un `dossier` peut agreger:

- plusieurs `source_item`
- plusieurs `document`
- plusieurs `claim`
- plusieurs `actor`
- plusieurs `report`
- plusieurs `cost_entry`

### Relation E

Un `topic` peut contenir plusieurs `dossier`.

### Relation F

Un `budget` peut couvrir:

- un axe global;
- un `topic`;
- un `dossier`;
- un outil.

---

## 7) Regles d'usage

### Regle 1 - Un item n'est pas un dossier

Une information entrante ne devient pas automatiquement un sujet a suivre.

### Regle 2 - Une analyse n'est pas une preuve

Les sorties LLM, classifications et suggestions doivent rester distinctes des `evidence`.

### Regle 3 - Une affirmation doit etre verifiable ou classee comme non verifiable

On n'entretient pas de pseudo-faits flous sans statut.

### Regle 4 - Un dossier doit avoir un statut et une chronologie

Sans cela, il redevient un simple tas de documents.

### Regle 5 - Chaque dossier lourd doit avoir une trace economique

Sinon MESANGE ne pourra pas arbitrer.

---

## 8) Etats cibles d'un dossier

Le cycle recommande est:

1. `a_trier`
2. `ouvert`
3. `en_analyse`
4. `a_valider`
5. `en_action`
6. `en_surveillance`
7. `resolu`
8. `archive`

Si de nouveaux faits apparaissent:

- `reouvert`

---

## 9) Etats cibles d'une affirmation

Le cycle recommande est:

1. `non_verifie`
2. `partiellement_etabli`
3. `etabli`
4. `trompeur`
5. `contredit_par_les_faits`
6. `non_documente`
7. `en_attente_de_reponse`
8. `obsolete`

Doctrine:

`Le statut d'une affirmation doit pouvoir changer dans le temps sans perdre l'historique precedent.`

---

## 10) Questions economiques minimales rattachees aux donnees

MESANGE doit pouvoir repondre a ces questions:

1. combien coute un dossier?
2. combien coute un sujet resolu?
3. quelles sources consomment sans produire de dossiers utiles?
4. quels livrables rapportent?
5. quels sujets ont une valeur strategique mais pas de revenu direct?
6. quel est le cout de verification d'une affirmation importante?

Si le schema ne permet pas ces reponses, il est incomplet.

---

## 11) MVP donnees recommande

Pour un demarrage realiste, je recommande de commencer par:

- `source`
- `source_item`
- `document`
- `concept`
- `claim`
- `evidence`
- `topic`
- `dossier`
- `dossier_event`
- `actor`
- `report`
- `budget`
- `cost_entry`
- `revenue_entry`

Peuvent attendre:

- `position`
- `value_assessment`
- systeme fin de versions complexes
- vues multi-clients avancees

---

## 12) Decision operative

MESANGE doit etre construit comme un systeme documentaire a memoire longue, pas comme une simple pipeline d'articles.

Le schema de donnees doit donc rendre possible:

- la reprise integrale d'un sujet;
- la verification des affirmations;
- le suivi des responsabilites;
- la production de chroniques;
- le calcul des couts et de la valeur.

---

## 13) Prochaine etape recommandee

Apres ce tableau, les deux documents les plus utiles sont:

1. une spec d'ecrans admin MESANGE
2. un workflow canonique `source -> claim -> dossier -> publication -> resolution`

