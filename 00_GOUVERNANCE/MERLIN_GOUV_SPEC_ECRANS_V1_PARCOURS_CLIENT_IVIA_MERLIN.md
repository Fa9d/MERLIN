# MERLIN - Spec ecrans V1 parcours client IVIA / MERLIN

Date: 2026-04-21
Statut: draft
Objet: definir les ecrans V1, leurs roles, les donnees lues/ecrites, les validations, les transitions et les acces

---

## 1) Role de cette spec

Cette spec complete la spec donnees V1.

Elle sert a transformer:
- les objets metier;
- les statuts;
- les consentements;
- les contraintes applicatives;

en parcours et interfaces codables.

Elle couvre:
- le parcours client public V1;
- le backoffice operateur V1;
- le minimum supervision V1.

Elle ne couvre pas encore:
- le portail praticiens avance;
- la couche formation continue praticiens;
- la couche research visible;
- les parcours mineurs / parents;
- les interfaces multi-organisations.

---

## 2) Principes UX et produit V1

### Principe 1 - Le client voit simple

Le client doit voir:
- peu d'ecrans;
- peu de champs;
- des formulations claires;
- un cadre explicite;
- un resultat concret.

### Principe 2 - L'operateur voit structure

L'operateur doit voir:
- les objets utiles;
- les validations metier;
- la continuite;
- les statuts critiques;
- les actions permises.

### Principe 3 - La supervision voit l'audit

La supervision doit voir:
- ce qui a ete derive;
- ce qui a ete valide;
- ce qui a ete rejete;
- ce qui est sensible;
- ce qui a ete remis ou transmis.

### Principe 4 - La recherche ne fuit pas en production

Les ecrans V1 ne doivent pas exposer accidentalement:
- la couche `research`;
- des hypotheses profondes non gouvernees;
- des analyses non validables en production.

---

## 3) Roles d'acces V1

### `public_client`

Accede a:
- landing;
- entree / qualification;
- consentements d'entree;
- confirmation;
- prise de rendez-vous ou demande de contact;
- reception d'un document derive simple si prevu.

### `operator`

Accede a:
- file de demandes;
- fiche client;
- creation et conduite de seance;
- note structuree;
- orientation;
- documents derives;
- historique court;
- consultation limitee des sources sensibles si autorise.

### `supervisor`

Accede a:
- audit des derives;
- validations/rejets;
- supervision des sorties IA;
- lecture des evenements critiques.

### `admin_tech`

Accede a:
- logs techniques;
- etats systeme;
- jobs;
- stockage et metadonnees;

Pas d'acces par defaut au contenu sensible lisible si cela n'est pas necessaire.

---

## 4) Cartographie des ecrans V1

### Parcours client public

1. `SCR-001` Landing client
2. `SCR-002` Entree / prequalification
3. `SCR-003` Consentements d'entree
4. `SCR-004` Fiche minimale / contact
5. `SCR-005` Confirmation / suite immediate
6. `SCR-006` Prise de rendez-vous ou demande de rappel

### Backoffice operateur

7. `SCR-101` Tableau de bord operateur
8. `SCR-102` Vue fiche client
9. `SCR-103` Creation / ouverture de seance
10. `SCR-104` Ecran de conduite de seance
11. `SCR-105` Ecran note structuree
12. `SCR-106` Ecran orientation
13. `SCR-107` Ecran document derive
14. `SCR-108` Vue historique court
15. `SCR-109` Vue sources sensibles

### Supervision / qualite

16. `SCR-201` File supervision IA / qualite
17. `SCR-202` Fiche revue de sortie IA
18. `SCR-203` Journal d'audit cible

### Ecrans explicitement hors V1

- portail pro commercial complet
- espace recherche
- tableau clinique avance
- espace mineurs / parents
- biometrie vocale
- training set manager

---

## 5) Specs ecran par ecran

## SCR-001 - Landing client

### Role

Page publique de comprehension et de conversion.

### Utilisateur

- `public_client`

### Objectif

- expliquer l'offre;
- poser les limites;
- donner une premiere porte d'entree;
- amener vers `SCR-002`.

### Donnees lues

- contenu editorial statique
- referentiels de services affichables si necessaire

### Donnees ecrites

- aucune donnee metier obligatoire
- eventuellement `audit_event` de navigation non sensible cote analytique

### CTA principaux

- `Commencer`
- `Prendre rendez-vous`
- `Comprendre notre approche`

### Validations

- aucune validation metier

### Transitions

- vers `SCR-002`
- vers `SCR-006`

### Règles UX

- mobile first
- headline claire
- mention non-urgence visible
- ton sobre, non manipulateur

---

## SCR-002 - Entree / prequalification

### Role

Qualifier la demande initiale en 6 a 8 questions maximum.

### Utilisateur

- `public_client`

### Objectif

- identifier pour qui est la demande;
- capter le besoin principal;
- capter l'urgence percue;
- preparer la creation de `intake_request`.

### Donnees lues

- referentiels:
  - `request_for_code`
  - `primary_need_code`
  - `perceived_urgency_code`

### Donnees ecrites

- `intake_request.request_for_code`
- `intake_request.primary_need_code`
- `intake_request.perceived_urgency_code`
- `intake_request.support_already_in_place`
- `intake_request.requested_outcome_text`

### Champs obligatoires

- pour qui
- besoin principal
- urgence percue

### Validations

- si urgence critique percue, afficher message de non-adequation + sortie d'escalade
- pas de texte libre long obligatoire

### Transitions

- vers `SCR-003`
- ou sortie d'escalade hors parcours si situation manifestement urgente

### Etats

- `draft`
- `completed`
- `blocked_by_urgency`

---

## SCR-003 - Consentements d'entree

### Role

Recueillir les consentements indispensables d'entree.

### Utilisateur

- `public_client`

### Objectif

- faire comprendre le cadre;
- capter les consentements structurels;
- ouvrir les consentements optionnels si necessaire.

### Donnees lues

- referentiels `consent_type_code`
- textes de consentement versionnes

### Donnees ecrites

- `consent`:
  - `consent_session`
  - `consent_session_note`
  - `consent_history`
  - optionnels selon contexte

### Validations

- impossible de poursuivre sans consentements structurels V1
- impossibilite de presumer un consentement audio / transcription

### Transitions

- vers `SCR-004`

### Etats

- `incomplete`
- `accepted_minimum`
- `declined_required`

---

## SCR-004 - Fiche minimale / contact

### Role

Creer ou completer la fiche minimale du client.

### Utilisateur

- `public_client`

### Objectif

- rendre la prise de contact ou le rendez-vous possible;
- minimiser la collecte.

### Donnees lues

- aucune obligatoire hors referentiels simples

### Donnees ecrites

- `client.first_name_or_alias`
- `client.email` ou `client.phone`
- `client.language_code`
- `client.timezone`
- `client.territory_code`
- `client.is_adult_confirmed`

### Champs obligatoires

- identifiant d'usage
- au moins un canal de contact
- confirmation adulte V1

### Validations

- pas de seance V1 si adulte non confirme
- pas de suite sans moyen de contact

### Transitions

- vers `SCR-005`

---

## SCR-005 - Confirmation / suite immediate

### Role

Restituer la prise en compte et preparer la prochaine etape.

### Utilisateur

- `public_client`

### Objectif

- confirmer;
- rassurer;
- remettre un premier cadre utile;
- pousser vers la reservation ou l'attente de rappel.

### Donnees lues

- `client`
- `intake_request`
- `consent`
- eventuel `document_derived` type `entry_summary`

### Donnees ecrites

- `document_derived` si un document d'entree est genere
- `client_timeline_event`

### CTA principaux

- `Prendre rendez-vous`
- `Recevoir la suite`

### Transitions

- vers `SCR-006`

---

## SCR-006 - Prise de rendez-vous ou demande de rappel

### Role

Transformer l'entree qualifiee en action.

### Utilisateur

- `public_client`

### Objectif

- reserver un horaire;
- ou demander un rappel / contact.

### Donnees lues

- disponibilites
- `client`
- `intake_request`

### Donnees ecrites

- `session.scheduled_start_at` si reservation directe
- ou eventuelle `intake_request` / `client_timeline_event` de rappel

### Validations

- pas de reservation sans client et consentements structurels

### Transitions

- fin de parcours public
- notification operateur / creation entree dashboard

---

## SCR-101 - Tableau de bord operateur

### Role

Vue de pilotage quotidienne.

### Utilisateur

- `operator`

### Objectif

- voir les nouvelles demandes;
- voir les rendez-vous;
- voir les suivis a traiter;
- acceder aux fiches client.

### Donnees lues

- `intake_request`
- `session`
- `client`
- `client_timeline_event`

### Donnees ecrites

- aucune ecriture metier principale
- `audit_event` de consultation si necessaire

### Actions principales

- ouvrir fiche client
- ouvrir seance
- marquer prise en charge

---

## SCR-102 - Vue fiche client

### Role

Vue centrale d'un client.

### Utilisateur

- `operator`
- `supervisor` lecture adaptee

### Objectif

- relire l'entree;
- voir l'historique court;
- voir les consentements;
- ouvrir ou preparer une seance.

### Donnees lues

- `client`
- `intake_request`
- `consent`
- `client_timeline_event`
- `session`

### Donnees ecrites

- modifications limitees de fiche

### Validations

- distinction claire entre donnees client, historique, consentements et documents

### Transitions

- vers `SCR-103`
- vers `SCR-108`

---

## SCR-103 - Creation / ouverture de seance

### Role

Ouvrir un objet `session`.

### Utilisateur

- `operator`

### Objectif

- creer la session;
- verifier cadre et consentements;
- preparer la conduite de seance.

### Donnees lues

- `client`
- `consent`
- `session` precedentes

### Donnees ecrites

- `session`

### Validations

- pas d'ouverture normale sans consentements structurels
- afficher drapeaux si consentement audio/transcription absent

### Transitions

- vers `SCR-104`

---

## SCR-104 - Ecran de conduite de seance

### Role

Support en cours de seance.

### Utilisateur

- `operator`

### Objectif

- voir l'essentiel du contexte;
- tenir la seance;
- tracer les evenements critiques;
- lancer captation ou transcription si autorisee.

### Donnees lues

- `client`
- `session`
- `session_note` draft
- `consent`
- historique court

### Donnees ecrites

- mises a jour `session`
- eventuelle creation `audio_source`
- eventuelles notes de travail temporaires

### Validations

- bouton `demarrer enregistrement` seulement si consentement adapte
- signalement visible si urgence / escalation

### Etats

- `scheduled`
- `in_progress`
- `paused` optionnel
- `completed_pending_note`
- `escalated`

### Transitions

- vers `SCR-105`
- vers escalation procedure si necessaire

---

## SCR-105 - Ecran note structuree

### Role

Formaliser la note operatoire de seance.

### Utilisateur

- `operator`

### Objectif

- produire la trace utile standard V1.

### Donnees lues

- `session`
- `client`
- eventuels `derived_fact`
- eventuel `transcript_source`

### Donnees ecrites

- `session_note`

### Champs minimum

- besoin presente
- elements cles
- vigilance
- prochaine etape
- resume operateur

### Validations

- pas de cloture standard sans note
- pas de formulation diagnostique reservee dans les templates V1

### Transitions

- vers `SCR-106`
- vers `SCR-107`

---

## SCR-106 - Ecran orientation

### Role

Saisir, revoir et valider l'orientation.

### Utilisateur

- `operator`
- `supervisor` lecture / validation si requis

### Objectif

- documenter pourquoi une orientation existe;
- classifier son niveau de confiance;
- eviter les formulations floues.

### Donnees lues

- `session_note`
- `risk_assessment`
- `derived_fact`
- referentiel `orientation_target_code`

### Donnees ecrites

- `orientation`
- eventuel `risk_assessment`

### Validations

- chaque orientation doit avoir une raison
- toute orientation `urgent_escalation` doit laisser trace forte

### Transitions

- vers `SCR-107`
- vers `SCR-108`

---

## SCR-107 - Ecran document derive

### Role

Generer, relire et eventuellement remettre un document derive.

### Utilisateur

- `operator`
- `supervisor` si validation requise

### Objectif

- produire `entry_summary`, `session_summary`, `care_journal_entry` ou `relay_note`

### Donnees lues

- `client`
- `session`
- `session_note`
- `orientation`
- `derived_fact`

### Donnees ecrites

- `document_derived`
- `client_timeline_event`

### Validations

- types de documents limites au perimetre V1
- document remis au client clairement distinct de la source brute
- `relay_note` non transmissible sans base adequate

### Transitions

- remise client
- vers `SCR-108`
- vers `SCR-202` si revue supervision necessaire

---

## SCR-108 - Vue historique court

### Role

Vue chronologique simple du parcours client.

### Utilisateur

- `operator`
- `supervisor`

### Objectif

- ne pas recommencer a zero;
- visualiser la continuite;
- comparer simplement.

### Donnees lues

- `client_timeline_event`
- `session`
- `session_note`
- `orientation`
- `document_derived`

### Donnees ecrites

- aucune en ecriture directe normalement

### Regles UX

- affichage synthétique;
- pas de verbatim massif;
- acces rapide aux objets lies

---

## SCR-109 - Vue sources sensibles

### Role

Acces controle a `audio_source` et `transcript_source`.

### Utilisateur

- `operator` si autorise
- `supervisor`

### Objectif

- consulter une source brute si necessaire;
- pas l'utiliser comme interface de travail principale.

### Donnees lues

- `audio_source`
- `transcript_source`

### Donnees ecrites

- `audit_event` obligatoire sur consultation restreinte

### Validations

- acces restreint;
- justification d'acces recommandee;
- pas de bouton de transmission brute par defaut

---

## SCR-201 - File supervision IA / qualite

### Role

Lister les sorties ou evenements a revoir.

### Utilisateur

- `supervisor`

### Objectif

- voir les `pending validation`;
- detecter les rejets;
- traiter les cas sensibles.

### Donnees lues

- `risk_assessment`
- `orientation`
- `document_derived`
- `derived_fact`
- `audit_event`

### Donnees ecrites

- mises a jour `human_validation_status`

---

## SCR-202 - Fiche revue de sortie IA

### Role

Relire une sortie IA ou un derive sensible et la valider/rejeter.

### Utilisateur

- `supervisor`

### Objectif

- separer ce qui peut entrer en production;
- tracer la decision.

### Donnees lues

- objet derive cible
- metadonnees IA
- prompt/regle version

### Donnees ecrites

- `human_validation_status`
- `audit_event`

### Validations

- impossible de "valider" sans trace auteur/date

---

## SCR-203 - Journal d'audit cible

### Role

Voir l'historique d'un objet sensible.

### Utilisateur

- `supervisor`
- `admin_tech` lecture adaptee

### Objectif

- comprendre qui a fait quoi;
- prouver;
- depanner.

### Donnees lues

- `audit_event`
- metadonnees objet

### Donnees ecrites

- aucune

---

## 6) Ecrans exclus du V1

Ces ecrans ne doivent pas etre ouverts maintenant.

### EX-01

Espace `research` visible ou pilotable dans l'application de production.

### EX-02

Portail praticiens commercial complet avec achat self-service de multiples plans.

### EX-03

Console d'analyse profonde client non gouvernee.

### EX-04

Visualisations complexes inter-seances ou scores proprietaires opaques.

### EX-05

Espace mineurs / parents et consentements associes.

---

## 7) Regles de navigation produit

### Regle 1

Le client public ne doit jamais voir l'architecture interne MERLIN ni la couche supervision.

### Regle 2

L'operateur ne doit pas travailler depuis la transcription brute comme ecran principal.

### Regle 3

La supervision ne doit pas re-ecrire silencieusement le passe; elle valide, rejette ou annote.

### Regle 4

Aucun ecran V1 ne doit presenter une lecture `research` comme un fait operatoire.

---

## 8) Etats globaux du parcours V1

### Parcours client

- `visit_started`
- `prequalification_started`
- `prequalification_completed`
- `consent_minimum_accepted`
- `client_minimum_created`
- `appointment_requested`
- `appointment_scheduled`

### Parcours seance

- `session_created`
- `session_in_progress`
- `session_completed_pending_note`
- `session_documented`
- `orientation_added`
- `document_generated`
- `document_delivered`

### Parcours supervision

- `ai_output_pending_review`
- `ai_output_validated`
- `ai_output_rejected`

---

## 9) Priorite de build des ecrans

Ordre recommande:

1. `SCR-001`
2. `SCR-002`
3. `SCR-003`
4. `SCR-004`
5. `SCR-006`
6. `SCR-101`
7. `SCR-102`
8. `SCR-103`
9. `SCR-105`
10. `SCR-106`
11. `SCR-107`
12. `SCR-108`
13. `SCR-104`
14. `SCR-109`
15. `SCR-201`
16. `SCR-202`
17. `SCR-203`

Logique:
- rendre le parcours facturable le plus vite possible;
- garder les ecrans sensibles pour apres stabilisation du coeur.

---

## 10) Ce que cette spec ferme

Cette spec ferme:
- la liste des ecrans V1;
- les roles d'acces;
- les parcours;
- les donnees lues/ecrites;
- les validations critiques;
- les transitions principales;
- les exclusions explicites.

Elle ouvre directement:
- le choix de stack front/back;
- le decoupage des routes;
- le plan de build UI;
- le calendrier de developpement.

---

## 11) Decision active

IVIA / MERLIN adopte cette spec ecrans V1 comme base de build du parcours client et operateur minimal.

Prochaine etape recommandee:
- figer la stack technique et le retroplanning de build.

References:
- [MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md)
- [MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md)
- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)
