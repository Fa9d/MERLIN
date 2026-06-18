# Sauvegarde chiffrée IVIA/MERLIN — OVH Object Storage (Québec)

Sauvegarde quotidienne **chiffrée** de la base + des audios, copiée **hors-site**
chez OVH Object Storage région **BHS (Beauharnois, Québec)** — conforme Loi 25
(données au Québec, chiffrées au repos et en transit).

Script : `deploy/backup.sh` · Restauration : voir plus bas.

---

## 1. À provisionner chez OVH (une fois)

1. **Public Cloud → Object Storage → Créer un conteneur**
   - Région : **Beauharnois (BHS)** · Type : *Standard* (ou *High Performance*).
   - Nom : `merlin-backups`.
2. **Utilisateur S3** (Public Cloud → Users & Roles → créer un utilisateur, puis
   « Generate S3 credentials ») → note l'**Access Key** et la **Secret Key**.
3. **Endpoint S3** de la région : `https://s3.bhs.io.cloud.ovh.net`.
4. (Recommandé) **Cycle de vie** sur le conteneur : expiration automatique des objets
   (ex. 90 jours) pour la rétention hors-site — se règle côté OVH, pas dans le script.

## 2. Secrets à ajouter dans `/opt/merlin/.env.prod` (jamais commités)

```env
MERLIN_BACKUP_PASSPHRASE=<générer: openssl rand -base64 48>
OVH_S3_ENDPOINT=https://s3.bhs.io.cloud.ovh.net
OVH_S3_REGION=bhs
OVH_S3_BUCKET=merlin-backups
AWS_ACCESS_KEY_ID=<access key S3 OVH>
AWS_SECRET_ACCESS_KEY=<secret key S3 OVH>
```

> ⚠️ **Conserver `MERLIN_BACKUP_PASSPHRASE` hors du VPS** (gestionnaire de mots de passe) :
> sans elle, les sauvegardes sont **irrécupérables**. C'est voulu (chiffrement fort).

## 3. Outils sur le VPS (une fois)

```bash
sudo apt-get update && sudo apt-get install -y awscli gnupg
aws --version && gpg --version
```

## 4. Premier test

```bash
cd /opt/merlin && bash deploy/backup.sh
aws --endpoint-url https://s3.bhs.io.cloud.ovh.net s3 ls s3://merlin-backups/db/
```

## 5. Planification (cron quotidien 03:30, heure du VPS)

```bash
crontab -e
# Sauvegarde IVIA — tous les jours à 03:30
30 3 * * * cd /opt/merlin && bash deploy/backup.sh >> /var/log/merlin-backup.log 2>&1
```

## 6. Restauration

**Base** :
```bash
gpg --batch --passphrase "$MERLIN_BACKUP_PASSPHRASE" -d db_AAAAMMJJ_HHMMSS.sql.gz.gpg \
  | gunzip \
  | docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T db \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

**Audios** :
```bash
gpg --batch --passphrase "$MERLIN_BACKUP_PASSPHRASE" -d recordings_AAAAMMJJ_HHMMSS.tar.gz.gpg \
  | docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T api \
    tar -xzf - -C /app/storage/recordings
```

## 7. Rétention & vérification

- **Locale** : 7 dernières (paramétrable `MERLIN_BACKUP_LOCAL_KEEP`).
- **Hors-site** : cycle de vie du conteneur OVH (recommandé 7 quotidiennes effectives via
  conservation ≥ rotation ; ajuster selon la politique de `IVIA_COUTS_CONFORMITE_DONNEES`).
- **Test de restauration trimestriel** à journaliser dans `05_JOURNAUX/`.
