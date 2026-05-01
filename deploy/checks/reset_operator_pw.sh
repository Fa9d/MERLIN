#!/bin/bash
set -e
EMAIL="davidphaneuf+test-merlin-operator-20260424c@gmail.com"
docker cp /home/ubuntu/gen_hash.py merlin-api-1:/tmp/gen_hash.py
HASH=$(docker exec merlin-api-1 python3 /tmp/gen_hash.py)
echo "Hash: $HASH"
docker exec merlin-db-1 psql -U merlin -d merlin_v1 -c "UPDATE app_users SET password_hash = '$HASH' WHERE email = '$EMAIL';"
docker exec merlin-db-1 psql -U merlin -d merlin_v1 -c "SELECT email, role FROM app_users WHERE email = '$EMAIL';"
echo "Done."
