# CONTRAT D'INTERFACE — PRATICIEN (v0.1 brouillon, 2026-07-10)

> Carte fonctionnelle GÉNÉRÉE DEPUIS LE CODE — ce que chaque écran affiche
> réellement, les données qu'il consomme, où mène chaque lien. Les blocs
> **But** sont à trancher par le fondateur en session de revue : garder /
> simplifier / fusionner / supprimer. Une fois tranché → v1.0 = canon du
> fonctionnement réel de l'interface. Complémentaire au registre
> `IVIA_VALIDATION_ECRANS_v1.0.md` (grille responsive/fonctionnelle).


---

## `/praticien/agenda.html` — agenda.html

**En-tête affiché** : Agenda
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `createScheduleException`, `deleteScheduleException`, `getAvailableSlots`, `getMyExceptions`, `getPractitionerAgenda`, `getWeekBounds`

**Liens sortants** :
- → `/connexion.html?retour=/praticien/agenda.html`
- → `/praticien/profil.html`

---

## `/praticien/carte-de-vie.html` — Carte de Vie (lecture praticien)

**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Constellation des onze axes
- Ligne de vie
- Horizon — orientation, pas destination

**Données consommées (API)** : `getClient`, `getClientAnalyses`, `getClientLifeEvents`

**Liens sortants** :
- → `/praticien/clients-journal.html`

---

## `/praticien/clients-journal.html` — clients-journal.html

**En-tête affiché** : Journal des clients
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Fiche client

**Données consommées (API)** : `_req`, `journalStructured`, `listMySessions`

**Liens sortants** :
- → `/praticien/carte-de-vie.html?client=${esc(client.id)}`

---

## `/praticien/compte-rendu-seance.html` — Compte-rendu de séance

**En-tête affiché** : Analyse introuvable
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Résumé
- Observation
- Pistes de suivi
- Axe de la prochaine séance
- Lecture multidimensionnelle
- Reformulation pour le client
- Validation humaine

**Données consommées (API)** : `createDerivedDocument`, `getSession`, `getSessionNote`, `validateSessionNote`

**Liens sortants** :
- → `/praticien/livraisons.html`

---

## `/praticien/compte.html` — compte.html

**En-tête affiché** : Mon compte
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Informations personnelles
- Mot de passe
- Coordonnées de virement
- Consentements — Loi 25
- Zone critique

**Données consommées (API)** : `apiMe`, `apiSetPassword`, `getMyProfil`, `updateMyProfil`

---

## `/praticien/dashboard.html` — Tableau de bord praticien

**En-tête affiché** : Tableau de bord
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- 📅 Prochains rendez-vous
- À valider en priorité
- Dernières analyses

**Données consommées (API)** : `_req`, `getSessionNotes`, `listMySessions`

**Liens sortants** :
- → `/praticien/guide.html`
- → `/praticien/livraisons.html`
- → `/praticien/livraisons.html?filtre=a-valider`
- → `/praticien/livraisons.html?filtre=vigilance`
- → `/praticien/seance-express.html`

---

## `/praticien/fiche.html` — Profil praticien·ne

**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- À propos
- Thèmes d'accompagnement
- Formats proposés
- Prêt·e à commencer ?

**Données consommées (API)** : `listPraticiens`

**Liens sortants** :
- → `/cgu.html`
- → `/confidentialite.html`
- → `/mentions.html`
- → `/rendez-vous.html`
- → `/reserver.html`

---

## `/praticien/guide.html` — Guide praticien·ne

**En-tête affiché** : Guide praticien·ne
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Premiers pas
- Comment se déroule une séance
- L'IA vous assiste — vous tranchez
- Vos espaces, en un coup d'œil

**Liens sortants** :
- → `/praticien/agenda.html`
- → `/praticien/compte.html`
- → `/praticien/dashboard.html`
- → `/praticien/livraisons.html`
- → `/praticien/profil.html`
- → `/praticien/seance-express.html`

---

## `/praticien/livraisons.html` — Analyses de séances

**En-tête affiché** : Analyses de séances
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `_req`, `archiveSession`, `deleteSession`, `getSessionNotes`, `listMySessions`, `sendClientFollowup`

**Liens sortants** :
- → `/praticien/compte-rendu-seance.html?note=${encodeURIComponent(n.id)}`
- → `/praticien/livraisons.html`

---

## `/praticien/ma-pratique.html` — Ma pratique

**En-tête affiché** : Ma pratique
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Déposer un retour de pratique
- Mon analyse de pratique
- Mes retours récents

**Données consommées (API)** : `createRetourPratique`, `listMesRefletsPratique`, `listMesRetours`, `requestRefletPratique`

---

## `/praticien/preparation.html` — Préparer l'entretien

**En-tête affiché** : Préparer l'entretien
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Le fil à reprendre
- Intentions actives du client
- Journal depuis la dernière séance
- Ancrages évoqués en séance
- Exercices
- Lectures &amp; analyses
- Restituer au client

**Données consommées (API)** : `apiSessionPreparation`, `deliverAnalysis`, `listActiveExercises`, `listSessionDeliveries`, `listSessionExercises`, `proposeExercise`, `withdrawDelivery`

**Liens sortants** :
- → `/praticien/agenda.html`

---

## `/praticien/profil.html` — profil.html

**En-tête affiché** : Mon profil
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Informations publiques
- Thèmes d'accompagnement
- Formats proposés
- Vos tarifs de séance
- Profil audio
- Vos disponibilités

**Données consommées (API)** : `createScheduleBlock`, `deleteScheduleBlock`, `getMyProfil`, `getMySchedule`, `getMyTarifs`, `setMyTarifs`, `updateMyProfil`

---

## `/praticien/seance-express.html` — Créer une séance express

**En-tête affiché** : Créer une séance express
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Séance créée

**Données consommées (API)** : `createExpressSession`

**Liens sortants** :
- → `/praticien/livraisons.html`
