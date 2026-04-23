# MERLIN - Schema service orientation (v1)

Date: 2026-04-19
Statut: draft
Type: schema

---

## Finalite

Un `service_orientation` decrit une ressource vers laquelle MERLIN peut orienter.

Ce schema sert a:
- comparer des portes d'entree proches;
- separer le role reel du service de son image courante;
- preparer un moteur d'orientation lisible par machine;
- garder distincts `service`, `regle de securite`, `source` et `validation locale`.

---

## Regle structurante

Un service ne doit pas contenir a lui seul la logique complete de triage.

Les situations de:
- danger immediat;
- suicide imminent;
- psychose aigue;
- violence severe;
- confusion aigue;
- sevrage medicalement dangereux;

doivent etre gerees par des `regles_triage` prioritaires, separees du service.

---

## Champs recommandes

- `id`
- `type_objet`
- `nom`
- `territoire`
- `statut_document`
- `categorie_service`
- `niveau_systeme`
- `statut_offre`
- `porte_entree_principale`
- `portes_entree_secondaires`
- `acces_direct`
- `reference_requise`
- `cout_usager`
- `niveau_urgence_cible`
- `besoins_pris_en_charge`
- `quand_orienter`
- `quand_ne_pas_orienter`
- `signaux_alerte_escalade`
- `services_alternatifs`
- `role_pour_merlin`
- `confusions_a_eviter`
- `niveau_fiabilite`
- `sources_principales`
- `a_valider_localement`
- `fiche_canonique_path`
- `notes`

---

## Valeurs conseillees

### `type_objet`

- `service_orientation`

### `statut_document`

- `draft`
- `review`
- `validated`
- `deprecated`

### `niveau_systeme`

- `premiere_ligne`
- `deuxieme_ligne`
- `specialise`
- `urgence`
- `soutien_communautaire`

### `statut_offre`

- `public`
- `prive`
- `communautaire`
- `mixte`

### `acces_direct`

- `oui`
- `non`
- `variable`

### `reference_requise`

- `oui`
- `non`
- `variable`

### `cout_usager`

- `gratuit`
- `payant`
- `mixte`
- `variable`

### `niveau_urgence_cible`

- `non_urgent`
- `subaigu`
- `urgence_sociale`
- `crise`
- `urgent`
- `critique`
- `post_urgence`

### `niveau_fiabilite`

- `faible`
- `moyen`
- `moyen_a_eleve`
- `eleve`

---

## Exemple minimal

```yaml
id: svc_psychologue_public_qc
type_objet: service_orientation
nom: psychologue public
territoire: Quebec
statut_document: draft
categorie_service: professionnel_sante_mentale
niveau_systeme: deuxieme_ligne
statut_offre: public
porte_entree_principale: CLSC
portes_entree_secondaires:
  - GMF
  - equipe_sante_mentale
acces_direct: non
reference_requise: oui
cout_usager: gratuit
niveau_urgence_cible: subaigu
besoins_pris_en_charge:
  - trouble_anxieux
  - trouble_depressif
  - psychotherapie
quand_orienter:
  - detresse_persistante_sans_danger_immediat
quand_ne_pas_orienter:
  - crise_suicidaire
  - psychose_aigue
signaux_alerte_escalade:
  - plan_suicidaire
  - symptomes_psychotiques_aigus
services_alternatifs:
  - svc_urgence_psy_qc
  - svc_travailleur_social_public_qc
role_pour_merlin: psychotherapie_publique_si_acces_pertinent
confusions_a_eviter:
  - psychologue_public_neq_psychiatre
niveau_fiabilite: moyen_a_eleve
sources_principales:
  - https://www.ordrepsy.qc.ca/ou-trouver
  - https://www.quebec.ca/sante/sante-mentale/trouver-aide-et-soutien-en-sante-mentale/etapes-pour-obtenir-soins-et-services-en-sante-mentale
a_valider_localement:
  - delais
  - criteres_programme
fiche_canonique_path: C:/MERLIN/05_PREUVES_SOURCES/CORPUS/SYSTEMES_SOINS_INSTITUTIONNELS/QUEBEC/SANTE_MENTALE/SOIN__canon__fiche-psychologue-public-qc__2026-04-19.md
notes: null
```

---

## Regle critique

Chaque `service_orientation` doit pointer vers:
- au moins une fiche canonique;
- au moins une source principale;
- et une liste explicite `a_valider_localement` si l'acces reel varie selon la region.
