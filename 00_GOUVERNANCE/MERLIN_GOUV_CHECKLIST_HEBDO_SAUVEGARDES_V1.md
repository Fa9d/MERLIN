# MERLIN - Checklist hebdomadaire sauvegardes V1

Date: 2026-04-27
Statut: actif
Objet: verifier chaque semaine que MERLIN dispose bien de copies exploitables du code, de la base et des sources audio

---

## 1) Controle code

- verifier le dernier `git push` vers le depot distant;
- lancer ou verifier le miroir Git local;
- verifier que le miroir a bien la date de la semaine;
- recopier le miroir sur disque externe chiffre.

Commande locale type:

```powershell
powershell -ExecutionPolicy Bypass -File C:\MERLIN\deploy\backup\merlin_sync_local_mirror.ps1 -MirrorPath C:\MERLIN_BACKUPS\git\MERLIN.git -BackupSourcePath C:\MERLIN_BACKUPS\payloads -ExternalDrivePath E:\
```

---

## 2) Controle VPS base

- verifier la presence d'un dump PostgreSQL recent dans `/var/backups/merlin/postgres`;
- verifier la presence du fichier `.sha256`;
- tester qu'un dump se decompresse sans erreur.

Commande type:

```bash
find /var/backups/merlin/postgres -type f -name 'merlin_postgres_*.sql.gz' | sort | tail -n 3
```

```bash
gzip -t "$(find /var/backups/merlin/postgres -type f -name 'merlin_postgres_*.sql.gz' | sort | tail -n 1)"
```

---

## 3) Controle VPS audio

- verifier la presence d'une archive audio recente dans `/var/backups/merlin/recordings`;
- verifier la presence du checksum;
- verifier que l'archive se liste.

Commande type:

```bash
find /var/backups/merlin/recordings -type f -name 'merlin_recordings_*.tgz' | sort | tail -n 3
```

```bash
tar -tzf "$(find /var/backups/merlin/recordings -type f -name 'merlin_recordings_*.tgz' | sort | tail -n 1)" | head
```

---

## 4) Copie hors VPS

- recuperer au moins le dernier dump PostgreSQL;
- recuperer au moins la derniere archive audio;
- deposer ces fichiers dans un repertoire local de secours;
- recopier ce repertoire sur disque externe chiffre.

Regle:

`si les backups restent uniquement sur le VPS, le backup n'est pas suffisant`

---

## 5) Secrets et acces

- verifier que la cle SSH principale fonctionne;
- verifier qu'une copie des secrets critiques existe hors Git;
- verifier que le runbook d'acces reste lisible et a jour;
- verifier que le disque externe chiffre reste montable.

---

## 6) Test de restauration minimal

- verifier qu'un dump PostgreSQL peut etre decompresse;
- verifier qu'une archive audio peut etre ouverte;
- verifier qu'un miroir Git local peut etre lu;
- verifier que la procedure de reprise n'a pas besoin d'une information manquante.

---

## 7) Trace hebdomadaire

A consigner a chaque verification:

- date;
- personne ayant verifie;
- dernier dump base;
- derniere archive audio;
- etat du miroir Git;
- copie disque externe `ok / non ok`;
- test de lecture `ok / non ok`;
- incident ou action corrective.

---

## 8) Decision active

Une semaine sans verification formelle de sauvegarde doit etre consideree comme une anomalie d'exploitation.
