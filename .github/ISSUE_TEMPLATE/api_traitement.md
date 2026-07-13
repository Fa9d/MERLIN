---
name: "[API] Traitement MERLIN"
about: "Suivi d'un endpoint ou d'un flux backend — bug, évolution ou nouveau traitement"
title: "[API] MÉTHODE /chemin — traitement"
labels: ["api", "merlin"]
---

<!-- Convention de titre : [API] POST /sessions — création séance -->

## Endpoint
- **Méthode & chemin** : `POST /api/v1/...`
- **Tag OpenAPI** : `sessions` <!-- voir https://api.ivia.quebec/docs -->
- **Fichier** : `10_backend_merlin_api/app/api/routes/....py`

## Objectif métier
<!-- Une ou deux phrases : à quoi sert ce traitement dans le parcours IVIA
     (client / praticien / admin), et quelle règle de la constitution il touche
     (validation humaine, Loi 21/25, triade O/H/O, vannes de capacités…). -->

## Input attendu
```json
{}
```
<!-- Corps, paramètres path/query, en-têtes particuliers. Schéma Pydantic : app/schemas/... -->

## Output attendu
```json
{}
```
<!-- Statut HTTP + schéma de réponse. -->

## Cas d'erreur
| Statut | Cas | Message attendu |
|---|---|---|
| 401 | non authentifié | |
| 403 | rôle/vanne insuffisant | |
| 404 | ressource hors périmètre | |
| 409/422/429 | métier | |

## Vérification
- [ ] Swagger : https://api.ivia.quebec/docs — section du tag ci-dessus
- [ ] Postman : `docs/api/merlin_postman_collection.json` — requête ajoutée/à jour
- [ ] Test pytest : `10_backend_merlin_api/tests/test_....py`
- [ ] Si sortie client IA : safety suite du registre passée (`managed_agents/evals.registry.yaml`)

## Notes / journal
<!-- Décisions prises, liens vers 05_JOURNAUX/ ou 00_GOUVERNANCE/ si structurant. -->
