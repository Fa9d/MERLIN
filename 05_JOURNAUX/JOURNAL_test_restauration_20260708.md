# JOURNAL — Premier test de restauration de sauvegarde (M5)

**Date** : 2026-07-08
**Opérateur** : Claude Code (Fable 5), via SSH `merlin-vps` (accès rétabli le même jour, M1)
**Références** : `docs/ops-sauvegarde.md` §6.1 (procédure ajoutée),
`00_GOUVERNANCE/IVIA_PLAN_DELIVERY_30-60-90_v1.0.md` (M5).

## Ce qui a été testé

Sauvegarde réelle de la nuit (`db_20260708_033001.sql.gz.gpg`, cron 3h30) :

1. Déchiffrement GPG (passphrase `.env.prod`) → dump SQL 272 Ko en clair.
2. Restauration complète dans une base jetable `merlin_restore_test`
   (`ON_ERROR_STOP=1`) — **zéro erreur**.
3. Comparaison restauré vs prod : head Alembic identique (`20260707_0050`),
   `clients` 7=7, `intake_requests` 1=1, `client_journal_entries` 4=4 ;
   `app_users` 9 vs 10 — l'écart est un compte créé **après** 3h30, ce qui
   confirme que l'instantané restauré est bien celui de la nuit.
4. Archive audios de la nuit : déchiffrée et listée intégralement (16 fichiers,
   tar intact).
5. Nettoyage : base jetable supprimée, dump temporaire effacé.

**Durée totale : < 2 minutes.** La chaîne sauvegarde → chiffrement →
déchiffrement → restauration est prouvée de bout en bout.

## Constat important — trou hors-site

`MERLIN_BACKUP_PASSPHRASE` est défini et le cron tourne, **mais les variables
OVH S3 sont vides** : aucune copie hors-site. Les 7 sauvegardes chiffrées
vivent sur le même disque que la prod — un incident disque/VPS emporte tout.
→ **Item M23 (P0)** au plan delivery : créer le bucket OVH Object Storage
(région BHS, Québec), renseigner les 5 variables, vérifier l'upload au
prochain cron. Action David (compte OVH requis).

## Leçon technique

Dans un script distant `ssh 'bash -s' <<EOF`, un `docker compose exec -T` sans
`< /dev/null` consomme le reste du script par stdin (le premier essai s'est
arrêté silencieusement après l'étape 2). Documenté dans `ops-sauvegarde.md`.

## Prochain test

Trimestriel : **octobre 2026** (suivre la procédure §6.1 de `ops-sauvegarde.md`).
