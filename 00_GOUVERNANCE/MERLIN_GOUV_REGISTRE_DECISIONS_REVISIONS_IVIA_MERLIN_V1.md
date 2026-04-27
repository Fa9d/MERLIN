# MERLIN - Registre decisions et revisions IVIA / MERLIN V1

Date: 2026-04-21
Statut: draft
Objet: centraliser les decisions structurantes, les revisions et les points de reference canoniques

---

## 1) Usage de ce registre

Ce registre sert a:
- retrouver vite ce qui est retenu;
- distinguer decision, hypothese et revision;
- savoir ou revenir si une direction doit etre corrigee;
- faire le pont entre conversation, gouvernance, marque, produit et prototype.

Chaque entree doit rester courte, verifiable et reliee a une source.

---

## 2) Decisions canoniques

| ID | Date | Type | Scope | Statement | Statut | Source principale |
|---|---|---|---|---|---|---|
| DEC-001 | 2026-04-20 | decision | marque | `IVIA` est la facade publique cote client. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-002 | 2026-04-20 | decision | marque | `MERLIN` est le moteur, la methode, la couche d'analyse et la valeur cote praticiens. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-003 | 2026-04-20 | decision | plateforme | Le portail praticien doit etre separe et non visible dans la navigation publique standard. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-004 | 2026-04-20 | decision | public | La promesse publique doit parler d'ecoute, clarification, orientation et continuite. | validated | `MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md` |
| DEC-005 | 2026-04-20 | decision | public | `IN VIVO IN ACTU` est une signature doctrinale et non un headline principal. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-006 | 2026-04-20 | decision | public | `La puissance du silence` peut servir de signature de campagne, pas de promesse unique. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-007 | 2026-04-20 | decision | offre | MERLIN ne doit pas etre presente comme therapie reservee ni comme diagnostic. | validated | `MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md` |
| DEC-008 | 2026-04-20 | decision | priorite | La diffusion client est prioritaire avant l'approfondissement du discours pro. | review | `MERLIN_GOUV_STRATEGIE_DIFFUSION_CLIENT_IVIA_V1.md` |
| DEC-009 | 2026-04-20 | decision | design | La direction visuelle retenue a ce stade est `editorial calme` pour IVIA et `documentaire net` pour MERLIN. | review | `MERLIN_GOUV_DIRECTION_VISUELLE_FINALE_IVIA_MERLIN_V1.md` |
| DEC-010 | 2026-04-20 | decision | logo | Le logo MERLIN doit rester celui fourni par l'utilisateur, sans reinterpretation graphique. | validated | `MERLIN_GOUV_NOTES_LOGO_MERLIN_RECUPERATION_V1.md` |
| DEC-011 | 2026-04-20 | decision | logo | La bougie IVIA de reference est la variante classique, sauf revision ulterieure explicite. | review | `MERLIN_GOUV_NOTES_LOGO_IVIA_VARIANTES_BOUGIE_V1.md` |
| DEC-012 | 2026-04-20 | decision | economie | Le modele economique doit distinguer cout direct par seance, frais fixes, marge brute et marge nette. | validated | `MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md` |
| DEC-013 | 2026-04-20 | decision | economie | Stripe peut etre mis a la charge du praticien dans le modele cible afin de proteger la marge MERLIN. | review | `MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md` |
| DEC-014 | 2026-04-20 | decision | offre praticiens | Les couches de service pro doivent etre lisibles par niveau: operationnel, reporting, lecture historique. | review | `MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md` |
| DEC-015 | 2026-04-21 | decision | memoire | Toute session importante doit produire un checkpoint memoire et un registre de decisions mis a jour. | validated | `MERLIN_MEMO_LOG_SESSION_2026-04-20_2026-04-21_v1.0.md` |
| DEC-016 | 2026-04-24 | decision | exploitation | L'acces admin standard au VPS MERLIN se fait via `ubuntu` + cle SSH, pas via mot de passe root. | validated | `MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md` |
| DEC-017 | 2026-04-25 | decision | exploitation | Un redeploiement manuel backend vers le VPS doit utiliser une archive legere sans `.venv`, caches ni bases locales, puis verifier le code charge dans le conteneur avant tout test fonctionnel. | validated | `MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md` |
| DEC-018 | 2026-04-25 | decision | economie | MESANGE doit integrer un pilotage economique par source, sujet, dossier et livrable, afin de relier couts, budgets, arbitrages et rentabilisation. | review | `MERLIN_GOUV_MODELE_ECO_MESANGE_PILOTAGE_COUTS_BUDGETS_RENTABILISATION_v1.0.md` |
| DEC-019 | 2026-04-25 | decision | donnees | MESANGE doit modeliser distinctement les sources, items ingeres, claims, evidences, dossiers, livrables et traces economiques afin de permettre un suivi complet des sujets jusqu'a leur resolution. | review | `MERLIN_GOUV_TABLEAU_DONNEES_MESANGE_SOURCES_DOSSIERS_CLAIMS_BUDGETS_V1.md` |
| DEC-020 | 2026-04-25 | decision | marche | Le point d'entree economique recommande pour MESANGE est `outil interne + services d'analyse + veille recurrente + observatoires`, avant un pari fort sur l'abonnement grand public ou le SaaS. | review | `MERLIN_GOUV_ETUDE_MARCHE_MESANGE_QUEBEC_REVENUS_MODELES_V1.md` |
| DEC-021 | 2026-04-25 | decision | offres | Les offres de depart MESANGE doivent rester simples et testables: `Signal clair`, `Dossier suivi`, `Veille active`, `Atelier methode`, puis `Observatoire Quebec`. | review | `MERLIN_GOUV_OFFRES_MESANGE_PACKAGES_VENDABLES_V1.md` |
| DEC-022 | 2026-04-25 | decision | economie | La trajectoire economique cible de MESANGE doit privilegier la recurrence tot (`Veille active`, `Observatoire Quebec`) en s'appuyant d'abord sur `Signal clair` et `Dossier suivi` comme portes d'entree commerciales. | review | `MERLIN_GOUV_SIMULATION_ECO_MESANGE_12_MOIS_V1.md` |
| DEC-023 | 2026-04-25 | decision | produit | Le noyau admin V1 de MESANGE doit etre construit autour de quatre flux: `ingestion -> tri`, `claim -> evidence -> verification`, `dossier -> publication -> resolution`, `budget -> cout -> revenu -> arbitrage`. | review | `MERLIN_GOUV_SPEC_ECRANS_ADMIN_MESANGE_V1.md` |
| DEC-024 | 2026-04-25 | decision | workflow | Le workflow canonique MESANGE doit suivre la chaine `source -> source_item -> tri -> claim -> evidence -> dossier -> report -> resolution`, afin d'empecher la confusion entre information entrante, verification et publication. | review | `MERLIN_GOUV_WORKFLOW_CANONIQUE_MESANGE_SOURCE_CLAIM_DOSSIER_RESOLUTION_V1.md` |
| DEC-025 | 2026-04-25 | decision | execution | L'ordre de build recommande pour MESANGE V1 est `noyau donnees et workflow -> ingestion et tri -> claims et evidences -> dossiers et chronologies -> livrables -> pilotage economique`, avant les couches plus sophistiquees de parametrage et de cartographie. | review | `MERLIN_GOUV_BACKLOG_PRODUIT_MESANGE_V1.md` |
| DEC-026 | 2026-04-26 | decision | execution | MERLIN doit etre traite comme entre en sprint de durcissement produit / droits / exploitation, avec objectif prioritaire de `pilote ferme` en `5 a 10 jours ouvrables`, avant toute ouverture plus large ou nouvelle extension produit. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| DEC-027 | 2026-04-26 | decision | droits | Le cloisonnement minimal des lectures operateur en production doit s'appuyer immediatement sur `SessionRecord.operator_user_id` comme ancre d'autorisation, en attendant un modele d'assignation plus large si necessaire. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| DEC-028 | 2026-04-26 | decision | diffusion | L'acces public au suivi client doit exiger conjointement `public_client_code` et `intake_request_id`; le `public_client_code` seul n'est pas une reference suffisante. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| DEC-029 | 2026-04-26 | decision | diffusion | Un document client issu d'une seance cloturee doit etre cree en `client_pending_review` tant que la note source n'est pas validee par `supervisor`, puis seulement passer en `client` et `client_visible = true`. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| DEC-030 | 2026-04-26 | decision | exploitation | Le stack prod canonique IVIA / MERLIN inclut desormais `frontend + api + nginx + db + livekit`, avec publication publique sur `ivia.quebec` et API sur `api.ivia.quebec`. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| DEC-031 | 2026-04-26 | decision | recette | La recette canonique de validation production doit desormais etre rejouee depuis zero sur le flux `public -> operator -> supervisor -> public`, et ne plus reposer sur des objets historiques deja existants. | validated | `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md` |
| DEC-032 | 2026-04-26 | decision | pilote | Au vu des validations production `J1` a `J8`, IVIA / MERLIN est autorise en `GO pilote ferme encadre`, mais reste en `NO-GO` pour une ouverture large tant que l'audio, la finition UX, l'exploitation manuelle et le nettoyage des traces de test ne sont pas davantage stabilises. | validated | `MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md` |
| DEC-033 | 2026-04-26 | decision | secrets | Les mots de passe, clefs privees et tokens utilises pour l'exploitation ou la recette prod ne doivent jamais etre stockes dans le repo; seuls les comptes, roles et procedures peuvent y etre documentes, les valeurs restant dans un coffre prive hors repo. | validated | `MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md` |
| DEC-034 | 2026-04-26 | decision | exploitation | Le redeploiement backend standard VPS doit suivre une procedure canonique unique `archive legere -> copie VPS -> backup code -> build api -> alembic upgrade head -> up -d api -> verification explicite du changement`, plutot que des gestes improvises repris depuis l'historique shell. | validated | `MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md` |
| DEC-035 | 2026-04-27 | decision | audio | La validation audio prod doit suivre une recette dediee unique fondee sur le flux canonique frontend `audio-sessions` / `audio-recordings`, avec jonction navigateur reelle et capture explicite des statuts BDD, plutot qu'un assemblage ad hoc de commandes shell et de routes legacy. | validated | `MERLIN_GOUV_CHECKLIST_VALIDATION_AUDIO_PROD_V1.md` |

---

## 3) Revisions canoniques

| ID | Date | Type | Scope | Revision | Statut | Source principale |
|---|---|---|---|---|---|---|
| REV-001 | 2026-04-20 | revision | marque | Abandon de la tentative de reconstitution du logo MERLIN. Retour au logo original utilisateur. | validated | `MERLIN_GOUV_NOTES_LOGO_MERLIN_RECUPERATION_V1.md` |
| REV-002 | 2026-04-20 | revision | priorite | Recentrage sur acquisition et diffusion client avant peaufinage du discours praticiens. | review | `MERLIN_GOUV_STRATEGIE_DIFFUSION_CLIENT_IVIA_V1.md` |
| REV-003 | 2026-04-20 | revision | discours | Abandon des formulations trop proches du medical, du diagnostic ou d'une promesse de guerison. | validated | `MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md` |
| REV-004 | 2026-04-20 | revision | prototype | Le site prototype est considere comme base structurelle seulement, non comme reference de finition. | validated | `MERLIN_MEMO_LOG_SESSION_2026-04-20_2026-04-21_v1.0.md` |
| REV-005 | 2026-04-24 | revision | production | Le backend prod a ete redeploye pour integrer `derived_documents` et la migration BDD associee, apres constat de derive entre code local et `/opt/merlin`. | validated | `MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md` |
| REV-006 | 2026-04-25 | revision | production | Le rendu du document derive client a ete corrige en prod: titre normalise `Synthese de seance {n}` et suppression des doubles ponctuations dans `body_text`. | validated | `MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md` |
| REV-007 | 2026-04-26 | revision | production | Le lot `J3` de restriction de lecture a ete deploye et verifie en production: `operator` ne voit que ses objets relies a ses seances, `supervisor` conserve une vue transverse, et les lectures directes non autorisees retournent `404`. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| REV-008 | 2026-04-26 | revision | production | Le lot `J4` a ete deploye et verifie en production: la lecture publique des documents derives cote client exige desormais `public_client_code + intake_request_id`, et une reference d'entree invalide retourne `404`. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| REV-009 | 2026-04-26 | revision | production | Le lot `J5` a ete deploye et verifie en production: un document destine au client reste non public tant que la note source n'est pas validee par `supervisor`; une tentative de validation par `operator` retourne `403`, puis la validation `supervisor` publie correctement le document. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| REV-010 | 2026-04-26 | revision | production | Le stack prod a ete etendu au frontend Next.js IVIA, servi via nginx sur `ivia.quebec`; le TLS multi-domaine `api.ivia.quebec + ivia.quebec` a ete corrige et le renouvellement Certbot simule avec succes. | validated | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` |
| REV-011 | 2026-04-26 | revision | production | Le lot `J8` de recette end-to-end a ete execute avec succes en production depuis zero: creation publique client et intake, creation et cloture de session par `operator`, blocage pre-validation, refus `403` cote `operator`, validation `200` cote `supervisor`, puis publication effective dans `/suivi`. | validated | `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md` |

---

## 4) Hypotheses encore ouvertes

| ID | Date | Type | Scope | Statement | Statut |
|---|---|---|---|---|---|
| HYP-001 | 2026-04-20 | assumption | economie | Un modele a frais de volume degressifs peut rester attractif et rentable. | review |
| HYP-002 | 2026-04-20 | assumption | acquisition | Une interface client plus editoriale et plus haut de gamme augmentera la conversion. | review |
| HYP-003 | 2026-04-20 | assumption | produit | La priorite client avant praticiens accelerera la clarte globale du produit. | review |
| HYP-004 | 2026-04-21 | assumption | memoire | Un systeme de checkpoints documentaires limitera la perte de contexte liee a la compression conversationnelle. | review |

---

## 5) Regle de maintenance

Quand une nouvelle decision est prise:
1. l'ajouter ici avec un ID stable;
2. lier la source canonique;
3. preciser si elle est `review` ou `validated`;
4. ne pas supprimer silencieusement l'entree precedente;
5. si une decision est annulee, la passer en `deprecated` ou ajouter une revision.

---

## 6) Decision active

Ce registre devient le point d'entree canonique pour:
- retrouver les arbitrages;
- verifier ce qui est vraiment retenu;
- eviter qu'une conversation utile se perde dans les fichiers disperses.
