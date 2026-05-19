# Journal — Refonte parcours client (magic link)

**Date** : 2026-05-19 (Montréal)
**Branche** : `refonte-ivia-site-unifie`
**Phase** : refonte « maison du vivant » — pont post-intake v0.3
**Décision structurante** : automatisation du mail d'activation à la soumission `/rendez-vous` ;
suppression du gate opérateur sur la première porte d'entrée ; raccourcissement des consentements publics
de 5 à 3 ; introduction d'un véritable espace membre minimal.

---

## 1. Contexte d'ouverture

Test E2E manuel du formulaire `/rendez-vous` par le fondateur. Symptôme rapporté :
*« Quand je fais la demande, je n'ai pas de confirmation. Cette demande devrait automatiquement
envoyer un mail à l'utilisateur (qu'il pourra utiliser afin de renseigner son nouveau mot de passe
et prendre le contrôle de son espace). »*

Le diagnostic technique a fait émerger deux écarts cumulatifs :

1. **Bug d'authentification sur les consentements publics** : le formulaire envoyait 5 consentements en cascade
   alors que le backend n'en autorise que 3 en mode public (`consent_session`, `consent_session_note`,
   `consent_history`). Le 4e (`consent_recording`) faisait sauter la chaîne avec un 401 *« Authentification requise
   pour ce type de consentement »*. Le client et l'intake étaient bien créés en base, mais aucune confirmation
   visuelle ne s'affichait, et aucun mail n'était jamais envoyé.

2. **Absence du mail d'activation automatique** : le pont post-intake v0.2 (PONT_POST_INTAKE_IMPLEMENTATION_2026-05-13.md)
   imposait un gate opérateur : un humain devait aller dans `/operator`, cliquer **« Inviter »** pour qu'un mail
   parte. Le code applicatif de cette invitation n'avait, par ailleurs, jamais été commité (seules la migration
   `20260513_0022_add_client_activation_bridge.py` et le service `client_activation.py` existaient — la chaîne d'API
   manquait).

---

## 2. Décisions produit (validées par David Phaneuf)

- **Casser le gate opérateur** : le mail d'activation part automatiquement à la soumission de `/rendez-vous`
  si un email est fourni. Raison : friction minimale, ancrage dans les 2 minutes où l'intention est la plus forte.
- **Trois consentements publics suffisent** : `consent_session`, `consent_session_note`, `consent_history`.
  `consent_recording` et `consent_transcription` seront capturés plus tard, au moment d'une séance réelle ou
  d'une activation du journal, avec une explication contextuelle. Cela respecte la posture Loi 25 (consentement
  éclairé au bon moment) tout en désencombrant la porte d'entrée.
- **Magic link plutôt que mot de passe obligatoire** : aucun mot de passe n'est demandé pour entrer la première fois.
  Le compte est créé avec un `password_hash` aléatoire jamais communiqué. L'utilisateur pourra définir un mot de passe
  plus tard depuis `/mon-espace` (optionnel).
- **Espace membre matérialisé** : la page `/mon-espace` n'existait pas dans le repo. Elle est créée avec un MVP :
  fiche client, prochaines actions, mes rendez-vous, mes crédits, ressources membres, placeholder journal.
- **Paiement déplacé** : les boutons Stripe/Interac sortent du formulaire intake. Ils seront proposés depuis
  `/mon-espace` au moment d'une réservation effective.

---

## 3. Ce qui a été implémenté

### Backend (`10_backend_merlin_api/`)

- **Nouveau template courriel** : `make_magic_link_email(display_name, magic_link_url, ttl_days=7)` dans
  `app/services/email.py`. Sujet du mail : *« Votre espace IVIA est prêt — un clic pour ouvrir »*.
- **Nouveau routeur** `app/api/routes/public_intake.py` enregistré dans `app/main.py` sous le préfixe `/api/v1` :
  - `POST /api/v1/public/intake/start` : orchestrateur unique — crée `Client`, `IntakeRequest`, 3 `Consent`,
    optionnellement `AppUser` lié + magic link envoyé par mail. Retourne `magic_link_sent`, `email_used`, `message`.
  - `POST /api/v1/public/activate/{token}` : consomme le magic link, marque `email_verified=True` et
    `client.activation_accepted_at`, retourne un JWT + le profil utilisateur pour ouverture de session.
  - `GET /api/v1/public/activate/preview/{token}` : prévalide le token sans le consommer, pour une UX douce
    sur la page `/activer`.
- **Nouveau endpoint** : `GET /api/v1/clients/me` (dans `app/api/routes/clients.py`) — retourne la fiche `Client`
  liée au compte connecté. Utilisé par `/mon-espace`.
- **Schéma `ClientRead`** étendu avec `app_user_id`, `activation_invited_at`, `activation_accepted_at`
  (datetime, sérialisé en ISO).
- **Réutilisation** intégrale du service existant `app/services/client_activation.py` (génération + hash
  sha256 + TTL 7 jours + expiration + clear).
- **Aucune nouvelle migration Alembic** introduite par ce sprint : tout repose sur les colonnes ajoutées par
  `20260513_0022_add_client_activation_bridge.py`.

### Frontend (`09_app_ivia_merlin/`)

- **`src/lib/merlin-api.ts`** : nouvelles fonctions et types
  - `startPublicIntake(payload)` → `PublicIntakeStartResult` (orchestrateur)
  - `consumeMagicLink(token)` → `PublicActivateResult`
  - `previewMagicLink(token)` → `PublicActivatePreview`
  - `getMyClient(token)` → `MyClientRecord | null`
- **`src/app/rendez-vous/page.tsx`** : réécriture complète. 3 consentements au lieu de 5. Un seul appel API
  au lieu de 7. Écran de confirmation `SubmissionSuccess` qui invite à vérifier la boîte mail, sans boutons
  de paiement immédiats.
- **`src/app/activer/page.tsx`** (nouveau) : prévalide le token via `previewMagicLink`, affiche
  *« Bienvenue {nom}. Votre espace IVIA est prêt à s'ouvrir. »*, bouton **« Ouvrir mon espace IVIA »**
  qui consomme le token et redirige vers `/mon-espace?welcome=magic`.
- **`src/app/mon-espace/page.tsx`** (nouveau) : dashboard client minimal — fiche, prochaines actions,
  rendez-vous, crédits, ressources membres, placeholder journal. Lecture de session via
  `readStoredPublicClientSession`. Bandeau d'accueil si `?welcome=magic`. Bouton déconnexion.

### Doctrine (`CLAUDE.md`)

- Section §13 enrichie : ajout des deux nouvelles routes (`public_intake.py`, `/clients/me`) et mention que
  le head Alembic appliqué reste `20260513_0022` (les révisions 0025/0026 payment/entitlement sont en cours
  d'intégration mais non commitées et non requises par ce sprint).
- Section §16 augmentée d'un encart **« Parcours public d'entrée — magic link »** qui fixe les règles dures :
  trois consentements maximum en public, un seul appel orchestrateur, mail automatique, pas de mot de passe
  imposé à l'entrée.

---

## 4. Validations exécutées

### Build et type-check

- `cd 09_app_ivia_merlin && npm run build` : **OK**, 27 routes générées (vs 25 avant) — `/activer` et
  `/mon-espace` apparaissent. Aucun blocage Suspense/`useSearchParams`. Aucune erreur TypeScript.

### Smoke E2E backend

Backend local dev lancé via :

```text
$env:MERLIN_DATABASE_URL='postgresql+psycopg://postgres:postgres@127.0.0.1:55432/merlin_v1'
$env:MERLIN_PILOT_EMAIL_OVERRIDE='1'
$env:FRONTEND_URL='http://localhost:3000'
$env:MERLIN_CORS_ORIGINS='http://localhost:3000,http://127.0.0.1:3000'
.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir 10_backend_merlin_api --host 127.0.0.1 --port 8001 --reload
```

Tests exécutés :

- `curl -X POST /api/v1/public/intake/start` avec un payload complet → HTTP **201 Created**, réponse :

  ```json
  {
    "client_id": "fbe8f0ef-...",
    "public_client_code": "CLI-B067357B96",
    "intake_request_id": "2ff7acf3-...",
    "magic_link_sent": true,
    "email_used": "test-magic-link@example.com",
    "message": "Demande reçue. Un lien d'activation vient d'être envoyé à test-magic-link@example.com..."
  }
  ```

  `magic_link_sent: true` confirme l'envoi SMTP réel via OVH (`ssl0.ovh.net:465`). Pilot override actif :
  destination effective = `davidphaneuf@gmail.com`, sujet préfixé `[PILOTE→test-magic-link@example.com]`.

- `GET /api/v1/public/activate/preview/bogus-token-123` → `{"valid":false,...}` (200) ✓
- `POST /api/v1/public/activate/bogus-token-123` → 404 *« Lien d'activation invalide ou déjà utilisé. »* ✓

### Frontend dev

- `npm run dev` démarré sur `http://localhost:3000` avec `.env` pointant vers le backend local 8001
  (corrigé de l'ancien 8001→8000 puis 8000→8001 en cours de session).
- Smoke HTTP : `/rendez-vous`, `/activer?token=test`, `/mon-espace` : tous **200**.

### Limites du smoke

Le smoke test backend n'exerce pas le scénario complet `intake → mail → clic → activate`, car le token
en clair n'est plus disponible côté serveur après émission (seul le hash sha256 est stocké). Le test E2E
complet exige une boucle navigateur côté David :

1. Soumettre `/rendez-vous` avec son courriel ;
2. Vérifier le mail dans `davidphaneuf@gmail.com` ;
3. Cliquer sur **« Ouvrir mon espace IVIA »** ;
4. Vérifier l'atterrissage sur `/mon-espace?welcome=magic`.

---

## 5. Décisions opérationnelles et garde-fous

1. **Pas de migration appliquée** par ce sprint : la migration `20260513_0022` est déjà passée sur la base
   Postgres locale (vue du sprint 72h). Les routes ajoutées utilisent uniquement des colonnes existantes.
2. **Pilot override SMTP** (`MERLIN_PILOT_EMAIL_OVERRIDE=1`) reste actif tant qu'on n'a pas migré vers
   un domaine de test contrôlé. Tous les mails partent vers `davidphaneuf@gmail.com` avec sujet
   `[PILOTE→<destinataire_original>]`.
3. **Le docker `merlin-backend-1`** continue de tourner sur le port 8000 avec l'ancien code. Le développement
   se fait avec un `uvicorn --reload` local sur le port 8001 pour itérer rapidement. Ne pas redéployer en prod
   sans rebuild docker + revue de la doctrine §12 (variables d'environnement).
4. **Le docker `merlin-nginx-1` reste en restarting loop** (`host not found in upstream "frontend:3000"`) —
   c'est un conteneur orphelin d'une ancienne stack `ivia-app`. Aucun impact sur le flow magic link.
   À ranger plus tard.
5. **Aucun mot de passe en clair, aucun token en clair** stocké côté backend. Le `password_hash` des comptes
   magic-link est un hash scrypt d'un `secrets.token_urlsafe(48)` aléatoire jamais émis ailleurs.

---

## 6. À faire dans un prochain sprint

### Court terme (prochaine séance)

- **Définir un mot de passe depuis `/mon-espace`** : endpoint backend `POST /auth/set-password` réservé à
  l'utilisateur connecté, et CTA frontend dans `/mon-espace` quand `?welcome=magic` ou que l'utilisateur
  est connecté sans mot de passe vraiment défini.
- **`/acces-client`** : ajouter une option **« Recevoir un lien magique par courriel »** en complément du
  login/password classique. Réduit la friction de retour pour les utilisateurs qui n'ont jamais défini de mdp.
- **Auditer `/praticien` (dashboard praticien) + `/espace-praticien`** : vérifier qu'aucun parcours d'inscription
  publique praticien n'a été oublié, harmoniser le ton « maison du vivant » sur ces surfaces internes.

### Moyen terme

- **Journal client réel** : page `/journal` sous `/mon-espace`, table backend `client_journal_entry`,
  écriture libre + horodatage. C'est à ce moment qu'on demande `consent_recording` + `consent_transcription`
  avec une vraie explication contextuelle.
- **Ressources réservées aux membres** : gate auth sur `/ressources` ou nouvelle route `/ressources-membres`.
- **Commit propre de la stack paiement/entitlement** non commitée (migrations `20260518_0025` + `20260518_0026`,
  modèles `payment_order`, `client_entitlement`, services `booking_flow`, `client_activation`, routes
  `client_entitlements`, `organization_leads`). À séparer en un commit cohérent dédié, doublé d'une mise à
  jour de CLAUDE.md §13 (head Alembic).

---

## 7. Phrase de conduite

Le parcours client tient désormais en quatre temps : **demande → mail → un clic → espace ouvert**. Tout ce qui
allonge ces quatre temps doit être justifié par une exigence éthique (consentement éclairé au bon moment),
légale (Loi 25, LPRPDE) ou sécurité (verrouillage anti-spam). Le reste est friction inutile.

> Demande déposée n'est pas rendez-vous confirmé. Espace ouvert n'est pas séance vécue. Mais la porte
> ne doit pas être plus lourde que la décision d'en parler.
