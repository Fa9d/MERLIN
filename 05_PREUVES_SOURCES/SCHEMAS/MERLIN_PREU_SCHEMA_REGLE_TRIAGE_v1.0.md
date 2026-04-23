# MERLIN - Schema regle triage (v1)

Date: 2026-04-19
Statut: draft
Type: schema

---

## Finalite

Une `regle_triage` sert a prioriser la securite avant l'orientation fine.

Elle ne decrit pas un service.
Elle decrit:
- un seuil;
- des declencheurs;
- une action;
- des services cibles;
- des services a ne pas proposer en premiere intention.

---

## Principe de precedence

Une `regle_triage` prioritaire ecrase une orientation de confort ou de specialite.

Exemple:
- si `plan_suicidaire_imminent` est detecte,
  alors `urgence` ou `911` prime sur `psychologue`, `travailleur_social`, `centre_de_crise` ou `ligne_d_ecoute`.

---

## Champs recommandes

- `id`
- `type_objet`
- `nom_regle`
- `priorite`
- `domaine`
- `declencheurs_any`
- `declencheurs_all`
- `indicateurs_exemples`
- `action_principale`
- `services_cibles`
- `services_a_eviter`
- `message_court`
- `justification`
- `niveau_fiabilite`
- `sources_principales`
- `a_valider_localement`
- `notes`

---

## Valeurs conseillees

### `type_objet`

- `regle_triage`

### `priorite`

- `critique`
- `haute`
- `moyenne`

### `domaine`

- `suicide`
- `psychose`
- `violence`
- `confusion`
- `dependance`
- `orientation_generale`

### `action_principale`

- `appeler_911`
- `aller_urgence`
- `orienter_urgence_psy`
- `orienter_centre_crise`
- `orienter_811`
- `orienter_service_specialise`
- `ne_pas_orienter_directement`

### `niveau_fiabilite`

- `faible`
- `moyen`
- `moyen_a_eleve`
- `eleve`

---

## Exemple minimal

```yaml
id: triage_suicide_imminent_qc
type_objet: regle_triage
nom_regle: risque suicidaire imminent
priorite: critique
domaine: suicide
declencheurs_any:
  - plan_suicidaire
  - moyens_letaux_disponibles
  - passage_a_l_acte_en_cours
declencheurs_all: []
indicateurs_exemples:
  - je vais me tuer ce soir
  - j ai deja les moyens
action_principale: appeler_911
services_cibles:
  - svc_urgence_psy_qc
services_a_eviter:
  - svc_psychologue_public_qc
  - svc_psychologue_prive_qc
  - svc_travailleur_social_public_qc
message_court: danger immediat probable; l orientation urgente prime.
justification: la securite ne peut pas etre laissee a un suivi non urgent.
niveau_fiabilite: eleve
sources_principales:
  - https://msss.gouv.qc.ca/professionnels/soins-et-services/guide-urgences-sante-mentale/
a_valider_localement:
  - protocole_etablissement
notes: null
```

---

## Regle critique

Une `regle_triage` doit toujours permettre de repondre clairement a deux questions:
- qu'est-ce qui declenche l'escalade;
- quel service ou canal doit primer immediatement.
