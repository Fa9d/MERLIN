---
id: BACKLOG-MAITRE
version: V2.1
date: 2026-05-08
statut: actif
auteur: David Phaneuf
remplace: MERLIN_GOUV_BACKLOG_MAITRE_V1.md + MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md + MERLIN_GOUV_BACKLOG_PRODUIT_MESANGE_V1.md
decision: DEC-041
maj_v2_1: smoke test prod 8 mai 2026 — INFRA-001→004 confirmés done, CONT-002 done
maj_v2_2: 8 mai 2026 — ROLES-001 done (enum + doc V1), ROLES-002 done (matrice 59 routes), ROLES-003 active (audit 64 % couverture explicite, 1 faille BACK-PAY-001)
---

# MERLIN — Backlog Maître V2

> **Source unique de vérité pour toutes les tâches du projet.**
> Cette V2 fusionne le Backlog Maître V1, le Backlog Implémentation Rôles & Accès, et le Backlog Produit MÉSANGE.
> Le tableau de bord hebdo est une vue filtrée de ce document.

---

## Convention de lecture

```
ID | Titre | Domaine | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie
```

**Statuts :** `todo` · `active` · `blocked` · `done` · `archived`
**Priorités :** `P1` bloquant · `P2` cette semaine · `P3` ce sprint · `P4` long terme
**Domaines :** `infra` · `backend` · `frontend` · `contenu` · `diffusion` · `gouvernance` · `qualite-ia` · `roles-acces` · `mesange` · `fondements`

---

## DOMAINE : infra / exploitation

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| INFRA-001 | scp docker-compose.prod.yml + fichiers Python backend vers VPS | P1 | `done` | `action-vps` | — | code prod = code local (51 routes vérifiées 2026-05-08) |
| INFRA-002 | Appliquer migrations Alembic sur DB VPS | P1 | `done` | `action-vps` | INFRA-001 | schéma `PraticienPublic` prod = local (champs `title_line`, `intro_text`, `spoken_languages`, `available_channels`) |
| INFRA-003 | Rebuild conteneurs après déploiement | P1 | `done` | `action-vps` | INFRA-002 | `api.ivia.quebec/api/health` répond `200` env=production db=ok (2026-05-08) |
| INFRA-004 | Smoke test post-déploiement — vérifier routes critiques | P1 | `done` | `recette` | INFRA-003 | 6 endpoints testés 2026-05-08 : health 200, /praticiens 200, /auth/me 401, POST /intake-requests 422, POST /auth/login 422, POST /register/client 422 (validation Pydantic active) |
| INFRA-005 | Recette e2e complète — rejouer flux `public → operator → supervisor → public` | P2 | `todo` | `recette` | INFRA-003 | checklist recette prod complétée |
| INFRA-006 | Recette audio — rejouer checklist audio prod | P2 | `todo` | `recette` | INFRA-003 | checklist validation audio prod complétée |
| INFRA-007 | Vérifier HTTPS + cookies sécurisés + CORS en production post-rebuild | P2 | `todo` | `recette` | INFRA-003 | TLS valide, réponses sans erreur CORS |
| INFRA-008 | Vérification Certbot — renouvellement TLS ivia.quebec + api.ivia.quebec | P3 | `todo` | `action-vps` | — | `certbot renew --dry-run` sans erreur |

---

## DOMAINE : backend

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| BACK-001 | SlotStatus nettoyé — 5 valeurs parasites retirées | P1 | `done` | `commit` | — | commit `a622b82` |
| BACK-002 | `POST /{session_id}/room` → `410 Gone` | P1 | `done` | `commit` | — | commit `c8846c5` |
| BACK-003 | CORS `allow_methods` explicite | P1 | `done` | `commit` | — | commit `0a9520a` |
| BACK-004 | `require_verified_email_user` sur `hold_slot` + `confirm_slot` | P1 | `done` | `commit` | — | commit `b43dfe5` |
| BACK-005 | `RequestChannelCode` enum + modèle + schéma + migration 0017 | P1 | `done` | `commit` | — | commit `fbcd670` |
| BACK-006 | Audit endpoints audio-sessions (routes LiveKit) | P2 | `todo` | `fichier-repo` | INFRA-003 | rapport d'audit dans `05_PREUVES_SOURCES/` |
| BACK-007 | Audit `intake-requests` — validation Pydantic complète | P2 | `todo` | `fichier-repo` | — | — |
| BACK-008 | Audit gestion des rôles praticien vs client — dépendances backend | P2 | `todo` | `fichier-repo` | — | cohérence avec ROLES-001 à ROLES-010 |
| BACK-009 | Revue chaîne de révisions Alembic — cohérence `down_revision` | P3 | `todo` | — | — | `alembic history` sans trou ni conflit |
| BACK-010 | Modéliser rôle `practitioner` côté backend | P3 | `todo` | `commit` | BACK-008, ROLES-003 | rôle distinct de `operator`, endpoints adaptés |

---

## DOMAINE : frontend

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| FRONT-001 | `ClientPayload` TypeScript — `record_status` + `data_sensitivity_class` | P1 | `done` | `commit` | — | commit `62e3a46` |
| FRONT-002 | `middleware.ts` → `proxy.ts` — corriger warning Next.js 16.2.4 | P2 | `todo` | `commit` | — | build sans warning middleware |
| FRONT-003 | `reserver/page.tsx` → `confirmation/page.tsx` — état `confirmed` | P2 | `todo` | `commit` | — | parcours réservation complet sans régression |
| FRONT-004 | Vérification parcours réservation bout-en-bout (hold → confirm → confirmation) | P2 | `active` | `recette` | FRONT-003, INFRA-003 | infra Playwright en place (config + 2 specs publiques + API santé + 401/422). Reste : flux authentifié hold→confirm à couvrir |
| FRONT-005 | Vérification page `espace-praticien` sans erreur console | P2 | `todo` | `recette` | INFRA-003 | zéro erreur console sur surfaces principales |
| FRONT-006 | Vérifier affichage page d'accueil IVIA — performance + rendu | P3 | `todo` | `recette` | — | Lighthouse score acceptable |

---

## DOMAINE : contenu éditorial

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| CONT-001 | 16 articles IVIA écrits et pushés sur GitHub (sections 1.1 → 4.4) | P1 | `done` | `commit` | — | commit `4af888b`, 16 fichiers dans `04_METHODES/articles/` |
| CONT-002 | Créer route `/ressources` ou `/blog` dans Next.js | P3 | `done` | `commit` | FRONT-002 | `ivia.quebec/ressources` répond 200 (vérifié 2026-05-08) |
| CONT-003 | Système de rendu MDX pour les articles dans Next.js | P3 | `todo` | `commit` | CONT-002 | articles lisibles sur `ivia.quebec/ressources` |
| CONT-004 | Implémenter composant "portes d'entrée" (accordéon 3 accroches) | P4 | `todo` | `commit` | CONT-003 | composant fonctionnel sur au moins 1 article |
| CONT-005 | Maillage interne entre articles (liens contextuels rédigés) | P4 | `todo` | `fichier-repo` | CONT-003 | liens actifs sur les articles publiés |

---

## DOMAINE : diffusion

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| DIFF-001 | Exécuter phase 1 calendrier éditorial 30 jours (semaines 1-2) | P3 | `todo` | `fichier-repo` | CONT-002 | premières publications effectuées |
| DIFF-002 | Ouvrir un canal de diffusion client (newsletter ou réseau) | P3 | `todo` | — | INFRA-003 | premier envoi ou première publication |
| DIFF-003 | Revue mentions légales et politique de confidentialité | P2 | `todo` | `fichier-repo` | — | mentions présentes sur `ivia.quebec` |

---

## DOMAINE : gouvernance

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| GOUV-001 | Créer le système de gestion opérationnel MERLIN V1 — 5 fichiers | P2 | `active` | `fichier-repo` | — | 5 fichiers dans `00_GOUVERNANCE/` + commit |
| GOUV-002 | Mettre à jour le registre décisions — DEC-036+ | P3 | `todo` | `fichier-repo` | — | entrées ajoutées dans REGISTRE_DECISIONS |
| GOUV-003 | Archiver 24 fichiers périmés → `ARCHIVES/` | P2 | `todo` | `commit` | — | dossier ARCHIVES créé + fichiers déplacés (DEC-041) |
| GOUV-004 | Critères GO/NO-GO lancement public — formaliser dans le registre | P3 | `todo` | `décision` | INFRA-005 | entrée DEC-03X dans le registre |
| GOUV-005 | Fusionner backlogs (F2-F5) — 4 fusions restantes | P3 | `todo` | `fichier-repo` | — | 4 fichiers V2 créés, sources archivées |
| GOUV-006 | Mettre à jour INDEX_GOUVERNANCE_V2.md post-audit | P3 | `todo` | `fichier-repo` | GOUV-003 | INDEX reflète la structure réelle |

---

## DOMAINE : qualité IA (Vague 6)

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| QIA-001 | MERLIN_CONTRAT_PROMPT_V1.md — commité et opérationnel | P1 | `done` | `fichier-repo` | — | fichier dans `00_GOUVERNANCE/` |
| QIA-002 | MERLIN_GRILLE_QUALITE_NOTE_V1.md — créer et commiter | P1 | `done` | `fichier-repo` | QIA-001 | fichier `00_GOUVERNANCE/MERLIN_GRILLE_QUALITE_NOTE_V1.md` (DEC-039, commit 8eb2e04, Vérifié 8 mai 2026) |
| QIA-003 | MERLIN_GRILLE_GONOGO_PROMPT_V1.md — créer et commiter | P1 | `done` | `fichier-repo` | QIA-001 | fichier `00_GOUVERNANCE/MERLIN_GRILLE_GONOGO_PROMPT_V1.md` (DEC-040, commit 8eb2e04, vérifié 8 mai 2026) |
| QIA-004 | Ajouter champ `test_associe` dans frontmatter de tous les prompts METH+PROD | P2 | `todo` | `commit` | QIA-001 | tous les prompts existants mis à jour |
| QIA-005 | Stratégie replay tests IA — budget token + fixtures + marqueurs pytest | P2 | `todo` | `fichier-repo` | — | pytest.ini + conftest.py updatés |
| QIA-006 | Découpage smoke tests — sous-scénarii par type de sortie | P3 | `todo` | `fichier-repo` | QIA-005 | tests/ structurés en sous-dossiers |
| QIA-007 | Encoder frontière hypothèse/fait dans schéma JSON (champs faits/hypotheses/recommandations) | P2 | `active` | `commit` | QIA-001 | ADR-0005 validé (DEC-044) spécifie le patch v1.0 → v1.1 (schéma + Pydantic + migration 0019 + 2 tests). Implémentation à exécuter |

---

## DOMAINE : rôles & accès (fusionné depuis BACKLOG_IMPLEMENTATION_ROLES)

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| ROLES-001 | Modèle de rôles défini : public / client / praticien / opérateur / superviseur / admin | P2 | `done` | `décision` | — | enum `AppRole` (5 valeurs) + doc V1 (368 lignes) `MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md` (22 avril 2026) |
| ROLES-002 | Matrice d'accès par rôle et par route (back + front) | P2 | `done` | `fichier-repo` | ROLES-001 | `MERLIN_GOUV_MATRICE_ROLES_ROUTES_V1.md` (8 mai 2026, 59 routes documentées) |
| ROLES-003 | Implémentation backend : guard par rôle sur routes protégées | P2 | `active` | `commit` | ROLES-002 | 38/59 routes guard explicite (64 %) + 13/59 publiques légitimes (22 %) ; 1 faille (BACK-PAY-001) + 4 incohérences à traiter — voir `AUDIT_ROLES_ROUTES_2026-05-08.md` |
| ROLES-004 | Implémentation frontend : visibilité conditionnelle par rôle | P3 | `todo` | `commit` | ROLES-003 | composants React n'affichent que ce que le rôle autorise |
| ROLES-005 | Interface espace praticien — accès dossiers clients assignés | P3 | `todo` | `commit` | ROLES-003 | praticien voit uniquement ses clients |
| ROLES-006 | Interface opérateur — tableau de bord demandes + assignation | P3 | `todo` | `commit` | ROLES-003 | opérateur peut assigner, pas modifier le contenu clinique |
| ROLES-007 | Interface superviseur — vue agrégée + validation notes | P3 | `todo` | `commit` | ROLES-006 | superviseur peut approuver/rejeter une note |
| ROLES-008 | Interface admin — gestion utilisateurs + config | P4 | `todo` | `commit` | ROLES-007 | admin peut créer/suspendre un compte praticien |
| ROLES-009 | Tests e2e par rôle — scénario complet pour chaque profil | P3 | `todo` | `recette` | ROLES-008 | pytest ou Playwright couvre les 5 rôles |
| ROLES-010 | Audit sécurité rôles — vérifier qu'aucune élévation de privilège n'est possible | P2 | `todo` | `fichier-repo` | ROLES-003 | rapport dans `05_PREUVES_SOURCES/` |

---

## DOMAINE : MÉSANGE (produit B2B praticiens)

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| MES-001 | Définir MVP MÉSANGE v0.1 — périmètre minimum vendable | P3 | `todo` | `décision` | — | entrée DEC-03X dans REGISTRE + document spec |
| MES-002 | Schéma de données MÉSANGE — entités praticien, cabinet, abonnement | P3 | `todo` | `fichier-repo` | MES-001 | schéma dans `00_GOUVERNANCE/` |
| MES-003 | Onboarding praticien — parcours self-service sans opérateur | P3 | `todo` | `commit` | MES-002, ROLES-003 | praticien peut s'inscrire et activer son espace autonomement |
| MES-004 | Tableau de bord praticien — agenda, clients, notes du jour | P3 | `todo` | `commit` | MES-003 | affichage fonctionnel, données réelles en dev |
| MES-005 | Module notes cliniques — saisie post-séance avec IA | P3 | `todo` | `commit` | MES-004, QIA-001 | note générée, validée par praticien, sauvegardée |
| MES-006 | Facturation MÉSANGE — Stripe ou équivalent QC | P4 | `todo` | `commit` | MES-003 | abonnement mensuel activable depuis l'onboarding |
| MES-007 | Pilote praticien — recruter 1 praticien test et recueillir feedback | P3 | `todo` | `recette` | MES-005 | compte actif, 1 séance testée, retour écrit |
| MES-008 | Grille qualité note clinique — évaluation systématique des sorties IA | P1 | `todo` | `fichier-repo` | QIA-002 | grille dans `00_GOUVERNANCE/`, intégrée au pilote |

---

## DOMAINE : fondements / méthodes

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| FOND-001 | Corpus 11 Nations QC — compléter les fiches manquantes | P4 | `todo` | `fichier-repo` | — | fiches dans `02_NATIONS_QC/` |
| METH-001 | Cadre méthode 11 Nations QC intl v1.0 — revoir et valider | P4 | `todo` | `fichier-repo` | — | document stable dans `04_METHODES/` |

---

## Suivi global (V2)

| Domaine | Total | Done | Active | Todo | Blocked |
|---|---|---|---|---|---|
| infra | 8 | 4 | 0 | 4 | 0 |
| backend | 10 | 5 | 0 | 5 | 0 |
| frontend | 6 | 1 | 1 | 4 | 0 |
| contenu | 5 | 2 | 0 | 3 | 0 |
| diffusion | 3 | 0 | 0 | 3 | 0 |
| gouvernance | 6 | 0 | 1 | 5 | 0 |
| qualité-ia | 7 | 3 | 1 | 3 | 0 |
| rôles-accès | 10 | 2 | 1 | 7 | 0 |
| mésange | 8 | 0 | 0 | 8 | 0 |
| fondements | 2 | 0 | 0 | 2 | 0 |
| **TOTAL** | **65** | **17** | **4** | **44** | **0** |

---

## Sources archivées (remplacées par ce document)

- `MERLIN_GOUV_BACKLOG_MAITRE_V1.md` → archiver dans `ARCHIVES/`
- `MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md` → archiver dans `ARCHIVES/`
- `MERLIN_GOUV_BACKLOG_PRODUIT_MESANGE_V1.md` → archiver dans `ARCHIVES/`
