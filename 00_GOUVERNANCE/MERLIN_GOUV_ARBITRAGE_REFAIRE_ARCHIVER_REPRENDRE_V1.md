# MERLIN - Arbitrage refaire, archiver, reprendre V1

Date: 2026-04-21
Statut: decision de travail
Objet: trancher explicitement ce qui doit etre refait, ce qui doit etre archive et ce qui peut etre repris partiellement depuis les anciens travaux

---

## 1) Decision directrice

MERLIN ne sera pas reconstruit a partir d'un projet legacy.

MERLIN sera:
- redeveloppe proprement dans `C:\MERLIN`;
- alimente par des decisions de gouvernance deja fermees;
- enrichi seulement par des fragments anciens choisis et archives.

Formule simple:

`on refait le systeme, pas la confusion`

---

## 2) Pourquoi cette decision

Les anciens travaux ont une vraie valeur.

Mais cette valeur se trouve surtout dans:
- les intuitions produit;
- certains objets metier;
- quelques structures techniques;
- des tests d'architecture deja rencontres;
- des tentatives qui montrent ce qu'il faut eviter.

Leur faiblesse commune est plus importante que leur interet comme base:
- trop de projets melanges;
- trop de stacks differentes;
- trop de noms de produits ou de concepts instables;
- trop de dette technique;
- trop de dependances locales;
- trop d'historique implicite non gouverne.

Si on repart de ces bases comme produit vivant:
- on gagne un peu de temps maintenant;
- on perd beaucoup de temps ensuite en nettoyage, incoherence et regressions.

---

## 3) Ce qu'on jette comme base executable

On ne jette pas l'idee.
On jette leur statut de base de production.

Cela concerne notamment:
- `vibratoire` comme base applicative;
- `Dev\\ivia-app` comme base applicative;
- `Dev\\TBO\\web` comme base applicative;
- les projets Pickelball / Combinatoire / archives diverses;
- les dossiers contenant `node_modules`, `.venv`, `vendor`, caches, bases locales et scripts de circonstance.

Regle:

`aucun ancien projet ne devient le nouveau coeur MERLIN`

---

## 4) Ce qu'on archive

On archive ce qui peut servir de:
- reference technique;
- reference metier;
- preuve de cheminement;
- source de migration partielle.

### A archiver en priorite

Depuis `C:\Users\PC\Desktop\OLD\MESANGE\IVIA-cercle\Fa9d\backend\api`:
- structure FastAPI;
- `auth.py`
- `repository.py`
- `services.py`
- `settings.py`
- `init_db.py`
- scripts de seed;
- smoke tests;
- README et runbooks.

### A archiver comme reference produit et audio

Depuis `C:\Users\PC\Desktop\OLD\vibratoire`:
- documents d'architecture;
- schemas de roles;
- idees de parcours client / praticien;
- nomenclature de certains objets proches du metier.

Depuis `C:\Users\PC\Desktop\OLD\VIDEO\EASEUS`:
- scripts d'extraction audio;
- scripts de transcription;
- notes pratiques sur les traitements media.

Regle:

`l'archive sert a consulter et a extraire, pas a lancer en production`

---

## 5) Ce qu'on reprend partiellement

### Patterns backend

On peut reprendre:
- la separation `main / services / repository / auth / settings`;
- les scripts de smoke;
- la discipline de seed demo;
- certains patterns de structuration FastAPI.

### Patterns metier

On peut reprendre:
- la distinction des roles;
- l'idee de dossier client;
- l'idee de seance, note, document, recording;
- certaines hypotheses de parcours client / praticien.

### Patterns audio

On peut reprendre plus tard:
- des scripts de preparation audio;
- des sequences de transcription;
- des essais d'automatisation media.

Condition absolue:

`tout element repris doit etre renomme, recadre et revalide dans la doctrine MERLIN`

---

## 6) Ce qu'on redevelloppe entierement

### Backend coeur MERLIN

A refaire:
- modele de donnees V1;
- schema PostgreSQL;
- auth et roles MERLIN;
- endpoints metier reels;
- journal d'audit;
- couche consentements;
- couche sessions;
- couche documents derives;
- pipeline de derivation gouvernee.

### Frontend

A refaire:
- site public IVIA;
- parcours client;
- espace operateur;
- espace supervision;
- experience praticien seulement si elle reste dans le perimetre V1 retenu.

### Couche IA

A refaire proprement:
- prompts;
- chaine transcription -> extraction -> resume -> orientation;
- validations;
- statuts de revue;
- objets derives.

### Infrastructure

A refaire proprement:
- variables d'environnement;
- services dev/test/prod;
- stockage;
- sauvegardes;
- monitoring;
- jobs asynchrones.

---

## 7) Ordre optimal de redevelopment

### Etape 1 - Fermer l'arbitrage technique

On valide:
- `MERLIN = workspace maitre`
- `frontend = Next.js`
- `backend coeur = Python / FastAPI`
- `BDD = PostgreSQL`
- pas de reprise d'un ancien projet comme socle vivant.

### Etape 2 - Importer seulement les references utiles

On cree un dossier d'archives dans `C:\MERLIN` et on y copie seulement:
- le backend Python utile;
- quelques documents vibratoire;
- eventuellement les scripts audio de reference.

### Etape 3 - Generer l'ossature propre

On cree:
- backend MERLIN neuf;
- schema de donnees neuf;
- conventions de dossiers;
- config d'environnement;
- premiere migration.

### Etape 4 - Coder le premier slice reel

Ordre recommande:
1. `client`
2. `intake_request`
3. `consent`
4. `session`
5. `session_note`

### Etape 5 - Ouvrir le parcours facturable minimum

On doit pouvoir:
- recevoir une demande;
- creer une fiche;
- enregistrer un consentement;
- produire une seance;
- sortir une note simple.

### Etape 6 - Brancher ensuite la valeur IA

Seulement apres existence du noyau:
- transcription;
- resume;
- historique court;
- orientation prudente;
- documents derives.

---

## 8) Ce qu'il ne faut plus faire

- changer de socle tous les deux jours;
- reouvrir des anciens projets comme s'ils etaient le futur coeur;
- confondre archive utile et base saine;
- remettre le cadrage structurel a plus tard;
- faire du design ou du discours comme substitut au build systeme;
- empiler des idees hors perimetre avant le noyau facturable.

---

## 9) Position nette

Si la question est:

`est-ce que l'ancien travail est vraiment interessant ?`

La reponse est:

`oui comme memoire technique et comme matiere premiere`

Si la question est:

`est-ce qu'il faut repartir de lui ?`

La reponse est:

`non`

Si la question est:

`est-ce qu'il faut tout refaire ?`

La reponse exacte est:

`il faut tout redevelopper proprement, sans tout reimaginer`

---

## 10) Decision active

MERLIN adopte la discipline suivante:

- nous refaisons le systeme de production;
- nous archivons les anciens travaux utiles;
- nous reprenons seulement des patterns, jamais des blocs legacy non gouvernes;
- nous construisons le nouveau coeur directement dans `C:\MERLIN`.
