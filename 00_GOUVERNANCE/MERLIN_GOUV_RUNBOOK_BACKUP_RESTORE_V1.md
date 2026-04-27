# MERLIN - Runbook backup et restore V1

Date: 2026-04-27
Statut: actif
Objet: fournir la sequence minimale pour installer, lancer et verifier les sauvegardes MERLIN

---

## 1) Installation VPS

Depuis le VPS:

```bash
sudo cp /opt/merlin/deploy/backup/merlin_backup_postgres.sh /usr/local/bin/merlin-backup-postgres.sh
sudo chmod 700 /usr/local/bin/merlin-backup-postgres.sh
sudo cp /opt/merlin/deploy/backup/merlin_backup_recordings.sh /usr/local/bin/merlin-backup-recordings.sh
sudo chmod 700 /usr/local/bin/merlin-backup-recordings.sh
sudo cp /opt/merlin/deploy/systemd/merlin-backup-postgres.service /etc/systemd/system/
sudo cp /opt/merlin/deploy/systemd/merlin-backup-postgres.timer /etc/systemd/system/
sudo cp /opt/merlin/deploy/systemd/merlin-backup-recordings.service /etc/systemd/system/
sudo cp /opt/merlin/deploy/systemd/merlin-backup-recordings.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now merlin-backup-postgres.timer
sudo systemctl enable --now merlin-backup-recordings.timer
```

---

## 2) Test manuel VPS

```bash
sudo /usr/local/bin/merlin-backup-postgres.sh
sudo /usr/local/bin/merlin-backup-recordings.sh
sudo systemctl status merlin-backup-postgres.service --no-pager
sudo systemctl status merlin-backup-recordings.service --no-pager
```

---

## 3) Verification fichiers VPS

```bash
find /var/backups/merlin/postgres -type f | sort | tail -n 5
find /var/backups/merlin/recordings -type f | sort | tail -n 5
```

---

## 4) Recuperation locale

Depuis PowerShell local:

```powershell
scp -i C:\Users\PC\.ssh\id_ed25519 ubuntu@137.74.42.121:/var/backups/merlin/postgres/* C:\MERLIN_BACKUPS\payloads\postgres\
```

```powershell
scp -i C:\Users\PC\.ssh\id_ed25519 ubuntu@137.74.42.121:/var/backups/merlin/recordings/* C:\MERLIN_BACKUPS\payloads\recordings\
```

Puis miroir Git + copie externe:

```powershell
powershell -ExecutionPolicy Bypass -File C:\MERLIN\deploy\backup\merlin_sync_local_mirror.ps1 -MirrorPath C:\MERLIN_BACKUPS\git\MERLIN.git -BackupSourcePath C:\MERLIN_BACKUPS\payloads -ExternalDrivePath E:\
```

---

## 5) Test de lecture local

```powershell
Get-ChildItem C:\MERLIN_BACKUPS\payloads\postgres | Sort-Object LastWriteTime | Select-Object -Last 3
Get-ChildItem C:\MERLIN_BACKUPS\payloads\recordings | Sort-Object LastWriteTime | Select-Object -Last 3
```

---

## 6) Decision active

La sauvegarde MERLIN n'est consideree valide que si:

- les timers VPS tournent;
- un dump base recent existe;
- une archive audio recente existe;
- une copie locale recente existe;
- une copie disque externe chiffree existe;
- la checklist hebdomadaire a ete executee.

---

## 7) References

- [MERLIN_GOUV_POLICY_SAUVEGARDE_RESTAURATION_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_SAUVEGARDE_RESTAURATION_V1.md)
- [MERLIN_GOUV_CHECKLIST_HEBDO_SAUVEGARDES_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_HEBDO_SAUVEGARDES_V1.md)
