# MERLIN — Backlog maître V1

Date: 2026-05-04
Statut: actif
Objet: inventaire central de toutes les tâches connues, triées par domaine

> Référence : `MERLIN_GOUV_SYSTEME_GESTION_OPERATIONNEL_V1.md` pour les conventions (statuts, priorités, types).
> Ce backlog est la source de vérité pour les tâches. Le tableau de bord hebdo en est la vue filtrée.

---

## Convention de lecture

```
ID | Titre | Domaine | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie
```

Statuts : `todo` · `active` · `blocked` · `done` · `archived`
Priorités : `P1` bloquant · `P2` cette semaine · `P3` ce sprint · `P4` long terme

---

## Domaine : infra / exploitation

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| INFRA-001 | scp docker-compose.prod.yml + 7 fichiers Python backend vers VPS | P1 | `todo` | `action-vps` | — | fichiers présents dans `/opt/merlin/` |
| INFRA-002 | `make migrate` — appliquer migration 0017 sur DB VPS | P1 | `todo` | `action-vps` | INFRA-001 | `alembic_version = 20260504_0017` dans la DB prod |
| INFRA-003 | `make up` — rebuild conteneurs après déploiement | P1 | `todo` | `action-vps` | INFRA-002 | `api.ivia.quebec/api/health` répond `200` |
| INFRA-004 | Smoke test post-déploiement — vérifier routes critiques | P1 | `todo` | `recette` | INFRA-003 | health OK + `POST /intake-requests` OK + login OK |
| INFRA-005 | Recette e2e complète — rejouer flux `public → operator → supervisor → public` | P2 | `todo` | `recette` | INFRA-003 | `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md` complétée |
| INFRA-006 | Recette audio — rejouer checklist audio prod | P2 | `todo` | `recette` | INFRA-003 | `MERLIN_GOUV_CHECKLIST_VALIDATION_AUDIO_PROD_V1.md` complétée |
| INFRA-007 | Vérifier HTTPS + cookies sécurisés + CORS en production post-rebuild | P2 | `todo` | `recette` | INFRA-003 | TLS valide, réponses sans erreur CORS |
| INFRA-008 | Vérification Certbot — renouvellement TLS ivia.quebec + api.ivia.quebec | P3 | `todo` | `action-vps` | — | `certbot renew --dry-run` sans erreur |

---

## Domaine : backend

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| BACK-001 | SlotStatus nettoyé — 5 valeurs parasites retirées | P1 | `done` | `commit` | — | commit `a622b82` |
| BACK-002 | `POST /{session_id}/room` → `410 Gone` | P1 | `done` | `commit` | — | commit `c8846c5` |
| BACK-003 | CORS `allow_methods` explicite | P1 | `done` | `commit` | — | commit `0a9520a` |
| BACK-004 | `require_verified_email_user` sur `hold_slot` + `confirm_slot` | P1 | `done` | `commit` | — | commit `b43dfe5` |
| BACK-005 | `RequestChannelCode` enum + modèle + schéma + migration 0017 | P1 | `done` | `commit` | — | commit `fbcd670` |
| BACK-006 | Audit endpoints audio-sessions (routes LiveKit) | P2 | `todo` | `fichier-repo` | INFRA-003 | rapport d'audit dans `05_PREUVES_SOURCES/` |
| BACK-007 | Audit `intake-requests` — validation Pydantic complète et exhaustive | P2 | `todo` | `fichier-repo` | — | — |
| BACK-008 | Audit gestion des rôles praticien vs client — dépendances backend | P2 | `todo` | `fichier-repo` | — | cohérence avec `MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md` |
| BACK-009 | Revue chaîne de révisions Alembic — cohérence `down_revision` | P3 | `todo` | — | — | `alembic history` sans trou ni conflit |
| BACK-010 | Modéliser rôle `practitioner` côté backend | P3 | `todo` | `commit` | BACK-008 | rôle distinct de `operator`, endpoints adaptés |

---

## Domaine : frontend

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| FRONT-001 | `ClientPayload` TypeScript — `record_status` + `data_sensitivity_class` | P1 | `done` | `commit` | — | commit `62e3a46` |
| FRONT-002 | `middleware.ts` → `proxy.ts` — corriger warning Next.js 16.2.4 | P2 | `todo` | `commit` | — | build sans warning middleware |
| FRONT-003 | `reserver/page.tsx` → `confirmation/page.tsx` — état `confirmed` | P2 | `todo` | `commit` | — | parcours réservation complet sans régression |
| FRONT-004 | Vérification parcours réservation bout-en-bout (hold → confirm → confirmation) | P2 | `todo` | `recette` | FRONT-003, INFRA-003 | flux sans blocage 3x de suite |
| FRONT-005 | Vérification page `espace-praticien` sans erreur console | P2 | `todo` | `recette` | INFRA-003 | zéro erreur console sur les surfaces principales |
| FRONT-006 | Vérifier affichage page d'accueil IVIA — performance + rendu | P3 | `todo` | `recette` | — | Lighthouse score acceptable |

---

## Domaine : contenu éditorial

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| CONT-001 | 16 articles IVIA écrits et pushés sur GitHub (sections 1.1 → 4.4) | P1 | `done` | `commit` | — | commit `4af888b`, 16 fichiers dans `04_METHODES/articles/` |
| CONT-002 | Créer route `/ressources` ou `/blog` dans Next.js | P3 | `todo` | `commit` | FRONT-002 | route accessible publiquement |
| CONT-003 | Système de rendu MDX ou markdown pour les articles dans Next.js | P3 | `todo` | `commit` | CONT-002 | articles lisibles sur `ivia.quebec/ressources` |
| CONT-004 | Implémenter composant "portes d'entrée" (accordéon 3 accroches) | P4 | `todo` | `commit` | CONT-003 | composant fonctionnel sur au moins 1 article |
| CONT-005 | Maillage interne entre articles (liens contextuels rédigés) | P4 | `todo` | `fichier-repo` | CONT-003 | liens actifs sur les articles publiés |

---

## Domaine : diffusion

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| DIFF-001 | Calendrier éditorial 30 jours — exécuter phase 1 (semaines 1-2) | P3 | `todo` | `fichier-repo` | CONT-002 | référence `MERLIN_GOUV_CALENDRIER_EDITORIAL_DIFFUSION_CLIENT_30_JOURS_IVIA_V1.md` |
| DIFF-002 | Ouvrir un canal de diffusion client (newsletter, réseau) | P3 | `todo` | — | INFRA-003 | premier envoi ou première publication |
| DIFF-003 | Revue mentions légales et politique de confidentialité | P2 | `todo` | `fichier-repo` | — | mentions présentes sur `ivia.quebec` |

---

## Domaine : gouvernance

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| GOUV-001 | Créer le système de gestion opérationnel MERLIN V1 — 5 fichiers | P2 | `active` | `fichier-repo` | — | 5 fichiers dans `00_GOUVERNANCE/` + commit |
| GOUV-002 | Mettre à jour le registre décisions — DEC-036+ (quick wins mai 2026) | P3 | `todo` | `fichier-repo` | — | entrées ajoutées dans `MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md` |
| GOUV-003 | Revue `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` — marquer J9/J10 | P3 | `todo` | `fichier-repo` | INFRA-003 | document à jour avec les validations post-déploiement |
| GOUV-004 | Critères GO/NO-GO lancement public — formaliser dans le registre | P3 | `todo` | `décision` | INFRA-005 | entrée DEC-03X dans le registre |

---

## Domaine : fondements / méthodes

| ID | Titre | Prio | Statut | Livrable attendu | Dépend de | Preuve / critère de sortie |
|---|---|---|---|---|---|---|
| FOND-001 | Corpus 11 Nations QC — compléter les fiches manquantes | P4 | `todo` | `fichier-repo` | — | fiches dans `02_NATIONS_QC/` |
| METH-001 | Cadre méthode 11 Nations QC intl v1.0 — revoir et valider | P4 | `todo` | `fichier-repo` | — | document stable dans `04_METHODES/` |

---

## Suivi global

| Domaine | Total | Done | Active | Todo | Blocked |
|---|---|---|---|---|---|
| infra | 8 | 0 | 0 | 8 | 0 |
| backend | 10 | 5 | 0 | 5 | 0 |
| frontend | 6 | 1 | 0 | 5 | 0 |
| contenu-éditorial | 5 | 1 | 0 | 4 | 0 |
| diffusion | 3 | 0 | 0 | 3 | 0 |
| gouvernance | 4 | 0 | 1 | 3 | 0 |
| fondements/méthodes | 2 | 0 | 0 | 2 | 0 |
| **Total** | **38** | **7** | **1** | **30** | **0** |
