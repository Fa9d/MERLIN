---
id: ADR-0004
titre: Normalisation progressive de l'arborescence racine
statut: accepted
couche: FOND
type: ADR
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [ADR-0001, MERLIN-CONVENTION-NOMMAGE-V2]
remplace: []
remplacé_par: []
décideurs: fondateur
arbitrage_requis: oui — modifie la structure racine du repo
source_canonique: 00_GOUVERNANCE/ADR/ADR-0004-normalisation-arborescence.md
décision_registre: DEC-039
---

# ADR-0004 — Normalisation progressive de l'arborescence racine

> **Statut** : accepted — 2026-05-05
> **Couche concernée** : FOND
> **Document de référence** : `MERLIN_CONVENTION_NOMMAGE_V2.md`

---

## Contexte

Le fichier `MERLIN_CONVENTION_NOMMAGE_V2.md` déclare une arborescence cible pour le repo :

```
00_GOUVERNANCE/
01_FONDEMENTS/
03_MODELES/
04_METHODES/
05_PREUVES/
06_IMPORTS/
07_PRODUITS/
08_OPERATIONS/
09_EXPORTS/
```

L'arborescence **réelle** du repo au 2026-05-05 est :

```
00_GOUVERNANCE/
01_FONDATEUR/           ← non déclaré dans V2
01_FONDEMENTS/          ← coexiste avec 01_FONDATEUR/ (doublon numérique)
02_NATIONS_QC/          ← absent de V2
03_MODELE_GOUVERNANCE/  ← V2 déclare "03_MODELES/"
04_METHODES/            ← conforme
05_PREUVES_SOURCES/     ← V2 déclare "05_PREUVES/"
06_IMPORTS_MESANGE/     ← V2 déclare "06_IMPORTS/"
07_EXPORTS/             ← V2 déclare "07_PRODUITS/" et "09_EXPORTS/"
08_EMPLOI/              ← V2 déclare "08_OPERATIONS/"
09_app_ivia_merlin/     ← non déclaré dans V2
10_backend_merlin_api/  ← non déclaré dans V2
11_PROMPTS/             ← ajouté en Vague 2 (ADR-0002), non déclaré dans V2
12_JURIDIQUE_AFFAIRES/  ← non déclaré dans V2
DAVID_CORPUS/           ← corpus externe non numéroté
deploy/                 ← infra, non déclaré
docs/                   ← documentation technique, non déclaré
memory/                 ← mémoire de session, non déclaré
nginx/                  ← configuration infra, non déclaré
_ARCHIVES_IMPORT/       ← archives, non déclaré
_runtime_logs/          ← logs, non déclaré
```

Cet écart est le résultat d'une **croissance organique non gouvernée** : chaque couche a été
ajoutée selon les besoins immédiats, sans alignement avec la convention. `V2` a été rédigée
après coup comme projection normative, pas comme reflet de l'état réel.

**Problèmes concrets :**
1. `01_FONDATEUR/` et `01_FONDEMENTS/` ont le même numéro préfixe — collision d'index.
2. `03_MODELE_GOUVERNANCE/` ne correspond pas à `03_MODELES/` — nom trop spécifique.
3. `05_PREUVES_SOURCES/` vs `05_PREUVES/` — suffixe non harmonisé.
4. `07_EXPORTS/` et `09_EXPORTS/` désignent la même chose selon quelle convention l'on suit.
5. `08_EMPLOI/` (contenu RH/opérationnel) vs `08_OPERATIONS/` (infrastructures).
6. `09_app_ivia_merlin/` et `10_backend_merlin_api/` n'ont pas de slot dans V2.
7. `11_PROMPTS/` a été créé par ADR-0002 mais V2 n'a pas été mis à jour.

---

## Options considérées

### Option A — Renommer tous les dossiers pour les aligner sur V2
**Avantages** : convention propre, navigation intuitive.
**Inconvénients** : opération massive, casse tous les chemins absolus dans le code backend,
les scripts PowerShell, les imports Python, les configs Nginx. Risque de régression en
production. Estimé : 2-3 jours de travail sécurisé.

**Rejetée** — trop risquée à ce stade (phase pilote en production).

### Option B — Mettre à jour V2 pour qu'elle reflète la réalité, sans renommer
**Avantages** : cohérence immédiate entre la convention et l'état réel. Coût nul sur
l'arborescence physique.
**Inconvénients** : la convention perd sa valeur normative prospective. Elle devient descriptive.

**Retenue partiellement** — mise à jour de V2 est nécessaire, mais insuffisante sans plan
de convergence.

### Option C — Gel de la convention et migration progressive sur 3 vagues
**Avantages** : équilibre entre gouvernance et stabilité. Chaque vague de migration est
bornée, testée, committée séparément.
**Inconvénients** : délai de convergence de plusieurs semaines.

**Retenue** — approche par défaut du modèle de couches MERLIN (ADR-0001).

---

## Décision

Adopter l'**Option C** : normalisation progressive par vagues, en commençant par les
corrections à coût nul (renommages de dossiers documentaires uniquement, sans impact code).

### Règles de normalisation adoptées

| Slot | Nom actuel (réel) | Nom cible normalisé | Priorité migration |
|---|---|---|---|
| 00 | `00_GOUVERNANCE/` | `00_GOUVERNANCE/` | N/A — conforme |
| 01a | `01_FONDATEUR/` | Fusionner dans `01_FONDEMENTS/` | P2 |
| 01b | `01_FONDEMENTS/` | `01_FONDEMENTS/` | P2 |
| 02 | `02_NATIONS_QC/` | `02_NATIONS_QC/` | Conserver — périmètre distinct |
| 03 | `03_MODELE_GOUVERNANCE/` | `03_MODELES/` | P3 |
| 04 | `04_METHODES/` | `04_METHODES/` | N/A — conforme |
| 05 | `05_PREUVES_SOURCES/` | `05_PREUVES/` | P3 |
| 06 | `06_IMPORTS_MESANGE/` | `06_IMPORTS/` | P3 |
| 07 | `07_EXPORTS/` | `07_EXPORTS/` | Conserver — nom clair |
| 08 | `08_EMPLOI/` | `08_OPERATIONS/` | P2 |
| 09 | `09_app_ivia_merlin/` | `09_FRONTEND/` | P2 |
| 10 | `10_backend_merlin_api/` | `10_BACKEND/` | P2 |
| 11 | `11_PROMPTS/` | `11_PROMPTS/` | N/A — créé par ADR-0002 |
| 12 | `12_JURIDIQUE_AFFAIRES/` | `12_JURIDIQUE/` | P3 |

**Dossiers hors-numérotation (conserver tels quels) :**
- `DAVID_CORPUS/` — corpus externe, périmètre à définir
- `deploy/`, `nginx/` — infra, hors périmètre documentaire
- `docs/` — documentation technique automatique
- `memory/` — mémoire de session, hors repo canonique
- `_ARCHIVES_IMPORT/`, `_runtime_logs/` — préfixe `_` = hors-navigation volontaire

### Mise à jour de `MERLIN_CONVENTION_NOMMAGE_V2.md`
`V2` sera mis à jour en `V3` pour refléter l'arborescence réelle + les noms cibles.
Cette mise à jour est la première action de Vague 3 (post-ADR-0004).

---

## Conséquences

### Avantages

- Normalisation progressive sans risque de régression en production (pas de renommage à chaud).
- La convention V2 devient descriptive de la réalité plutôt que normative sur une arborescence brisée.
- Chaque migration est bornée, testée et committée séparément — réversible à tout moment.
- Les dossiers applicatifs (`09_app_ivia_merlin/`, `10_backend_merlin_api/`) et `11_PROMPTS/` obtiennent un slot explicite dans la convention V3.

### Inconvénients ou risques

- Délai de convergence : plusieurs semaines avant que l'arborescence réelle soit conforme à V3.
  → Règle : utiliser les noms actuels dans le code jusqu'à migration formelle tracée par ADR ou log de gouvernance.
- `MERLIN_CONVENTION_NOMMAGE_V2.md` est temporairement incohérent avec l'arborescence réelle jusqu'à création de V3.
  → Action : priorité P1 en Vague 3 (action 2 ci-dessous).

---

## Actions requises

1. Ajouter **DEC-039** au registre des décisions MERLIN.
2. Créer `MERLIN_CONVENTION_NOMMAGE_V3.md` en Vague 3 — aligner convention sur réalité +
   noms cibles normalisés.
3. Fusionner `01_FONDATEUR/` dans `01_FONDEMENTS/` en Vague 3 (P2).
4. Renommer `08_EMPLOI/` → `08_OPERATIONS/` en Vague 3 — vérifier impact sur scripts PowerShell.

---

## Entrée registre associée

> DEC-039 | 2026-05-05 | arborescence | normalisation progressive arborescence racine — migration par vagues | validated | ADR-0004

---

## Historique de révisions

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création — ADR Vague 2 |
