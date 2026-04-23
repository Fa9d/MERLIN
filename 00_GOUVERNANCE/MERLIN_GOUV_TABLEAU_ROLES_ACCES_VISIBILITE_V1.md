# IVIA / MERLIN - Tableau roles / acces / visibilite V1

Date: 2026-04-22
Statut: actif
Objet: fixer quels roles existent, ce qu'ils peuvent voir, ce qu'ils peuvent faire, et ce qui doit rester invisible selon le role

---

## 1) Decision courte

MERLIN distingue des maintenant 3 niveaux differents:

1. `role applicatif`
2. `perimetre d'acces`
3. `visibilite documentaire`

La regle centrale est:

`avoir un compte ne donne pas un droit general de lecture`

et:

`un role technique, un role operatoire et un role de supervision ne doivent pas etre confondus`

---

## 2) Principe directeur

Le systeme doit separer:

- la `production`
- la `supervision`
- la `technique`
- la `diffusion client`
- la `gouvernance`

En consequence:

- l'operateur produit la relation et la trace utile;
- le superviseur relit, valide et arbitre les points sensibles;
- l'admin technique maintient la machine sans devenir lecteur clinique libre;
- le client ne voit que ce qui lui est explicitement destine;
- la gouvernance fixe les regles mais n'a pas a etre exposee comme role produit standard.

---

## 3) Roles retenus

## A. Roles applicatifs actifs V1

Les roles actuellement presents dans le backend sont:

- `public_client`
- `operator`
- `supervisor`
- `admin_tech`

## B. Roles de gouvernance ou d'evolution

Ces roles ou statuts existent deja comme besoin metier, mais pas encore comme enum applicatif autonome:

- `super_admin_gouvernance`
- `practitioner`

Regle:

`super_admin_gouvernance` n'est pas un simple super-utilisateur de backoffice.

C'est une autorite de regle, d'arbitrage et d'acces exceptionnel gouverne.

Et:

`practitioner` est un role futur de plateforme, distinct de `operator`.

Il ne doit pas etre simule durablement par un compte operateur.

---

## 4) Definition operative par role

| Role | Nature | Finalite | Exposition |
|---|---|---|---|
| `public_client` | role externe | demander, suivre, recevoir ce qui lui est destine | visible cote client |
| `operator` | role de production | intake, seance, note, orientation, continuite | non public |
| `supervisor` | role de controle qualite | revue de cas, validation, arbitrage documentaire sensible | non public |
| `admin_tech` | role technique | auth, incidents, maintenance, observabilite, securite | non public |
| `super_admin_gouvernance` | autorite de gouvernance | decision de politique, acces exceptionnel motive, audit de haut niveau | non expose comme role standard V1 |
| `practitioner` | role futur metier | usage pro de MERLIN, seances, documents, formation continue | non public au lancement |

---

## 5) Tableau principal des acces

| Domaine | `public_client` | `operator` | `supervisor` | `admin_tech` | `super_admin_gouvernance` | `practitioner` futur |
|---|---|---|---|---|---|---|
| Site public IVIA | lecture | lecture | lecture | lecture | lecture | lecture eventuelle |
| Formulaire d'entree / rendez-vous | creation de sa propre demande | lecture | lecture | non par contenu, oui par incident technique | lecture aggregatee ou ponctuelle motivee | non par defaut |
| Fiche client | lecture de sa propre fiche utile | lecture / mise a jour | lecture large | acces tres limite si incident | acces exceptionnel gouverne | lecture de ses propres clients seulement quand ce role existera |
| Consentements | lecture de ses consentements | creation / lecture utile | lecture / audit | metadonnees et integrite | arbitrage de politique | lecture de consentements de ses clients si applicable |
| Seances | lecture de ses propres seances et statuts utiles | creation / conduite / cloture | lecture / revue | metadonnees seulement sauf incident grave motive | acces exceptionnel gouverne | gestion de ses seances propres |
| Audio session in-app | jonction a sa propre seance si autorise | provision / conduite | lecture selon besoin de supervision | acces technique sur salle et enregistrement, pas lecture libre de contenu | acces exceptionnel gouverne | conduite de ses seances futures |
| Audio source brut | non | acces operatoire si necessaire | acces de revue si necessaire | acces technique restreint pour maintenance ou export encadre | acces exceptionnel motive et journalise | acces a ses propres seances seulement si le cadre le permet |
| Transcription brute | non | oui si utile a la note et a la continuite | oui | non par defaut | acces exceptionnel motive et journalise | oui pour ses propres seances futures selon cadre |
| Note operateur / note structuree | non par defaut | creation / lecture / mise a jour selon flux | lecture / validation | non par defaut | acces exceptionnel gouverne | lecture / creation de ses notes propres futures |
| Resume client diffusable | lecture de ses propres sorties | creation si marque diffusable | validation sensible possible | non | acces de controle | diffusion vers ses propres clients futurs |
| Hypotheses internes / derivees sensibles | non | oui si necessaire a la production | oui | non | oui sous cadre strict | oui pour ses dossiers futurs si le contrat et le cadre legal le permettent |
| Audit metier | non | lecture partielle utile | lecture large | lecture technique large | lecture large | non par defaut |
| Audit technique / logs / secrets | non | non | non sauf vue de conformite partielle | oui | oui si necessaire | non |
| Gestion utilisateurs internes | non | non | non | oui | arbitrage de droit, pas gestion manuelle quotidienne obligatoire | non |
| Export documentaire / transmission tiers | seulement ses documents remis | preparation selon mandat | validation sur cas sensibles | execution technique eventuelle, pas decision de fond | arbitrage exceptionnel | futur selon son perimetre |
| Recherche / apprentissage methode | non | non par defaut | selon mandat gouverne | non par contenu | oui sous gouvernance | futur eventuel, jamais par defaut |

---

## 6) Tableau de visibilite par objet

| Objet | Visible client | Visible operateur | Visible supervision | Visible admin technique | Visible gouvernance |
|---|---|---|---|---|---|
| Coordonnees du client | oui, les siennes | oui | oui | seulement si besoin technique legitime | oui si acces motive |
| Code client public | oui, le sien | oui | oui | oui si necessaire | oui |
| Motif libre d'entree | partiellement si restitue | oui | oui | non par defaut | oui si acces motive |
| Niveau de vigilance interne | version simplifiee seulement si utile | oui | oui | non | oui si acces motive |
| Audio brut | non | oui si necessaire | oui si necessaire | acces restreint | oui si acces exceptionnel journalise |
| Transcription brute | non | oui | oui | non par defaut | oui si acces exceptionnel journalise |
| Note brute operateur | non | oui | oui | non | oui si acces motive |
| Note `client_visible` | oui | oui | oui | non | oui |
| Commentaire de supervision | non | non par defaut | oui | non | oui |
| Journal d'audit | non | partiel | oui | oui | oui |
| Secrets, tokens, configuration | non | non | non | oui | oui |

---

## 7) Regles d'acces par role

## A. `public_client`

Le client peut:

- creer une demande d'entree;
- consulter ses informations utiles;
- rejoindre sa propre seance si le flux l'autorise;
- voir ses sorties explicitement diffusees;
- consulter ses statuts, rendez-vous, confirmations et prochaines etapes.

Le client ne peut pas voir:

- transcription brute;
- note brute;
- hypothese interne;
- commentaire de supervision;
- logique interne de classement ou de risque;
- audit;
- autres clients;
- identite interne des operateurs non necessaire.

## B. `operator`

L'operateur peut:

- lire la fiche client utile;
- creer et conduire une seance;
- acceder a l'audio rattache a la seance;
- lire la transcription utile;
- produire une note structuree;
- marquer certaines sorties comme diffusables;
- consulter l'historique utile de production.

L'operateur ne doit pas avoir:

- acces libre aux secrets techniques;
- acces libre aux journaux techniques complets;
- acces libre aux dossiers hors besoin operatoire reel;
- acces automatique aux commentaires de supervision;
- acces research par defaut.

## C. `supervisor`

Le superviseur peut:

- relire les cas;
- consulter transcription, audio, note et derivees utiles;
- valider ou invalider certaines sorties sensibles;
- consulter l'audit metier;
- arbitrer certains cas limites de diffusion ou d'escalade.

Le superviseur ne doit pas:

- gerer les secrets et l'infrastructure comme un admin technique;
- devenir un role de production courant sur tous les dossiers;
- disposer d'une lecture globale non justifiee si la supervision est ciblee par lot, file ou signal.

## D. `admin_tech`

L'admin technique peut:

- creer des utilisateurs internes selon la logique V1;
- maintenir l'authentification;
- voir les statuts, journaux, integrations et incidents;
- intervenir sur les ressources de stockage, audio, files et disponibilite.

L'admin technique ne doit pas:

- lire librement les contenus sensibles comme s'il etait superviseur;
- consulter par confort les transcriptions;
- exploiter les notes operateur comme matiere clinique;
- exporter des contenus sensibles sans mandat et traque d'audit.

## E. `super_admin_gouvernance`

La gouvernance peut:

- fixer les politiques;
- autoriser certains acces exceptionnels;
- revoir des cas ou ensembles de cas selon base legitime;
- controler la conformite des droits accordes;
- auditer les usages et les ecarts.

Mais:

- cet acces doit etre `rare`, `motive`, `journalise`, `revocable`;
- il ne doit pas devenir un pretexte pour contourner les separations de roles du produit.

## F. `practitioner` futur

Le praticien doit a terme pouvoir:

- gerer ses propres clients et seances;
- produire ses propres notes;
- acceder a ses propres transcriptions;
- recevoir certains modules de supervision ou de formation continue;
- ne jamais voir les dossiers MERLIN internes qui ne lui appartiennent pas.

Regle:

`practitioner` sera un tenant metier distinct, pas un operateur MERLIN rebaptise.

---

## 8) Regles de visibilite produit

### A. Navigation publique

Ne doivent pas etre visibles en facade publique:

- la supervision;
- l'administration technique;
- la recherche;
- le portail praticien au lancement;
- les ecrans MERLIN internes de production.

Doivent etre visibles en facade publique:

- l'offre IVIA client;
- la prise de rendez-vous;
- les limites du service;
- les tarifs;
- les acces client si actives.

### B. Backoffice production

Le backoffice production doit montrer a l'operateur:

- seulement ce qui aide a la prise en charge;
- l'historique utile;
- les consentements utiles;
- la note de cloture et la suite.

Il ne doit pas montrer par defaut:

- les couches de supervision;
- les commentaires internes de validation;
- les consoles techniques;
- les journaux bas niveau.

### C. Supervision

La supervision doit etre une couche distincte de la production.

Elle sert a:

- relire;
- arbitrer;
- valider;
- auditer.

Elle ne doit pas contaminer l'ecran principal de production.

### D. Administration technique

L'administration technique doit etre separee des ecrans metier.

Un meme utilisateur peut cumuler des prerogatives a titre transitoire,
mais pas dans la meme interface sans distinction nette de contexte.

---

## 9) Regles d'implementation

Avant d'ouvrir un endpoint, un ecran ou un export, verifier:

1. `qui en a reellement besoin ?`
2. `voit-il de la source brute ou une sortie filtree ?`
3. `cet acces releve-t-il de la production, de la supervision ou de la technique ?`
4. `l'action est-elle journalisee ?`
5. `la meme chose pourrait-elle etre faite avec moins de visibilite ?`

Si la reponse a la question 5 est oui:

- il faut reduire l'acces.

---

## 10) Ecart actuel entre cible et code V1

Le code actuel montre deja une separation de roles minimale,
mais il reste plus large que la cible de gouvernance.

Etat constate:

- beaucoup de routes internes acceptent encore indistinctement `operator`, `supervisor` et `admin_tech`;
- `admin_tech` peut aujourd'hui acceder a plusieurs operations metier pour des raisons de bootstrap et de dev;
- `supervisor` n'a pas encore de couche de droits plus fine que la production;
- `public_client` existe comme role enum, mais sa surface d'application authentifiee reste encore faible;
- `practitioner` et `super_admin_gouvernance` ne sont pas encore modelises comme roles applicatifs.

Decision active:

`le document de gouvernance fait foi sur la cible`

et:

`le code devra converger vers cette cible, pas l'inverse`

---

## 11) Consequences produit immediates

A partir de cette note:

- les ecrans `operator`, `supervision` et `admin` doivent etre penses comme trois couches distinctes;
- toute future route de lecture de transcription, d'audio ou de note doit expliciter le role attendu;
- `client_visible` devient un vrai verrou de diffusion, pas un simple champ decoratif;
- le portail praticien futur doit etre concu comme perimetre separe;
- la gouvernance n'autorise pas un role technique a devenir lecteur clinique par commodite.

---

## 12) Decision active

MERLIN retient a compter de cette note:

- une separation nette entre production, supervision, technique, diffusion client et gouvernance;
- un client limite aux sorties qui lui sont explicitement destinees;
- un operateur centre sur la prise en charge et la trace utile;
- un superviseur centre sur la validation et l'arbitrage;
- un admin technique centre sur la machine, pas sur la lecture clinique libre;
- un futur role praticien distinct de l'operateur MERLIN;
- une convergence progressive du code vers cette matrice d'acces.

---

## 13) References

- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)
- [MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md)
- [MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md)
- [MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md)
- [enums.py](C:/MERLIN/10_backend_merlin_api/app/models/enums.py)
