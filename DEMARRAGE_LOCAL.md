# Démarrage local — IVIA / MERLIN

> Guide pour faire tourner le projet sur ta machine depuis le clone propre
> `C:\Dev\IVIA\MERLIN`. **Source unique** : `Fa9d/MERLIN` @ `refonte-ivia-site-unifie`.

---

## 0. Toujours commencer par se synchroniser
Double‑clic sur **`sync.bat`** (= `git pull`) → ton dossier récupère les dernières
modifs (Claude Code, Perplexity, Copilot) depuis GitHub.

---

## 1. Voir le SITE en local (immédiat, sans secret) ✅
Le frontend public est **statique** (HTML + Tailwind) — aucune dépendance.

**Double‑clic sur `demarrer_frontend.bat`** → ouvre `http://localhost:8080`.
*(Requiert seulement Python installé.)*

C'est suffisant pour travailler l'accueil, les pages client/praticien, le design,
les maquettes `design-system/`.

---

## 2. Faire tourner le BACKEND en local (complet)
Nécessaire seulement pour tester l'API (auth, séances, profilage…). Plus lourd :
il faut **une base PostgreSQL** + **tes secrets**.

### a) Base de données (PostgreSQL via Docker)
Le backend attend Postgres sur `127.0.0.1:55432`.
```
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d db
```
> ⚠️ Ne JAMAIS lancer `docker compose up` nu (déclenche le compose DEV et peut
> entrer en conflit). Toujours `--env-file .env.prod -f docker-compose.prod.yml`.

### b) Environnement Python
```
cd 10_backend_merlin_api
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### c) Secrets — `.env` (PAS dans git, à recréer)
Copie `.env.example` → `.env.prod` et renseigne **tes** valeurs :
`POSTGRES_PASSWORD`, `MERLIN_AUTH_SECRET_KEY`, `ANTHROPIC_API_KEY`, `LIVEKIT_API_SECRET`…
*(Claude Code n'a pas tes secrets — c'est à toi.)*

### d) Migrations + lancement
```
cd 10_backend_merlin_api
.venv\Scripts\alembic upgrade head      REM applique jusqu'au head 0039
.venv\Scripts\uvicorn app.main:app --reload
```
→ API sur `http://localhost:8000` · santé : `http://localhost:8000/api/health`

---

## 3. Ce qui NE « tourne » pas (et c'est normal)
- **Agents C‑suite** (`11_PROMPTS/06_CSUITE/`) et **modèles comportementaux** : ce sont
  des **prompts / documents**, lus par un agent IA — ils ne s'exécutent pas.
- **Profilage / insights** : code présent mais **gated** (migration 0039 non appliquée
  en prod, insights Anthropic désactivés) tant que la barrière B1‑B4 n'est pas levée.

---

## 4. Règles d'or (pour ne plus se perdre)
- **Un seul dossier de travail** : `C:\Dev\IVIA\MERLIN`. (Abandonner les anciens.)
- **Ouvre le DOSSIER** dans VS Code, pas un `.code-workspace`.
- **Tout ce qui sert vit dans le repo** ; pas de fichiers utiles hors git.
- **Tous les agents (Perplexity/Copilot/Claude) sur la branche canonique** `refonte-ivia-site-unifie`.
- Avant de bosser : `sync.bat`. Après : `git push`.
