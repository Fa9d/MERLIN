# MERLIN_STRATEGIE_TESTS_IA_V1

**Version:** 1.0  
**Statut:** ACTIF  
**Date:** 2026-05-06  
**Décision associée:** DEC-041  
**Dépend de:** MERLIN_CONTRAT_PROMPT_V1, pytest.ini  

---

## 1. Objectif

Rendre les tests d'intégration IA **100% rejouables**, avec un budget token prévisible et une distinction claire entre tests avec appel API réel et tests en mode replay.

Objectif : ne jamais dépendre d'un "état terminal chanceux".

---

## 2. Marqueurs pytest

Deux marqueurs sont définis dans `pytest.ini` :

| Marqueur | Usage | Appel API réel ? | CI ? |
|---|---|---|---|
| `@pytest.mark.integration` | Tests smoke Copilot (test_api_smoke.py) | Non (HTTP local) | Exclu par défaut |
| `@pytest.mark.real_api` | Tests Anthropic réels (J3) | **Oui** | Exclu par défaut |
| `@pytest.mark.replay` | Tests sur fixtures JSON enregistrées | Non | **Inclus** |
| *(aucun marqueur)* | Tests unitaires purs (J1, J2) | Non | **Inclus** |

### Ajout dans pytest.ini

```ini
[pytest]
pythonpath = .
testpaths = tests
markers =
    integration: Tests d'intégration HTTP API locale (Copilot smoke)
    real_api: Tests avec appel Anthropic réel — nécessite ANTHROPIC_API_KEY
    replay: Tests sur fixtures JSON enregistrées — rejouables sans API
addopts = -m "not integration and not real_api"
```

**Effet :** `pytest` sans argument ne lance que les tests unitaires + replay. Les tests real_api nécessitent `pytest -m real_api`.

---

## 3. Budget token par test

Chaque test `@pytest.mark.real_api` doit définir un budget token maximal via une fixture dédiée.

### 3.1 Fixture `token_budget`

À ajouter dans `conftest.py` :

```python
import pytest

TOKEN_BUDGETS = {
    "default": 1000,
    "note_generation": 2000,
    "triage_urgence": 500,
    "validation": 800,
}

@pytest.fixture
def token_budget(request):
    """Retourne le budget token pour le test courant."""
    budget_key = request.node.get_closest_marker("token_budget")
    if budget_key:
        key = budget_key.args[0]
        return TOKEN_BUDGETS.get(key, TOKEN_BUDGETS["default"])
    return TOKEN_BUDGETS["default"]
```

### 3.2 Usage dans un test

```python
@pytest.mark.real_api
@pytest.mark.token_budget("note_generation")
def test_generation_note_reelle(token_budget):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=token_budget,  # ← budget contrôlé
        messages=[...]
    )
    assert response.usage.input_tokens + response.usage.output_tokens <= token_budget
```

---

## 4. Stratégie replay (fixtures enregistrées)

Les tests `@pytest.mark.replay` utilisent des réponses JSON pré-enregistrées pour valider la logique sans consommer de tokens.

### 4.1 Structure des fixtures

```
tests/
  fixtures/
    real_api_responses/
      meth001_note_valide_v1.json        ← réponse Claude enregistrée
      meth001_note_invalide_signal_v1.json
      meth004_urgence_confirmee_v1.json
```

### 4.2 Enregistrement d'une fixture

```python
# Script utilitaire : scripts/record_fixture.py
import anthropic, json, sys
from pathlib import Path

def record(fixture_name: str, messages: list, max_tokens: int = 1000):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=max_tokens,
        messages=messages
    )
    output = {
        "model": response.model,
        "usage": {"input": response.usage.input_tokens, "output": response.usage.output_tokens},
        "content": response.content[0].text,
        "recorded_at": "2026-05-06"
    }
    path = Path(f"tests/fixtures/real_api_responses/{fixture_name}.json")
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"✅ Fixture enregistrée : {path}")
```

### 4.3 Test replay type

```python
@pytest.mark.replay
def test_meth001_note_structure_replay():
    """Valide la structure JSON d'une sortie METH-001 sans appel API."""
    fixture = json.loads(
        Path("tests/fixtures/real_api_responses/meth001_note_valide_v1.json").read_text()
    )
    note = json.loads(fixture["content"])
    assert "faits" in note
    assert "hypotheses" in note
    assert "recommandations" in note
    assert isinstance(note["faits"], list)
```

---

## 5. Séquence d'exécution recommandée

```
pytest                          → Unitaires + Replay (CI, gratuit)
pytest -m real_api              → Tests Anthropic réels (manuel, avant merge)
pytest -m integration           → Smoke tests API locale (avant déploiement)
pytest -m "real_api or replay"  → Suite complète IA (validation release)
```

---

## 6. Règles de maintenance

- Une nouvelle réponse Claude enregistrée = une nouvelle fixture JSON dans `tests/fixtures/`
- Les fixtures sont versionnées dans Git (petites tailles JSON)
- Une fixture est re-enregistrée uniquement si le prompt change de version
- Le nom de la fixture doit inclure l'ID prompt + le scénario + la version : `{id}_{scenario}_v{n}.json`

---

*Document de gouvernance MERLIN — stratégie de tests IA reproducibles.*
