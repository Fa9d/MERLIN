# ============================================================
# SEED COMPLET - Environnement de test IVIA/MERLIN
# Parcours: Marie Tremblay (client) + Jean Beaumont (praticien)
# ============================================================

$BASE_URL = "http://localhost:8000"
$JEAN_ID = "7ca2b2cc-3295-4659-aa1a-cdaf7c5f9bcb"

function Write-Step($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Write-OK($msg) { Write-Host "OK: $msg" -ForegroundColor Green }
function Write-ERR($msg) { Write-Host "ERREUR: $msg" -ForegroundColor Red }
function Write-WARN($msg) { Write-Host "WARN: $msg" -ForegroundColor Yellow }

# ============================================================
# STEP 1 — Tokens
# ============================================================
Write-Step "LOGIN ADMIN + PRATICIEN"

$adminToken = (Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST `
    -Body (@{email="admin@ivia.quebec";password="AdminIVIA2026!"} | ConvertTo-Json) `
    -ContentType "application/json").access_token
Write-OK "Admin token obtenu"

$praticienLogin = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST `
    -Body (@{email="jean.beaumont@example.com";password="TestIVIA2026!"} | ConvertTo-Json) `
    -ContentType "application/json"
$praticienToken = $praticienLogin.access_token
$praticienUserId = $praticienLogin.user.id
Write-OK "Praticien token obtenu (user_id=$praticienUserId)"

$adminHeaders = @{"Authorization"="Bearer $adminToken"}
$praticienHeaders = @{"Authorization"="Bearer $praticienToken"}

# ============================================================
# STEP 2 — Creer profil client Marie Tremblay
# ============================================================
Write-Step "CREER CLIENT MARIE TREMBLAY"

$clientBody = @{
    first_name_or_alias = "Marie"
    last_name = "Tremblay"
    email = "marie.tremblay@example.com"
    phone = "514 555 0001"
    language_code = "fr-CA"
    timezone = "America/Toronto"
    territory_code = "QC"
    is_adult_confirmed = $true
} | ConvertTo-Json

try {
    $marie = Invoke-RestMethod -Uri "$BASE_URL/api/v1/clients" -Method POST `
        -Body $clientBody -ContentType "application/json" -Headers $praticienHeaders
    $marieId = $marie.id
    $mariePCC = $marie.public_client_code
    Write-OK "Marie Tremblay: id=$marieId, code=$mariePCC"
} catch {
    Write-WARN "Tentative de recuperer Marie existante..."
    $clients = Invoke-RestMethod -Uri "$BASE_URL/api/v1/clients" -Method GET -Headers $praticienHeaders
    $marie = $clients | Where-Object { $_.email -eq "marie.tremblay@example.com" } | Select-Object -First 1
    if ($marie) {
        $marieId = $marie.id
        $mariePCC = $marie.public_client_code
        Write-OK "Marie existante trouvee: id=$marieId, code=$mariePCC"
    } else {
        Write-ERR "Impossible de trouver Marie Tremblay"
        exit 1
    }
}

# ============================================================
# STEP 3 — Creer une intake request pour Marie
# ============================================================
Write-Step "CREER INTAKE REQUEST"

$intakeBody = @{
    client_id = $marieId
    first_name_or_alias = "Marie"
    email = "marie.tremblay@example.com"
    is_adult_confirmed = $true
    primary_need_code = "support"
    perceived_urgency_code = "non_urgent"
    requested_outcome_text = "Je traverse une periode difficile au travail et je cherche un espace pour en parler et retrouver mon equilibre."
    entry_summary_text = "Pression professionnelle, fatigue emotionnelle, besoin d'ecoute"
    consent_terms_accepted = $true
} | ConvertTo-Json

try {
    $intake = Invoke-RestMethod -Uri "$BASE_URL/api/v1/intake-requests" -Method POST `
        -Body $intakeBody -ContentType "application/json" -Headers $praticienHeaders
    $intakeId = $intake.id
    Write-OK "Intake cree: id=$intakeId"
} catch {
    Write-WARN "Erreur intake: $_ — on continue sans intake_request_id"
    $intakeId = $null
}

# ============================================================
# STEP 4 — Creer une session
# ============================================================
Write-Step "CREER SESSION (seance d'ecoute)"

$sessionBody = @{
    client_id = $marieId
    praticien_id = $praticienUserId
    session_mode_code = "intake"
    session_channel_code = "audio_live"
    scheduled_start_at = (Get-Date).ToUniversalTime().AddHours(-2).ToString("yyyy-MM-ddTHH:mm:ssZ")
    session_status_code = "scheduled"
    data_sensitivity_class = "high"
    retention_class = "standard"
} | ConvertTo-Json
if ($intakeId) {
    $sessionBody = @{
        client_id = $marieId
        intake_request_id = $intakeId
        praticien_id = $praticienUserId
        session_mode_code = "intake"
        session_channel_code = "audio_live"
        scheduled_start_at = (Get-Date).ToUniversalTime().AddHours(-2).ToString("yyyy-MM-ddTHH:mm:ssZ")
        session_status_code = "scheduled"
        data_sensitivity_class = "high"
        retention_class = "standard"
    } | ConvertTo-Json
}

try {
    $session = Invoke-RestMethod -Uri "$BASE_URL/api/v1/sessions" -Method POST `
        -Body $sessionBody -ContentType "application/json" -Headers $praticienHeaders
    $sessionId = $session.id
    Write-OK "Session creee: id=$sessionId"
} catch {
    Write-ERR "Echec creation session: $_"
    exit 1
}

# ============================================================
# STEP 5 — Demarrer la session
# ============================================================
Write-Step "DEMARRER LA SESSION"

try {
    $startBody = @{
        actual_start_at = (Get-Date).ToUniversalTime().AddHours(-2).ToString("yyyy-MM-ddTHH:mm:ssZ")
    } | ConvertTo-Json
    $sessionStarted = Invoke-RestMethod -Uri "$BASE_URL/api/v1/sessions/$sessionId/start" -Method POST `
        -Body $startBody -ContentType "application/json" -Headers $praticienHeaders
    Write-OK "Session demarree (status=$($sessionStarted.session_status_code))"
} catch {
    Write-WARN "Route /start: $_ — on continue"
}

# ============================================================
# STEP 6 — Ajouter des notes de seance
# ============================================================
Write-Step "AJOUTER NOTES DE SEANCE"

$noteBody = @{
    session_id = $sessionId
    client_id = $marieId
    note_sequence_number = 1
    summary_text = "Seance d'ecoute initiale avec Marie Tremblay. Contexte professionnel charge."
    observations_text = "Marie exprime une fatigue profonde liee a une surcharge de travail depuis plusieurs mois. Elle mentionne des difficultes a demarrer le matin et une perte de plaisir dans les activites habituelles."
    immediate_context_text = "Projet termine la semaine derniere avec beaucoup de pression. Maintenant Marie ressent un vide et une confusion sur ce qu'elle veut."
    coeur_summary_text = "Tristesse douce, sentiment d'etre incomprise par son equipe, nostalgie d'un travail plus creatif."
    corps_summary_text = "Tension dans les epaules, sommeil perturbe, appetit reduit."
    esprit_summary_text = "Questionnement sur l'orientation professionnelle, doute sur ses capacites de leadership."
    etre_summary_text = "Recherche d'un espace de validation et d'ecoute sans jugement."
    follow_up_actions_text = "1. Tenir un court journal de 3 lignes par soir pendant 7 jours. 2. Observer les moments ou l'energie remonte spontanement."
    next_session_focus_text = "Explorer les besoins fondamentaux non satisfaits dans le contexte professionnel."
    client_facing_summary_text = "Vous avez exprime avec beaucoup de clarte la fatigue accumulee et le besoin d'etre entendue. Votre lucidite sur votre etat est deja une ressource importante."
    vigilance_level_code = "non_urgent"
} | ConvertTo-Json -Depth 3

try {
    $note = Invoke-RestMethod -Uri "$BASE_URL/api/v1/session-notes" -Method POST `
        -Body $noteBody -ContentType "application/json" -Headers $praticienHeaders
    $noteId = $note.id
    Write-OK "Note creee: id=$noteId"
} catch {
    Write-ERR "Echec creation note: $_"
    $noteId = $null
}

# ============================================================
# STEP 7 — Cloturer la session
# ============================================================
Write-Step "CLOTURER LA SESSION"

$closeBody = @{
    actual_start_at = (Get-Date).ToUniversalTime().AddHours(-2).ToString("yyyy-MM-ddTHH:mm:ssZ")
    actual_end_at = (Get-Date).ToUniversalTime().AddMinutes(-30).ToString("yyyy-MM-ddTHH:mm:ssZ")
    session_status_code = "completed"
    presenting_topic_text = "Fatigue professionnelle et besoin de retrouver un sens au quotidien."
    session_highlights_text = "Marie a pu nommer clairement ses emotions. Bonne ouverture au suivi. Proposition du journal de soir bien accueillie."
    operator_assessment_text = "Marie presente un episode de burnout modere sans ideation. Suivi regulier recommande. Pas d'orientation vers des ressources exterieures necessaire pour l'instant."
} | ConvertTo-Json -Depth 3

try {
    $closed = Invoke-RestMethod -Uri "$BASE_URL/api/v1/sessions/$sessionId/close" -Method POST `
        -Body $closeBody -ContentType "application/json" -Headers $praticienHeaders
    Write-OK "Session cloturee (status=$($closed.session_status_code))"
} catch {
    Write-WARN "Erreur cloture: $_ — tentative PATCH..."
    try {
        $patchBody = @{session_status_code = "completed"} | ConvertTo-Json
        $patched = Invoke-RestMethod -Uri "$BASE_URL/api/v1/sessions/$sessionId" -Method PATCH `
            -Body $patchBody -ContentType "application/json" -Headers $praticienHeaders
        Write-OK "Session mise a jour via PATCH"
    } catch {
        Write-WARN "PATCH echoue aussi: $_"
    }
}

# ============================================================
# STEP 8 — Creer un document derive (compte rendu)
# ============================================================
Write-Step "CREER DOCUMENT DERIVE (compte rendu)"

if ($noteId) {
    $docDate = (Get-Date).ToString("dd-MM-yyyy")
    $docBodyText = "Seance d ecoute - Marie Tremblay`nDate: $docDate`nPraticien: Jean Beaumont`n`nCe que vous avez apporte:`nVous avez partage la fatigue accumulee au cours des derniers mois. Vous avez nomme un sentiment de vide, une perte de plaisir et des difficultes a retrouver votre rythme.`n`nCe qui a ete entendu:`nVotre fatigue est reelle et legitime. La confusion que vous ressentez est souvent le signe d une transition interieure en cours.`n`nPour la semaine:`nTenez un court journal de 3 lignes le soir pendant 7 jours : un moment ou vous avez eu de l energie, un moment ou vous en avez manque, et une pensee du jour.`n`n---`nCe document vous appartient. Il est genere a partir des notes de seance avec votre consentement."

    $docBody = @{
        client_id = $marieId
        session_id = $sessionId
        source_note_id = $noteId
        document_kind_code = "session_summary"
        audience_code = "client"
        title = "Compte rendu - Seance du $docDate"
        body_text = $docBodyText
        client_visible = $true
        data_sensitivity_class = "high"
        retention_class = "standard"
    } | ConvertTo-Json -Depth 3

    try {
        $doc = Invoke-RestMethod -Uri "$BASE_URL/api/v1/derived-documents" -Method POST `
            -Body $docBody -ContentType "application/json" -Headers $praticienHeaders
        $docId = $doc.id
        Write-OK "Document derive cree: id=$docId"
    } catch {
        Write-ERR "Echec creation document: $_"
    }
} else {
    Write-WARN "Pas de noteId — document derive non cree"
}

# ============================================================
# RECAP
# ============================================================
Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Magenta
Write-Host "RECAP DU SEEDING" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Magenta
Write-Host "  Admin:          admin@ivia.quebec / AdminIVIA2026!" -ForegroundColor White
Write-Host "  Praticien:      jean.beaumont@example.com / TestIVIA2026!" -ForegroundColor White
Write-Host "  Client:         marie.tremblay@example.com / TestIVIA2026!" -ForegroundColor White
Write-Host "  Client ID:      $marieId" -ForegroundColor White
Write-Host "  Client Code:    $mariePCC" -ForegroundColor White
if ($intakeId) { Write-Host "  Intake ID:      $intakeId" -ForegroundColor White }
Write-Host "  Session ID:     $sessionId" -ForegroundColor White
if ($noteId) { Write-Host "  Note ID:        $noteId" -ForegroundColor White }
if ($docId) { Write-Host "  Document ID:    $docId" -ForegroundColor White }
Write-Host ""
Write-Host "TEST URLs:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000/acces-client" -ForegroundColor White
Write-Host "  http://localhost:3000/mon-espace" -ForegroundColor White
Write-Host "  http://localhost:3000/espace-praticien" -ForegroundColor White
Write-Host "  http://localhost:3000/suivi?code=$($mariePCC)" -ForegroundColor White
