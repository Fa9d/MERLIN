---
titre: Standard de métadonnées documentaires — MERLIN
id: MERLIN-STANDARD-META-V1
statut: active
type: charte
couche: FOND
périmètre: repo entier
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [MERLIN-TAXONOMIE-DOC-V1, MERLIN-MODELE-COUCHES-V1]
remplace: []
arbitrage_requis: oui — ajout ou modification d'un champ obligatoire
source_canonique: 00_GOUVERNANCE/MERLIN_STANDARD_METADATA_V1.md
---

# MERLIN — Standard de métadonnées documentaires V1

> **Statut** : active — 2026-05-05
> **S'applique** : à tous les documents structurants de MERLIN (types charte, ADR, fondement,
> méthode, politique, spec produit, protocole, prompt).
> **Facultatif** : notes temporaires, exports, audits simples.

---

## Préambule

Un document sans métadonnées est un document difficile à auditer, à classer et à réviser.
Ce standard définit un bloc de métadonnées minimal, lisible et cohérent à travers tout MERLIN.

Il existe deux formes de métadonnées dans MERLIN :
1. **YAML frontmatter** — pour les documents qui seront traités par des outils (scripts, indexeurs).
2. **Bloc Markdown simple** — pour les documents à usage purement humain et institutionnel.

Les deux formes sont valides. Le YAML frontmatter est préféré pour les documents structurants.

---

## 1. Champs de métadonnées

| Champ | Obligatoire | Description |
|---|---|---|
| `titre` | Oui | Titre complet et lisible du document |
| `id` | Oui | Identifiant unique stable (format : `MERLIN-[DOMAINE]-[SUJET]-V[N]`) |
| `statut` | Oui | `draft` / `active` / `deprecated` / `superseded` |
| `type` | Oui | Type documentaire selon la taxonomie (charte, ADR, fondement, etc.) |
| `couche` | Oui | Couche MERLIN : `FOND` / `METH` / `EDIT` / `PROD` |
| `périmètre` | Oui | Ce que couvre le document (repo entier, module, produit) |
| `auteur` | Oui | Auteur principal (nom ou rôle : `fondateur`, `équipe`, etc.) |
| `date` | Oui | Date de création initiale (YYYY-MM-DD) |
| `version` | Oui | Version sémantique : `MAJOR.MINOR` |
| `dépend_de` | Non | Liste des IDs de documents dont celui-ci dépend directement |
| `remplace` | Non | ID du document que celui-ci remplace |
| `arbitrage_requis` | Non | `oui` + condition, ou `non` |
| `source_canonique` | Non | Chemin relatif dans le repo — pour les documents avec copies multiples |

---

## 2. Modèle YAML frontmatter (recommandé)

Utiliser ce bloc en début de fichier, avant toute autre ligne :

```yaml
---
titre: [Titre complet du document]
id: MERLIN-[DOMAINE]-[SUJET]-V[N]
statut: draft
type: [charte | ADR | fondement | preuve | méthode | export | prompt | spec | protocole | politique | audit | note]
couche: [FOND | METH | EDIT | PROD]
périmètre: [repo entier | 00_GOUVERNANCE | backend | frontend | 11_PROMPTS | ...]
auteur: fondateur
date: YYYY-MM-DD
version: 1.0
dépend_de: []
remplace: []
arbitrage_requis: [non | oui — condition]
source_canonique: [chemin/relatif/dans/repo.md]
---
```

---

## 3. Modèle bloc Markdown simple (alternatif)

Pour les documents où le YAML n'est pas souhaité (ex. : ADR courts, notes de gouvernance) :

```markdown
> **Titre** : [Titre du document]
> **ID** : MERLIN-[DOMAINE]-[SUJET]-V[N]
> **Statut** : draft | active | deprecated
> **Type** : charte | ADR | fondement | ...
> **Couche** : FOND | METH | EDIT | PROD
> **Auteur** : fondateur
> **Date** : YYYY-MM-DD
> **Version** : 1.0
> **Dépend de** : [liste ou vide]
> **Remplace** : [ID ou vide]
```

---

## 4. Exemple concret — Charte d'architecture

```yaml
---
titre: Charte d'architecture — MERLIN
id: MERLIN-CHARTE-ARCH-V1
statut: active
type: charte
couche: FOND
périmètre: repo entier
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: []
remplace: []
arbitrage_requis: oui — toute modification de cette charte
source_canonique: 00_GOUVERNANCE/MERLIN_CHARTE_ARCHITECTURE_V1.md
---
```

---

## 5. Exemple concret — Prompt système triage clinique

```yaml
---
titre: Prompt système — Triage clinique première ligne
id: MERLIN-PROMPT-TRIAGE-V1
statut: active
type: prompt
couche: PROD
périmètre: 11_PROMPTS/01_session
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [MERLIN-MODELE-COUCHES-V1, MERLIN-METH-CADRE-11NAT-V1]
remplace: []
arbitrage_requis: oui — tout changement de logique de triage
source_canonique: 11_PROMPTS/01_session/MERLIN_PROMPT_SESSION_TRIAGE_v1.0.md
---
```

---

## 6. Règles d'application

### Champs obligatoires

Les champs `titre`, `id`, `statut`, `type`, `couche`, `auteur`, `date`, `version`
sont obligatoires pour tout document structurant.
Un document sans ces champs ne peut pas être considéré comme un document de référence actif.

### Gestion des versions

- `MAJOR` : changement structurel du contenu (redéfinition, réécriture substantielle).
- `MINOR` : ajout, clarification, correction sans changement de sens.
- Ne jamais modifier un document actif sans bumper la version.
- La première publication est toujours `1.0`.

### Gestion des statuts

| Statut | Signification |
|---|---|
| `draft` | En rédaction, non validé, ne fait pas référence |
| `active` | Document de référence validé et en vigueur |
| `deprecated` | Retiré sans remplacement direct |
| `superseded` | Remplacé par un autre document (indiquer lequel dans `remplace` du nouveau) |

### Identifiants

L'identifiant `id` doit être :
- unique dans le repo,
- stable (ne change pas quand le contenu change — seule la version change),
- lisible sans lookup (il doit donner une idée du contenu).

Format recommandé : `MERLIN-[DOMAINE EN MAJUSCULES]-[SUJET COURT]-V[N]`

Exemples :
- `MERLIN-CHARTE-ARCH-V1`
- `MERLIN-METH-TRIAGE-QC-V1`
- `MERLIN-PROMPT-SYNTHESE-SEANCE-V2`
- `MERLIN-POL-CONSENTEMENT-V1`

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 1 structuration |
