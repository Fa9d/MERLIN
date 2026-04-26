# MERLIN - Log test prod / trace / nettoyage 2026-04-24 v1.0

Date: 2026-04-24
Statut: ouvert
Objet: tracer tous les objets crees pour le test prod de flux `session -> session_note -> derived_document` afin de permettre un nettoyage complet avant usage reel

---

## 1) Regle de test

Tout objet cree pour ce test doit:

- etre fictif;
- etre marque par un prefixe explicite `TEST-2026-04-24-QC`;
- rester distinguable d'une vraie activite;
- etre inscrit ici avec son identifiant exact.

---

## 2) Scenario vise

Scenario:

- client fictif quebecois;
- intake fictif;
- seance fictive;
- transcript fictif en francais quebecois;
- note structuree generee;
- document derive client genere.

---

## 3) Objets a tracer

| Type | Identifiant | Marqueur lisible | Statut nettoyage | Notes |
|---|---|---|---|---|
| `admin_user` | `97f51dc7-df05-4655-a383-77c6295dec9c` | `TEST-2026-04-24-QC Admin` | pending | `davidphaneuf+test-merlin-20260424@gmail.com` |
| `operator_user` | `5c65e043-b6ef-49d3-a533-38f8300235f1` | `TEST-2026-04-24-QC Operateur` | pending | `davidphaneuf+test-merlin-operator-20260424-1@gmail.com` |
| `client` | `2742062b-877c-4f32-ab8a-8f85f67c3306` | `TEST-2026-04-24-QC Mathieu Bouchard` | pending | client fictif Quebec |
| `public_client_code` | `CLI-970D713FF4` | `TEST-2026-04-24-QC` | pending | route publique testee avec succes |
| `intake_request` | `7b00fa4a-76f0-48d2-a2c7-b09307d1554b` | `TEST-2026-04-24-QC` | pending | demande d'entree fictive |
| `session` | `1afa4673-5b6f-4bbd-b9db-c93544997a4e` | `TEST-2026-04-24-QC` | pending | seance fictive cloturee avec transcript |
| `session_note` | `27519427-7a47-4dcf-8b22-d888500b89db` | `TEST-2026-04-24-QC` | pending | note generee automatiquement |
| `derived_document` | `79b658aa-9437-4872-8c36-9bca6e44df07` | `TEST-2026-04-24-QC` | pending | document client visible genere automatiquement |

---

## 4) Principe de nettoyage

Le backend V1 ne fournit pas encore de routes de suppression gouvernees pour ces objets.

En consequence:

- le nettoyage final devra etre fait explicitement;
- il devra etre execute en base dans l'ordre inverse des dependances;
- rien ne devra etre supprime sans verification des IDs traces ici.

Ordre de suppression cible:

1. `derived_documents`
2. `session_notes`
3. `sessions`
4. `intake_requests`
5. `consents` lies au test si crees
6. `clients`
7. `app_users` de test si crees

---

## 5) Etat courant

Etat au 2026-04-24 11:49 America/Toronto:

- le flux prod `auth -> client -> intake_request -> session -> close session -> session_note -> derived_document` a ete execute avec succes;
- la route interne `GET /api/v1/derived-documents?client_id=...` retourne bien le document genere;
- la route publique `GET /api/v1/derived-documents/public/client/CLI-970D713FF4` retourne bien le document client visible;
- le test confirme le fonctionnement technique du pipeline d'analyse texte avec generation de note et document derive;
- le nettoyage n'a pas encore ete execute.

Points de vigilance releves:

- le rendu redactionnel du `body_text` genere reste perfectible;
- double ponctuation observee dans le document derive;
- normalisation linguistique a polir avant usage reel.

### Complement 2026-04-25

Un redeploiement correctif du backend a ete effectue afin de corriger:

- le titre genere du document client;
- la ponctuation terminale du `body_text`;
- l'assemblage defensif des fragments textuels issus de l'IA.

Validation finale executee en prod le 2026-04-25:

- le conteneur `merlin-api-1` charge bien les fonctions `_ensure_terminal_punctuation` et `_build_generated_document_title`;
- un nouveau cycle `client -> session -> close session -> session_note -> derived_document` a ete execute avec succes;
- le nouveau document genere porte le titre `Synthese de seance 1`;
- le `body_text` ne contient plus de `..`;
- le pipeline Anthropic reste fonctionnel avec `model_used = claude-sonnet-4-20250514` et `prompt_version = session_note_cercle_v1`.

Objets supplementaires traces le 2026-04-25:

| Type | Identifiant | Marqueur lisible | Statut nettoyage | Notes |
|---|---|---|---|---|
| `client` | `ae6ee00e-3cf6-454e-a059-0b3fb64237fb` | `TEST-2026-04-25-QC Julie Gagnon` | pending | client fictif Quebec, cycle de validation final |
| `session` | `7b63b46d-5a1b-41ea-90cd-1fe47899c113` | `TEST-2026-04-25-QC` | pending | seance fictive cloturee avec transcript court |
| `session_note` | `48ad752d-0a58-4adb-8e25-085a441ba213` | `TEST-2026-04-25-QC` | pending | note generee automatiquement, rendu final valide |
| `derived_document` | `1b44ee83-adf0-48e7-81d3-ab4cc94d3e46` | `TEST-2026-04-25-QC` | pending | titre et ponctuation corriges valides en prod |

Conclusion de validation:

- le flux prod est confirme fonctionnel de bout en bout;
- le correctif de rendu du document client est confirme en prod;
- le nettoyage n'a toujours pas ete execute sur les objets traces.

### Complement 2026-04-26

Le sprint de durcissement `J1` a `J6` a ete rejoue et verifie en production sur les points suivants:

- frontend IVIA deployee en prod sur `https://ivia.quebec`;
- API revalidee sur `https://api.ivia.quebec/api/health`;
- TLS multi-domaine corrige pour `api.ivia.quebec` et `ivia.quebec`;
- renouvellement Certbot simule avec succes apres nettoyage des anciennes configurations cassees;
- acces public `/suivi` borne par `public_client_code + intake_request_id`;
- workflow documentaire confirme: document cree en `client_pending_review`, non public avant validation `supervisor`;
- tentative de validation par `operator` rejetee en `403`;
- validation par `supervisor` acceptee en `200`;
- lecture operateur de son document derive confirmee en `200`.

Objets et references de verification utilises le 2026-04-26:

| Type | Identifiant | Marqueur lisible | Statut nettoyage | Notes |
|---|---|---|---|---|
| `operator_user` | `b6335c38-27ea-4ab0-b8c1-f7ae6176a219` | `TEST Operator 2` | pending | `davidphaneuf+test-merlin-operator-2-20260426@gmail.com` |
| `supervisor_user` | `7fc2f846-8763-4f17-83ce-58362776ff41` | `TEST Supervisor` | pending | `davidphaneuf+test-merlin-supervisor-20260426@gmail.com` |
| `client` | `cc453562-1c46-4411-a893-f505d2b17672` | client de verification diffusion | pending | reutilise pour verifier `J4` et `J5` |
| `public_client_code` | `CLI-C487399860` | reference publique de verification | pending | couple attendu avec intake |
| `intake_request` | `3cbd327e-27a5-400b-ac73-565a6ef3272c` | reference d'entree de verification | pending | requis pour la route publique `/suivi` |
| `session` | `cbad3e36-9b1f-4443-9c68-8c6520c0cd29` | seance 4 de verification diffusion | pending | seance cloturee testee avant / apres validation |
| `session_note` | `f2babab4-512f-4dde-b67c-2ab271d10f01` | note supervision 2026-04-26 | pending | validation `operator` refusee, validation `supervisor` acceptee |
| `derived_document` | `73f8ab05-3e4a-4527-82e0-2e8788abacc3` | document client diffusion 2026-04-26 | pending | document public apres validation supervision |

Note d'exploitation:

- les mots de passe des comptes de test `operator 2` et `supervisor` ont ete reinitialises pendant la verification prod afin de rejouer proprement les tests d'auth;
- les nouvelles valeurs ne doivent pas etre consignees dans ce fichier public de repo et doivent etre stockees uniquement dans le runbook securise.

### Complement 2026-04-26 - Validation `J8` e2e depuis zero

La checklist de recette prod e2e `J8` a ete executee en production avec succes depuis zero.

Verification rejouee:

- authentification `operator` et `supervisor` avec comptes de test dedies;
- creation publique d'un `client`;
- creation publique d'une `intake_request`;
- creation puis cloture d'une `session` par `operator`;
- creation automatique d'une `session_note` et d'un `derived_document`;
- verification avant validation: document en `client_pending_review` et `client_visible = false`;
- verification negative: `/suivi` retourne `[]` avant validation et `404` avec une mauvaise `intake_request_id`;
- verification negative: validation de la note par `operator` rejetee en `403`;
- verification positive: validation de la note par `supervisor` acceptee en `200`;
- verification finale: le document apparait ensuite dans le flux public `/suivi`.

Objets traces confirms par la sortie de test:

| Type | Identifiant | Marqueur lisible | Statut nettoyage | Notes |
|---|---|---|---|---|
| `client` | `63db6770-66fd-494b-a361-50b8f0accef1` | `TEST-E2E-20260426...` | pending | client public cree pendant la recette `J8` |
| `public_client_code` | `CLI-E0F6278DF6` | reference publique `J8` | pending | code client publie pour la verification finale `/suivi` |
| `intake_request` | `3d3971b6-8612-4556-b1c7-e5adf65fe04a` | intake e2e production | pending | demande creee publiquement pendant `J8` |
| `session` | `7a9805c3-0861-4320-9c19-c43cfcd2e54f` | session e2e production | pending | seance cloturee par `operator` pendant `J8` |
| `session_note` | `538713fc-5ac7-4db3-ba15-54f667b26d2c` | note e2e production | pending | validation `operator` refusee puis validation `supervisor` acceptee |
| `derived_document` | `9bc81ac6-3a63-47a8-bf97-b1f7230eac36` | document diffusion e2e production | pending | passe de `client_pending_review` a `client` |

Verification complementaire:

- les liaisons `derived_document -> session_note -> session -> client -> intake_request` ont ensuite ete recontrolees en base sur le VPS avant execution du nettoyage.

## 6) SQL cible de nettoyage

Nettoyage cible, strictement borne aux IDs de test traces ci-dessus:

```sql
BEGIN;

DELETE FROM derived_documents
WHERE id = '79b658aa-9437-4872-8c36-9bca6e44df07';

DELETE FROM derived_documents
WHERE id = '1b44ee83-adf0-48e7-81d3-ab4cc94d3e46';

DELETE FROM session_notes
WHERE id = '27519427-7a47-4dcf-8b22-d888500b89db';

DELETE FROM session_notes
WHERE id = '48ad752d-0a58-4adb-8e25-085a441ba213';

DELETE FROM audio_recordings
WHERE audio_session_id IN (
    SELECT id FROM audio_sessions WHERE session_id = '1afa4673-5b6f-4bbd-b9db-c93544997a4e'
);

DELETE FROM audio_sessions
WHERE session_id = '1afa4673-5b6f-4bbd-b9db-c93544997a4e';

DELETE FROM sessions
WHERE id = '1afa4673-5b6f-4bbd-b9db-c93544997a4e';

DELETE FROM audio_recordings
WHERE audio_session_id IN (
    SELECT id FROM audio_sessions WHERE session_id = '7b63b46d-5a1b-41ea-90cd-1fe47899c113'
);

DELETE FROM audio_sessions
WHERE session_id = '7b63b46d-5a1b-41ea-90cd-1fe47899c113';

DELETE FROM sessions
WHERE id = '7b63b46d-5a1b-41ea-90cd-1fe47899c113';

DELETE FROM intake_requests
WHERE id = '7b00fa4a-76f0-48d2-a2c7-b09307d1554b';

DELETE FROM consents
WHERE client_id = '2742062b-877c-4f32-ab8a-8f85f67c3306';

DELETE FROM clients
WHERE id = '2742062b-877c-4f32-ab8a-8f85f67c3306';

DELETE FROM clients
WHERE id = 'ae6ee00e-3cf6-454e-a059-0b3fb64237fb';

DELETE FROM app_users
WHERE id IN (
    '97f51dc7-df05-4655-a383-77c6295dec9c',
    '5c65e043-b6ef-49d3-a533-38f8300235f1'
);

COMMIT;
```

Ajout cible pour le run `J8` du 2026-04-26, a executer seulement apres verification que le client `63db6770-66fd-494b-a361-50b8f0accef1` n'est relie qu'a des objets de test:

```sql
BEGIN;

DELETE FROM derived_documents
WHERE id = '9bc81ac6-3a63-47a8-bf97-b1f7230eac36';

DELETE FROM session_notes
WHERE id = '538713fc-5ac7-4db3-ba15-54f667b26d2c';

DELETE FROM audio_recordings
WHERE audio_session_id IN (
    SELECT id FROM audio_sessions WHERE session_id = '7a9805c3-0861-4320-9c19-c43cfcd2e54f'
);

DELETE FROM audio_sessions
WHERE session_id = '7a9805c3-0861-4320-9c19-c43cfcd2e54f';

DELETE FROM sessions
WHERE id = '7a9805c3-0861-4320-9c19-c43cfcd2e54f';

DELETE FROM intake_requests
WHERE id = '3d3971b6-8612-4556-b1c7-e5adf65fe04a';

DELETE FROM consents
WHERE client_id = '63db6770-66fd-494b-a361-50b8f0accef1';

DELETE FROM clients
WHERE id = '63db6770-66fd-494b-a361-50b8f0accef1';

COMMIT;
```

Verification post-nettoyage:

```sql
SELECT
    (SELECT count(*) FROM app_users WHERE id IN (
        '97f51dc7-df05-4655-a383-77c6295dec9c',
        '5c65e043-b6ef-49d3-a533-38f8300235f1'
    )) AS app_users_test,
    (SELECT count(*) FROM clients WHERE id = '2742062b-877c-4f32-ab8a-8f85f67c3306') AS clients_test,
    (SELECT count(*) FROM clients WHERE id = 'ae6ee00e-3cf6-454e-a059-0b3fb64237fb') AS clients_test_20260425,
    (SELECT count(*) FROM intake_requests WHERE id = '7b00fa4a-76f0-48d2-a2c7-b09307d1554b') AS intake_test,
    (SELECT count(*) FROM sessions WHERE id = '1afa4673-5b6f-4bbd-b9db-c93544997a4e') AS sessions_test,
    (SELECT count(*) FROM sessions WHERE id = '7b63b46d-5a1b-41ea-90cd-1fe47899c113') AS sessions_test_20260425,
    (SELECT count(*) FROM sessions WHERE id = '7a9805c3-0861-4320-9c19-c43cfcd2e54f') AS sessions_test_20260426_j8,
    (SELECT count(*) FROM intake_requests WHERE id = '3d3971b6-8612-4556-b1c7-e5adf65fe04a') AS intake_test_20260426_j8,
    (SELECT count(*) FROM session_notes WHERE id = '27519427-7a47-4dcf-8b22-d888500b89db') AS notes_test,
    (SELECT count(*) FROM session_notes WHERE id = '48ad752d-0a58-4adb-8e25-085a441ba213') AS notes_test_20260425,
    (SELECT count(*) FROM session_notes WHERE id = '538713fc-5ac7-4db3-ba15-54f667b26d2c') AS notes_test_20260426_j8,
    (SELECT count(*) FROM derived_documents WHERE id = '79b658aa-9437-4872-8c36-9bca6e44df07') AS documents_test,
    (SELECT count(*) FROM derived_documents WHERE id = '1b44ee83-adf0-48e7-81d3-ab4cc94d3e46') AS documents_test_20260425,
    (SELECT count(*) FROM derived_documents WHERE id = '9bc81ac6-3a63-47a8-bf97-b1f7230eac36') AS documents_test_20260426_j8,
    (SELECT count(*) FROM clients WHERE id = '63db6770-66fd-494b-a361-50b8f0accef1') AS clients_test_20260426_j8;
```


## 7) References

- [MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md)
- [MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md)
- [MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md)
