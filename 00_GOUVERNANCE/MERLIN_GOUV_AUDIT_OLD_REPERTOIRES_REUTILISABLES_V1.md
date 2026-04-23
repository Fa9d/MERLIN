# Audit des repertoires OLD reutilisables pour MERLIN V1

Date: 2026-04-21
Statut: travail
Objet: identifier dans `C:\Users\PC\Desktop\OLD` ce qui peut etre rapatrie dans `C:\MERLIN` sans recreer la dispersion historique

---

## 1) Conclusion executive

Oui, `C:\Users\PC\Desktop\OLD` contient des elements utiles.

Mais il ne faut pas tout rapatrier.

La bonne logique est:
- rapatrier seulement les briques techniques ou conceptuelles directement reutilisables;
- laisser de cote les archives de projets non lies, les medias bruts, les environnements locaux et les dependances vendorees;
- reconstruire le systeme MERLIN dans `C:\MERLIN` avec une architecture propre, puis y injecter seulement les morceaux valides.

---

## 2) Repertoire le plus interessant

### Source prioritaire

`C:\Users\PC\Desktop\OLD\MESANGE\IVIA-cercle\Fa9d\backend\api`

Constat:
- c'est le seul backend Python encore coherent et lisible;
- il contient un vrai squelette FastAPI;
- il contient une logique de services separee;
- il contient auth, repository, settings, scripts de seed et tests;
- il confirme qu'une architecture backend Python separee du frontend a deja existe en pratique.

Fichiers notables:
- `main.py`
- `repository.py`
- `services.py`
- `auth.py`
- `settings.py`
- `init_db.py`
- `seed_demo.py`
- `requirements.txt`
- `test_main.py`

Limites:
- oriente `IVIA-EMPLOI`, pas MERLIN soins;
- persistance MVP en SQLite, pas en PostgreSQL de production;
- modele de donnees trop simple pour le perimetre MERLIN;
- nomenclature et endpoints a refondre.

Decision:
- ne pas le reutiliser tel quel;
- s'en servir comme base de patterns backend Python:
  - structure FastAPI;
  - separation `main / services / repository / auth / settings`;
  - runbooks et tests de smoke.

---

## 3) Repertoires secondaires utiles comme reference

### `C:\Users\PC\Desktop\OLD\vibratoire`

Utilite:
- interessant comme archive d'intentions produit;
- plusieurs objets metier proches de MERLIN y apparaissent:
  - client;
  - praticien;
  - seance;
  - recording;
  - note;
  - document;
  - roles.

Interet principal:
- documentation d'architecture;
- schemas d'interfaces et parcours;
- idees de separation des roles;
- experimentation autour de l'audio et de l'analyse.

Faiblesses:
- stack heterogene et instable:
  - Laravel/PHP;
  - Vue;
  - scripts Python adjacents;
  - legacy partout;
- naming et cadrage trop "vibratoire" ou holistique pour le positionnement actuel;
- beaucoup de dette technique et de duplication;
- pas une base saine a cloner dans MERLIN.

Decision:
- ne pas importer le projet;
- relire seulement certains documents et quelques noms d'objets metier;
- ne reprendre que des idees, pas le code applicatif principal.

### `C:\Users\PC\Desktop\OLD\VIDEO\EASEUS`

Utilite:
- scripts Python autour de:
  - extraction audio;
  - transcription;
  - traitement de sorties texte;
  - automatisation media.

Interet:
- utile pour inspirer un futur sous-module de preparation audio/transcription;
- peut fournir des morceaux de script ou des hypotheses de pipeline.

Limites:
- oriente media generaliste, pas dossier client sensible;
- pas integre a un cadre donnees / consentements / seances MERLIN.

Decision:
- reference technique seulement;
- a reevaluer quand on branchera le pipeline audio.

---

## 4) Repertoires a faible valeur pour MERLIN

### `C:\Users\PC\Desktop\OLD\MESANGE\ivia\backend`

Constat:
- ne contient plus le coeur du code;
- surtout des tests, des fichiers d'environnement, des bases SQLite et un `requirements.txt`.

Decision:
- faible valeur de rapatriement;
- garder seulement comme trace historique.

### `C:\Users\PC\Desktop\OLD\Dev\ivia-app`

Constat:
- ensemble volumineux et melange;
- plusieurs sous-projets differents;
- nombreux restes frontend/backend non alignes avec MERLIN;
- risque fort de reimporter la confusion que nous essayons justement d'eviter.

Decision:
- ne pas utiliser comme base.

### `C:\Users\PC\Desktop\OLD\Dev\TBO\web`

Constat:
- projet Next.js/Prisma mais non lie au coeur MERLIN;
- utile seulement pour quelques patterns techniques generiques.

Decision:
- ne pas rapatrier.

### Dossiers personnels, archives, medias, recherches

Exemples:
- `BS-EMPLOI`
- `TOME I`
- `Qc I`
- `ANALYSE`
- `Enregistrements audio`
- `Pickelball`
- `COMBINATOIRE`

Decision:
- hors perimetre produit MERLIN;
- ne rien importer dans le socle applicatif.

---

## 5) Ce qu'il faut rapatrier en pratique

### A importer dans MERLIN sous forme d'archive technique referencee

Depuis `C:\Users\PC\Desktop\OLD\MESANGE\IVIA-cercle\Fa9d\backend\api`:
- `main.py`
- `repository.py`
- `services.py`
- `auth.py`
- `settings.py`
- `init_db.py`
- `seed_demo.py`
- `requirements.txt`
- `README.md`
- `test_main.py`
- `smoke_test_api.py`
- `smoke_e2e_api.py`

Destination recommandee:
- `C:\MERLIN\_ARCHIVES_IMPORT\2026-04-21_old_mesange_ivia_backend_api\`

But:
- conserver la reference technique;
- permettre une lecture comparative;
- eventuellement reextraire certains patterns dans le nouveau backend MERLIN.

### A importer eventuellement plus tard

Depuis `C:\Users\PC\Desktop\OLD\VIDEO\EASEUS`:
- scripts de transcription;
- scripts d'extraction audio;
- notes de cout ou de workflow.

Destination recommandee:
- `C:\MERLIN\_ARCHIVES_IMPORT\2026-04-21_old_video_easeus\`

Condition:
- seulement au moment ou on attaque la brique audio.

---

## 6) Ce qu'il ne faut surtout pas faire

- ne pas copier des projets entiers avec `node_modules`, `.venv`, `vendor`, caches et bases locales;
- ne pas repartir d'un projet legacy complet;
- ne pas laisser MERLIN dependre d'un ancien repertoire `Desktop\\OLD`;
- ne pas melanger les anciens noms de produits avec la nouvelle architecture IVIA/MERLIN.

---

## 7) Decision recommandee

Decision de travail:

`MERLIN reste le seul workspace maitre.`

`Nous pouvons importer des fragments choisis de l'ancien travail, mais uniquement comme archive technique ou reference de migration.`

`Le seul candidat serieux a une reutilisation partielle immediate est l'ancien backend Python situe dans MESANGE\\IVIA-cercle\\Fa9d\\backend\\api.`

---

## 8) Prochaine action recommande e

1. Creer un dossier d'archives d'import dans `C:\MERLIN`.
2. Y copier uniquement le backend Python utile.
3. Comparer sa structure a notre scaffold actuel.
4. Decider du backend final MERLIN:
   - FastAPI Python pour le coeur metier et IA;
   - Next.js pour le frontend.
5. Puis reconstruire le premier slice reel dans `C:\MERLIN`.
