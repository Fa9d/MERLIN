# MERLIN - Politique sauvegarde et restauration V1

Date: 2026-04-27
Statut: actif
Objet: fixer une strategie canonique de sauvegarde, de repli et de restauration pour MERLIN

---

## 1) Decision courte

MERLIN adopte une strategie de sauvegarde `3-2-1`:

- `3` copies utiles;
- `2` supports distincts;
- `1` copie hors serveur principal.

La regle operative est:

`Git ne suffit pas.`

Le code, la base, les enregistrements audio, les documents derives et les secrets n'ont pas le meme regime de sauvegarde.

---

## 2) Couches a proteger

### A. Code et configuration versionnee

Exemples:

- depot Git MERLIN;
- scripts de deploiement;
- gouvernance;
- migrations Alembic;
- templates nginx et systemd.

Objectif:

- pouvoir reconstituer le code source exact;
- pouvoir redemarrer un environnement propre;
- pouvoir auditer les changements.

### B. Donnees applicatives

Exemples:

- PostgreSQL;
- clients;
- intakes;
- sessions;
- notes;
- documents derives;
- objets audio en base.

Objectif:

- restaurer l'etat metier;
- ne pas perdre l'historique utile;
- conserver la tracabilite.

### C. Fichiers sensibles hors base

Exemples:

- enregistrements audio `.ogg`;
- exports ou archives de restauration;
- eventuels artefacts de transmission ou de reprise.

Objectif:

- ne pas perdre les sources audio necessaires a la continuite ou a l'audit;
- conserver une copie hors VPS.

### D. Secrets et acces

Exemples:

- `.env.prod`;
- cles SSH;
- credentiels techniques;
- runbooks d'acces.

Objectif:

- restaurer l'exploitation;
- ne pas bloquer la reprise pour une simple perte d'acces.

---

## 3) Supports obligatoires

MERLIN doit maintenir en parallele:

- un depot Git distant;
- un miroir Git local;
- une copie locale de travail;
- un disque dur externe chiffre;
- des sauvegardes VPS hors du repertoire applicatif;
- idealement une copie hors site supplementaire.

Pour V1, le minimum non negociable est:

- `Git distant + miroir local + disque externe chiffre + backups VPS`.

---

## 4) Regles par type de donnee

### A. Code

Sauvegarde requise:

- push Git regulier;
- miroir Git local mis a jour au minimum une fois par semaine;
- copie du miroir ou d'une archive sur disque externe au minimum une fois par semaine.

### B. Base PostgreSQL

Sauvegarde requise:

- dump quotidien automatise;
- conservation locale VPS en repertoire dedie;
- copie reguliere hors VPS;
- verification hebdomadaire qu'un dump est lisible et recent.

### C. Enregistrements audio

Sauvegarde requise:

- archive quotidienne ou apres sessions critiques;
- copie hors VPS;
- copie sur disque externe chiffre si conservation autorisee.

Regle:

`une sauvegarde audio ne doit jamais etre posee en clair sur un support nomade non chiffre`

### D. Secrets

Sauvegarde requise:

- copie separee du code;
- coffre ou emplacement restreint;
- jamais dans Git;
- verification d'acces apres tout changement majeur.

---

## 5) Frequence minimale

### Quotidien

- dump PostgreSQL;
- backup des enregistrements audio;
- verification sommaire que les scripts ont produit un fichier date.

### Hebdomadaire

- mise a jour du miroir Git local;
- copie sur disque externe chiffre;
- controle manuel des dates de backup;
- verification des checksums;
- test de restauration minimal sur un echantillon.

### Mensuel

- exercice de restauration plus complet;
- verification que la documentation de reprise est encore juste;
- revue des supports physiques et de leur acces.

---

## 6) Exigence de test

Une sauvegarde non testee n'est pas consideree comme fiable.

Le minimum hebdomadaire est:

- verifier qu'un dump PostgreSQL se decompresse;
- verifier qu'une archive audio se liste;
- verifier que le miroir Git local peut etre lu;
- verifier qu'une restauration partielle reste faisable.

---

## 7) Repli local

MERLIN doit pouvoir repartir localement si le VPS est indisponible.

Le repli local minimal suppose:

- code local a jour;
- miroir Git local a jour;
- dump PostgreSQL recent;
- archive audio recente;
- secrets exploitables;
- stack Docker locale capable de remonter le service.

Regle:

`le local n'est pas seulement un espace de dev. C'est aussi un point de reprise.`

---

## 8) Disque externe

Le disque externe est obligatoire comme support de secours supplementaire.

Contraintes:

- chiffrement actif;
- acces limite;
- rangement physique distinct du poste principal;
- rotation et verification hebdomadaire;
- aucune archive sensible non chiffree en transit ou en stockage durable.

Le disque externe doit contenir au minimum:

- miroir Git;
- dumps PostgreSQL exportes;
- archives audio exportees;
- runbooks et politique de restauration;
- inventaire de sauvegarde date.

---

## 9) Outillage V1 retenu

Scripts V1 fournis:

- [merlin_backup_postgres.sh](C:/MERLIN/deploy/backup/merlin_backup_postgres.sh)
- [merlin_backup_recordings.sh](C:/MERLIN/deploy/backup/merlin_backup_recordings.sh)
- [merlin_sync_local_mirror.ps1](C:/MERLIN/deploy/backup/merlin_sync_local_mirror.ps1)

Timers systemd V1 fournis:

- [merlin-backup-postgres.service](C:/MERLIN/deploy/systemd/merlin-backup-postgres.service)
- [merlin-backup-postgres.timer](C:/MERLIN/deploy/systemd/merlin-backup-postgres.timer)
- [merlin-backup-recordings.service](C:/MERLIN/deploy/systemd/merlin-backup-recordings.service)
- [merlin-backup-recordings.timer](C:/MERLIN/deploy/systemd/merlin-backup-recordings.timer)

---

## 10) Lignes rouges

Interdits:

- compter sur Git comme seule sauvegarde;
- garder les audios uniquement sur le VPS;
- utiliser un disque externe non chiffre pour des donnees sensibles;
- supposer qu'un backup existe sans verifier les dates et checksums;
- faire un redeploiement majeur sans backup recent exploitable;
- stocker `.env.prod` ou des secrets critiques dans un depot Git.

---

## 11) Decision active

A compter de cette note:

- MERLIN exige une sauvegarde multi-supports;
- la base et les audios ont un regime de backup distinct du code;
- une verification hebdomadaire humaine devient obligatoire;
- le disque externe chiffre fait partie du dispositif normal;
- la restauration testee devient un critere d'exploitation, pas une option.

---

## 12) References

- [MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md)
- [MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md)
- [MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md)
