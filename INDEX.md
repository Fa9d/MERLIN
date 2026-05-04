# MERLIN — Index du dépôt

> **Branche active : `master`** (corpus documentaire + articles IVIA + infrastructure)
> Branche `main` : plateforme technique Next.js — ne pas confondre.

---

## Structure des dossiers

```
C:\MERLIN\
├── 00_GOUVERNANCE/          # Décisions, politiques, conventions, benchmarks, backlogs
├── 01_FONDATEUR/            # Fondements philosophiques et doctrine du projet (hors IVIA)
├── 01_FONDEMENTS/           # Documents fondateurs IVIA (charte, cercle, plan éditorial)
├── 02_NATIONS_QC/           # Fiches-nations, cadres concepts autochtones Québec
├── 03_MODELE_GOUVERNANCE/   # Modèle opératoire MERLIN, axes CERCLE
├── 04_METHODES/             # Playbooks, méthodes, articles éditoriaux IVIA
│   └── articles/            # 16 articles fondateurs IVIA (S1→S16)
├── 05_PREUVES_SOURCES/      # Références, audits, sources vérifiées
├── 06_IMPORTS_MESANGE/      # Imports one-way horodatés depuis sources historiques
├── 07_EXPORTS/              # Livrables publiés et versions de diffusion
├── 08_EMPLOI/               # Runbooks, checklists, control center emploi
├── 09_app_ivia_merlin/      # Application frontend Next.js + Prisma (branche master ≠ main)
├── 10_backend_merlin_api/   # API backend FastAPI + Alembic + SQLAlchemy
├── DAVID_CORPUS/            # Corpus personnel David Phaneuf (écrits, références)
├── deploy/                  # Scripts et config de déploiement VPS
├── docs/                    # Documentation technique complémentaire
├── nginx/                   # Configuration Nginx (reverse proxy, SSL)
└── memory/                  # Couche mémoire opérationnelle (ignorée par git)
```

---

## Fichiers de configuration clés à la racine

| Fichier | Rôle |
|---|---|
| `.env.example` | Variables d'environnement dev (template) |
| `.env.prod.example` | Variables d'environnement production (template) |
| `docker-compose.yml` | Stack locale (dev) |
| `docker-compose.prod.yml` | Stack production (VPS) |
| `Makefile` | Commandes courantes : `up`, `down`, `logs`, `migrate` |
| `deploy.sh` | Script de déploiement automatisé sur VPS |
| `.gitignore` | Exclusions git (logs, imports, exports, certs, archives) |
| `README.md` | Point d'entrée général du projet |

---

## Convention de nommage

Les fichiers documentaires suivent la convention :
`MERLIN_[DOMAINE]_[TYPE]_[SUJET]_v[MAJOR].[MINOR].md`

Voir [00_GOUVERNANCE/MERLIN_CONVENTION_NOMMAGE_V1.md](00_GOUVERNANCE/MERLIN_CONVENTION_NOMMAGE_V1.md)

---

## Repères techniques

- **Repo GitHub** : `https://github.com/Fa9d/MERLIN`
- **Branche documentaire** : `master` ← vous êtes ici
- **Branche technique** : `main` (Next.js standalone, à ne pas merger avec master)
- **VPS** : `ubuntu@137.74.42.121:/opt/merlin`
- **API base URL** : `https://api.ivia.quebec/api/v1`
- **Frontend** : `https://ivia.quebec`

---

*Dernière mise à jour : Mai 2026*
