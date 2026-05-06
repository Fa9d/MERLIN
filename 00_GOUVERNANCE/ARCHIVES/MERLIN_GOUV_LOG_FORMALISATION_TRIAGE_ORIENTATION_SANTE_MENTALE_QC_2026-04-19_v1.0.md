# MERLIN - Log formalisation triage et orientation sante mentale Quebec

Date: 2026-04-19
Statut: draft
Objet: tracer le passage du corpus documentaire vers une couche operationnelle minimale pour MERLIN

## Livrables crees

- `MERLIN_PREU_SCHEMA_SERVICE_ORIENTATION_v1.0.md`
- `MERLIN_PREU_SCHEMA_REGLE_TRIAGE_v1.0.md`
- `SOIN__referentiel__services-orientation-sante-mentale-qc__2026-04-19.yaml`
- `SOIN__referentiel__regles-triage-sante-mentale-qc__2026-04-19.yaml`
- `SOIN__tests__cas-triage-sante-mentale-qc__2026-04-19.yaml`

## Decision structurelle

MERLIN distingue maintenant explicitement:
- `service_orientation`
- `regle_triage`
- `suite_tests_triage`

Cette separation evite de noyer la securite dans les fiches service.

## Principe actif

Les `regles_triage` priment sur la selection fine d'un service.

Autrement dit:
- le danger immediat ecrase l'orientation de confort;
- la crise non vitale ecrase le suivi non urgent;
- le determinant social dominant reoriente vers le social meme en presence de detresse psychique;
- le besoin psychotherapeutique non urgent reste traite comme un parcours distinct.

## Limites maintenues

- ces referentiels restent `draft`;
- ils ne remplacent pas un jugement clinique;
- les modalites locales d'acces restent a valider;
- certaines actions critiques devront etre precisees au niveau produit si MERLIN devient conversationnel temps reel.
- le referentiel ne contient pas encore une fiche canonique distincte pour `urgence hospitaliere generale`; certains cas medicaux urgents utilisent donc provisoirement un proxy hospitalier.

## Etape suivante recommandee

1. ajouter un parseur ou validateur minimal YAML / JSON;
2. transformer les signaux libres en taxonomie de symptomes et contextes;
3. brancher les cas de test a un moteur de decision simple;
4. renforcer les regles critiques par ingestion ciblee de sources primaires.
