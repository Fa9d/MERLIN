# CONTRAT D'INTERFACE — ADMIN (v0.1 brouillon, 2026-07-10)

> Carte fonctionnelle GÉNÉRÉE DEPUIS LE CODE — ce que chaque écran affiche
> réellement, les données qu'il consomme, où mène chaque lien. Les blocs
> **But** sont à trancher par le fondateur en session de revue : garder /
> simplifier / fusionner / supprimer. Une fois tranché → v1.0 = canon du
> fonctionnement réel de l'interface. Complémentaire au registre
> `IVIA_VALIDATION_ECRANS_v1.0.md` (grille responsive/fonctionnelle).


---

## `/admin/analyses.html` — Analyses &amp; droits — Admin

**En-tête affiché** : Analyses &amp; droits
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Capacités d'analyse par profil
- Reconnaissances professionnelles

**Données consommées (API)** : `adminAnalysisCapabilities`, `adminCreateCredential`, `adminListAccounts`, `adminListCredentials`, `adminSetAnalysisCapability`, `adminUpdateCredential`

---

## `/admin/comptabilite.html` — Comptabilité — Admin

**En-tête affiché** : Comptabilité
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `adminAccountingLedger`, `adminAccountingSummary`

---

## `/admin/comptes.html` — Comptes — Admin

**En-tête affiché** : Comptes &amp; accès
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `adminDeleteAccount`, `adminListAccounts`, `adminResendVerification`, `adminSetAdmin`, `adminSetRole`, `adminSetStatus`, `adminSetSubscription`, `adminVerifyAccount`

---

## `/admin/connexion.html` — Administration  — Connexion

**En-tête affiché** : Accès réservé
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `apiLogin`

**Liens sortants** :
- → `/connexion.html`

---

## `/admin/demandes.html` — Demandes d'entrée — Admin

**En-tête affiché** : Demandes d'entrée
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `adminListIntake`, `adminUpdateIntakeHandling`, `listPraticiens`

---

## `/admin/dossiers.html` — Dossiers clients

**En-tête affiché** : Dossiers clients
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- ${esc(dos.nom)}

**Données consommées (API)** : `adminClientDossier`, `adminListClients`

---

## `/admin/economie.html` — Économie IA — Admin

**En-tête affiché** : Économie IA
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Coûts par finalité d'analyse
- Économie par séance

**Données consommées (API)** : `adminEconomicsSessions`, `adminEconomicsSummary`

---

## `/admin/facturation.html` — Facturation — Admin

**En-tête affiché** : Facturation — interrupteurs par offre
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Données consommées (API)** : `apiGetBillingFlags`, `apiSetBillingFlags`

---

## `/admin/index.html` — Administration

**En-tête affiché** : Console d'administration
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Liens sortants** :
- → `/admin/analyses.html`
- → `/admin/comptabilite.html`
- → `/admin/comptes.html`
- → `/admin/demandes.html`
- → `/admin/dossiers.html`
- → `/admin/facturation.html`
- → `/admin/vue.html`

---

## `/admin/lectures.html` — Atelier des lectures — Admin

**En-tête affiché** : L'Atelier des lectures
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Nouveau type de séance
- Exercices
- Proposer une nouvelle technique d'analyse

**Données consommées (API)** : `adminAnalysisCapabilities`, `adminCreateExercise`, `adminCreateSessionType`, `adminListExercises`, `adminListSessionTypes`, `adminPatchExercise`, `adminPatchSessionTypeCapability`

---

## `/admin/vue.html` — Vue d'ensemble — Admin

**En-tête affiché** : Vue d'ensemble
**But (à trancher par le fondateur)** : ☐ garder ☐ simplifier ☐ fusionner ☐ supprimer — _pourquoi cet écran existe :_ ________

**Sections affichées** :
- Alertes de vigilance

**Données consommées (API)** : `adminOverview`
