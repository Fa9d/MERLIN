# JOURNAL — Carte de Vie réelle (client test Daniel David)

**Date** : 2026-07-07
**Opérateur** : Claude Code (session agents/cleanup-production-workflow)
**Références** : JOURNAL précédents de la même branche (compte praticien réel, ménage mock)

---

## Contexte

La page démo `praticien/carte-de-vie-demo.html` (données inventées) a été remplacée par une
vraie page praticien `praticien/carte-de-vie.html`, 100 % branchée sur l'API. Demande du
fondateur : « on enlève mode démo, affiche les bonnes valeurs, utilise les deux textes que
j'ai intégrés au journal ».

## Ce qui a été fait

### Backend (commit `48dd13e`, déployé --build)
- Capacité `carte_de_vie` ajoutée au catalogue `capability_gate` (max hypothese, données sur serveur).
- `GET /api/v1/analysis/clients/{id}` — analyses par client, filtrées par vanne de profil.
- `PUT /api/v1/analysis/clients/{id}/carte-de-vie` — le praticien enregistre sa lecture (upsert).

### Frontend (même commit)
- `praticien/carte-de-vie.html` : fiche client, ligne de vie (client_life_events),
  constellation D3 (11 axes, territoire au centre), tensions, triade O/H/O — tout depuis l'API
  et les référentiels vivants. Bouton « Carte de Vie » sur chaque carte de
  `clients-journal.html`. Cache api.js bump `v=20260707c`.

### Données réelles (seed prod, ce jour)
Source : les deux textes littéraires déposés par Daniel David dans son journal
(entrées des 3 et 7 juillet 2026 — récit « Oli », Les Vans / retour à Montréal).

- **10 `client_life_events`** créés (1945 curé Label → 2026 retour à Montréal),
  avec liens parent (devoir→« sois correct » ; référendum 1995→appel de Rémi),
  narrative_then / narrative_now cités depuis les textes.
- **1 `analysis_results`** capability=`carte_de_vie`, sensitivity=`hypothese`,
  engine_version=`carte-de-vie-v1`, created_by = praticien davidphaneuf@gmail.com.
  Payload : sol (2 volets), 11 axes avec résonance+note, 3 tensions
  (appartenance, charge/exigences, sens), fil, fil à tirer, triade
  Observation / Hypothèse / Orientation (aucun vocabulaire diagnostic —
  « burn-out / dépression » cités uniquement comme mots du client),
  charges par événement + marqueurs narrated_now (1995 revécu via l'appel de Rémi).

## Vérifications
- DB prod : 10 rows `client_life_events`, 1 row `analysis_results` (payload 5137 c.).
- `GET /analysis/clients/{id}` sans auth → 401 (protection OK).
- Page live `https://ivia.quebec/praticien/carte-de-vie.html` → 200.
- Parcours praticien : clients-journal → bouton « Carte de Vie » → carte de Daniel.

## Conformité
- Posture non-médicale respectée : triade O/H/O, aucune prescription.
- Données du client test uniquement (compte de test du fondateur).
- Exposition filtrée par `capability_gate` selon le profil.

## Reste à faire
- Le fondateur vérifie la carte connecté comme praticien et ajuste sa lecture
  via le bouton d'édition (PUT carte-de-vie) si souhaité.
