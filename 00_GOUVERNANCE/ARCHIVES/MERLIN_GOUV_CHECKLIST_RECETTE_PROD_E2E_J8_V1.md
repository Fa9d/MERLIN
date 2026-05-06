# MERLIN - Checklist recette prod e2e J8 V1

Date: 2026-04-26
Statut: actif
Objet: fournir une recette production unique, courte et rejouable pour verifier le flux `public -> operator -> supervisor -> public`

---

## 1) Usage

Cette checklist sert a verifier en production:

- la disponibilite publique IVIA;
- la disponibilite API MERLIN;
- l'authentification `operator` et `supervisor`;
- le flux public `client -> intake_request`;
- le flux interne `session -> close -> session_note -> derived_document`;
- le verrouillage de supervision;
- la diffusion publique finale cote client.

Regle d'execution:

- executer `une commande par ligne`;
- ne pas coller le prompt shell avec les commandes;
- conserver les IDs retournes dans les variables d'environnement de la session courante.

---

## 2) Preconditions

Necessaire:

- acces SSH au VPS prod;
- acces au repertoire `/opt/merlin`;
- `curl`, `python3`, `docker`, `docker compose`;
- mots de passe courants des comptes de test `operator` et `supervisor`, conserves hors repo selon le runbook securise.

Comptes de test recommandes:

- `davidphaneuf+test-merlin-operator-2-20260426@gmail.com`
- `davidphaneuf+test-merlin-supervisor-20260426@gmail.com`

Important:

- ne pas consigner les mots de passe dans ce fichier ni dans le repo;
- si les mots de passe de test ne fonctionnent plus, les reinitialiser via procedure securisee avant de poursuivre.

Reference operatoire:

- [MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md)

---

## 3) Preflight infra

Depuis le VPS:

```bash
cd /opt/merlin
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
curl -I https://ivia.quebec
curl -I https://ivia.quebec/rendez-vous
curl -I https://ivia.quebec/suivi
curl -I https://ivia.quebec/operator
curl -I https://ivia.quebec/supervision
curl https://api.ivia.quebec/api/health
```

Resultat attendu:

- les routes `ivia.quebec` repondent `200`;
- `https://api.ivia.quebec/api/health` retourne `status = ok`.

---

## 4) Authentification comptes de test

```bash
read -s OPERATOR2_PW; echo
```

```bash
export OPERATOR2_TOKEN=$(curl -s -X POST https://api.ivia.quebec/api/v1/auth/login -H 'Content-Type: application/json' -d "{\"email\":\"davidphaneuf+test-merlin-operator-2-20260426@gmail.com\",\"password\":\"$OPERATOR2_PW\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

```bash
read -s SUPERVISOR_PW; echo
```

```bash
export SUPERVISOR_TOKEN=$(curl -s -X POST https://api.ivia.quebec/api/v1/auth/login -H 'Content-Type: application/json' -d "{\"email\":\"davidphaneuf+test-merlin-supervisor-20260426@gmail.com\",\"password\":\"$SUPERVISOR_PW\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

```bash
printf 'OPERATOR2_TOKEN=%s\nSUPERVISOR_TOKEN=%s\n' "${OPERATOR2_TOKEN:+set}" "${SUPERVISOR_TOKEN:+set}"
```

Resultat attendu:

- les deux variables affichent `set`;
- si une commande echoue avec `KeyError: 'access_token'`, les identifiants sont invalides.

---

## 5) Creation d'un client public de test

```bash
export TEST_TS=$(date +%Y%m%d%H%M%S)
```

```bash
export TEST_EMAIL="merlin-e2e-$TEST_TS@example.com"
```

```bash
export CLIENT_JSON=$(curl -s -X POST https://api.ivia.quebec/api/v1/clients -H 'Content-Type: application/json' -d "{\"first_name_or_alias\":\"TEST-E2E-$TEST_TS\",\"email\":\"$TEST_EMAIL\",\"is_adult_confirmed\":true}")
```

```bash
export CLIENT_ID=$(printf '%s' "$CLIENT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

```bash
export CLIENT_CODE=$(printf '%s' "$CLIENT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['public_client_code'])")
```

```bash
printf 'CLIENT_ID=%s\nCLIENT_CODE=%s\n' "$CLIENT_ID" "$CLIENT_CODE"
```

Resultat attendu:

- un `CLIENT_ID` et un `CLIENT_CODE` sont crees;
- l'entree publique client passe sans token.

---

## 6) Creation d'une intake publique de test

```bash
export INTAKE_JSON=$(curl -s -X POST https://api.ivia.quebec/api/v1/intake-requests -H 'Content-Type: application/json' -d "{\"client_id\":\"$CLIENT_ID\",\"request_channel_code\":\"web_form\",\"request_for_code\":\"self\",\"primary_need_code\":\"clarification\",\"perceived_urgency_code\":\"non_urgent\",\"support_already_in_place\":false,\"requested_outcome_text\":\"Clarifier la situation et repartir avec une suite concrete.\",\"entry_summary_text\":\"TEST E2E production.\"}")
```

```bash
export INTAKE_ID=$(printf '%s' "$INTAKE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

```bash
printf 'INTAKE_ID=%s\n' "$INTAKE_ID"
```

Resultat attendu:

- une `INTAKE_ID` est creee;
- le flux public `client + intake_request` est complet.

---

## 7) Creation et cloture de seance cote operator

```bash
export SESSION_JSON=$(curl -s -X POST https://api.ivia.quebec/api/v1/sessions -H "Authorization: Bearer $OPERATOR2_TOKEN" -H 'Content-Type: application/json' -d "{\"client_id\":\"$CLIENT_ID\",\"intake_request_id\":\"$INTAKE_ID\",\"session_mode_code\":\"follow_up\",\"session_channel_code\":\"phone\",\"session_status_code\":\"scheduled\"}")
```

```bash
export SESSION_ID=$(printf '%s' "$SESSION_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

```bash
printf 'SESSION_ID=%s\n' "$SESSION_ID"
```

```bash
export CLOSE_JSON=$(curl -s -X POST https://api.ivia.quebec/api/v1/sessions/$SESSION_ID/close -H "Authorization: Bearer $OPERATOR2_TOKEN" -H 'Content-Type: application/json' -d '{"actual_start_at":"2026-04-26T16:00:00Z","actual_end_at":"2026-04-26T16:50:00Z","session_status_code":"completed","presenting_topic_text":"Besoin de clarification","session_highlights_text":"La cliente a mieux nomme sa surcharge et ses besoins","operator_assessment_text":"Echange stable et coherent","vigilance_level_code":"watch","follow_up_actions_text":"Proposer un suivi dans une semaine","next_session_focus_text":"Clarifier les sources de pression","client_visible":true}')
```

```bash
export NOTE_ID=$(printf '%s' "$CLOSE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['generated_note']['id'])")
```

```bash
export DOCUMENT_ID=$(printf '%s' "$CLOSE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['generated_document']['id'])")
```

```bash
printf 'NOTE_ID=%s\nDOCUMENT_ID=%s\n' "$NOTE_ID" "$DOCUMENT_ID"
```

Resultat attendu:

- `SESSION_ID`, `NOTE_ID` et `DOCUMENT_ID` existent;
- le document est cree en attente de supervision.

---

## 8) Assertions avant validation supervision

Lecture operateur du document derive:

```bash
curl -s -i -H "Authorization: Bearer $OPERATOR2_TOKEN" "https://api.ivia.quebec/api/v1/derived-documents?session_id=$SESSION_ID"
```

Lecture publique avant validation:

```bash
curl -s -i "https://api.ivia.quebec/api/v1/derived-documents/public/client/$CLIENT_CODE?intake_request_id=$INTAKE_ID"
```

Acces public avec mauvaise reference:

```bash
curl -s -i "https://api.ivia.quebec/api/v1/derived-documents/public/client/$CLIENT_CODE?intake_request_id=00000000-0000-0000-0000-000000000000"
```

Tentative de validation par operator:

```bash
curl -s -i -X PATCH "https://api.ivia.quebec/api/v1/session-notes/$NOTE_ID/validate" -H "Authorization: Bearer $OPERATOR2_TOKEN" -H "Content-Type: application/json" -d '{"validated":true,"corrections":null}'
```

Resultat attendu:

- la lecture operateur repond `200` et montre un document `client_pending_review` avec `client_visible = false`;
- la lecture publique avant validation retourne `200` avec une liste vide;
- la mauvaise `intake_request_id` retourne `404`;
- la tentative de validation par `operator` retourne `403`.

---

## 9) Validation supervision

Validation simple:

```bash
curl -s -i -X PATCH "https://api.ivia.quebec/api/v1/session-notes/$NOTE_ID/validate" -H "Authorization: Bearer $SUPERVISOR_TOKEN" -H "Content-Type: application/json" -d '{"validated":true,"corrections":null}'
```

Resultat attendu:

- la route repond `200`;
- `validated_by_practitioner = true`.

Option correction supervision:

```bash
curl -s -i -X PATCH "https://api.ivia.quebec/api/v1/session-notes/$NOTE_ID/validate" -H "Authorization: Bearer $SUPERVISOR_TOKEN" -H "Content-Type: application/json" -d '{"validated":true,"corrections":{"coeur":"Charge affective a surveiller","vigilance":"watch","next_step":"Clarifier les pressions principales"}}'
```

Usage:

- n'utiliser cette variante que si l'objectif est de verifier l'enregistrement des corrections supervision;
- sinon conserver la validation simple precedente.

---

## 10) Assertions apres validation supervision

Lecture operateur du document derive:

```bash
curl -s -i -H "Authorization: Bearer $OPERATOR2_TOKEN" "https://api.ivia.quebec/api/v1/derived-documents?session_id=$SESSION_ID"
```

Lecture publique apres validation:

```bash
curl -s -i "https://api.ivia.quebec/api/v1/derived-documents/public/client/$CLIENT_CODE?intake_request_id=$INTAKE_ID"
```

Resultat attendu:

- la lecture operateur repond `200` avec `audience_code = client` et `client_visible = true`;
- la lecture publique repond `200` avec le document derive visible.

---

## 11) Trace minimale a consigner

Conserver hors repo:

- date et heure du test;
- nom ou initiales du relecteur;
- `CLIENT_ID`
- `CLIENT_CODE`
- `INTAKE_ID`
- `SESSION_ID`
- `NOTE_ID`
- `DOCUMENT_ID`
- verdict global `PASS / FAIL`
- ecarts observes.

Conserver dans le repo seulement:

- les constats de validation;
- les IDs de test si necessaires au nettoyage;
- jamais les mots de passe.

---

## 12) Verdict PASS minimal

La recette `J8` est consideree `PASS` si:

- le front public et l'API repondent;
- `operator` et `supervisor` se connectent;
- un client public et une intake publique peuvent etre crees;
- `operator` peut creer et cloturer une seance;
- le document derive est bloque avant validation supervision;
- `operator` ne peut pas valider la note;
- `supervisor` peut valider la note;
- le document devient ensuite visible dans le flux public `/suivi`;
- le mauvais `intake_request_id` reste bloque en `404`.

---

## 13) References

- [MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md)
- [MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md)
- [MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md)
