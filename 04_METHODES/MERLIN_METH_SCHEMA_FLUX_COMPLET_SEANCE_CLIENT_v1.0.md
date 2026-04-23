# MERLIN - Schema flux complet seance client (v1)

Date: 2026-04-19
Statut: draft
Objet: vue d'ensemble du flux complet d'une seance MERLIN, depuis l'entree jusqu'aux objets derives, a l'historique, au journal client et a la transmission eventuelle

---

## 1) Finalite

Ce schema sert a voir MERLIN comme un systeme complet et non comme une juxtaposition de documents.

Il relie:
- l'accueil;
- le cadrage;
- les consentements;
- la seance;
- le triage;
- la note;
- l'historique;
- la transcription si elle existe;
- les objets derives;
- la transmission;
- l'apprentissage interne.

---

## 2) Vue d'ensemble simplifiee

```text
1. Demande entrante
   ->
2. Qualification initiale
   ->
3. Cadrage du role MERLIN
   ->
4. Consentements applicables
   ->
5. Seance
   ->
6. Triage / orientation / bascule urgence
   ->
7. Production de trace
      - note structuree
      - historique client
      - transcription source si regime applicable
   ->
8. Objets derives
      - synthese praticien
      - recommandations prochaine seance
      - journal de parcours client
      - note de relais professionnel
   ->
9. Boucle de suivi
   ->
10. Apprentissage interne
      - methode
      - veille
      - patterns terrain
      - impact des changements
```

---

## 3) Etape 1 - Demande entrante

Formes possibles:
- appel direct
- proche inquiet
- demande de soutien
- demande d'alternatif
- demande de suivi

Questions implicites:
- qui appelle?
- pour qui?
- pour quoi?
- y a-t-il deja un signe d'urgence?

Sortie attendue:
- type d'appel pre-identifie

Reference:
- [MERLIN_METH_PROTOCOLE_ENTREE_CLIENT_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PROTOCOLE_ENTREE_CLIENT_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)

---

## 4) Etape 2 - Qualification initiale

Objectif:
- voir si la demande entre dans le champ MERLIN;
- reperer tres vite si le seuil urgent est deja la.

Si hors champ total:
- orienter sans ouvrir une pseudo-seance.

Si champ compatible:
- passer au cadrage.

Reference:
- [MERLIN_METH_PROTOCOLE_ENTREE_CLIENT_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PROTOCOLE_ENTREE_CLIENT_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)

---

## 5) Etape 3 - Cadrage du role MERLIN

MERLIN doit poser:
- ce qu'il fait;
- ce qu'il ne fait pas;
- le but de la rencontre;
- la possibilite d'une bascule urgence.

Sortie attendue:
- cadre explicite et accepte

Reference:
- [MERLIN_GOUV_POLICY_CHAMPS_INTERVENTION_PREMIERE_LIGNE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_CHAMPS_INTERVENTION_PREMIERE_LIGNE_v1.0.md)

---

## 6) Etape 4 - Consentements applicables

MERLIN determine quels consentements sont requis:

### Toujours

- consentement a la seance
- consentement a la note structuree

### Selon le regime choisi

- consentement a l'historique
- consentement a l'enregistrement
- consentement a la transcription
- consentement a la transmission a un tiers

### Cas sensible

- mineur / parent

Sortie attendue:
- trace claire de ce qui est consenti et de ce qui ne l'est pas

References:
- [MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md)
- [MERLIN_METH_PACK_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PACK_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md)

---

## 7) Etape 5 - Seance

Types de seance actuels:
- standard 30 min
- proche inquiet
- demande d'alternatif
- bascule urgence

Objectif:
- clarifier;
- sonder le risque;
- identifier le besoin dominant;
- nommer la bonne prochaine action.

References:
- [MERLIN_METH_SCRIPT_SEANCE_STANDARD_30_MIN_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_SEANCE_STANDARD_30_MIN_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_PROCHE_INQUIET_30_MIN_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_PROCHE_INQUIET_30_MIN_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_DEMANDE_ALTERNATIF_30_MIN_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_DEMANDE_ALTERNATIF_30_MIN_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_BASCULE_URGENCE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_BASCULE_URGENCE_SANTE_MENTALE_v1.0.md)

---

## 8) Etape 6 - Triage / orientation / bascule urgence

Trois grands cas de sortie:

### A. Non urgent

- psychologue
- travailleur social
- CLSC
- psychiatre selon gravite
- ressource communautaire
- dependance

### B. Crise non vitale

- centre de crise
- ligne de crise
- 811

### C. Urgence

- 911
- urgence
- urgence psychiatrique

Reference:
- [SOIN__referentiel__regles-triage-sante-mentale-qc__2026-04-19.yaml](C:/MERLIN/05_PREUVES_SOURCES/CORPUS/ORIENTATION_PARCOURS_ACCES/PORTES_ENTREE/SOIN__referentiel__regles-triage-sante-mentale-qc__2026-04-19.yaml)

---

## 9) Etape 7 - Production de trace

### Regime par defaut

Produire:
- note structuree
- historique client court

### Regime approfondi

Peut produire en plus:
- transcription complete source

### Audio brut

Si enregistrement existe:
- usage transitoire
- suppression rapide recommandee apres transcription verifiee

References:
- [MERLIN_METH_FORMULAIRE_NOTE_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_FORMULAIRE_NOTE_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)
- [MERLIN_GOUV_POLICY_TRANSCRIPTION_GOUVERNEE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_TRANSCRIPTION_GOUVERNEE_v1.0.md)
- [MERLIN_PREU_SCHEMA_HISTORIQUE_CLIENT_PREMIERE_LIGNE_v1.0.md](C:/MERLIN/05_PREUVES_SOURCES/SCHEMAS/MERLIN_PREU_SCHEMA_HISTORIQUE_CLIENT_PREMIERE_LIGNE_v1.0.md)

---

## 10) Etape 8 - Objets derives

A partir de la seance et, si applicable, de la transcription source, MERLIN peut produire:

- note de seance
- historique client
- synthese praticien
- recommandations prochaine seance
- journal de parcours client
- note de relais professionnel

Doctrine:

`la transcription source n'est pas l'objet d'usage courant; les objets derives le sont`

References:
- [MERLIN_METH_TEMPLATE_JOURNAL_PARCOURS_CLIENT_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_TEMPLATE_JOURNAL_PARCOURS_CLIENT_v1.0.md)
- [MERLIN_METH_TEMPLATE_NOTE_RELAIS_PROFESSIONNEL_SANTE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_TEMPLATE_NOTE_RELAIS_PROFESSIONNEL_SANTE_v1.0.md)

---

## 11) Etape 9 - Boucle de suivi

Avant la prochaine seance, MERLIN devrait pouvoir relire rapidement:

- motif principal precedent
- niveau de risque precedent
- besoin dominant precedent
- orientation deja donnee
- ce qui a ete tente
- ce qui reste bloque
- signaux de vigilance

But:
- ne pas recommencer a zero;
- ne pas tout relire;
- preparer la continuite.

---

## 12) Etape 10 - Transmission a un professionnel ou un tiers

Si orientation vers un professionnel:
- transmission seulement avec consentement explicite adapte;
- transmission d'une synthese de continuite;
- pas d'interpretation clinique sauvage;
- pas de verbatim integral par defaut.

Cas mineurs:
- prudence accrue;
- distinguer parole du jeune, parole parentale et point de vigilance securitaire.

References:
- [MERLIN_GOUV_POLICY_MINEURS_PARENTS_SANTE_MENTALE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_MINEURS_PARENTS_SANTE_MENTALE_v1.0.md)

---

## 13) Etape 11 - Apprentissage interne

Les seances ne servent pas seulement au suivi client.

Elles alimentent aussi, de maniere separee:
- registre methode
- registre veille
- registre patterns terrain
- registre impact changements

Important:

`les donnees client ne deviennent pas directement doctrine`

Il faut passer par:
- revue
- tri
- qualification
- promotion explicite

References:
- [MERLIN_METH_SYSTEME_APPRENTISSAGE_INTERNE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SYSTEME_APPRENTISSAGE_INTERNE_v1.0.md)
- [MERLIN_METH_PROTOCOLE_REVUE_MENSUELLE_APPRENTISSAGE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PROTOCOLE_REVUE_MENSUELLE_APPRENTISSAGE_v1.0.md)

---

## 14) Les 5 noeuds critiques du systeme

### Noud 1 - Cadrage initial

Si le cadre n'est pas pose, le reste se brouille.

### Noud 2 - Triage

Si le risque est mal lu, tout le systeme devient dangereux.

### Noud 3 - Consentement

Si les consentements sont flous, la gouvernance des donnees s'effondre.

### Noud 4 - Objets derives

Si MERLIN travaille directement sur le brut, la surcharge documentaire augmente.

### Noud 5 - Boucle d'apprentissage

Si les apprentissages ne sont pas tries, la methode s'empile au lieu de s'affiner.

---

## 15) Vue resume operatoire

```text
Entrer -> cadrer -> consentir -> tenir la seance -> trier -> orienter -> noter -> historiser -> deriver -> transmettre si besoin -> apprendre
```

---

## 16) Decision active

MERLIN adopte ce flux comme schema directeur provisoire de son systeme de seance client.

Il devra servir de reference pour:
- la conception produit;
- la formation operateur;
- la gouvernance des donnees;
- la structuration des outils;
- la revue mensuelle.

---

## 17) Socle operatoire V1 a figer

Le risque actuel n'est pas le manque de documents.
Le risque actuel est la dispersion.

Pour rendre MERLIN operable, il faut geler un socle V1 simple.

### Parcours V1 recommande

- public adulte
- detresse non urgente ou crise non vitale a reperer
- seance standard `30 min`
- canal prioritaire `telephone`
- note structuree obligatoire
- historique client court si consenti
- journal de parcours en sortie seulement si utile
- note de relais seulement si orientation effective et consentie
- pas de transcription complete par defaut

### Objets obligatoires V1

Sans ces objets, MERLIN n'est pas encore operable:

1. politique de champ d'intervention
2. cadrage oral de debut de seance
3. consentement seance + note
4. script de triage et de clarification
5. note structuree
6. orientation documentee
7. historique client court

### Objets optionnels V1

Ces objets augmentent la valeur mais ne doivent pas bloquer le lancement:

- enregistrement
- transcription complete
- journal de parcours client
- note de relais professionnel
- regime mineur / parent
- analyses terrain approfondies

Regle:

`MERLIN doit d'abord bien faire le socle avant d'industrialiser les couches riches`

---

## 18) Ordre reel de consolidation

L'ordre recommande n'est pas documentaire.
Il est systemique.

### Phase 1 - Geler l'offre reelle

Definir une seule promesse V1:
- accueil et ecoute active
- clarification
- triage prudent
- orientation
- continuite minimale

Exclure du lancement:
- promesses de transformation profonde
- analyse intergenerationnelle systematique
- transcription premium par defaut
- regimes multiples mal maitrises

### Phase 2 - Assembler le noyau operateur

Faire fonctionner ensemble, sans ambiguite:
- [MERLIN_GOUV_POLICY_CHAMPS_INTERVENTION_PREMIERE_LIGNE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_CHAMPS_INTERVENTION_PREMIERE_LIGNE_v1.0.md)
- [MERLIN_METH_PLAYBOOK_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PLAYBOOK_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_SEANCE_STANDARD_30_MIN_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_SEANCE_STANDARD_30_MIN_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_FORMULAIRE_NOTE_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_FORMULAIRE_NOTE_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)
- [SOIN__referentiel__regles-triage-sante-mentale-qc__2026-04-19.yaml](C:/MERLIN/05_PREUVES_SOURCES/CORPUS/ORIENTATION_PARCOURS_ACCES/PORTES_ENTREE/SOIN__referentiel__regles-triage-sante-mentale-qc__2026-04-19.yaml)

Objectif:
- un operateur doit savoir quoi dire, quoi demander, quoi noter et vers quoi orienter sans reconstruire la methode a chaque seance.

### Phase 3 - Poser la memoire utile

Ne pas partir de la transcription.
Partir de la continuite.

Il faut d'abord fiabiliser:
- historique client court
- recommandations prochaine seance
- relance et relecture rapide avant rendez-vous

La transcription gouvernee ne vient qu'ensuite comme couche source enrichie.

### Phase 4 - Transformer l'existant en produit

Une fois le socle stable, traduire le flux en objets produit:
- inscription / qualification initiale
- ecran ou formulaire de consentement
- fiche operateur en direct
- ecran de cloture avec prochaine etape
- generation de documents derives

### Phase 5 - Ouvrir les couches avancees

Seulement apres stabilisation du V1:
- mineurs / parents
- transcription premium
- note de relais automatisee
- veille et apprentissage terrain plus outilles
- eventuelles offres complementaires preparees et gouvernees

---

## 19) Decision de pilotage

A partir de maintenant, MERLIN ne doit plus etre developpe comme une somme de documents independants.

MERLIN doit etre pilote comme un systeme a quatre couches:

1. doctrine
2. operation de seance
3. memoire de continuite
4. couches optionnelles d'enrichissement

Cela implique une discipline:
- tout nouveau document doit soit renforcer une couche existante,
- soit remplacer une ambiguite,
- soit rester en backlog tant que le socle V1 n'est pas ferme.
