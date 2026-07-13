# TASKS.md — Tâches pour Claude Code

Ce fichier liste les tâches prioritaires que Claude Code peut exécuter directement.
Chaque tâche est autonome et décrit clairement le contexte, les fichiers concernés, et le résultat attendu.

---

## Tâche 1 — Documenter tous les endpoints existants

**Objectif** : Ajouter une docstring claire à chaque route FastAPI qui n'en a pas.

**Format attendu** :
```python
@router.post("/sessions/create")
async def create_session(data: SessionCreate) -> SessionResponse:
    """
    Crée une nouvelle séance entre un praticien et un patient.

    Paramètres :
    - data.praticien_id : identifiant du praticien
    - data.patient_id : identifiant du patient
    - data.type_seance : type de séance (individuel, groupe, évaluation)
    - data.contexte : dictionnaire de contexte optionnel

    Retourne :
    - session_id : identifiant unique de la séance
    - room_url : URL de la salle LiveKit
    - created_at : horodatage de création
    - statut : statut initial de la séance
    """
```

**Fichiers à parcourir** : tous les fichiers dans `/routes/`

**Ne pas modifier** : la logique métier, les schémas, les imports

---

## Tâche 2 — Générer un fichier `openapi_summary.md`

**Objectif** : Lire tous les endpoints et produire un fichier Markdown listant :
- la route
- la méthode HTTP
- la description courte
- les paramètres d'entrée
- la sortie attendue

**Format du fichier produit** :
```markdown
## POST /sessions/create

Crée une nouvelle séance.

**Entrée** : `SessionCreate`
- praticien_id (str)
- patient_id (str)
- type_seance (str)
- contexte (dict, optionnel)

**Sortie** : `SessionResponse`
- session_id (str)
- room_url (str)
- created_at (datetime)
- statut (str)
```

**Fichier à créer** : `/docs/openapi_summary.md`

---

## Tâche 3 — Harmoniser les schémas Pydantic

**Objectif** : Vérifier que tous les schémas dans `/schemas/` respectent les conventions :
- Utiliser Pydantic v2 (`model_config`, `model_validator`, pas `@validator`)
- Ajouter `Field(description="...")` sur chaque champ
- Ajouter un exemple `model_config = ConfigDict(json_schema_extra={"example": {...}})`

**Exemple cible** :
```python
from pydantic import BaseModel, Field, ConfigDict

class SessionCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "praticien_id": "prat_001",
            "patient_id": "pat_042",
            "type_seance": "individuel",
            "contexte": {}
        }
    })

    praticien_id: str = Field(description="Identifiant unique du praticien")
    patient_id: str = Field(description="Identifiant unique du patient")
    type_seance: str = Field(description="Type de séance : individuel, groupe, évaluation")
    contexte: dict = Field(default={}, description="Informations contextuelles optionnelles")
```

**Fichiers concernés** : tous les fichiers dans `/schemas/`

---

## Tâche 4 — Créer les tests unitaires manquants

**Objectif** : Pour chaque module dans `/modules/comportementaux/`, créer un fichier de test dans `/tests/comportementaux/`.

**Format attendu** :
```python
# tests/comportementaux/test_strate_1.py

import pytest
from modules.comportementaux.strate_1 import analyse

def test_analyse_retourne_structure_valide():
    données_test = {
        "session_id": "test_001",
        "contenu": "Le patient décrit une situation de stress..."
    }
    résultat = analyse(données_test)
    assert "patterns" in résultat
    assert isinstance(résultat["patterns"], list)

def test_analyse_gere_données_vides():
    résultat = analyse({})
    assert résultat is not None
```

**Convention** : un fichier de test par module, préfixé `test_`.

---

## Tâche 5 — Créer un script de démarrage `start.sh`

**Objectif** : Créer un script shell qui :
1. Vérifie que `.env` existe
2. Active le virtualenv s'il existe
3. Lance `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
4. Affiche les URLs d'accès

**Fichier à créer** : `start.sh` à la racine du projet

```bash
#!/bin/bash
# start.sh — Démarrage du serveur MERLIN

set -e

if [ ! -f ".env" ]; then
  echo "❌ Fichier .env manquant. Copie .env.example vers .env et remplis les variables."
  exit 1
fi

echo "✅ Environnement chargé"
echo "🚀 Démarrage de MERLIN (FastAPI)..."
echo "   API : http://localhost:8000"
echo "   Docs : http://localhost:8000/docs"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Tâche 6 — Créer `.env.example`

**Objectif** : Créer un fichier `.env.example` à la racine du projet avec toutes les variables requises, sans valeurs sensibles.

```env
# MERLIN — Variables d'environnement
# Copie ce fichier vers .env et remplis les valeurs

# Environnement
ENVIRONMENT=development

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/merlin_db

# LiveKit
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Sécurité
SECRET_KEY=your_secret_key_here

# (optionnel) Transcription audio
WHISPER_MODEL=base
# ou
OPENAI_API_KEY=your_openai_key
```

---

## Tâche 7 — Audit de la structure du projet

**Objectif** : Lire la structure du projet et produire un rapport `docs/audit_structure.md` qui liste :
- Les dossiers et fichiers principaux
- Ce qui semble manquant ou incomplet
- Les doublons ou incohérences de nommage
- Les recommandations de réorganisation si nécessaire

**Format** : Markdown simple, clair, en français.

---

## Notes pour Claude Code

- Toujours vérifier si un fichier existe avant de le créer
- Ne jamais effacer de code sans le commenter d'abord (`# DEPRECATED — ...`)
- Si une tâche est ambiguë, créer un fichier `TODO.md` à la racine avec les questions
- Chaque modification doit être accompagnée d'un message de commit clair en français
- Prioriser la lisibilité sur la performance dans un premier temps
