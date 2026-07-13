# Vue de travail API MERLIN — docs, tests, suivi

> Mis en place le 2026-07-13. Trois outils, un par besoin : **voir** (Swagger),
> **tester** (Postman), **suivre** (GitHub Issues/Project).

## 1. Documentation vivante (Swagger / ReDoc)

| Où | URL |
|---|---|
| Prod | https://api.ivia.quebec/docs · https://api.ivia.quebec/redoc |
| Local | http://localhost:8000/docs · http://localhost:8000/redoc |

Lancer en local (PowerShell) :
```powershell
cd C:\_IVIA\10_backend_merlin_api
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
# puis ouvrir http://localhost:8000/docs
```
La description générale, la version (`2026.07`) et l'ordre des ~40 groupes
sont définis dans `app/main.py` (bloc `OPENAPI_TAGS`). Toute nouvelle route
DOIT porter un tag existant ou ajouter son entrée à ce bloc.

## 2. Collection de test (Postman / Insomnia)

Fichier : **`docs/api/merlin_postman_collection.json`** (Postman v2.1 —
Insomnia l'importe aussi : *Create → Import From File*).

Import : Postman → *Import* → choisir le fichier. Puis :
1. Variable `base_url` : prod par défaut ; local = `http://localhost:8000/api/v1` ;
2. Lancer **Auth / Login** : le JWT est capturé automatiquement dans `{{token}}` ;
3. Dérouler les dossiers : Comptes → Séance praticien (création → salle LiveKit
   → enregistrement → clôture) → Notes (validation) → Client solo & miroirs.

Règles : données **fictives** uniquement ; la route `/sessions/{id}/room` est
dépréciée (410) — la salle passe par `/audio-sessions/sessions/{id}/provision`.

## 3. Suivi GitHub (issues + Project)

**Issues** — template : `.github/ISSUE_TEMPLATE/api_traitement.md`.
Convention de titre : `[API] POST /sessions — création séance`.
Labels : `api`, `merlin` (+ `bug` ou `evolution`).

**Project (kanban)** — création en 2 minutes dans l'interface GitHub :
1. Repo → onglet **Projects** → *New project* → modèle **Board* → nom `MERLIN — traitements API` ;
2. Renommer les colonnes : **À analyser · En cours · En test · En production** ;
3. *Workflows* (⚡ en haut du board) : activer *Item added to project → À analyser*
   et *Item closed → En production* ;
4. Lier une issue : dans l'issue, panneau droit → *Projects* → sélectionner le board.

En ligne de commande (facultatif, nécessite `gh auth refresh -s project`) :
```powershell
gh project create --owner Fa9d --title "MERLIN — traitements API"
gh issue create --title "[API] PATCH /session-notes/{id}/validate — validation humaine" --label api,merlin --body-file .github/ISSUE_TEMPLATE/api_traitement.md
```

Une carte = un traitement (endpoint ou flux complet), reliée à son issue,
sa section Swagger et sa requête Postman.
