# CONTRAT D'INTERFACE — CLIENT (v0.1 brouillon, 2026-07-10)

> Carte fonctionnelle GÉNÉRÉE DEPUIS LE CODE — ce que chaque écran affiche
> réellement, les données qu'il consomme, où mène chaque lien. Les blocs
> **But** sont à trancher par le fondateur en session de revue : garder /
> simplifier / fusionner / supprimer. Une fois tranché → v1.0 = canon du
> fonctionnement réel de l'interface. Complémentaire au registre
> `IVIA_VALIDATION_ECRANS_v1.0.md` (grille responsive/fonctionnelle).


---

## `/client/agenda.html` — Réserver une séance

**Fil d'Ariane** : agenda
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

---

## `/client/carte-de-vie.html` — Votre carte de vie

**En-tête affiché** : Carte du vivant · onze axes
**Fil d'Ariane** : voir
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Onze dimensions, un seul chemin
- Axe en lumière
- Progression par axe
- Ligne de vie

**Données consommées (API)** : `getMyBookings`, `getMyDocuments`, `getMyJournal`, `getMyRecordings`, `journalStructured`

**Liens sortants** :
- → `/client/journal.html`
- → `/client/ma-progression.html`
- → `/reserver.html`

---

## `/client/compte.html` — Mon compte

**En-tête affiché** : Mon compte
**Fil d'Ariane** : aujourdhui › Mon compte
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Informations personnelles
- Mot de passe
- Consentements
- Zone critique

**Données consommées (API)** : `apiMe`, `apiSetPassword`

**Liens sortants** :
- → `/confidentialite.html#n3`

---

## `/client/dashboard.html` — Mon espace

**En-tête affiché** : Mon espace
**Fil d'Ariane** : aujourdhui
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Mes intentions
- Proposition du jour
- Structurer vos données vivantes

**Données consommées (API)** : `apiMe`, `createMyIntention`, `getMyBookings`, `getMyDocuments`, `getMyIntentions`, `getMyJournal`, `getMyRecordings`, `journalStructured`, `updateMyIntention`

**Liens sortants** :
- → `/client/carte-de-vie.html`
- → `/client/journal.html`
- → `/client/ma-progression.html`
- → `/client/mes-exercices.html`
- → `/client/mes-reperes.html`
- → `/client/mon-reflet.html`
- → `/client/seances.html?vue=a-venir`
- → `/client/seances.html?vue=vecues`
- → `/reserver.html`

---

## `/client/enregistrement.html` — Enregistrer ma voix

**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `uploadMyRecording`

**Liens sortants** :
- → `/client/dashboard.html`
- → `/client/journal.html`

---

## `/client/journal-nouvelle-entree.html` — Nouvelle entrée de journal

**En-tête affiché** : Nouvelle entrée
**Fil d'Ariane** : ecrire
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Liens sortants** :
- → `/client/journal.html`

---

## `/client/journal.html` — Journal

**En-tête affiché** : Analyse du jour
**Fil d'Ariane** : ecrire
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Où j'en suis
- Mon Architecte intérieur
- Exercice du jour
- Journal quotidien
- Repères de séances validées

**Données consommées (API)** : `createMyJournalEntry`, `getMyDocuments`, `getMyJournal`, `journalStructured`

**Liens sortants** :
- → `/client/dashboard.html`
- → `/client/mon-reflet.html`

---

## `/client/ma-progression.html` — Ma progression

**En-tête affiché** : Ma progression
**Fil d'Ariane** : voir › Ma progression
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Vos repères de pratique
- Vos 7 derniers jours
- Votre activité, semaine par semaine
- Votre état du jour
- Ce qui pèse, ce qui recharge
- Jalons de votre parcours
- Ligne de vie

**Données consommées (API)** : `getMyBookings`, `getMyDocuments`, `getMyJournal`, `getMyRecordings`, `journalStructured`

---

## `/client/mes-enregistrements.html` — Mes enregistrements

**En-tête affiché** : Mes enregistrements
**Fil d'Ariane** : aujourdhui › Mes enregistrements
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Mes séances enregistrées
- Repères par mois

**Données consommées (API)** : `getMyRecordings`, `requestSeanceReflet`

**Liens sortants** :
- → `/client/enregistrement.html`
- → `/client/mon-reflet.html`

---

## `/client/mes-exercices.html` — Mes exercices

**En-tête affiché** : Mes exercices
**Fil d'Ariane** : aujourdhui › Mes exercices
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- ${esc(e.exercise.title)}

**Données consommées (API)** : `listMyExercises`, `updateMyExercise`

---

## `/client/mes-reperes.html` — Mes repères

**En-tête affiché** : Mes repères
**Fil d'Ariane** : aujourdhui › Mes repères
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `listMyReperes`

---

## `/client/mes-resumes.html` — Mes résumés de séance

**En-tête affiché** : Mes résumés de séance
**Fil d'Ariane** : aujourdhui › Mes résumés
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- ${titre.replace(/[

**Données consommées (API)** : `getMyDocuments`

---

## `/client/mon-profil.html` — Mon profil

**En-tête affiché** : Votre profil
**Fil d'Ariane** : aujourdhui › Mon profil
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `getMyClient`, `updateMyClient`

---

## `/client/mon-reflet.html` — Mon reflet

**En-tête affiché** : Mon reflet
**Fil d'Ariane** : ecrire › Mon reflet
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `listMyReflets`, `requestMyReflet`

**Liens sortants** :
- → `/client/journal.html`

---

## `/client/mot-de-passe-oublie.html` — Mot de passe oublié

**En-tête affiché** : Mot de passe oublié
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Liens sortants** :
- → `/connexion.html`

---

## `/client/premier-ancrage.html` — Premier ancrage

**En-tête affiché** : Ce que vous portez en arrivant.
**Fil d'Ariane** : aujourdhui › Premier ancrage
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Votre ancrage est posé.

**Liens sortants** :
- → `/client/dashboard.html`

---

## `/client/seance-active.html` — Séance en cours

**En-tête affiché** : Votre espace est prêt
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Séance terminée.

**Liens sortants** :
- → `/client/dashboard.html`

---

## `/client/seance-express-join.html` — Votre séance

**En-tête affiché** : Lien introuvable
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Réécoutez avant d'envoyer
- Merci — votre voix est bien arrivée.

**Données consommées (API)** : `blobToBase64`, `getExpressSession`, `uploadExpressRecording`

**Liens sortants** :
- → `/confidentialite.html`

---

## `/client/seance.html` — Votre séance

**En-tête affiché** : Séance IVIA
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Mylène est là.
- Séance terminée.

**Liens sortants** :
- → `/client/dashboard.html`

---

## `/client/seances.html` — Mes séances

**En-tête affiché** : Mes séances
**Fil d'Ariane** : aujourdhui › Mes séances
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Calendrier des séances

**Données consommées (API)** : `formatHeure`, `getMyBookings`, `getMyJournal`, `journalStructured`

**Liens sortants** :
- → `/client/journal.html`
- → `/client/mes-enregistrements.html`
- → `/reserver.html`
