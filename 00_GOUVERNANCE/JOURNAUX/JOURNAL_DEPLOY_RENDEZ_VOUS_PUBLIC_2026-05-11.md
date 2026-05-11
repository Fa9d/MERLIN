# Journal de deploiement - Parcours public rendez-vous

Date: 2026-05-11
Portee: IVIA production - https://ivia.quebec/rendez-vous

## Contexte

Le parcours public de demande de seance affichait l'erreur: "Authentification requise pour ce type de consentement."

Cause identifiee: le frontend public envoyait des consentements `consent_recording` et `consent_transcription`, mais l'API ne les autorisait pas dans la liste des consentements acceptes sans authentification pour le flux public d'intake.

Decision produit confirmee: le prospect et le client doivent rester separes. Le prospect ne doit pas etre envoye vers une creation de compte avant sa demande initiale.

## Correctifs livres

- Backend: ajout de `consent_recording` et `consent_transcription` aux consentements publics autorises pour l'intake.
- Backend: test de regression du flux public, incluant le refus maintenu de `consent_third_party_transmission` sans authentification.
- Frontend: page `/rendez-vous` alignee sur les cinq consentements du parcours public.
- Frontend: `/rendez-vous/reserver` redirige vers `/rendez-vous` afin d'eviter un mur de compte pour les prospects.
- Frontend: suppression de la dependance de build a `src/generated/prisma/client` dans `src/lib/db.ts`, car le frontend production passe par l'API FastAPI et le client Prisma genere n'est pas archive.

## Commits deployes et pousses

- `3312c79 fix(rendez-vous): align public prospect intake flow`
- `662f002 fix(frontend): remove generated prisma build dependency`
- `1497096 docs(deploy): journal public rendez-vous production fix`

Note: le deploiement VPS a ete effectue avant le rebase final sur `origin/master`, depuis les memes contenus source. Les SHA pre-rebase etaient `81ea32a` et `fbead84`.

## Validation locale

- Backend cible: `python -m pytest tests/test_public_intake_flow.py` reussi.
- Frontend: `npm run build` reussi apres correction de `src/lib/db.ts`.

## Validation production API

API production saine:

- `merlin-api-1` en etat healthy.
- `/health` interne: `status=ok`, `database=ok`.
- Preflight CORS externe vers `/api/v1/consents`: `HTTP/2 200`, `access-control-allow-origin: https://ivia.quebec`.

Validation directe du flux public:

- Client cree: `006f0fd0-03ad-476b-92af-b168eaaa6b64`, code `CLI-BE64BF5926`.
- Intake cree: `c07397ab-86b1-42a7-8de6-130c126daf6c`.
- Consentements publics acceptes en `201`:
  - `consent_session`
  - `consent_session_note`
  - `consent_history`
  - `consent_recording`
  - `consent_transcription`

## Validation production frontend

Frontend reconstruit et recree via Docker Compose sur `/opt/merlin`.

Etat observe apres redeploiement:

- `merlin-frontend-1` demarre et sert Next.js sur `3000/tcp`.
- `https://ivia.quebec/rendez-vous` retourne `200` et contient la copie: "Les quatre premiers consentements".
- L'ancienne copie "Les deux premiers consentements" est absente.
- `https://ivia.quebec/rendez-vous/reserver` retourne `307` vers `/rendez-vous`, puis `200`.
- Test navigateur production: soumission reussie depuis la page live, confirmation visible sans erreur d'authentification.
  - Reference client: `CLI-887E55269A`.
  - Reference d'entree: `f5381f30-64d8-4914-8dc8-6f9672dcb2fb`.

## Notes operationnelles

- Le premier smoke test frontend a recu un `502` pendant les secondes de redemarrage du conteneur; verification suivante saine.
- Le deploiement manuel a utilise `git archive` pour eviter d'inclure `.venv` et les artefacts locaux.
- Les repertoires production peuvent etre possedes par root; extraction effectuee avec `sudo tar --touch --no-same-owner --no-same-permissions`, puis `sudo chown`.

## Etat final

Le message "Authentification requise pour ce type de consentement" ne se reproduit plus pour le parcours prospect public attendu. Le backend accepte les cinq consentements publics requis/optionnels du formulaire, et le frontend production sert la version alignee du parcours.
