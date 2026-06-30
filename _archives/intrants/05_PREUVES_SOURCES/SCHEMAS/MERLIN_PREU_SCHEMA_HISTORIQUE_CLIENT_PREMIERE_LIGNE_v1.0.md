# MERLIN - Schema historique client premiere ligne (v1)

Date: 2026-04-19
Statut: draft
Type: schema

---

## Finalite

Ce schema sert a conserver un historique client minimal utile a la continuite des seances MERLIN.

Il ne sert pas a constituer un dossier clinique exhaustif.

---

## Principe

Chaque entree doit etre:
- breve;
- factuelle;
- orientee vers la continuite;
- lisible rapidement par un operateur.

---

## Champs recommandes

- `client_id`
- `session_id`
- `date`
- `type_seance`
- `motif_principal`
- `drapeaux_rouges`
- `niveau_risque_percu`
- `besoin_dominant`
- `orientation_recommandee`
- `prochaine_action`
- `mise_en_garde`
- `consentement_note`
- `consentement_enregistrement`
- `consentement_transcription`
- `audio_exists`
- `transcript_exists`
- `retention_class`
- `last_updated`
- `notes_operateur_breves`

---

## Valeurs conseillees

### `type_seance`

- `standard`
- `proche_inquiet`
- `demande_alternatif`
- `bascule_urgence`
- `autre`

### `niveau_risque_percu`

- `non_urgent`
- `subaigu`
- `urgence_sociale`
- `crise`
- `urgent`
- `critique`

### `retention_class`

- `note_only`
- `transcript_exception`
- `recording_exception`

---

## Exemple minimal

```yaml
client_id: cli_0001
session_id: ses_2026_04_19_001
date: 2026-04-19
type_seance: standard
motif_principal: detresse anxieuse persistante et confusion sur la bonne ressource
drapeaux_rouges: []
niveau_risque_percu: non_urgent
besoin_dominant: psychologique_psychotherapie
orientation_recommandee:
  - psychologue_public_via_clsc
  - psychologue_prive_selon_acces
prochaine_action: contacter CLSC ou psychologue dans les 7 jours
mise_en_garde: reevaluer urgence si idees suicidaires avec plan ou aggravation nette
consentement_note: true
consentement_enregistrement: false
consentement_transcription: false
audio_exists: false
transcript_exists: false
retention_class: note_only
last_updated: 2026-04-19
notes_operateur_breves: pas de diagnostic; besoin de suivi stable
```

---

## Regle critique

Si `audio_exists` ou `transcript_exists` vaut `true`, alors:
- le consentement correspondant doit etre `true`;
- la finalite et la retention doivent etre documentees ailleurs;
- la conservation ne doit pas etre implicite ou indefinite.
