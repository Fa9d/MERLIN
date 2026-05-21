# IVIA - Modele entree / sortie par role

**Date** : 2026-05-12  
**Statut** : reference operationnelle active  
**Dependance** : `IVIA_LEXIQUE_ROLES_PROSPECT_CLIENT_PRATICIEN_ADMIN_2026-05-12.md`  
**Objet** : definir, pour chaque role, ce qui entre, ce qui est traite, ce qui sort, et ce qui reste invisible.

---

## 1. Principe central

IVIA ne doit pas etre pense comme une suite d'ecrans, mais comme une chaine de transformation.

```text
Prospect
  -> demande d'entree
  -> accueil clinique
  -> qualification
  -> client actif
  -> seance
  -> note interne
  -> document diffusable
  -> suivi client / prochaine etape
```

Chaque passage doit produire au moins un de ces trois resultats :

- une **decision** ;
- une **trace** ;
- une **prochaine action**.

---

## 2. Files operationnelles V1

| File | Role principal | Objet traite | Sortie attendue |
|---|---|---|---|
| File d'entree | accueil clinique | `IntakeRequest` | qualification, rappel, vigilance, hors cadre ou planification |
| File de planification | accueil clinique + praticien | prospect qualifie | `Session` planifiee, praticien assigne, consentements verifies |
| File de production | praticien / production V1 | `Session` | seance conduite, note produite, vigilance qualifiee |
| File de sortie | praticien + superviseur clinique | `SessionNote`, `DerivedDocument` | document diffusable, prochaine etape, fermeture ou suivi |
| File technique | admin technique | incident, utilisateur, integration | resolution technique sans lecture clinique libre |

---

## 3. Prospect

### Entree

- Arrive par `/rendez-vous` ou par une entree directe saisie par l'accueil clinique.
- Fournit un nom ou alias, un contact, un motif libre et les consentements initiaux.

### Objet principal

- `IntakeRequest`
- fiche technique `Client` creee pour rattacher la demande et les consentements
- `Consent`

### Traitement attendu

- Deposer une demande comprehensible.
- Confirmer le cadre minimal : adulte, non urgence immediate, consentements requis.

### Sortie possible

- reste prospect en attente ;
- devient prospect a rappeler ;
- passe en vigilance ;
- sort hors cadre ;
- devient client actif si une suite IVIA est acceptee ou planifiee.

### Invisible pour lui

- classement interne complet ;
- notes de qualification ;
- hypotheses internes ;
- commentaires de supervision.

---

## 4. Client

### Entree

- Devient client apres qualification positive ou planification d'une suite.
- Peut aussi exister comme `Client` technique avant ce moment, mais le statut produit reste prospect.

### Objets principaux

- `Client`
- `Session`
- `Consent`
- `DerivedDocument` visible si diffuse

### Traitement attendu

- Recevoir une suite claire : rendez-vous, accompagnement, document, prochaine action ou fermeture explicite.

### Sortie possible

- seance planifiee ;
- seance completee ;
- suivi ouvert ;
- document remis ;
- dossier ferme ou archive selon cadre.

### Visible pour lui

- ses informations utiles ;
- ses rendez-vous ;
- ses documents diffuses ;
- les prochaines etapes explicites.

### Invisible pour lui

- transcription brute ;
- note brute interne ;
- hypothese interne ;
- commentaire de supervision ;
- audit.

---

## 5. Accueil clinique (`operator` technique)

### Entree

- File prospects.
- Demandes publiques.
- Entrees directes par telephone ou autre canal.
- Alertes de consentement incomplet ou vigilance.

### Objets principaux

- `IntakeRequest`
- `Client` technique
- `Consent`
- `Session` quand une suite est acceptee

### Actions

- Qualifier la demande.
- Verifier les consentements requis.
- Contacter ou rappeler.
- Marquer : `new`, `a_rappeler`, `contacte`, `planifie`, `vigilance`, `hors_cadre`, `archive`.
- Creer une seance lorsque le cadre est bon.
- Preparer la salle audio si necessaire.

### Sortie attendue

- decision de qualification ;
- note interne de traitement ;
- prospect planifie ou classe ;
- client actif si suite engagee.

### Limites

- N'est pas l'admin technique.
- N'est pas automatiquement le praticien final.
- Ne doit pas devenir un acces libre a tous les dossiers hors besoin operatoire.

---

## 6. Praticien

### Entree

- Seance planifiee.
- Client actif.
- Consentements verifies.
- Motif d'entree et contexte utile.

### Objets principaux

- `Session`
- `AudioSession`
- `SessionNote`
- `DerivedDocument` si une sortie client est produite

### Actions

- Conduire l'ecoute ou l'accompagnement.
- Demarrer et cloturer la seance.
- Produire une note utile.
- Identifier vigilance, suite, orientation ou fermeture.
- Proposer une prochaine etape.

### Sortie attendue

- seance `completed`, `cancelled`, `no_show` ou `escalated` ;
- note interne structuree ;
- prochaines actions ;
- document diffusable si approprie.

### Limites

- Ne gere pas les utilisateurs systeme.
- Ne lit que les dossiers rattaches a son perimetre.
- Ne valide pas seul les cas qui exigent une supervision.

---

## 7. Superviseur clinique

### Entree

- Cas de vigilance.
- Notes a valider.
- Sorties sensibles.
- Demandes d'arbitrage clinique.

### Objets principaux

- `SessionNote`
- `DerivedDocument`
- signaux de vigilance
- historique utile du cas

### Actions

- Relire.
- Valider ou refuser une sortie.
- Demander correction.
- Arbitrer hors cadre, escalade ou diffusion.

### Sortie attendue

- validation ;
- correction demandee ;
- escalade ;
- decision documentee.

### Limites

- Ne remplace pas l'accueil clinique dans le traitement courant.
- Ne remplace pas l'admin technique.
- Son acces doit rester lie a un mandat de qualite, risque ou validation.

---

## 8. Admin technique

### Entree

- Incident technique.
- Besoin de creation ou correction d'utilisateur interne.
- Probleme d'integration, logs, secrets, infrastructure.

### Objets principaux

- `AppUser`
- configuration
- logs techniques
- etat des services
- migrations

### Actions

- Maintenir l'authentification.
- Gerer les comptes internes.
- Corriger les incidents.
- Appliquer les migrations.
- Surveiller la disponibilite.

### Sortie attendue

- service stable ;
- compte corrige ;
- incident documente ;
- configuration coherente.

### Limites

- Ne lit pas librement les contenus cliniques.
- Ne traite pas la file prospects.
- Ne valide pas les notes cliniques.

---

## 9. Gouvernance

### Entree

- Besoin de regle.
- Arbitrage de politique.
- Audit.
- Exception d'acces.

### Objets principaux

- politiques ;
- matrices de roles ;
- preuves et audits ;
- decisions d'arbitrage.

### Actions

- Fixer les regles.
- Auditer l'usage des roles.
- Autoriser ou refuser des exceptions.
- Clarifier les limites de diffusion.

### Sortie attendue

- decision gouvernee ;
- trace d'audit ;
- regle mise a jour ;
- backlog de correction si ecart.

### Limites

- Ne doit pas devenir une lecture clinique quotidienne.
- Les acces exceptionnels doivent etre rares, motives, journalises et revocables.

---

## 10. Definition de pret pour chaque passage

| Passage | Pret quand |
|---|---|
| Prospect -> accueil clinique | demande recue, contact present ou assumee anonyme, consentements initiaux traitables |
| Accueil clinique -> client actif | cadre accepte, urgence exclue ou geree, consentements requis verifies, suite planifiee ou acceptee |
| Client actif -> seance | praticien ou production V1 assigne, horaire defini, canal defini, contexte transmis |
| Seance -> note interne | seance cloturee, faits utiles notes, vigilance qualifiee, prochaines actions posees |
| Note interne -> document diffusable | contenu relu, donnees sensibles filtrees, visibilite client explicite |
| Document diffusable -> suivi client | document remis ou accessible, prochaine etape claire, statut de suivi mis a jour |

---

## 11. Regle de nommage interface

- Sur l'entree publique : parler de **demande** et de **prospect**, pas de dossier clinique.
- Sur la file : parler d'**accueil clinique** et de **file prospects**.
- Sur la seance : parler de **praticien**, **client**, **seance**.
- Sur la sortie : parler de **synthese**, **document remis**, **prochaine etape**.
- Sur la technique : parler d'**admin technique**, jamais d'operateur.