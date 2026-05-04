# MERLIN — Mode d'emploi du système de gestion V1

Date: 2026-05-04
Statut: actif
Objet: guide pratique pour utiliser le système de pilotage au quotidien

> Ce document répond à une seule question : que fais-je avec ces 5 fichiers demain matin ?

---

## Les 5 fichiers — en une ligne chacun

| Fichier | Usage quotidien |
|---|---|
| `SYSTEME_GESTION_OPERATIONNEL_V1.md` | Référence — lire une fois, consulter si on doute d'une convention |
| `TABLEAU_BORD_HEBDO_V1.md` | Ouvrir chaque matin — mettre à jour l'état réel |
| `BACKLOG_MAITRE_V1.md` | Consulter avant de démarrer une tâche — mettre à jour le statut après |
| `JOURNAL_EXECUTION_V1.md` | Ajouter une ligne après chaque action significative |
| `MODE_EMPLOI_SYSTEME_GESTION_V1.md` | Ce document — relire si on est perdu |

---

## Routine quotidienne (5 à 10 minutes)

### Le matin

1. Ouvrir `TABLEAU_BORD_HEBDO_V1.md`
2. Identifier la tâche P1 ou P2 à traiter aujourd'hui
3. Dans `BACKLOG_MAITRE_V1.md`, passer son statut de `todo` à `active`
4. Travailler

### Après une action significative

Tout ce qui produit un résultat mesurable (commit, commande VPS, fichier créé, décision prise) doit générer une ligne dans `JOURNAL_EXECUTION_V1.md`.

Format :
```
| 2026-MM-JJ | Ce qui a été fait | Zone impactée | commit ou référence | Résultat | Prochaine étape |
```

### Le soir (ou en fin de session)

1. Dans `BACKLOG_MAITRE_V1.md`, passer la tâche de `active` à `done` si terminée, ou documenter le blocage si `blocked`
2. Mettre à jour le tableau de bord : statut du chantier, blocage éventuel, livrable suivant
3. Si un blocage existe : écrire explicitement la cause et la prochaine action débloquante dans le tableau de bord

---

## Routine hebdomadaire (lundi, 15 à 20 minutes)

1. Dans `BACKLOG_MAITRE_V1.md` :
   - passer les tâches `done` depuis plus de 2 semaines en `archived`
   - réévaluer les priorités (`P1/P2/P3/P4`) en fonction de l'état réel
   - ajouter les nouvelles tâches identifiées

2. Dans `TABLEAU_BORD_HEBDO_V1.md` :
   - archiver la semaine précédente (une ligne par chantier clôturé dans le journal)
   - remettre le tableau à zéro avec les chantiers actifs de la nouvelle semaine
   - mettre à jour l'entête `Semaine: ...` et `Mis à jour: ...`

3. Dans `JOURNAL_EXECUTION_V1.md` :
   - vérifier que toutes les actions de la semaine sont bien tracées

---

## Comment ouvrir un nouveau chantier

1. Identifier les tâches qui composent le chantier
2. Ajouter chaque tâche dans `BACKLOG_MAITRE_V1.md` avec un ID unique (`DOMAINE-NNN`), une priorité, un livrable attendu et un critère de sortie
3. Ajouter le chantier dans `TABLEAU_BORD_HEBDO_V1.md` si c'est pour la semaine en cours
4. Ajouter une ligne dans `JOURNAL_EXECUTION_V1.md` : `ouverture chantier [nom]`

---

## Comment clôturer une tâche

1. Vérifier que la preuve existe (commit visible sur GitHub, log terminal, fichier créé)
2. Dans `BACKLOG_MAITRE_V1.md` : statut → `done`, colonnes `Commit / Preuve` renseignées
3. Dans `TABLEAU_BORD_HEBDO_V1.md` : mettre à jour le statut du chantier concerné
4. Dans `JOURNAL_EXECUTION_V1.md` : ajouter la ligne avec le résultat et la prochaine étape

---

## Comment relier une tâche à un commit

Dans `BACKLOG_MAITRE_V1.md`, colonne `Preuve / critère de sortie` :
```
commit `abc1234`
```

Dans `JOURNAL_EXECUTION_V1.md`, colonne `Commit / Réf` :
```
abc1234
```

Régle : le hash court git de 7 caractères suffit. Pas besoin de l'URL complète GitHub.

---

## Comment relier une tâche à un document de gouvernance

Dans `BACKLOG_MAITRE_V1.md`, colonne `Preuve / critère de sortie` ou `Dépend de` :
```
référence : `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md`
```

Ne pas recopier le contenu du document. Faire référence au nom de fichier.

---

## Comment éviter de dupliquer l'information

Règle centrale : **une information a un seul endroit canonique.**

| Information | Où elle vit | Où on y fait référence |
|---|---|---|
| Une décision structurante | `MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md` | Journal + Backlog (`réf: DEC-0XX`) |
| Une procédure technique | `PROCEDURE_*` ou `RUNBOOK_*` | Backlog (`livrable: suivre PROCEDURE_*`) |
| Une checklist de validation | `CHECKLIST_*` | Backlog + Journal |
| Un log d'incident | `LOG_INCIDENT_*` | Journal (`réf: LOG_INCIDENT_*`) |
| Un résultat d'audit | `05_PREUVES_SOURCES/` | Backlog (critère de sortie) |
| Une tâche en cours | `BACKLOG_MAITRE_V1.md` | Tableau de bord (ID de tâche) |

**Si une information apparaît à deux endroits : c'est un bug de gouvernance. Garder la source canonique, remplacer la copie par une référence.**

---

## Signaux d'alerte — quand le système décroche

| Signal | Cause probable | Action corrective |
|---|---|---|
| Le tableau de bord n'a pas été mis à jour depuis 3 jours | Session intensive sans pause de pilotage | Prendre 15 min pour resynchroniser backlog + journal |
| Une tâche est `active` depuis plus de 5 jours | Tâche trop grande ou bloquage non documenté | Couper en sous-tâches ou documenter le blocage explicitement |
| Le journal n'a pas de nouvelle entrée depuis 2 jours | Actions non tracées | Reconstituer les entrées depuis les commits git |
| Des tâches apparaissent dans le tableau de bord sans être dans le backlog | Contournement du système | Toujours passer par le backlog d'abord |

---

## Compatibilité avec GitHub

Le système est entièrement markdown et git-native.

- Chaque modification d'un des 5 fichiers peut faire l'objet d'un commit `chore(gouv): ...`
- Les fichiers sont dans `00_GOUVERNANCE/`, versionné dans le repo `Fa9d/MERLIN`
- Le journal d'exécution fait le lien avec les commits git sur les autres fichiers du repo

---

## Ce système ne fait pas

- Il ne remplace pas les outils de planification longue durée (référence : `MERLIN_GOUV_RETROPLANNING_BUILD_8_SEMAINES_V1.md`)
- Il ne remplace pas le registre de décisions (`MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md`)
- Il ne remplace pas les runbooks techniques (`MERLIN_GOUV_RUNBOOK_*`)
- Il ne gère pas les secrets ni les accès (référence : `MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md`)
