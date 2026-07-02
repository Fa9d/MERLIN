# Guide — Ajout du champ `test_associe` dans les frontmatters prompts

**Version:** 1.0  
**Date:** 2026-05-06  
**Décision associée:** DEC-041  

---

## Contexte

Tous les prompts METH et PROD doivent avoir un champ `test_associe` dans leur frontmatter YAML pour maintenir la **lisibilité causale** : chaque prompt est lié à un test qui valide son comportement.

---

## Frontmatter cible (modèle complet)

```yaml
---
id: METH-001
version: "1.2"
layer: methode
trigger: post_session
surface: backend
status: actif
date: 2026-04-15
test_associe: test_prompt_injection.py::test_meth001_no_diagnosis
changement_v1_2: "Description du changement"
impact_attendu: "Ce que ce changement améliore"
---
```

---

## Patches à appliquer par fichier

### Prompts METH (à patcher en priorité)

| Fichier | ID | `test_associe` à ajouter |
|---|---|---|
| `11_PROMPTS/01_methode/METH-001_*.md` | METH-001 | `test_prompt_injection.py::test_meth001_no_diagnosis` |
| `11_PROMPTS/01_methode/METH-002_*.md` | METH-002 | `test_json_schema_validation.py::test_meth002_schema_structure` |
| `11_PROMPTS/01_methode/METH-003_*.md` | METH-003 | `test_json_schema_validation.py::test_meth003_required_fields` |
| `11_PROMPTS/01_methode/METH-004_*.md` | METH-004 | `test_prompt_injection.py::test_meth004_urgence_fields` |

### Prompts PROD (à patcher en priorité)

| Fichier | ID | `test_associe` à ajouter |
|---|---|---|
| `11_PROMPTS/02_production/PROD-001_*.md` | PROD-001 | `test_json_schema_validation.py::test_prod001_output` |
| `11_PROMPTS/02_production/PROD-009_*.md` | PROD-009 | `test_json_schema_validation.py::test_prod009_validation_schema` |
| *(autres PROD-002→008)* | PROD-002→008 | `test_json_schema_validation.py::test_prod_generic` |

---

## Prompt Claude Code pour appliquer les patches

Coller dans Claude Code une fois le commit Vague 6 pushé :

```
@workspace Vague 6 — Patch frontmatter P2

Pour chaque fichier prompt dans 11_PROMPTS/01_methode/ et 11_PROMPTS/02_production/ :
1. Lire le frontmatter YAML existant
2. Ajouter le champ `test_associe` selon la table du fichier FRONTMATTER_PATCH_GUIDE.md
3. Ajouter le champ `impact_attendu` avec la valeur "À documenter lors de la prochaine modification"
   si le champ est absent
4. Ne pas modifier le contenu du prompt — frontmatter uniquement
5. Commiter avec : "chore(prompts): ajout champ test_associe dans frontmatters METH+PROD — DEC-041"
```

---

## Vérification post-patch

```powershell
# Vérifier que tous les prompts METH ont un test_associe
Select-String -Path "11_PROMPTS\01_methode\*.md" -Pattern "test_associe" | Measure-Object
# Attendu : autant de lignes que de fichiers .md dans le dossier

# Même vérification pour PROD
Select-String -Path "11_PROMPTS\02_production\*.md" -Pattern "test_associe" | Measure-Object
```

---

*Document de travail Vague 6 — supprimer après application des patches.*
