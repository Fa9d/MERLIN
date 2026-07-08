# JOURNAL — Mise en service de la sauvegarde chiffrée (Loi 25)

**Date** : 2026-07-04
**Opérateur** : Copilot CLI (session agents/cleanup-production-workflow), supervision David Phaneuf
**Référence** : `deploy/backup.sh` · `docs/ops-sauvegarde.md`

## État avant

- Deux crons legacy non chiffrés (`~/bin/merlin-backup-postgres.sh`, `merlin-backup-recordings.sh`) → retirés.
- Aucune variable de sauvegarde dans `.env.prod`, `awscli` absent du VPS.

## Actions réalisées

1. Installation `awscli` (1.22.34) sur le VPS (gpg 2.2.27 déjà présent).
2. Génération `MERLIN_BACKUP_PASSPHRASE` (openssl rand -base64 48) → ajoutée à `/opt/merlin/.env.prod`.
   ⚠️ Passphrase remise au fondateur pour conservation **hors VPS** (gestionnaire de mots de passe).
3. Crons legacy remplacés par le cron canonique : `30 3 * * * cd /opt/merlin && bash deploy/backup.sh >> /var/log/merlin-backup.log`.
4. Test complet : dump PostgreSQL + archive audios, chiffrement AES-256 (gpg), rétention 7.
5. Test de déchiffrement réussi (`gpg -d | gunzip` → dump lisible).

## État après

- Sauvegarde quotidienne 03:30, chiffrée AES-256, rétention locale 7 jours.
- **Hors-site OVH : NON configuré** — en attente des identifiants S3 OVH (bucket `merlin-backups`, région BHS).
  Dès que `OVH_S3_ENDPOINT/OVH_S3_REGION/OVH_S3_BUCKET/AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY`
  seront dans `.env.prod`, le script enverra automatiquement les copies hors-site (aucun autre changement requis).

## Reste à faire

- [ ] Créer le conteneur Object Storage OVH BHS + identifiants S3 (console OVH) → renseigner `.env.prod`.
- [ ] Vérifier le premier envoi hors-site (`aws s3 ls s3://merlin-backups/db/`).
- [ ] Test de restauration trimestriel (prochain : octobre 2026).
