# MERLIN — Index du dépôt

> **Branche active : `master`** (corpus documentaire + articles IVIA + infrastructure)
> Branche `main` : plateforme technique Next.js — ne pas confondre.

---

## Structure des dossiers

```
C:\MERLIN\
├── 00_GOUVERNANCE/          # Décisions, politiques, conventions, benchmarks, backlogs
├── 01_FONDATEUR/            # Fondements philosophiques et doctrine du projet (hors IVIA)
├── 01_FONDEMENTS/           # Documents fondateurs IVIA (charte, cercle, positionnement stratégique, plan éditorial)
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

Exception formalisée — corpus IVIA : `IVIA_[TYPE]_[SUJET]_v[MAJOR].[MINOR].md`

**Référence active :** [00_GOUVERNANCE/MERLIN_CONVENTION_NOMMAGE_V2.md](00_GOUVERNANCE/MERLIN_CONVENTION_NOMMAGE_V2.md)
*(remplace V1 — formalise IVIA_, BACK_, FRONT_)*

---

## Documents de référence rapide

| Fichier | Rôle |
|---|---|
| [00_GOUVERNANCE/MERLIN_CONVENTION_NOMMAGE_V2.md](00_GOUVERNANCE/MERLIN_CONVENTION_NOMMAGE_V2.md) | Convention de nommage active (v2) |
| [00_GOUVERNANCE/IVIA_INDEX_BASE_DOCUMENTAIRE_v2.0.md](00_GOUVERNANCE/IVIA_INDEX_BASE_DOCUMENTAIRE_v2.0.md) | **Index complet base documentaire IVIA v2.0** (point d'entrée corpus) |
| [00_GOUVERNANCE/IVIA_BILAN_COHERENCE_REFONTE_v2.0.md](00_GOUVERNANCE/IVIA_BILAN_COHERENCE_REFONTE_v2.0.md) | Bilan refonte v2.0 post-DÉC-V3-15 (12/12 livrées) |
| [00_GOUVERNANCE/IVIA_HISTORIQUE_DECISIONS_STRATEGIQUES_v2.0.md](00_GOUVERNANCE/IVIA_HISTORIQUE_DECISIONS_STRATEGIQUES_v2.0.md) | Journal des décisions stratégiques (DÉC-V3-1 → V3-15) |
| [00_GOUVERNANCE/IVIA_CHARTE_DOCTRINAIRE_v2.0.md](00_GOUVERNANCE/IVIA_CHARTE_DOCTRINAIRE_v2.0.md) | Charte doctrinaire IVIA v2.0 |
| [00_GOUVERNANCE/IVIA_GOUVERNANCE_INTERNE_v2.0.md](00_GOUVERNANCE/IVIA_GOUVERNANCE_INTERNE_v2.0.md) | Gouvernance interne (SPA-mère + OBNL satellite) |
| [12_JURIDIQUE_AFFAIRES/IVIA_STRUCTURE_JURIDIQUE_RECOMMANDEE_v2.0.md](12_JURIDIQUE_AFFAIRES/IVIA_STRUCTURE_JURIDIQUE_RECOMMANDEE_v2.0.md) | Structure juridique cible (DÉC-V3-15) |
| [12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.0.md](12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.0.md) | Business Plan v2.0 (refonte post-DÉC-V3-15) |
| [01_FONDEMENTS/IVIA_POSITIONNEMENT_STRATEGIQUE_EDITORIAL_v1.0.md](01_FONDEMENTS/IVIA_POSITIONNEMENT_STRATEGIQUE_EDITORIAL_v1.0.md) | Positionnement IVIA, cadre légal, textes site, capsules audio |
| [01_FONDEMENTS/IVIA_DOCUMENT_DIRECTEUR_v1.0.md](01_FONDEMENTS/IVIA_DOCUMENT_DIRECTEUR_v1.0.md) | Charte philosophique — 7 principes fondateurs |
| [04_METHODES/IVIA_PLAN_EDITORIAL_v1.0.md](04_METHODES/IVIA_PLAN_EDITORIAL_v1.0.md) | Plan 16 articles × calendrier 16 semaines |
| [00_GOUVERNANCE/IVIA_ARBITRAGE_AXE_FREQUENCE_v1.md](00_GOUVERNANCE/IVIA_ARBITRAGE_AXE_FREQUENCE_v1.md) | Arbitrage axe FRÉQUENCE — décision APPROUVÉE |

---

## Refonte v2.0 (DÉC-V3-15) — État

**Décision pivot :** IVIA inc. (SPA-mère LSAQ à mission, 100 % David Phaneuf) ──licence sociale──▶ IVIA OBNL (satellite LCQ III).
Sous IVIA inc. : MERLIN, MÉSANGE, COVOITURAGE, LOGISTIQUE, NHL ANALYTICS, futurs projets civiques.

- **12/12 documents refondus** (BP, structure juridique, gouvernance, modèle valorisation, etc.)
- **3 documents archivés** (`00_GOUVERNANCE/ARCHIVES/v1_pre_DEC-V3-15/`) : ancienne structure OBNL+MERLIN inc.
- **3 briefs juridico-fiscaux livrés** : avocat société multi-entités, fiscaliste (CRIC + RS&DE), shortlist 6 cabinets Montréal.
- **Pilote MERLIN actif** depuis 31 mai 2026.

Voir le bilan complet : [IVIA_BILAN_COHERENCE_REFONTE_v2.0.md](00_GOUVERNANCE/IVIA_BILAN_COHERENCE_REFONTE_v2.0.md)

---

## Repères techniques

- **Repo GitHub** : `https://github.com/Fa9d/MERLIN`
- **Branche documentaire** : `master` ← vous êtes ici
- **Branche technique** : `main` (Next.js standalone, à ne pas merger avec master)
- **VPS** : `ubuntu@137.74.42.121:/opt/merlin`
- **API base URL** : `https://api.ivia.quebec/api/v1`
- **Frontend** : `https://ivia.quebec`

---

*Dernière mise à jour : 8 mai 2026 — refonte v2.0 dispatchée (DÉC-V3-15)*
