# MERLIN - Schema entree client premiere ligne (v1)

Date: 2026-04-20
Statut: draft
Type: schema

---

## Finalite

Ce schema sert a formaliser l'objet `entree_client` pour MERLIN.

Il decrit la couche de qualification initiale avant:
- l'ouverture d'une seance;
- une orientation immediate;
- une bascule crise;
- une bascule urgence.

Il sert a:
- harmoniser accueil telephone, web et application;
- produire des champs stables lisibles par machine;
- garder une trace minimale utile;
- relier l'entree au flux, aux consentements et a la suite de parcours.

Il ne sert pas a:
- constituer un dossier clinique exhaustif;
- remplacer la note de seance;
- stocker un recit complet.

---

## Principe

Une `entree_client` doit etre:
- breve;
- structur ee;
- centree sur la qualification;
- compatible avec la securite;
- compatible avec une evolution de referentiel.

Doctrine:

`l'entree capte le minimum decisif, pas le maximum narratif`

---

## Champs recommandes

- `entry_id`
- `type_objet`
- `date`
- `canal`
- `appel_pour`
- `appelant_role`
- `client_id`
- `session_id`
- `statut_entree`
- `motif_brut_court`
- `champ_compatible_merlin`
- `type_appel`
- `danger_immediat_reporte`
- `drapeaux_rouges_initiaux`
- `niveau_risque_initial`
- `besoin_dominant_initial`
- `blocage_principal_initial`
- `consentement_echange`
- `consentement_note`
- `consentement_historique`
- `sortie_entree`
- `orientation_initiale`
- `prochaine_action_initiale`
- `regles_triage_declenchees`
- `referentiel_version`
- `created_at`
- `updated_at`
- `notes_breves`

---

## Valeurs conseillees

### `type_objet`

- `entree_client`

### `canal`

- `telephone`
- `web`
- `mobile`
- `visio`
- `presentiel`
- `autre`

### `appel_pour`

- `soi`
- `proche`

### `appelant_role`

- `client`
- `parent`
- `proche`
- `conjoint`
- `ami`
- `intervenant`
- `autre`

### `statut_entree`

- `ouverte`
- `qualifiee`
- `redirigee`
- `transformee_en_seance`
- `close`

### `champ_compatible_merlin`

- `oui`
- `non`
- `partiel`

### `type_appel`

- `standard`
- `proche_inquiet`
- `demande_alternatif`
- `crise_a_orienter`
- `hors_champ_a_orienter`

### `danger_immediat_reporte`

- `oui`
- `non`
- `incertain`

### `drapeaux_rouges_initiaux`

Liste ouverte, valeurs conseillees:
- `idee_suicidaire`
- `plan_suicidaire`
- `moyens_disponibles`
- `passage_a_l_acte_en_cours`
- `hallucinations_ou_psychose_probable`
- `confusion_aigue`
- `violence_ou_danger_autrui`
- `incapacite_securite_minimale`
- `intoxication_ou_sevrage_grave`

### `niveau_risque_initial`

- `non_urgent`
- `subaigu`
- `urgence_sociale`
- `crise`
- `urgent`
- `critique`
- `indetermine`

### `besoin_dominant_initial`

- `psychologique_psychotherapie`
- `psychiatrique_gravite_specialisee`
- `social_psychosocial`
- `crise_immediate`
- `litteratie_parcours`
- `complement_prudent`
- `mixte`
- `indetermine`

### `blocage_principal_initial`

- `meconnaissance_systeme`
- `peur_ou_evitement`
- `refus_aide`
- `delais`
- `cout`
- `isolement`
- `desorganisation`
- `aucun_identifie`
- `autre`

### `consentement_echange`

- `oui`
- `non`

### `consentement_note`

- `oui`
- `non`

### `consentement_historique`

- `oui`
- `non`
- `non_demande`

### `sortie_entree`

- `ouverture_seance_maintenant`
- `prise_de_rendez_vous`
- `orientation_immediate_service`
- `bascule_crise`
- `bascule_urgence`
- `refus_hors_champ_avec_orientation`

---

## Exemple minimal

```yaml
entry_id: ent_2026_04_20_001
type_objet: entree_client
date: 2026-04-20
canal: telephone
appel_pour: soi
appelant_role: client
client_id: null
session_id: null
statut_entree: qualifiee
motif_brut_court: se sent depasse et ne sait pas vers quelle aide se tourner
champ_compatible_merlin: oui
type_appel: standard
danger_immediat_reporte: non
drapeaux_rouges_initiaux: []
niveau_risque_initial: subaigu
besoin_dominant_initial: litteratie_parcours
blocage_principal_initial: meconnaissance_systeme
consentement_echange: oui
consentement_note: oui
consentement_historique: non_demande
sortie_entree: ouverture_seance_maintenant
orientation_initiale: []
prochaine_action_initiale: ouverture de seance standard 30 min
regles_triage_declenchees: []
referentiel_version: triage_qc_2026_04_19
created_at: 2026-04-20T10:15:00-04:00
updated_at: 2026-04-20T10:17:00-04:00
notes_breves: cadre pose; aucun danger immediat rapporte
```

---

## Regles critiques

### Regle 1 - Pas de seance sans trace de qualification

Si une seance est ouverte, une `entree_client` minimale doit exister ou etre derivee.

### Regle 2 - Le risque prime

Si `danger_immediat_reporte = oui` ou si `drapeaux_rouges_initiaux` contient un seuil critique, alors:
- `sortie_entree` ne doit pas etre `prise_de_rendez_vous`;
- une regle de triage doit primer.

### Regle 3 - Pas de note implicite

Si `consentement_note = non`, l'ouverture d'une seance standard doit etre reevaluee selon la politique MERLIN.

### Regle 4 - Compatibilite historique

Les codes comme `besoin_dominant_initial`, `niveau_risque_initial` et `sortie_entree` doivent rester interpretable s dans le temps.

Pour cela:
- stocker les codes;
- stocker `referentiel_version`;
- ne pas dependre d'un simple libelle d'interface.

### Regle 5 - Le brut reste court

`motif_brut_court` ne doit pas devenir un compte rendu complet.

Le recit detaille appartient a la seance ou a la note, pas a l'objet d'entree.

---

## Articulations

Ce schema doit etre compatible avec:
- [MERLIN_METH_PROTOCOLE_ENTREE_CLIENT_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PROTOCOLE_ENTREE_CLIENT_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)
- [MERLIN_PREU_SCHEMA_REGLE_TRIAGE_v1.0.md](C:/MERLIN/05_PREUVES_SOURCES/SCHEMAS/MERLIN_PREU_SCHEMA_REGLE_TRIAGE_v1.0.md)
- [MERLIN_PREU_SCHEMA_HISTORIQUE_CLIENT_PREMIERE_LIGNE_v1.0.md](C:/MERLIN/05_PREUVES_SOURCES/SCHEMAS/MERLIN_PREU_SCHEMA_HISTORIQUE_CLIENT_PREMIERE_LIGNE_v1.0.md)
- [MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md)

---

## Decision active

MERLIN adopte `entree_client` comme objet machine minimal de la couche `entry/intake`.

Cet objet doit servir de point de passage commun entre:
- accueil humain;
- formulaire web ou mobile;
- base de donnees;
- logique de routage;
- ouverture de seance ou redirection.
