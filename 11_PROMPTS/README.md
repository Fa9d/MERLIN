# 11_PROMPTS — Bibliothèque de prompts MERLIN

**Date création**: 2026-05-05  
**Statut**: actif  
**Responsable**: David Phaneuf

## Objectif

Centraliser et versionner tous les prompts utilisés dans le système MERLIN (IVIA, EMPLOI, ACTES).  
Chaque prompt est un fichier `.md` isolé, composable et traçable comme n'importe quel artefact du projet.

## Structure

```
11_PROMPTS/
├── README.md                          # Ce fichier
├── 01_session/
│   ├── PROMPT_note_clinique.md        # Audio → note structurée
│   ├── PROMPT_resume_session.md       # Résumé court pour opérateur
│   └── PROMPT_extraction_entites.md  # Extraction dates, noms, actions
├── 02_document/
│   ├── PROMPT_generation_rapport.md   # Note → document formel client
│   ├── PROMPT_validation_contenu.md   # Vérification qualité avant diffusion
│   └── PROMPT_lettre_client.md        # Génération lettre/communication client
├── 03_supervision/
│   ├── PROMPT_relecture_note.md       # Aide superviseur pour correction
│   └── PROMPT_flags_anomalies.md      # Détection anomalies dans les sessions
└── 04_admin/
    ├── PROMPT_onboarding_client.md    # Assistant création fiche client
    └── PROMPT_audit_dossier.md        # Revue complète d'un dossier
```

## Convention de format

Chaque fichier prompt suit cette structure standard :

```markdown
# PROMPT — [Nom]

## Contexte
Quand et par qui ce prompt est utilisé.

## Rôle
Instruction de persona pour le modèle.

## Instructions
1. ...
2. ...

## Format de sortie
Description ou exemple du format attendu.

## Version
vX.X — AAAA-MM-JJ
```

## Références
- [Fabric](https://github.com/danielmiessler/fabric) — inspiration structure
- [LangChain Hub](https://smith.langchain.com/hub) — patterns de chaîne
- [Claude Prompt Library](https://docs.anthropic.com/en/prompt-library) — prompts de base
