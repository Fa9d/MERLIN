# MERLIN - Spec axes d'analyse Cercle V1

Date: 2026-04-22
Statut: actif
Objet: traduire le noyau doctrinal du Cercle en axes d'analyse utilisables par MERLIN

---

## 1) But

Ce document traduit la doctrine en spec operatoire.

Il sert a definir:

- quels axes MERLIN observe;
- comment ils sont renseignes;
- quelles derivees peuvent etre produites;
- ce qui peut aller en note interne;
- ce qui peut eventuellement etre rendu diffusable au client.

Cette spec ne cree pas un diagnostic.

Elle cree:

- une grille de lecture;
- une structure de note;
- une base de derivees documentaires.

---

## 2) Structure generale

MERLIN analysera une situation selon cinq blocs:

1. `dimensions`
2. `contexte`
3. `tensions`
4. `vigilance`
5. `prochaine_etape`

Les cinq blocs doivent rester:

- lisibles;
- justifiables;
- auditables;
- non opaques.

---

## 3) Bloc dimensions

Chaque session ou synthese peut contenir une lecture sur:

- `coeur`
- `corps`
- `esprit`
- `etre`

Pour chaque dimension, MERLIN doit pouvoir stocker:

- `etat_resume`
- `signaux_observes`
- `tensions_principales`
- `besoins_presumes`
- `citations_ou_indices`
- `niveau_de_confiance`

Format interne recommande:

- `etat_resume`: texte court
- `signaux_observes`: liste courte
- `tensions_principales`: liste courte
- `besoins_presumes`: liste courte
- `niveau_de_confiance`: `faible` / `moyen` / `eleve`

Important:

`besoins_presumes` signifie hypothese utile, pas verite psychologique.

---

## 4) Bloc contexte

Le contexte doit etre releve sur au moins six familles:

- `materiel`
- `travail_ou_charge`
- `logement_et_stabilite`
- `reseau_relationnel`
- `rapport_aux_institutions`
- `territoire_langue_culture`

Champs internes recommandes:

- `facteurs_de_soutien`
- `facteurs_de_fragilite`
- `contraintes_actives`
- `ressources_mobilisables`

MERLIN doit pouvoir distinguer:

- ce qui vient principalement du contexte;
- ce qui vient du fonctionnement relationnel;
- ce qui releve d'un frottement mixte.

---

## 5) Bloc tensions

Les tensions sont le coeur de la lecture.

Une tension est:

- un frottement recurrent;
- une contradiction vecue;
- un desequilibre de charge;
- un conflit entre besoin, contexte et possibilites.

Catalogue initial de tensions autorisees:

- `tension_rythme`
- `tension_reciprocite`
- `tension_appartenance`
- `tension_sens`
- `tension_dignite`
- `tension_charge_exigences`
- `tension_isolement`
- `tension_insecurite`
- `tension_confusion`
- `tension_desorientation`

Pour chaque tension:

- `code_tension`
- `description`
- `dimensions_impactees`
- `indices`
- `intensite_presumee`
- `niveau_de_confiance`
- `client_visible_par_defaut = false`

Valeurs recommande es pour `intensite_presumee`:

- `faible`
- `moderee`
- `marquee`

---

## 6) Bloc vigilance

La vigilance ne doit pas etre un score opaque.

MERLIN retient une logique simple:

- `non_urgent`
- `watch`
- `priority`
- `urgent`

Cette vigilance doit etre fondee sur:

- indices explicites;
- contexte;
- charge actuelle;
- capacite apparente de stabilisation;
- besoin possible de relais.

Regle:

`la vigilance ne vaut jamais diagnostic`

Sortie client:

- seulement version simple, utile et non alarmiste;
- jamais la logique profonde brute.

---

## 7) Bloc prochaine etape

Toute lecture utile doit produire une prochaine etape.

Types de prochaines etapes possibles:

- `continuer_a_parler_et_structurer`
- `clarifier_un_point_majeur`
- `stabiliser_rythme_et_charge`
- `mobiliser_une_ressource_relationnelle`
- `orienter_vers_un_service_approprie`
- `proposer_un_suivi`
- `escalader_vers_urgence_ou_relais_immediat`

Pour chaque prochaine etape:

- `type`
- `formulation_interne`
- `formulation_client_eventuelle`
- `raison_principale`
- `niveau_de_priorite`

---

## 8) Questions d'entretien guidees par axe

## A. `Coeur`

Questions types:

- avec qui cela pese-t-il le plus ?
- ou manque-t-il de soutien ou de reciprocite ?
- y a-t-il une relation qui prend toute la place ?

## B. `Corps`

Questions types:

- comment le corps tient-il ces jours-ci ?
- qu'en est-il du sommeil, de la fatigue, de la tension ?
- a quel moment sentez-vous que cela deborde physiquement ?

## C. `Esprit`

Questions types:

- qu'est-ce qui tourne le plus dans votre tete ?
- qu'est-ce qui reste flou ou contradictoire ?
- comment comprenez-vous ce qui vous arrive aujourd'hui ?

## D. `Etre`

Questions types:

- ou vous sentez-vous le plus perdu ou desancre ?
- qu'est-ce qui vous semble ne plus tenir ensemble ?
- de quoi auriez-vous besoin pour vous sentir plus aligne ou plus debout ?

## E. `Contexte`

Questions types:

- qu'est-ce qui, autour de vous, aggrave ou soulage la situation ?
- de quelles ressources disposez-vous reellement ?
- qu'est-ce qui vous manque le plus concretement en ce moment ?

Ces questions sont:

- des guides d'entretien;
- pas un questionnaire ferme obligatoire.

---

## 9) Objets derives a prevoir

Cette spec implique au moins cinq familles de derivees.

## A. `dimension_observation`

Objet portant une observation par dimension.

Champs recommandes:

- `session_id`
- `dimension_code`
- `summary_text`
- `observed_signals_json`
- `presumed_needs_json`
- `confidence_code`

## B. `context_factor`

Objet portant un facteur de contexte.

Champs recommandes:

- `client_id`
- `session_id`
- `factor_family_code`
- `factor_type_code`
- `impact_direction_code`
- `summary_text`

## C. `analysis_tension`

Objet portant une tension.

Champs recommandes:

- `client_id`
- `session_id`
- `tension_code`
- `intensity_code`
- `confidence_code`
- `supporting_evidence_text`
- `client_visible`

## D. `analysis_orientation`

Objet portant la prochaine etape ou l'orientation.

Champs recommandes:

- `client_id`
- `session_id`
- `orientation_type_code`
- `priority_code`
- `internal_rationale_text`
- `client_rationale_text`
- `client_visible`

## E. `analysis_snapshot`

Objet de synthese d'une session ou d'une periode.

Champs recommandes:

- `client_id`
- `session_id`
- `clarity_level_code`
- `vigilance_level_code`
- `dominant_dimensions_json`
- `dominant_tensions_json`
- `next_step_summary_text`

---

## 10) Regles de diffusion client

Peut devenir diffusable au client:

- une reformulation simple d'une tension;
- une prochaine etape concrete;
- une synthese courte et intelligible;
- un rappel de points deja exprimes par la personne;
- une lecture de progression ou de continuite tres prudente.

Ne doit pas etre diffuse tel quel:

- le detail des dimensions en langage interne;
- les tensions en langage trop systemique;
- le niveau de confiance;
- la logique d'interpretation profonde;
- les hypotheses existentielles;
- tout vocabulaire doctrinal brut.

Regle:

`une derivee d'analyse n'est pas une sortie client`

---

## 11) Regles de supervision

La supervision peut:

- relire les dimensions;
- contester une tension attribuee;
- baisser ou hausser un niveau de confiance;
- invalider une formulation client visible;
- ajuster la prochaine etape.

La supervision ne doit pas:

- transformer la grille en doctrine rigide;
- encourager la surinterpretation;
- renforcer artificiellement la confiance la ou les indices sont faibles.

---

## 12) Regles de robustesse

Avant d'ajouter un axe ou une tension au moteur:

1. `est-ce intelligible ?`
2. `est-ce utile a la prise en charge ?`
3. `est-ce suffisamment observable ?`
4. `est-ce formulable sans danger pour le client ?`
5. `est-ce compatible avec notre cadre non diagnostique ?`

Si une categorie echoue:

- elle reste en recherche.

---

## 13) Premier mapping vers le produit

Cette spec se branche naturellement sur les objets deja existants:

- `intake_request`
- `session`
- `session_note`
- futures derivees de type `analysis_tension`
- futures derivees de type `analysis_snapshot`

Ordre de branchement recommande:

1. enrichir la note de seance avec les quatre dimensions;
2. ajouter les facteurs de contexte;
3. ajouter les tensions principales;
4. ajouter une synthese de clarte et vigilance;
5. seulement ensuite automatiser des derivees IA.

---

## 14) Decision active

A compter de cette note:

- MERLIN retient cinq blocs analytiques:
  - dimensions
  - contexte
  - tensions
  - vigilance
  - prochaine etape
- la structure `Coeur / Corps / Esprit / Etre` devient une base de spec, pas un texte poetique;
- les tensions sont retenues comme unites documentaires utiles;
- le contexte devient obligatoire dans la lecture;
- aucune derivee issue de cette spec n'est diffusable au client sans reformulation et validation.

---

## 15) References

- [MERLIN_GOUV_DOCTRINE_CERCLE_NOYAU_UTILISABLE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DOCTRINE_CERCLE_NOYAU_UTILISABLE_V1.md)
- [MERLIN_GOUV_ARBITRAGE_DOCUMENT_FONDATEUR_LE_CERCLE_V0_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_ARBITRAGE_DOCUMENT_FONDATEUR_LE_CERCLE_V0_V1.md)
- [MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md)
- [MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md)
