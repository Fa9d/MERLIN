# IVIA - Lexique canonique des roles et statuts

**Date** : 2026-05-12  
**Statut** : reference produit active  
**Objet** : stabiliser le vocabulaire prospect, client, praticien, accueil clinique, supervision et administration.

**Modele operationnel associe** : `IVIA_MODELE_ENTREE_SORTIE_PAR_ROLE_2026-05-12.md`.

---

## 1. Decision courte

IVIA distingue desormais clairement :

1. le **statut relationnel** d'une personne accompagnee ;
2. le **role metier** de l'intervenant humain ;
3. le **role applicatif** utilise par le backend.

Le mot `operator` reste un code technique V1, mais son libelle produit est : **accueil clinique**.

---

## 2. Personnes accompagnees

### Prospect

Personne qui a depose une demande d'entree, mais dont le cadre n'est pas encore qualifie.

Un prospect peut avoir une fiche technique `client` en base pour permettre le suivi, les consentements et la file de traitement. Produitement, il ne devient pas encore un client actif.

### Client

Personne acceptee dans le cadre IVIA, avec une suite ouverte : seance planifiee, accompagnement commence, espace de suivi actif ou document client destine.

Le client n'est pas seulement une ligne en base. C'est une relation IVIA engagee.

---

## 3. Roles internes

### Accueil clinique

Libelle produit du role technique `operator` lorsqu'il traite la file d'entree.

Responsabilites :

- qualifier les prospects ;
- verifier le cadre et les consentements ;
- contacter, rappeler ou classer hors cadre ;
- signaler les cas de vigilance ;
- transformer une demande recevable en suite planifiee.

L'accueil clinique n'est pas l'admin technique. Il n'est pas necessairement le praticien final.

### Praticien

Personne qui realise l'ecoute ou l'accompagnement.

Responsabilites :

- conduire les seances ;
- tenir la relation d'accompagnement ;
- produire ou valider les traces utiles selon le cadre ;
- gerer son agenda et ses disponibilites quand le role applicatif `practitioner` est utilise.

### Superviseur clinique

Role de controle, qualite, validation et arbitrage clinique.

### Admin technique

Role de gestion systeme, securite et maintenance.

L'admin technique ne doit pas devenir un lecteur clinique libre.

---

## 4. Correspondance avec les codes applicatifs

| Code applicatif | Libelle produit | Sens |
|---|---|---|
| `public_client` | client public | utilisateur externe authentifie ou destinataire d'un suivi |
| `operator` | accueil clinique | traitement de la file prospects et production V1 |
| `practitioner` | praticien | accompagnement, agenda, seances propres |
| `supervisor` | superviseur clinique | validation, qualite, arbitrage |
| `admin_tech` | admin technique | systeme, securite, utilisateurs, incidents |

---

## 5. Regles de langage

- Dire **prospect** avant qualification.
- Dire **client** apres acceptation ou planification d'une suite.
- Dire **accueil clinique** dans l'interface quand le code backend est `operator` mais que la fonction reelle est la qualification.
- Dire **praticien** pour la personne qui accompagne.
- Dire **admin technique** pour la gestion systeme.
- Ne pas utiliser **admin** pour designer l'accueil clinique.
- Ne pas utiliser **client** pour masquer le moment prospect dans l'experience publique.

---

## 6. Routes recommandees

| Surface | Terme produit | Route V1 |
|---|---|---|
| Demande publique | prospect | `/rendez-vous` |
| File d'entree | accueil clinique | `/operator` |
| Espace praticien | praticien | `/praticien` ou `/espace-praticien` |
| Administration | admin technique | `/admin` |
| Supervision | superviseur clinique | `/supervision` |

La route `/operator` peut rester techniquement stable en V1. Le libelle produit doit cependant parler d'**accueil clinique**.

---

## 7. Point d'attention V1

Le modele technique cree aujourd'hui une fiche `client` des la demande publique afin de rattacher consentements, intake et suivi. Cette decision est acceptable si le langage produit continue de distinguer :

- **prospect** : relation demandee, non encore qualifiee ;
- **client** : relation acceptee ou suite engagee.

Cette distinction doit guider les textes d'interface, les tableaux de bord et les futurs exports.