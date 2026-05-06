---
id: GRILLE-GONOGO-001
version: V1
date: 2026-05-06
statut: actif
auteur: David Phaneuf
decision: DEC-040
test_associe: ROD-TEST-001-A
---

# MERLIN — Grille Go/No-Go prompt V1

> **Merge gate obligatoire.** Tout prompt soumis en PR doit passer cette grille.
> **Un seul ❌ bloque le merge, sans exception.**
> Check 10 doit être validé par un humain (praticien ou superviseur) — jamais IA-sur-IA.

---

## Les 10 checks

| # | Check | Critère | Automatisable |
|---|---|---|---|
| 1 | **Frontmatter complet** | Champs obligatoires présents : `id`, `version`, `date`, `statut`, `type_sortie`, `test_associe` | ✅ Oui |
| 2 | **Contrat prompt référencé** | Le prompt cite explicitement `MERLIN_CONTRAT_PROMPT_V1.md` ou son successeur | ✅ Oui |
| 3 | **Type de sortie déclaré** | `type_sortie` est l'un de : `note_clinique`, `triage_urgence`, `validation_pilote`, `synthese_dossier` | ✅ Oui |
| 4 | **Schéma JSON déclaré** | Le prompt exige une sortie structurée avec au minimum `faits`, `hypotheses`, `recommandations` | ✅ Oui |
| 5 | **Interdits absents** | Aucun des interdits absolus du contrat prompt n'est présent (diagnostic DSM, pronostic, prescription) | ⚠️ Semi |
| 6 | **Ton autorisé respecté** | Le prompt utilise le ton clinique-neutre (pas de ton empathique-conversationnel ni d'assertivité médicale) | ⚠️ Semi |
| 7 | **Niveau de preuve explicite** | Le prompt demande de distinguer faits observés vs inférences vs recommandations | ✅ Oui |
| 8 | **Test associé existant** | Le fichier `test_associe` référencé existe dans `tests/` | ✅ Oui |
| 9 | **Exemple bon/mauvais présent** | Le prompt inclut au moins 1 exemple de sortie conforme et 1 non conforme | ⚠️ Semi |
| 10 | **Validation humaine** | Un praticien ou superviseur a relu la sortie produite avec ce prompt sur un cas réel ou simulé | ❌ Non — humain obligatoire |

---

## Fiche de PR (à joindre à chaque PR de prompt)

```markdown
## Grille Go/No-Go — [NOM_PROMPT_V1]

| # | Check | Statut | Remarque |
|---|---|---|---|
| 1 | Frontmatter complet | ✅ / ❌ | |
| 2 | Contrat prompt référencé | ✅ / ❌ | |
| 3 | Type de sortie déclaré | ✅ / ❌ | |
| 4 | Schéma JSON déclaré | ✅ / ❌ | |
| 5 | Interdits absents | ✅ / ❌ | |
| 6 | Ton autorisé respecté | ✅ / ❌ | |
| 7 | Niveau de preuve explicite | ✅ / ❌ | |
| 8 | Test associé existant | ✅ / ❌ | |
| 9 | Exemple bon/mauvais présent | ✅ / ❌ | |
| 10 | Validation humaine | ✅ / ❌ | Validé par : [NOM] le [DATE] |

**Décision :** ✅ GO / ❌ NO-GO
**Bloquants :** (liste si NO-GO)
```

---

## Automatisation recommandée (QIA-005)

Les checks 1, 2, 3, 4, 7, 8 peuvent être validés par un script pre-commit ou une GitHub Action :

```python
# scripts/check_prompt_gonogo.py
import yaml, sys
from pathlib import Path

def check_prompt(path: Path) -> list[str]:
    errors = []
    content = path.read_text()
    # Extraire frontmatter YAML
    if not content.startswith("---"):
        errors.append("CHECK-1: Frontmatter YAML absent")
        return errors
    fm_raw = content.split("---")[1]
    fm = yaml.safe_load(fm_raw)
    for field in ["id", "version", "date", "statut", "type_sortie", "test_associe"]:
        if field not in fm:
            errors.append(f"CHECK-1: Champ {field} manquant")
    if "MERLIN_CONTRAT_PROMPT" not in content:
        errors.append("CHECK-2: Contrat prompt non référencé")
    valid_types = ["note_clinique", "triage_urgence", "validation_pilote", "synthese_dossier"]
    if fm.get("type_sortie") not in valid_types:
        errors.append(f"CHECK-3: type_sortie invalide — valeurs acceptées : {valid_types}")
    for field in ["faits", "hypotheses", "recommandations"]:
        if field not in content:
            errors.append(f"CHECK-4: Champ JSON {field} non déclaré dans le prompt")
    tests_dir = Path("tests")
    test_ref = fm.get("test_associe", "")
    if test_ref and not any(tests_dir.rglob(f"*{test_ref}*")):
        errors.append(f"CHECK-8: Fichier test {test_ref} introuvable dans tests/")
    return errors

if __name__ == "__main__":
    path = Path(sys.argv[1])
    errors = check_prompt(path)
    if errors:
        print("❌ NO-GO — Corrections requises :")
        for e in errors: print(f"  • {e}")
        sys.exit(1)
    print("✅ Checks automatiques passés — validation humaine (check 10) requise avant merge")
```

---

## Évolution prévue

- **V2** (post-pilote) : intégration score GRILLE_QUALITE_NOTE moyen sur les 3 derniers tests comme condition supplémentaire
- **V3** : GitHub Action automatique sur PR ciblant `03_PROMPTS/` et `04_METHODES/`
