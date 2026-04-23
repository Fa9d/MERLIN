# IVIA / MERLIN - Backlog d'implementation roles / acces / visibilite V1

Date: 2026-04-22
Statut: actif
Objet: traduire la matrice de gouvernance des roles et acces en chantiers techniques concrets pour le backend et le backoffice

---

## 1) But

Ce document sert a eviter un ecart durable entre:

- la gouvernance cible;
- le backend actuel;
- les ecrans actuels.

Il ne redefinit pas la politique.

Il dit:

- `quoi corriger`
- `dans quel ordre`
- `avec quel niveau de priorite`

---

## 2) Constat de depart

L'etat V1 actuel est fonctionnel pour developer vite,
mais il est encore trop large en matiere de droits.

Constats principaux:

1. beaucoup de routes backend acceptent encore ensemble `operator`, `supervisor`, `admin_tech`;
2. l'ecran `/operator` concentre aujourd'hui du bootstrap, de la production, de l'audio et du test client;
3. `public_client` existe comme role enum, mais sans vraie surface authentifiee stabilisee;
4. la supervision existe comme intention produit, mais pas encore comme couche de droits differenciee;
5. `admin_tech` reste proche d'un compte passe-partout de build;
6. le role `practitioner` n'est pas encore modelise.

---

## 3) Decision d'execution

L'ordre retenu est:

1. `resserrer les permissions backend`
2. `separer les interfaces`
3. `ouvrir une vraie surface client`
4. `preparer le role praticien`

Regle:

`on ne cree pas de nouveaux roles visibles avant d'avoir ferme les frontieres des roles existants`

---

## 4) Tableau des ecarts prioritaires

| Ecart | Risque | Priorite | Decision |
|---|---|---|---|
| `admin_tech` voit trop large sur les routes metier | confusion technique / clinique | critique | reduire l'acces par route et par objet |
| `operator` et `supervisor` partagent presque les memes droits | supervision fictive | critique | separer droits de production et de validation |
| `/operator` melange bootstrap admin, production, audio et tests | contamination des contextes | haute | decouper les ecrans |
| `client-join` est genere depuis une route interne | absence de vrai flux client gouverne | haute | creer un flux client dedie |
| absence de surface authentifiee `public_client` | role non reel en produit | haute | ouvrir un mini espace client V1 |
| absence de filtrage par ownership ou contexte | lecture potentiellement trop large | haute | introduire des filtres de perimetre |
| `client_visible` existe mais sans workflow de validation | diffusion encore faible en gouvernance | moyenne | poser un statut documentaire plus clair |
| role `practitioner` non modelise | dette d'architecture pro | moyenne | preparer sans activer publiquement |

---

## 5) Chantiers backend

## B-01 - Creer des dependances de roles plus fines

Probleme:

La plupart des routes utilisent directement:

- `require_roles(AppRole.operator, AppRole.supervisor, AppRole.admin_tech)`

Action:

- creer des dependances nommees du type:
  - `require_production_roles()`
  - `require_supervision_roles()`
  - `require_admin_tech()`
  - `require_internal_clinical_roles()`

But:

- rendre le code lisible;
- eviter les triples listes repetees;
- rendre le durcissement progressif plus simple.

Priorite:

`critique`

## B-02 - Resserer `admin_tech` sur les routes metier

Routes concernees en premier:

- `clients`
- `sessions`
- `session-notes`
- `consents`
- `audio-sessions`
- `audio-recordings`

Action:

- retirer `admin_tech` des routes de lecture de contenu sensible quand ce n'est pas necessaire;
- ne lui laisser que:
  - auth;
  - health;
  - monitoring;
  - gestion utilisateurs;
  - incidents techniques;
  - operations techniques justifiees sur audio et stockage.

But:

- empecher qu'un admin technique devienne lecteur clinique par defaut.

Priorite:

`critique`

## B-03 - Distinguer production et supervision

Probleme:

`supervisor` peut aujourd'hui agir presque comme `operator`.

Action:

- revoir route par route:
  - ce qui releve de la creation / conduite de seance = `operator`
  - ce qui releve de la relecture / validation / audit = `supervisor`
- ajouter des endpoints de supervision distincts si necessaire,
  plutot que d'utiliser les routes de production pour tout.

Exemples:

- `POST /sessions` = `operator` d'abord
- `POST /sessions/{id}/close` = `operator`, avec futur point de validation supervision si besoin
- `GET /session-notes` sensible = `operator` ou `supervisor` selon contexte
- futurs endpoints de validation = `supervisor`

Priorite:

`critique`

## B-04 - Introduire un perimetre de lecture

Probleme:

Les listes sont aujourd'hui larges par defaut.

Action:

- preparer des filtres ou regles de scope:
  - dossiers assignes a l'operateur;
  - file active;
  - client cible;
  - lot de supervision;
  - incident technique cible.

But:

- passer d'un acces par role seul a un acces par role + perimetre.

Priorite:

`haute`

## B-05 - Creer une surface `public_client` reelle

Action:

- creer des routes client authentifiees minimales:
  - lecture de sa fiche utile
  - lecture de ses rendez-vous
  - lecture de ses notes ou resumes diffusables
  - jonction a sa propre seance audio

Interdit:

- exposer transcription brute;
- exposer note brute;
- exposer hypothese interne.

Priorite:

`haute`

## B-06 - Sortir `client-join` du flux interne test

Probleme:

La route `client-join` est aujourd'hui appelee depuis l'espace operateur pour generer un lien local de test.

Action:

- conserver le test local si necessaire, mais le marquer explicitement comme `dev only`;
- preparer un vrai endpoint client relie a:
  - son identite;
  - sa seance;
  - son autorisation temporelle;
  - son consentement.

Priorite:

`haute`

## B-07 - Durcir l'enregistrement et l'audio

Action:

- distinguer:
  - droit de provision audio
  - droit de rejoindre comme operateur
  - droit de rejoindre comme client
  - droit de demarrer / arreter un enregistrement
- journaliser ces actions comme evenements sensibles.

Priorite:

`haute`

## B-08 - Poser un vrai workflow de diffusion client

Probleme:

`client_visible` est un bon verrou, mais encore trop binaire pour la suite.

Action:

- conserver `client_visible` en V1;
- ajouter ensuite un statut ou workflow documentaire du type:
  - `internal_only`
  - `prepared_for_client`
  - `validated_for_client`
  - `delivered_to_client`

But:

- ne pas assimiler marquage de diffusion et diffusion effective.

Priorite:

`moyenne`

## B-09 - Preparer le role `practitioner`

Action:

- ne pas l'activer maintenant en public;
- mais preparer:
  - enum ou modele futur;
  - contraintes de perimetre;
  - separation de tenant;
  - objets qu'un praticien peut posseder.

Priorite:

`moyenne`

---

## 6) Chantiers frontend

## F-01 - Scinder `/operator`

Probleme:

La page actuelle melange:

- bootstrap admin;
- connexion;
- creation de seance;
- audio;
- test client;
- cloture;
- lecture de notes.

Action:

- garder temporairement une page unique si necessaire pour dev;
- mais viser rapidement:
  - `/operator`
  - `/supervision`
  - `/admin`
  - `/client` ou espace client equivalent

Priorite:

`critique`

## F-02 - Sortir le bootstrap admin de l'ecran operateur

Probleme:

L'ecran de connexion operateur contient encore la creation initiale de l'`admin_tech`.

Action:

- conserver le bootstrap comme procedure de dev ou page admin technique temporaire;
- ne pas le laisser comme partie normale du backoffice operateur.

Priorite:

`haute`

## F-03 - Cacher les fonctions dev/test du flux operateur standard

Probleme:

Le lien client test et certains flux audio sont utiles au build,
mais ne doivent pas rester dans le flux operateur final.

Action:

- placer ces actions sous condition de dev;
- ou les deplacer dans un panneau technique.

Priorite:

`haute`

## F-04 - Creer un espace supervision minimal

Action:

- transformer `/supervision` en vraie couche de travail:
  - file de cas a relire
  - revue de note
  - validation de sorties sensibles
  - lecture d'audit metier utile

Priorite:

`moyenne`

## F-05 - Creer un espace client minimal

Action:

- proposer un premier espace `public_client` avec:
  - rendez-vous
  - statuts
  - acces a la seance
  - resumes diffuses

Priorite:

`haute`

---

## 7) Ordre d'implementation recommande

### Sprint A - Verrou critique

Objectif:

- fermer les plus gros ecarts sans casser le cycle V1.

Contenu:

1. B-01 dependances de roles plus fines
2. B-02 reduction de `admin_tech` sur routes metier
3. B-03 distinction initiale `operator` / `supervisor`
4. F-02 sortie du bootstrap admin hors flux operateur
5. F-03 masquage des outils dev/test dans l'interface operateur

### Sprint B - Surface client reelle

Objectif:

- rendre `public_client` reel dans le produit.

Contenu:

1. B-05 routes client authentifiees minimales
2. B-06 vrai flux client `join`
3. F-05 espace client minimal

### Sprint C - Consolidation de gouvernance

Objectif:

- rendre la supervision et la diffusion plus propres.

Contenu:

1. B-04 scope de lecture
2. B-07 journalisation audio sensible
3. B-08 workflow de diffusion
4. F-04 espace supervision minimal

### Sprint D - Preparation plateforme pro

Objectif:

- preparer la suite sans l'ouvrir trop tot.

Contenu:

1. B-09 role `practitioner`
2. separation de tenant
3. surfaces pro futures

---

## 8) Ce qu'il ne faut pas faire maintenant

Interdits de sequence:

- ouvrir publiquement le role `practitioner` avant fermeture de `public_client`;
- complexifier le role `super_admin_gouvernance` dans le code avant d'avoir resserre `admin_tech`;
- lancer une UI admin finale avant d'avoir decide les scopes;
- multiplier les permissions fines par objet si les grandes frontieres par role ne sont pas encore fermees.

Formule de controle:

`on ferme d'abord les frontieres macro, puis on affine les exceptions`

---

## 9) Definition de termine

Le chantier roles / acces / visibilite sera considere comme suffisamment ferme en V1 quand:

1. `admin_tech` ne pourra plus lire librement les contenus cliniques;
2. `operator` et `supervisor` auront des differences reelles dans le code;
3. le client aura une surface authentifiee minimale;
4. l'audio client passera par un flux client gouverne;
5. les interfaces `operator`, `supervision` et `admin` seront distinctes au moins dans leur intention et leur navigation;
6. la diffusion client reposera sur autre chose qu'un simple affichage opportuniste.

---

## 10) Decision active

MERLIN retient a compter de cette note:

- le prochain chantier produit transverse porte sur la convergence des roles et acces;
- cette convergence commence par le backend, puis se prolonge dans les ecrans;
- le role `public_client` doit devenir reel avant l'ouverture praticien;
- `admin_tech` doit perdre son caractere de role universel de build.

---

## 11) References

- [MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md)
- [MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md)
- [MERLIN_GOUV_SPEC_WORKFLOW_DIFFUSION_CLIENT_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_WORKFLOW_DIFFUSION_CLIENT_V1.md)
- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)
- [auth.py](C:/MERLIN/10_backend_merlin_api/app/api/routes/auth.py)
- [clients.py](C:/MERLIN/10_backend_merlin_api/app/api/routes/clients.py)
- [sessions.py](C:/MERLIN/10_backend_merlin_api/app/api/routes/sessions.py)
- [session_notes.py](C:/MERLIN/10_backend_merlin_api/app/api/routes/session_notes.py)
- [audio_sessions.py](C:/MERLIN/10_backend_merlin_api/app/api/routes/audio_sessions.py)
- [audio_recordings.py](C:/MERLIN/10_backend_merlin_api/app/api/routes/audio_recordings.py)
- [page.tsx](C:/MERLIN/09_app_ivia_merlin/src/app/operator/page.tsx)
