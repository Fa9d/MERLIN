#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-https://api.ivia.quebec/api/v1}"
APP_BASE_URL="${APP_BASE_URL:-https://ivia.quebec}"
PROD_DIR="${PROD_DIR:-/opt/merlin}"
OPERATOR_EMAIL="${OPERATOR_EMAIL:-davidphaneuf+test-merlin-operator-2-20260426@gmail.com}"
ENV_FILE="${ENV_FILE:-/tmp/merlin_audio_validation_last.env}"

CLIENT_ID=""
CLIENT_CODE=""
INTAKE_ID=""
SESSION_ID=""
AUDIO_SESSION_ID=""
AUDIO_RECORDING_ID=""

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Commande requise absente: $1" >&2
    exit 1
  }
}

json_get() {
  local path="$1"
  python3 -c "import json,sys; path=sys.argv[1].split('.'); data=json.load(sys.stdin); value=data
for part in path:
    value = value[int(part)] if isinstance(value, list) else value[part]
print('' if value is None else json.dumps(value, ensure_ascii=True) if isinstance(value, (dict, list)) else value)" "$path"
}

json_url() {
  local role="$1"
  local payload="$2"
  python3 -c "import json,sys; from urllib.parse import urlencode
base=sys.argv[1]
role=sys.argv[2]
payload=json.load(sys.stdin)
params=urlencode({'wsUrl': payload['ws_url'], 'token': payload['token'], 'roomName': payload['room_name'], 'identity': payload['participant_identity'], 'role': role})
print(f'{base}/audio-test?{params}')" "$APP_BASE_URL" "$role" <<<"$payload"
}

save_env() {
  cat >"$ENV_FILE" <<EOF
CLIENT_ID=${CLIENT_ID}
CLIENT_CODE=${CLIENT_CODE}
INTAKE_ID=${INTAKE_ID}
SESSION_ID=${SESSION_ID}
AUDIO_SESSION_ID=${AUDIO_SESSION_ID}
AUDIO_RECORDING_ID=${AUDIO_RECORDING_ID}
EOF
}

cleanup_test_objects() {
  if [[ -z "$CLIENT_ID" ]]; then
    return 0
  fi

  docker exec -i merlin-db-1 psql -U merlin -d merlin_v1 <<SQL
BEGIN;
DELETE FROM audio_recordings WHERE audio_session_id = '${AUDIO_SESSION_ID}';
DELETE FROM audio_sessions WHERE id = '${AUDIO_SESSION_ID}';
DELETE FROM derived_documents WHERE session_id = '${SESSION_ID}';
DELETE FROM session_notes WHERE session_id = '${SESSION_ID}';
DELETE FROM sessions WHERE id = '${SESSION_ID}';
DELETE FROM intake_requests WHERE id = '${INTAKE_ID}';
DELETE FROM consents WHERE client_id = '${CLIENT_ID}';
DELETE FROM clients WHERE id = '${CLIENT_ID}';
COMMIT;
SQL
}

on_error() {
  echo
  echo "Echec durant la validation audio." >&2
  echo "Variables de travail sauvegardees dans $ENV_FILE" >&2
}

trap on_error ERR

require_cmd curl
require_cmd python3
require_cmd docker

cd "$PROD_DIR"
docker compose --env-file .env.prod -f docker-compose.prod.yml ps >/dev/null

echo "Validation audio prod MERLIN"
echo "API: $API_BASE_URL"
echo "Operateur: $OPERATOR_EMAIL"
echo

read -rsp "Nouveau mot de passe temporaire operateur: " OPERATOR_PASSWORD
echo

docker exec \
  -e OPERATOR_EMAIL="$OPERATOR_EMAIL" \
  -e OPERATOR_PASSWORD="$OPERATOR_PASSWORD" \
  merlin-api-1 sh -lc "python -c \"import os; from app.core.security import hash_password; from app.db.session import SessionLocal; from app.models.app_user import AppUser; db=SessionLocal(); user=db.query(AppUser).filter(AppUser.email == os.environ['OPERATOR_EMAIL']).first(); assert user is not None, 'Compte operateur introuvable: %s' % os.environ['OPERATOR_EMAIL']; user.password_hash = hash_password(os.environ['OPERATOR_PASSWORD']); db.commit(); print(user.email); db.close()\""

LOGIN_JSON=$(curl -s -X POST "$API_BASE_URL/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$OPERATOR_EMAIL\",\"password\":\"$OPERATOR_PASSWORD\"}")
OPERATOR_TOKEN=$(printf '%s' "$LOGIN_JSON" | json_get access_token)

TEST_TS=$(date +%Y%m%d%H%M%S)
CLIENT_JSON=$(curl -s -X POST "$API_BASE_URL/clients" \
  -H 'Content-Type: application/json' \
  -d "{\"first_name_or_alias\":\"TEST-AUDIO-$TEST_TS\",\"email\":\"merlin-audio-$TEST_TS@example.com\",\"is_adult_confirmed\":true}")
CLIENT_ID=$(printf '%s' "$CLIENT_JSON" | json_get id)
CLIENT_CODE=$(printf '%s' "$CLIENT_JSON" | json_get public_client_code)
save_env

INTAKE_JSON=$(curl -s -X POST "$API_BASE_URL/intake-requests" \
  -H 'Content-Type: application/json' \
  -d "{\"client_id\":\"$CLIENT_ID\",\"request_channel_code\":\"web_form\",\"request_for_code\":\"self\",\"primary_need_code\":\"clarification\",\"perceived_urgency_code\":\"non_urgent\",\"support_already_in_place\":false,\"requested_outcome_text\":\"Validation audio production.\",\"entry_summary_text\":\"TEST AUDIO PROD.\"}")
INTAKE_ID=$(printf '%s' "$INTAKE_JSON" | json_get id)
save_env

SESSION_JSON=$(curl -s -X POST "$API_BASE_URL/sessions" \
  -H "Authorization: Bearer $OPERATOR_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"client_id\":\"$CLIENT_ID\",\"intake_request_id\":\"$INTAKE_ID\",\"session_mode_code\":\"follow_up\",\"session_channel_code\":\"phone\",\"session_status_code\":\"scheduled\"}")
SESSION_ID=$(printf '%s' "$SESSION_JSON" | json_get id)
save_env

curl -s -X POST "$API_BASE_URL/sessions/$SESSION_ID/start" \
  -H "Authorization: Bearer $OPERATOR_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"actual_start_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >/dev/null

AUDIO_SESSION_JSON=$(curl -s -X POST "$API_BASE_URL/audio-sessions/sessions/$SESSION_ID/provision" \
  -H "Authorization: Bearer $OPERATOR_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"practitioner_participant_identity":"operator-browser-test"}')
AUDIO_SESSION_ID=$(printf '%s' "$AUDIO_SESSION_JSON" | json_get id)
save_env

OPERATOR_JOIN_JSON=$(curl -s -X POST "$API_BASE_URL/audio-sessions/$AUDIO_SESSION_ID/operator-join" \
  -H "Authorization: Bearer $OPERATOR_TOKEN")
CLIENT_JOIN_JSON=$(curl -s -X POST "$API_BASE_URL/audio-sessions/$AUDIO_SESSION_ID/client-join" \
  -H "Authorization: Bearer $OPERATOR_TOKEN")

OPERATOR_TEST_URL=$(json_url operator "$OPERATOR_JOIN_JSON")
CLIENT_TEST_URL=$(json_url client "$CLIENT_JOIN_JSON")

echo
echo "Objets crees"
printf 'CLIENT_ID=%s\nINTAKE_ID=%s\nSESSION_ID=%s\nAUDIO_SESSION_ID=%s\n' \
  "$CLIENT_ID" "$INTAKE_ID" "$SESSION_ID" "$AUDIO_SESSION_ID"
echo
echo "URL navigateur operateur"
echo "$OPERATOR_TEST_URL"
echo
echo "URL navigateur client"
echo "$CLIENT_TEST_URL"
echo
echo "1. Ouvrir chaque URL dans un navigateur distinct."
echo "2. Autoriser le micro."
echo "3. Cliquer sur 'Rejoindre la salle' dans les deux pages."
echo
read -r -p "Quand les deux participants sont connectes et peuvent parler, appuyer sur Entree pour lancer l'enregistrement..." _

RECORDING_START_JSON=$(curl -s -X POST "$API_BASE_URL/audio-recordings/audio-sessions/$AUDIO_SESSION_ID/start" \
  -H "Authorization: Bearer $OPERATOR_TOKEN")
AUDIO_RECORDING_ID=$(printf '%s' "$RECORDING_START_JSON" | json_get id)
save_env

START_STATUS=$(printf '%s' "$RECORDING_START_JSON" | json_get audio_recording_status_code)
START_FAILURE_REASON=$(printf '%s' "$RECORDING_START_JSON" | python3 -c "import json,sys; print((json.load(sys.stdin).get('failure_reason') or ''))")

echo
echo "Demarrage enregistrement"
echo "$RECORDING_START_JSON"

if [[ "$START_STATUS" == "recording" ]]; then
  read -r -p "Parlez 5 a 10 secondes, puis appuyer sur Entree pour arreter l'enregistrement..." _

  RECORDING_STOP_JSON=$(curl -s -X POST "$API_BASE_URL/audio-recordings/$AUDIO_RECORDING_ID/stop" \
    -H "Authorization: Bearer $OPERATOR_TOKEN")
  echo
  echo "Arret enregistrement"
  echo "$RECORDING_STOP_JSON"

  OUTPUT_LOCATION=$(printf '%s' "$RECORDING_STOP_JSON" | json_get output_location || true)
  if [[ -n "$OUTPUT_LOCATION" && "$OUTPUT_LOCATION" == /* ]]; then
    echo
    echo "Verification fichier en conteneur api"
    docker exec merlin-api-1 sh -lc "ls -lh '$OUTPUT_LOCATION'"
  fi
else
  echo
  echo "L'enregistrement n'est pas passe en statut 'recording'." >&2
  if [[ -n "$START_FAILURE_REASON" ]]; then
    echo "failure_reason=$START_FAILURE_REASON" >&2
  fi
fi

echo
echo "Etat BDD audio"
docker exec merlin-db-1 psql -U merlin -d merlin_v1 -c "select s.id as session_id, s.session_status_code, a.id as audio_session_id, a.audio_session_status_code, a.room_name, r.id as audio_recording_id, r.audio_recording_status_code, r.output_location, r.failure_reason from sessions s left join audio_sessions a on a.session_id = s.id left join audio_recordings r on r.audio_session_id = a.id where s.id = '$SESSION_ID' order by r.created_at desc nulls last;"

echo
echo "Variables sauvegardees dans $ENV_FILE"
read -r -p "Nettoyer maintenant les objets de test audio crees par ce script ? [y/N] " CLEANUP_REPLY
if [[ "$CLEANUP_REPLY" =~ ^[Yy]$ ]]; then
  cleanup_test_objects
  echo "Nettoyage termine."
else
  echo "Nettoyage saute. Utiliser $ENV_FILE pour supprimer les objets plus tard."
fi
