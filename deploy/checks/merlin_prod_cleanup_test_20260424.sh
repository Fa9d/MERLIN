#!/usr/bin/env bash
# MERLIN - Nettoyage objets de test prod 2026-04-24
# Source: MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md
# Usage: executer depuis le VPS en tant que ubuntu dans /opt/merlin
#   bash /home/ubuntu/merlin_prod_cleanup_test_20260424.sh
# Prerequis: docker compose prod en cours d'execution
# Ce script supprime uniquement les objets de test identifies au 2026-04-24.
# Les comptes utilisateurs de test (admin + operator) sont gardes en commentaire
# pour decision manuelle explicite avant suppression.

set -euo pipefail

echo "=== MERLIN - Nettoyage test prod 2026-04-24 ==="
echo ""
echo "Objets cibles:"
echo "  derived_document : 79b658aa-9437-4872-8c36-9bca6e44df07"
echo "  session_note     : 27519427-7a47-4dcf-8b22-d888500b89db"
echo "  session          : 1afa4673-5b6f-4bbd-b9db-c93544997a4e"
echo "  intake_request   : 7b00fa4a-76f0-48d2-a2c7-b09307d1554b"
echo "  consents         : lies au client 2742062b-877c-4f32-ab8a-8f85f67c3306"
echo "  client           : 2742062b-877c-4f32-ab8a-8f85f67c3306"
echo ""
echo "Comptes utilisateurs NON supprimes automatiquement (decision manuelle requise):"
echo "  admin_user    : 97f51dc7-df05-4655-a383-77c6295dec9c (davidphaneuf+test-merlin-20260424@gmail.com)"
echo "  operator_user : 5c65e043-b6ef-49d3-a533-38f8300235f1 (davidphaneuf+test-merlin-operator-20260424-1@gmail.com)"
echo ""

read -r -p "Confirmer la suppression des objets de test ci-dessus ? [oui/NON] " CONFIRM
if [[ "$CONFIRM" != "oui" ]]; then
  echo "Annulation. Aucun objet supprime."
  exit 0
fi

echo ""
echo "Execution du nettoyage..."

docker exec -i merlin-db-1 psql -U merlin -d merlin_v1 <<'SQL'
BEGIN;

-- 1. Document derive
DELETE FROM derived_documents
WHERE id = '79b658aa-9437-4872-8c36-9bca6e44df07';

-- 2. Note de seance
DELETE FROM session_notes
WHERE id = '27519427-7a47-4dcf-8b22-d888500b89db';

-- 3. Seance
DELETE FROM sessions
WHERE id = '1afa4673-5b6f-4bbd-b9db-c93544997a4e';

-- 4. Demande d'entree
DELETE FROM intake_requests
WHERE id = '7b00fa4a-76f0-48d2-a2c7-b09307d1554b';

-- 5. Consentements du client
DELETE FROM consents
WHERE client_id = '2742062b-877c-4f32-ab8a-8f85f67c3306';

-- 6. Client
DELETE FROM clients
WHERE id = '2742062b-877c-4f32-ab8a-8f85f67c3306';

COMMIT;
SQL

echo ""
echo "Nettoyage termine."
echo ""
echo "Verification post-nettoyage:"
docker exec -i merlin-db-1 psql -U merlin -d merlin_v1 <<'SQL'
SELECT 'derived_documents' AS table_name, COUNT(*) AS lignes_restantes FROM derived_documents WHERE id = '79b658aa-9437-4872-8c36-9bca6e44df07'
UNION ALL
SELECT 'session_notes', COUNT(*) FROM session_notes WHERE id = '27519427-7a47-4dcf-8b22-d888500b89db'
UNION ALL
SELECT 'sessions', COUNT(*) FROM sessions WHERE id = '1afa4673-5b6f-4bbd-b9db-c93544997a4e'
UNION ALL
SELECT 'intake_requests', COUNT(*) FROM intake_requests WHERE id = '7b00fa4a-76f0-48d2-a2c7-b09307d1554b'
UNION ALL
SELECT 'clients', COUNT(*) FROM clients WHERE id = '2742062b-877c-4f32-ab8a-8f85f67c3306';
SQL

echo ""
echo "Attendu: 0 pour chaque ligne."
echo "Si non-zero, verifier les contraintes de cle etrangere manuellement."
echo ""
echo "Comptes utilisateurs a supprimer manuellement si souhaite:"
echo "  DELETE FROM app_users WHERE id = '97f51dc7-df05-4655-a383-77c6295dec9c';"
echo "  DELETE FROM app_users WHERE id = '5c65e043-b6ef-49d3-a533-38f8300235f1';"
