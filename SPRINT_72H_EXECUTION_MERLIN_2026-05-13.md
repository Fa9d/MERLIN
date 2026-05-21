# Sprint 72h execution MERLIN

Date : 2026-05-13  
Objectif : fermer le circuit de valeur minimal sans lancer les 56 taches du backlog.

## 1. Etat apres demarrage

### Vert

- Depot canonique deja tranche : `C:\MERLIN`.
- Depot imbrique `C:\MERLIN\MERLIN` a traiter comme source secondaire/quarantaine.
- Registres existants : agents, tools, evals.
- Registres ajoutes : workflows, memory.
- Validateur `tools/validate_managed_agents.py` etendu aux workflows et contrats memoire.
- Gate agentique complete relancee avec succes le 2026-05-13.
- Alembic head backend canonique : `20260513_0024 (head)` apres pont activation client, seed horaires pilotes et restauration idempotente des personas.

### A surveiller

- `C:\MERLIN` contient beaucoup de changements frontend/backend non commites, probablement issus de l'autre chantier UI/performance.
- `C:\MERLIN\MERLIN` contient encore des changements matching actifs.
- Docker Desktop a ete demarre ensuite ; `merlin_postgres` est healthy et la migration PostgreSQL est appliquee jusqu'a `20260513_0024`.
- Les tests pytest sont maintenant proteges contre la base Postgres locale : `tests/conftest.py` force une SQLite de test sauf opt-in explicite `PYTEST_MERLIN_ALLOW_EXTERNAL_DB=1`.

Le blocage d'environnement initial est leve. Le matching et la reservation E2E sont valides sur API Postgres locale.

### Audit frontend rapide

- `/rendez-vous` existe et cree client + intake + consentements.
- `/rendez-vous/reserver` redirigeait seulement vers `/rendez-vous`; une page de reservation v0.1 a ete implementee le 2026-05-13.
- `/espace-praticien` est une vraie interface riche, mais a tester avec donnees backend.
- `/suivi` existe comme suivi public par references, pas comme espace client authentifie.
- `/ressources` est editorial statique et son CTA pointe vers une reservation non operationnelle.
- `/audio-room` utilise LiveKit avec query params tokenises.
- `/connexion`, `/creer-mon-compte`, `/mon-espace` ont ete ajoutees le 2026-05-13.
- Le token d'invitation post-intake et le lien durable `Client.app_user_id -> AppUser.id` ont ete ajoutes le 2026-05-13.

Rapport detaille : `AUDIT_FRONTEND_PARCOURS_CLIENT_PRATICIEN_2026-05-13.md`.
Implementation : `PONT_POST_INTAKE_IMPLEMENTATION_2026-05-13.md`.

## 2. Validations executees

### Socle agentique

Commandes equivalentes a `make check-agentic` executees avec succes :

- `python tools/validate_managed_agents.py`
- `python tools/run_telescope_minimal.py`
- `python tools/run_telescope_note_e2e.py`
- `python tools/run_merlin_note_fixture.py`
- `python tools/check_merlin_note_negative_runtime.py`
- `python tools/run_merlin_note_fixture.py --candidate-input ...`
- `python tools/validate_runtime_artifacts.py --candidate ...`
- `python tools/run_merlin_note_fixture.py --candidate-source sandbox ...`
- `python tools/validate_runtime_artifacts.py`

Resultat : gate verte.

### Backend canonique

Depuis `C:\MERLIN\10_backend_merlin_api` :

- `python -m alembic heads` : OK, `20260513_0024 (head)`.
- `python -m alembic upgrade head` sur PostgreSQL Docker : OK, `alembic_version = 20260513_0024`.
- `python -m compileall ...` sur les fichiers du pont durable : OK.
- `pytest tests/test_public_intake_flow.py -q` : OK, 5 tests passes.
- `python -m pytest tests/test_matching_recommend.py tests/test_public_intake_flow.py -q` : OK, 9 tests passes sur SQLite de test protegee.
- Smoke HTTP complet sur API PostgreSQL `8002` : OK pour client -> intake -> invitation -> register token -> login -> `/clients/me`.
- Matching Phase C Postgres : OK, `deuil/fr` donne Solene puis Telma.
- Matching `identite/fr/psychocorporel` : OK, Seve puis Nael.
- Matching `distress/fr` depuis intake : OK, Telma, Aelis, Seve.
- Reservation E2E Postgres : OK, matching vers Solene puis 28 creneaux disponibles.
- `POST /bookings/hold-calculated` : HTTP 200, statut `hold`.
- `POST /bookings/confirm` : HTTP 200, statut `confirmed`.
- `GET /bookings/my` : HTTP 200, rendez-vous confirme retrouve.

### Frontend pont client

Depuis `C:\MERLIN\09_app_ivia_merlin` :

- `npm run build` : OK.
- Frontend local relance avec `NEXT_PUBLIC_MERLIN_API_BASE_URL=http://127.0.0.1:8002`.
- Smoke HTTP pages locales : `/connexion`, `/creer-mon-compte`, `/mon-espace`, `/rendez-vous/reserver`, `/operator` : HTTP 200.

### Correction pytest ajoutee pendant validation reservation

Une fixture `autouse=True` supprimait `app_users` avant chaque test, y compris quand le terminal pointait vers Postgres local. Elle est maintenant limitee aux bases SQLite, et pytest force une SQLite de test par defaut. Postgres local a ete restaure avec `20260513_0024` et `tools/seed_local_demo_access.py`.

### Correction auth ajoutee pendant validation Postgres

Les praticiens seedes par migration faisaient que la creation du premier admin etait refusee (`403`) car la logique regardait le nombre total d'utilisateurs. La route `/auth/register` regarde maintenant le nombre d'admins `admin_tech` : le premier admin reste creable sans token tant qu'aucun admin n'existe, puis les creations suivantes redeviennent admin-gated.

## 3. Decisions operationnelles

1. Ne pas toucher aux fichiers frontend/backend modifies dans `C:\MERLIN` sans audit cible du chantier UI.
2. Ne pas rapatrier automatiquement les fichiers du depot imbrique `C:\MERLIN\MERLIN`.
3. Valider le matching par comportement des que le backend et la base sont disponibles. Fait sur Postgres local.
4. Demander du code brut complet seulement pour migrations DB, securite, donnees sensibles ou actions irreversibles.
5. Pour routes API et UI reversibles, valider par tests observables.

## 4. Prochaine action Copilot / Claude Code

Message court a donner a l'agent qui travaille dans le code :

```text
Objectif suivant : rendre le rendez-vous exploitable cote praticien et operateur, sans coller de code dans le chat.

Depuis l'environnement local MERLIN, garde le backend et la base disponibles, puis execute :

1. Verifier que le rendez-vous confirme apparait dans la vue praticien ou endpoint interne approprie.

2. Creer ou relier une SessionRecord a la reservation confirmee.

3. Verifier que l'operateur voit le statut : intake -> invite -> active -> reserve.

4. Ajouter le statut financier minimal : paiement requis, paye, exempt, remboursement/annulation.

Si erreur, corrige, redemarre, reteste. Ne retourne que : statut, tests lances, resultats, fixes effectues, blocage restant s'il y en a un.
```

## 5. Prochaine action Perplexity

Message court :

```text
Produis une v0.1 Quebec pour IVIA : mentions legales, politique de confidentialite, consentement donnees et clause de limites de service. Ce n'est pas un avis juridique final. Cite les points a faire valider par un juriste et les obligations Loi 25 a ne pas oublier.
```

## 6. Prochaine action produit

Auditer l'etat reel de ces pages :

- `/espace-praticien`
- `/rendez-vous/reserver`
- `/suivi`
- `/ressources`
- `/audio-room`

Puis specifier ou construire :

- `/connexion`
- `/creer-mon-compte`
- `/mon-espace`

## 7. Definition de succes du sprint

Le sprint est reussi si, dans 72h, on peut demontrer :

1. depot canonique stable ;
2. gate agentique verte ;
3. Alembic head connu ;
4. Phase C matching validee par tests API ; fait.
5. etat reel des pages clefs connu ;
6. chemin client post-intake specifie et reserve ; fait jusqu'au booking confirme.
7. message praticien pilote pret a envoyer ;
8. legal v0.1 pret pour validation humaine.

## 8. Phrase de conduite

Tout doit rapprocher MERLIN d'une chaine testee : client -> intake -> matching -> praticien -> compte -> reservation -> session -> suivi -> revenu.
