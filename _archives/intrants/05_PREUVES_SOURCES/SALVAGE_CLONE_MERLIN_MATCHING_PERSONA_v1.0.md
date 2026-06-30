# Récupération — WIP du clone imbriqué `MERLIN/MERLIN/` (matching / carte abstraite / persona)

**Date** : 2026-06-26
**Statut** : intention **sauvegardée** (le code divergent n'est PAS mergé). Décision produit en attente.

> But : préserver dans le contrôle de version l'**intention** d'un WIP trouvé dans un **clone
> imbriqué périmé** (`C:\MERLIN\MERLIN\`, snapshot ~9-10 mai, branche `master` `3089ae9` « Copilot
> Sprint 2 »), pour pouvoir le **supprimer sans rien perdre**.

---

## 1. Ce qu'est le clone
Un **2ᵉ clone complet** du projet, gitignored, daté de **début mai** (son `CLAUDE.md` dit encore
frontend Next.js/Prisma, HEAD `0017`, dossiers `06_IMPORTS_MESANGE/07/08`). C'est une **lignée
divergente abandonnée** : le repo principal a **placeholdé** par-dessus (`20260511_0021_placeholder_restore_chain`),
donc les migrations `0019/0020` du clone n'ont **jamais** rejoint la chaîne principale (head actuel `0039`).

## 2. Pourquoi NE PAS back-merger
- `matching.py` (68 l.), `schemas/matching.py` (36 l.), `practitioner_profile.py` (18 l.),
  `services/matching.py` (14 l.) ont **évolué autrement** dans le principal → écraser = régression.
- Les migrations `0019/0020` ne s'insèrent pas (chaîne placeholdée) → casseraient l'historique.
- `docker-compose.yml` (198 l.) = vieux fichier dev → ne pas toucher.

## 3. Intention salvageable (capturée ici — re-dérivable sans le clone)

### 3.1 Carte abstraite praticien + modalité (migration `0019`)
Ajoute à `practitioner_profiles` (colonnes `String(64)`, nullable) :
- `abstract_palette`, `abstract_texture`, `abstract_motif` — **identité visuelle abstraite**
  (pas de photo ; conforme à `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md`).
- `listening_modality` — modalité d'écoute du praticien.
- `pilot_persona_label` — étiquette de persona pilote.

### 3.2 Seed 6 personas pilotes (migration `0020`)
Insère 6 personas pilotes (données de démarrage du matching). *(Contenu détaillé : voir le clone,
`…/alembic/versions/20260510_0020_seed_6_personas_pilotes.py`.)*

### 3.3 Mapping besoin → domaine (`services/intake_to_matching.py`)
Relie le `NeedCode` (Mésange) au `Domaine` (matching) — **petite pépite propre, réutilisable telle quelle** :
```
clarification → identite     support     → relation
orientation   → transition   loneliness  → relation
distress      → anxiete      other/def.  → autre
```

## 4. Pointeurs (dans le clone, à miner si on ré-implémente)
- `C:\MERLIN\MERLIN\10_backend_merlin_api\app\services\intake_to_matching.py`
- `…\alembic\versions\20260510_0019_praticien_carte_abstraite_modalite_persona.py`
- `…\alembic\versions\20260510_0020_seed_6_personas_pilotes.py`
- `…\app\{api/routes/matching.py, schemas/matching.py, services/matching.py, models/practitioner_profile.py}` (versions divergentes)

## 5. Recommandation
- **Si la feature est voulue** : la **ré-implémenter proprement sur la lignée actuelle** (matching
  courant, nouvelle migration > `0039`) — décision produit, pas un merge. Le mapping §3.3 est
  directement réutilisable ; la carte abstraite §3.1 s'aligne sur la doctrine existante.
- **Une fois cette note validée**, le clone `C:\MERLIN\MERLIN\` peut être **supprimé sans perte**.

## 6. Non fait (volontaire)
Aucun back-merge, aucune migration ajoutée, aucun fichier du principal modifié, clone non supprimé.
