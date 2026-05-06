# MERLIN_GRILLE_GONOGO_PROMPT_V1

**Version:** 1.0  
**Statut:** ACTIF  
**Date:** 2026-05-06  
**Décision associée:** DEC-039  
**Usage :** Gate de merge — à compléter pour tout PR modifiant un fichier prompt  

---

## Grille Go/No-Go — 10 checks obligatoires

À cocher **avant tout merge** sur `master` impliquant un fichier prompt (METH, PROD, OPER, SYS).

Un seul ❌ = **merge bloqué jusqu'à correction**.

---

| # | Check | Critère de passage | Go ✅ / No-Go ❌ |
|---|---|---|---|
| 1 | **Frontmatter complet** | Les champs `id`, `version`, `layer`, `trigger`, `surface`, `status`, `date`, `test_associe` sont tous présents | |
| 2 | **Version incrémentée** | Le numéro de version est plus élevé que la version précédente sur `master` | |
| 3 | **Impact documenté** | Le champ `impact_attendu` décrit ce que ce changement est censé améliorer | |
| 4 | **Test associé existant** | Le fichier de test référencé dans `test_associe` existe dans `tests/` | |
| 5 | **Test associé passant** | `pytest -k <test_associe>` retourne 0 failures | |
| 6 | **Aucun interdit présent** | Scan manuel ou automatique : aucun des interdits de MERLIN_CONTRAT_PROMPT_V1 §4 détecté | |
| 7 | **Distinction faits/hypothèses/recommandations** | Le prompt produit (ou exige) une sortie avec ces trois niveaux séparés | |
| 8 | **Format de sortie valide** | La sortie du prompt est conforme au schéma JSON défini dans MERLIN_CONTRAT_PROMPT_V1 §5 | |
| 9 | **Ton neutre vérifié** | Aucune formulation évaluative, diagnostique ou prescriptive dans le prompt ou ses exemples | |
| 10 | **Revue humaine faite** | Au moins une relecture humaine du prompt a été effectuée (pas seulement IA-sur-IA) | |

---

## Fiche de merge (à joindre au PR)

```
PR : #_______
Prompt modifié : ________________
Version : _______ → _______
Auteur : ________________
Date : ________________

Check 1  — Frontmatter complet       : ✅ / ❌
Check 2  — Version incrémentée       : ✅ / ❌
Check 3  — Impact documenté          : ✅ / ❌
Check 4  — Test associé existant     : ✅ / ❌
Check 5  — Test associé passant      : ✅ / ❌
Check 6  — Aucun interdit présent    : ✅ / ❌
Check 7  — Faits/Hypothèses/Reco     : ✅ / ❌
Check 8  — Format de sortie valide   : ✅ / ❌
Check 9  — Ton neutre vérifié        : ✅ / ❌
Check 10 — Revue humaine faite       : ✅ / ❌

RÉSULTAT : GO ✅ / NO-GO ❌
```

---

## Notes d'application

- **Check 5** est le seul check automatisable en CI. Les autres sont sous responsabilité humaine.
- **Check 10** ne peut pas être satisfait par l'IA seule. Une relecture humaine, même courte (5 min), est obligatoire.
- En cas de No-Go sur check 6 ou 9 : documenter l'élément problématique dans le commentaire du PR avant de corriger.
- Cette grille s'applique à tous les prompts, même les corrections mineures de formulation.

---

*Document de gouvernance MERLIN — outil de merge gate, non substituable au jugement éditorial.*
