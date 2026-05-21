# Pont post-intake - Implementation v0.2

Date : 2026-05-13  
Objectif : transformer une demande client en chemin activable vers compte, reservation et espace personnel.

Etat v0.3 : pont durable finalise sur PostgreSQL local. Le token d'invitation est valide cote backend, le compte `public_client` est lie a la fiche `Client`, `/clients/me` permet au dashboard client de retrouver la fiche durable, et le parcours matching -> disponibilite -> hold -> confirmation -> `/bookings/my` est valide sur Postgres.

## 1. Ce qui a ete implemente

### Frontend

- `/connexion` : connexion multi-role, stockage local par role et redirection automatique.
- `/creer-mon-compte` : creation de compte client publique ou par invitation tokenisee.
- `/mon-espace` : dashboard client minimal avec fiche client liee, etat de parcours, reservations et lien vers suivi public.
- `/rendez-vous/reserver` : vraie page de reservation, avec liste praticiens, disponibilites et confirmation.
- `/operator` : bouton `Inviter` dans la file prospects pour generer/envoyer le lien d'activation client.

### Backend

- `POST /api/v1/bookings/hold-calculated` : materialise un creneau calcule disponible, place un hold pour le client connecte, puis permet la confirmation via `/bookings/confirm`.
- `POST /api/v1/intake-requests/{id}/client-invitation` : genere une invitation post-intake reservee aux roles internes.
- `GET /api/v1/register/client-invitations/{token}` : lit le contexte public d'une invitation valide.
- `POST /api/v1/register/client` accepte `invitation_token` et active directement le compte si le token est valide.
- `GET /api/v1/clients/me` retourne la fiche `Client` durablement liee au compte `public_client`.
- Migration Alembic `20260513_0022_add_client_activation_bridge.py` ajoute `clients.app_user_id` et les champs d'activation.
- Migration Alembic `20260513_0023_seed_pilot_schedules.py` ajoute des disponibilites pilotes idempotentes.
- Migration Alembic `20260513_0024_ensure_pilot_personas.py` restaure les personas pilotes si une base a `head` les a perdues.
- `tools/seed_local_demo_access.py` restaure les comptes locaux de demo avec mots de passe temporaires connus, sans afficher de hash.
- `POST /api/v1/auth/register` autorise maintenant la creation du premier `admin_tech` tant qu'aucun admin n'existe, meme si les migrations ont deja seede des praticiens.
- `tests/conftest.py` force une SQLite pytest par defaut et ne nettoie plus `app_users` sur une base non-test.

### API frontend

- `getCurrentUser` ajoute pour `/auth/me`.
- `holdCalculatedSlot` ajoute pour `/bookings/hold-calculated`.
- `CalculatedHoldPayload` ajoute.
- `getClientInvitation`, `createClientActivationInvitation`, `getMyClient` ajoutes.

### Intake

- `/rendez-vous` enregistre la derniere reference intake dans `localStorage` pour que `/creer-mon-compte` et `/mon-espace` puissent offrir un pont temporaire cote navigateur.

## 2. Flux v0.1 obtenu

```text
/rendez-vous
  -> client + intake + consentements
  -> reference stockee localement

/creer-mon-compte
  -> si token invitation valide : compte cree, email considere verifie, Client lie
  -> sinon : inscription client publique + verification courriel envoyee

/connexion
  -> login
  -> public_client => /mon-espace
  -> practitioner => /espace-praticien
  -> operator => /operator
  -> supervisor => /supervision
  -> admin_tech => /admin

/mon-espace
  -> fiche Client liee via /clients/me
  -> reservations client via /bookings/my
  -> lien vers /rendez-vous/reserver
  -> lien fallback vers /suivi si reference intake locale

/rendez-vous/reserver
  -> praticiens publics
  -> disponibilites calculees
  -> hold-calculated
  -> confirm
```

## 3. Validations executees

- `python -m compileall app\api\routes\bookings.py` : OK.
- Import FastAPI et routes bookings : OK.
- Routes bookings enregistrees :
  - `/api/v1/bookings/hold`
  - `/api/v1/bookings/hold-calculated`
  - `/api/v1/bookings/confirm`
  - `/api/v1/bookings/cancel`
  - `/api/v1/bookings/my`
- `npm run build` dans `09_app_ivia_merlin` : OK.
- `pytest tests\test_public_intake_flow.py -q` : OK, 4 tests passes dont le parcours invitation -> compte -> `/clients/me`.
- Apres correction auth du premier admin apres seed : `pytest tests\test_public_intake_flow.py -q` : OK, 5 tests passes.
- Smoke HTTP complet sur API SQLite `8001` : OK.
- Migration PostgreSQL Docker appliquee : `alembic_version = 20260513_0022`.
- Smoke HTTP complet sur API PostgreSQL `8002` : OK.
- Migration PostgreSQL Docker appliquee ensuite : `alembic_version = 20260513_0024`.
- Matching Postgres valide : deuil -> Solene/Telma ; identite + psychocorporel -> Seve/Nael ; distress -> Telma/Aelis/Seve.
- Reservation E2E Postgres valide : matching -> 28 creneaux Solene -> hold-calculated -> confirm -> `/bookings/my` contient le rendez-vous confirme.
- Donnees locales restaurees apres durcissement pytest : `app_users=14`, `practitioner_profiles=6`, `practitioner_schedules=18`.
- `python -m pytest tests\test_matching_recommend.py tests\test_public_intake_flow.py -q` : OK, 9 tests passes sans toucher PostgreSQL local.
- Frontend local relance avec `NEXT_PUBLIC_MERLIN_API_BASE_URL=http://127.0.0.1:8002`.
- Serveur frontend local : `http://localhost:3000` : OK.
- API locale PostgreSQL : `http://127.0.0.1:8002/openapi.json` : HTTP 200.
- Smoke test frontend :
  - `/connexion` : HTTP 200.
  - `/creer-mon-compte` : HTTP 200.
  - `/mon-espace` : HTTP 200.
  - `/rendez-vous/reserver` : HTTP 200.
  - `/operator` : HTTP 200.

## 4. Limites connues

- Le port `8000` est occupe par Docker/WSL dans l'environnement courant. L'API MERLIN tourne donc sur `8002` pour le test local.
- La chaine Alembic SQLite historique est bloquee avant les revisions recentes par une ancienne migration qui tente `ALTER TABLE session_notes ALTER COLUMN ...` non supporte par SQLite ; ce n'est pas lie a PostgreSQL, qui est maintenant migre.
- Le courriel d'invitation depend de la configuration SMTP. Le smoke Postgres a retourne `email_sent=True` dans l'environnement courant.
- `/mon-espace` affiche maintenant la fiche Client liee et les bookings ; les documents client detailles restent a enrichir.
- La confirmation de reservation exige toujours un courriel verifie, conformement a `require_verified_email_user`. Un compte cree via invitation est active directement.

## 5. Prochaine etape technique

Pour relancer l'etat valide actuel :

```text
cd C:\MERLIN\10_backend_merlin_api
docker compose up -d merlin_postgres
$env:MERLIN_DATABASE_URL='postgresql+psycopg://postgres:postgres@127.0.0.1:55432/merlin_v1'
python -m alembic upgrade head
python -m uvicorn app.main:app --app-dir "C:\MERLIN\10_backend_merlin_api" --host 127.0.0.1 --port 8002

$env:NEXT_PUBLIC_MERLIN_API_BASE_URL='http://127.0.0.1:8002'
npm --prefix "C:\MERLIN\09_app_ivia_merlin" run dev -- --port 3000
```

## 6. Definition de done suivante

Le test local deja passe couvre :

1. soumettre `/rendez-vous` ;
2. generer une invitation operateur ;
3. lire `/creer-mon-compte?token=...` ;
4. creer un compte client active ;
5. se connecter ;
6. lire la fiche durable via `/clients/me`.

Valide avec PostgreSQL et donnees praticiens :

1. ouvrir `/rendez-vous/reserver` ;
2. choisir un praticien et un creneau ;
3. confirmer ;
4. voir le rendez-vous dans `/mon-espace`.

Prochaine marche : rendre ce rendez-vous visible cote praticien/operateur avec statut de session, puis brancher la session exploitable et le statut financier minimal.
