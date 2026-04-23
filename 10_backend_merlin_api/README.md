# MERLIN backend API

Backend coeur MERLIN V1.

Objectif de ce dossier:
- poser un backend Python propre;
- servir de source de verite metier;
- exposer le premier noyau V1:
  - `client`
  - `intake_request`
  - `consent`
  - `session`

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2
- PostgreSQL

## Demarrage local

1. Demarrer PostgreSQL et LiveKit local:

```powershell
Set-Location C:\MERLIN\10_backend_merlin_api
docker compose up -d
```

Port local MERLIN:
- `55432`
- Media LiveKit local:
  - `ws://127.0.0.1:7880`
- API backend par defaut:
  - `http://127.0.0.1:8000`

2. Creer un environnement virtuel.
3. Installer les dependances:

```powershell
Set-Location C:\MERLIN\10_backend_merlin_api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Creer `.env` a partir de `.env.example`.

5. Appliquer la migration initiale:

```powershell
alembic upgrade head
```

6. Lancer l'API:

```powershell
uvicorn app.main:app --reload
```

7. Lancer le smoke test:

```powershell
pytest -q
```

## Endpoints initiaux

- `GET /health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/clients`
- `POST /api/v1/clients`
- `GET /api/v1/clients/{client_id}`
- `POST /api/v1/intake-requests`
- `GET /api/v1/intake-requests/{intake_request_id}`
- `POST /api/v1/consents`
- `GET /api/v1/consents/{consent_id}`
- `POST /api/v1/sessions`
- `GET /api/v1/sessions/{session_id}`
- `POST /api/v1/sessions/{session_id}/start`
- `POST /api/v1/sessions/{session_id}/close`
- `POST /api/v1/audio-sessions/sessions/{session_id}/provision`
- `POST /api/v1/audio-sessions/{audio_session_id}/operator-join`
- `POST /api/v1/audio-recordings/audio-sessions/{audio_session_id}/start`
- `POST /api/v1/audio-recordings/{audio_recording_id}/stop`
- `GET /api/v1/audio-recordings`
- `GET /api/v1/audio-sessions`

## Auth minimale

- le premier utilisateur cree peut etre un `admin_tech` sans token;
- ensuite, la creation d'utilisateurs exige un token `admin_tech`;
- les routes internes de lecture et les operations de seance / consentement sont protegees par Bearer token.

Exemple de bootstrap:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/auth/register -ContentType 'application/json' -Body '{"email":"admin@example.com","password":"admin-secret","display_name":"Admin","role":"admin_tech"}'
```

Connexion:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/auth/login -ContentType 'application/json' -Body '{"email":"admin@example.com","password":"admin-secret"}'
```

## Note importante

Ce backend contient deja le noyau metier et une premiere couche audio:
- gestion des seances;
- generation de note structuree de cloture;
- provision d'une salle audio;
- creation d'un contexte de connexion operateur LiveKit.

Il ne contient pas encore:
- transcription;
- derivees IA;
- workers.

L'enregistrement est maintenant prepare au niveau metier:
- mode `metadata_only` pour le dev local et la trace de cycle;
- mode `livekit_egress` prevu pour le vrai export fichier.

La capture binaire finale et la transcription viennent juste apres validation de ce cycle.

## Note environnement local

La machine contient deja un PostgreSQL Windows historique sur `5432`.

Pour eviter tout conflit, le PostgreSQL Docker de MERLIN est publie sur:
- `127.0.0.1:55432`

Le backend autorise par defaut les origines frontend de dev:
- `http://127.0.0.1:3000`
- `http://localhost:3000`

## Variables audio locales

Le fichier `.env` de dev local doit contenir:

```env
MERLIN_MEDIA_PROVIDER_CODE=livekit
MERLIN_MEDIA_LIVEKIT_WS_URL=ws://127.0.0.1:7880
MERLIN_MEDIA_LIVEKIT_API_KEY=...
MERLIN_MEDIA_LIVEKIT_API_SECRET=...
```

Tant que ces variables ne sont pas definies, l'endpoint `operator-join` repondra en `409`.
