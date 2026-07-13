# CLAUDE.md — IVIA / MERLIN Project

## Contexte du projet

IVIA est une plateforme de santé mentale contextualisée ancrée au Québec.
MERLIN est le moteur de structuration et d'analyse des séances.
MÉSANGES est l'interface vocale relationnelle.

Ce dépôt contient le backend FastAPI (MERLIN), les assets web (IVIA.quebec), et les modules de modèles comportementaux.

---

## Architecture globale

```
IVIA (maison d'accueil, site public)
  └── MERLIN (backend FastAPI — moteur d'analyse et de sessions)
        └── MÉSANGES (interface vocale — LiveKit + audio)
```

---

## Stack technique

- **Backend** : Python / FastAPI
- **Audio / Vidéo** : LiveKit
- **Base de données** : à confirmer (PostgreSQL ou SQLite selon l'environnement)
- **Déploiement** : à définir (Docker, serveur dédié ou cloud)
- **Frontend** : à définir (léger, intégré à IVIA.quebec)

---

## Priorités actuelles

1. Stabiliser les endpoints critiques de MERLIN (sessions, notes, audio)
2. Harmoniser les schémas d'entrée et de sortie
3. Documenter chaque flux (voir `/docs/flux/`)
4. Préparer un premier pilote avec 2–3 praticiens
5. Aligner la démo produit avec le deck investisseurs

---

## Ce que Claude Code doit savoir

- Ne pas casser les endpoints existants sans validation explicite
- Toujours documenter les nouvelles fonctions avec une docstring claire
- Respecter la séparation entre traitement métier (MERLIN) et interface (IVIA)
- Les modèles comportementaux sont dans `/modules/comportementaux/`
- Les flux de séances sont dans `/routes/sessions/`
- Les schémas Pydantic sont dans `/schemas/`

---

## Conventions de code

- Python 3.11+
- Black pour le formatage
- Pydantic v2 pour les schémas
- Noms de fonctions en snake_case, noms de classes en PascalCase
- Commentaires en français sauf pour les noms de variables et fonctions
- Chaque endpoint doit avoir un docstring avec : description, paramètres attendus, sortie

---

## Fichiers importants à ne pas toucher sans instruction

- `main.py` — point d'entrée FastAPI
- `config.py` — configuration globale
- `auth/` — gestion d'accès (ne pas modifier sans validation)
- `modules/comportementaux/` — modèles sensibles, toute modification doit être documentée

---

## Commandes utiles

```bash
# Lancer le serveur de développement
uvicorn main:app --reload

# Lancer les tests
pytest tests/

# Formater le code
black .

# Vérifier les types
mypy .
```

---

## Contexte investisseurs / pilotes

Le projet est en phase de préparation au pilote.
Le deck investisseurs est disponible dans AppFlowy (espace Shared).
Toute modification majeure à l'architecture doit être alignée avec la roadmap produit.
