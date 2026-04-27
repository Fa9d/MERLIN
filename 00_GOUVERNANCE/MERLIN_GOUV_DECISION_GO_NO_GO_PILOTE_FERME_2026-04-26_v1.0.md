# MERLIN - Decision go / no-go pilote ferme 2026-04-26 v1.0

Date: 2026-04-26
Statut: valide
Objet: statuer sur l'ouverture d'un pilote ferme IVIA / MERLIN apres verification production des lots `J1` a `J8`

---

## 1) Decision

Decision retenue:

`GO pilote ferme encadre`

Interpretation:

- MERLIN / IVIA est juge suffisamment stable pour un pilote ferme limite, encadre et reversible;
- cette decision ne vaut pas `ouverture large`;
- elle n'efface pas les risques residuels identifies ci-dessous.

---

## 2) Base factuelle

Les points suivants ont ete verifies en production:

- backend redeployable et healthcheck API stable;
- frontend IVIA deployee sur `https://ivia.quebec`;
- TLS multi-domaine corrige pour `ivia.quebec` et `api.ivia.quebec`;
- renouvellement Certbot simule avec succes;
- separation minimale des roles `operator` / `supervisor`;
- filtrage de lecture operateur borne a ses propres objets;
- route publique `/suivi` borne par `public_client_code + intake_request_id`;
- workflow documentaire client gouverne:
  - document initial en `client_pending_review`
  - non visible publiquement avant validation
  - publication apres validation `supervisor`
- recette e2e `public -> operator -> supervisor -> public` executee avec succes depuis zero.

---

## 3) Portee du go

Le `GO` couvre:

- un petit nombre de comptes internes ou utilisateurs tests encadres;
- un usage centre sur les parcours:
  - `rendez-vous`
  - `suivi`
  - `operator`
  - `supervision`
- une activite pilote avec controle humain explicite;
- un usage non medical, adulte, non urgent, conforme au cadrage IVIA / MERLIN actuel.

Le `GO` ne couvre pas:

- une ouverture publique plus large sans encadrement;
- une promesse de robustesse clinique et operationnelle complete;
- un perimetre audio de production considere comme stabilise;
- une couche praticien mature ou multi-organisation.

---

## 4) Conditions d'ouverture

Le pilote ferme doit rester conditionne a:

- un runbook securise pour les comptes de test et comptes internes;
- un nettoyage documente des traces de test prod;
- une discipline stricte sur les redeploiements manuels;
- un usage des comptes `supervisor` reserve a la relecture et a la validation;
- une surveillance rapprochee des premiers usages pilotes.

---

## 5) Risques residuels

### Risque 1 - Audio non considere comme ferme

Constat:

- un flux audio / enregistrement de test a deja remonte en `failed`;
- ce point n'empeche pas le pilote ferme sur le coeur documentaire, mais il empeche de presenter la chaine audio comme completement stabilisee.
- une checklist dediee existe desormais pour rejouer ce perimetre sur le flux audio canonique sans improviser les commandes.

Consequence:

- ne pas faire reposer le pilote sur la promesse audio avancee;
- traiter l'audio comme perimetre prudent ou secondaire tant qu'une recette dediee n'est pas bouclee.
- utiliser la checklist audio prod canonique avant toute affirmation de stabilisation.

### Risque 2 - Finition UX encore partielle

Constat:

- des correctifs UX restent souhaitables;
- le lint global frontend n'est pas encore propre sur certains fichiers existants hors lot critique.

Consequence:

- le produit est pilotable;
- il n'est pas encore au niveau de finition d'une ouverture large.

### Risque 3 - Dette d'exploitation encore presente

Constat:

- le runtime prod est redeployable, mais l'exploitation reste encore manuelle;
- la procedure est praticable, pas encore industrialisee.

Consequence:

- chaque redeploiement doit rester sobre, explicite et verifie;
- une erreur humaine reste possible si la discipline de runbook se relache.

### Risque 4 - Donnees de test encore presentes

Constat:

- plusieurs objets de test prod restent traces et non nettoyes.

Consequence:

- le pilote doit demarrer avec hygiene documentaire et nettoyage progressif des traces de test.

---

## 6) Decision pratique immediate

Autoriser:

- un pilote ferme restreint;
- des demonstrations encadrees;
- des tests utilisateurs limites;
- une observation rapprochee des parcours `public`, `operator` et `supervision`.

Ne pas autoriser encore:

- une ouverture large;
- une communication publique forte sur une maturite produit complete;
- une dependance forte a la couche audio / enregistrement;
- une multiplication des nouveaux chantiers produit avant consolidation.

---

## 7) Prochaine etape recommandee

Mini-sprint suivant recommande:

- corriger les irritants UX les plus visibles;
- nettoyer les traces de test prod prioritaires;
- durcir le runbook comptes / secrets / nettoyage;
- verifier specifiquement la chaine audio via la checklist dediee si elle doit entrer dans le pilote.

---

## 8) Verdict executif

Verdict:

`GO pour un pilote ferme encadre, NO-GO pour une ouverture large`

Formule courte:

`MERLIN / IVIA est pret pour un pilote ferme reel sous supervision humaine, mais pas encore pour une diffusion large sans filet.`

---

## 9) References

- [MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md)
- [MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md)
- [MERLIN_GOUV_CHECKLIST_VALIDATION_AUDIO_PROD_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_VALIDATION_AUDIO_PROD_V1.md)
- [MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md)
- [MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md)
