---
titre: Gouvernance des prompts — versionnage, localisation, auditabilité
id: ADR-0002
statut: accepted
couche: PROD
type: ADR
auteur: fondateur
date: 2026-05-05
version: 1.0
décideurs: fondateur
remplace: []
remplacé_par: []
---

# ADR-0002 — Gouvernance des prompts : versionnage, localisation, auditabilité

> **Statut** : accepted — 2026-05-05
> **Couche concernée** : PROD (les prompts appartiennent à la couche PROD)
> **Politique de données liée** : ADR-0003

---

## Contexte

MERLIN utilise des prompts IA pour des tâches de natures très différentes :
- triage et orientation clinique (à forte portée métier),
- synthèse de séances (à forte portée légale),
- génération de contenus éditoriaux (à faible portée métier),
- administration et routage (à portée technique).

Dans l'état actuel du repo, une partie de ces prompts est hardcodée directement
dans le backend Python (`10_backend_merlin_api/`) sans :
- version Markdown de référence,
- localisation dans une bibliothèque,
- traçabilité des changements,
- lien explicite à la couche ou à la méthode qu'ils implémentent.

Un prompt hardcodé est une règle métier invisible. Si un modèle IA change de comportement
parce qu'un prompt a été modifié silencieusement, l'impact est indétectable sans relecture
du code source.

La règle MERLIN est que **toute instruction structurelle ou métier à un modèle IA
est un document de gouvernance**, soumis aux mêmes règles que les autres documents
de la couche PROD.

---

## Options considérées

**Option A — Prompts hardcodés dans le code, commentaires suffisants**
Simple à court terme.
*Rejeté* : les commentaires de code ne sont pas versionnés de la même façon que les décisions
de gouvernance. Un changement de prompt ne déclenche pas de révision de politique.
Impossible à auditer sans lire le code.

**Option B — Prompts dans des fichiers `.txt` non versionnés**
Plus lisibles que le code inline.
*Rejeté* : pas de métadonnées, pas de statut, pas de lien à une couche, pas de bump obligatoire.
Le problème de traçabilité demeure.

**Option C — Bibliothèque de prompts versionnés en Markdown dans `11_PROMPTS/`**
Chaque prompt est un document Markdown avec métadonnées (type, couche, version, usage).
Les prompts sont chargés dynamiquement depuis les fichiers, ou leur version de référence
est maintenue en Markdown et toute modification doit être reflétée dans les deux.
*Retenu* : aligné avec le modèle de couches, auditable, compatible avec la délégation
à un outil IA ou à un collaborateur.

---

## Décision

1. **Tout prompt structurel ou métier doit avoir une version Markdown de référence
   dans `11_PROMPTS/`**, avec les métadonnées standard (voir `MERLIN_STANDARD_METADATA_V1.md`).

2. **Aucun prompt ne peut être modifié en production** sans un bump de version
   dans le fichier Markdown de référence correspondant.

3. **Tout changement de logique** d'un prompt de triage, de synthèse, ou de politique
   exige un arbitrage explicite (et un ADR si le changement est structurant).

4. **Les prompts sont classés en sous-dossiers** selon leur nature :
   - `01_session/` — prompts de séance (triage, orientation, transcription)
   - `02_document/` — prompts de génération de documents (synthèse, note, rapport)
   - `03_supervision/` — prompts de supervision et de détection de signaux
   - `04_admin/` — prompts administratifs (onboarding, routage, confirmation)
   - `05_pilote/` — prompts d'évaluation et de pilotage

5. **Un prompt qui n'est pas dans `11_PROMPTS/`** n'est pas un prompt gouverné.
   Il peut exister dans le code comme valeur par défaut temporaire,
   mais doit être migré avant toute mise en production d'une fonctionnalité qui l'utilise.

6. **La couche d'un prompt** doit être définie dans ses métadonnées.
   Exemples : un prompt de triage clinique est PROD (avec dépendance vers METH) ;
   un prompt de génération de page publique est PROD (avec dépendance vers EDIT).

---

## Conséquences

### Avantages

- Chaque prompt peut être audité, révisé et délégué sans lire le code source.
- Un changement de comportement du modèle peut être tracé à un diff dans `11_PROMPTS/`.
- La bibliothèque de prompts devient une ressource réutilisable et documentable.
- La conformité légale (Loi 25, LPRPDE) est plus facile à démontrer si les instructions
  au modèle sont explicites et versionnées.

### Inconvénients ou risques

- Migration initiale des prompts existants : coût d'extraction et de documentation.
  → Règle de priorité : prompts de triage et de synthèse en premier.
- Risque de désynchronisation entre le code et le Markdown si le processus n'est pas respecté.
  → Règle : le Markdown est la source canonique ; le code doit le charger ou le référencer.

### Actions requises

- [ ] Créer la structure de dossiers `11_PROMPTS/01_session/`, `02_document/`, etc.
- [ ] Extraire et documenter les prompts existants dans le backend (Vague 2).
- [ ] Ajouter une règle dans `CLAUDE.md` : "Tout nouveau prompt doit d'abord exister dans 11_PROMPTS/".
- [ ] Ajouter l'entrée DEC-037 dans le registre de décisions.

---

## Entrée registre associée

> DEC-037 | 2026-05-05 | prompts | gouvernance des prompts — versionnage + localisation + auditabilité | validated | ADR-0002

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 2 |
