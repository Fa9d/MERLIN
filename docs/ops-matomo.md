# Ops — Matomo (mesure d'audience souveraine)

**Créé** : 2026-07-06
**Pourquoi** : mesure d'audience hébergée sur notre VPS (données Québec, Loi 25) au lieu de
Google Analytics. Prérequis du plan de mise en marché (`12_JURIDIQUE_AFFAIRES/IVIA_PLAN_MISE_EN_MARCHE_v1.1.md` §4.2)
avant toute publicité payante.

---

## Architecture

| Composant | Détail |
|---|---|
| `matomo` | image `matomo:5-apache`, volume `merlin_matomo_data` |
| `matomo-db` | image `mariadb:11`, volume `merlin_matomo_db` |
| Accès | `https://stats.ivia.quebec` (proxy nginx — bloc commenté tant que DNS/cert absents) |
| Balise | `ivia_site_v2/shared/analytics.js` — chargée par toutes les pages publiques |

## Conformité Loi 25 — mode sans témoin

La balise (`analytics.js`) est configurée **cookieless** :
- `disableCookies` → aucun témoin déposé → **pas de bandeau de consentement requis**
- `setDoNotTrack` → respecte le signal du navigateur
- Compléter côté serveur Matomo (Administration → Confidentialité) :
  - anonymisation IP à 2 octets,
  - suppression des journaux bruts après 90 jours,
  - désactiver la collecte du User-ID.

**Si un jour on active les pixels Meta/Google** (plan §10) : là il faudra un bandeau de
consentement — Matomo seul n'en a pas besoin dans cette configuration.

## Variables d'environnement (`.env.prod` sur le VPS)

```env
MATOMO_DB_ROOT_PASSWORD=   # généré : openssl rand -base64 24
MATOMO_DB_PASSWORD=        # généré : openssl rand -base64 24
```

## Mise en service (à faire une fois)

1. **DNS** : créer chez OVH un enregistrement `A` → `stats.ivia.quebec` → `137.74.42.121`.
2. **Secrets** : sur le VPS, ajouter les 2 variables ci-dessus à `/opt/merlin/.env.prod`.
3. **Démarrer les conteneurs** :
   ```bash
   cd /opt/merlin && git pull
   docker compose --env-file .env.prod -f docker-compose.prod.yml up -d matomo-db matomo
   docker compose --env-file .env.prod -f docker-compose.prod.yml restart nginx  # prend le server_name port 80
   ```
4. **Certificat TLS** (après propagation DNS) :
   ```bash
   docker run --rm -v /opt/merlin/nginx/certs:/etc/letsencrypt \
     -v /opt/merlin/nginx/certbot/www:/var/www/certbot \
     certbot/certbot certonly --webroot -w /var/www/certbot -d stats.ivia.quebec
   ```
5. **Activer le proxy** : décommenter le bloc `stats.ivia.quebec` dans `nginx/default.conf`,
   commit + `pull-deploy.sh`, puis `docker compose ... restart nginx`.
6. **Assistant Matomo** : ouvrir `https://stats.ivia.quebec`, suivre l'installation
   (la BD est pré-configurée par variables d'env), créer le site **ivia.quebec** (idSite = 1 —
   la balise suppose `setSiteId 1`), créer le compte admin (mot de passe fort, gestionnaire de mots de passe).
7. **Confidentialité** : appliquer les réglages Loi 25 ci-dessus.
8. **Vérifier** : visiter ivia.quebec, la visite doit apparaître dans Matomo → Visiteurs en temps réel.

## Événements de conversion

| Événement | Où | Déclencheur |
|---|---|---|
| `conversion / demande_envoyee / reservation_checkout` | `reserver.html` | clic « Confirmer et payer » réussi (départ vers paiement) |
| `conversion / demande_envoyee / paiement_confirme` | `checkout/success.html` | retour de paiement réussi |

Dans Matomo : créer un **Objectif** « Demande envoyée » déclenché par l'événement
`conversion / demande_envoyee` pour suivre le taux de conversion par canal/campagne.

## Codes de campagne

Utiliser les paramètres natifs Matomo dans tous les liens payants et publications :
`?mtm_campaign=<campagne>&mtm_source=<canal>&mtm_medium=<type>`
Exemple : `https://ivia.quebec/attente?mtm_campaign=c1-attente&mtm_source=meta&mtm_medium=payant`

## Renouvellement du certificat

Le script `deploy/certbot/renew-merlin-certs.sh` renouvelle tous les certificats du dossier —
`stats.ivia.quebec` sera inclus automatiquement après l'émission initiale.
