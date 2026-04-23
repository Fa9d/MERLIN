# MERLIN - Politique de memoire evolutive (v1)

Date: 2026-04-18
Statut: draft
Objet: enregistrer les conversations, structurer les decisions, garder le modele reinterpretable

---

## 1) Principe

MERLIN doit conserver:
- les conversations utiles;
- les decisions explicites;
- les hypotheses;
- les tensions non resolues;
- les revisions de doctrine et de modele.

Le but n'est pas de figer la pensee.
Le but est de pouvoir:
- reinterpreter;
- inverser;
- augmenter;
- affiner;
- optimiser;
- comparer les versions sans perte d'historique.

---

## 2) Regles de base

1. Une conversation n'est pas la verite canonique.
2. Une decision explicite doit etre extraite de la conversation.
3. Un fait, une interpretation et une doctrine doivent rester distincts.
4. Toute correction importante doit laisser une trace.
5. Aucune version ne doit ecraser silencieusement la precedente.

---

## 3) Unites a memoriser

Chaque element memorise doit pouvoir etre classe comme:
- `fact`
- `decision`
- `assumption`
- `pattern`
- `risk`
- `question`
- `revision`

Chaque element doit contenir au minimum:
- `id`
- `date`
- `scope`
- `type`
- `statement`
- `source`
- `status`

Statuts recommandes:
- `draft`
- `review`
- `validated`
- `deprecated`

---

## 4) Couches memoire

1. `session`
- resume d'une conversation datee;
- decisions extraites;
- questions ouvertes.

2. `project`
- etat du modele courant;
- objets metier;
- architecture cible;
- priorites.

3. `long-term`
- doctrines retenues;
- conventions stables;
- patterns confirmes.

4. `staging`
- apprentissages nouveaux;
- contradictions;
- elements a verifier avant promotion.

---

## 5) Workflow de mise a jour

1. Enregistrer la session.
2. Extraire les decisions.
3. Classer les elements en `fact`, `assumption`, `decision`, `risk`, `revision`.
4. Promouvoir vers `project` ou `long-term` si une formulation devient stable.
5. Conserver les points fragiles dans `staging`.
6. Enregistrer un `checkpoint` quand une sequence modifie la marque, le produit, le modele eco ou l'architecture.
7. Noter explicitement les points de retour arriere possibles si une hypothese forte echoue.

---

## 6) Application a notre travail

Le modele MERLIN en cours doit rester ouvert a:
- de nouvelles cosmologies;
- de nouvelles entites;
- de nouvelles grilles d'analyse;
- des revisions de doctrine;
- des optimisations de performance;
- des changements de schema de donnees.

Pour cela, MERLIN doit traiter chaque proposition comme un element versionnable plutot qu'une phrase definitive.

---

## 7) Decision active

A compter de maintenant, les conversations de travail utiles doivent etre resumees dans `memory/`, et les decisions structurantes doivent etre promues explicitement depuis ces resumes.

Un changement important n'est considere comme memoire exploitable que s'il laisse:
- une source;
- une decision ou une revision;
- un checkpoint;
- et un point de retour arriere identifiable.
