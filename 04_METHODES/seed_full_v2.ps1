# SEED COMPLET - Environnement de test IVIA/MERLIN
# Parcours: Marie Tremblay (client) + Jean Beaumont (praticien)

$BASE_URL = "http://localhost:8000"

function Write-Step { param($m); Write-Host "`n=== $m ===" -ForegroundColor Cyan }
function Write-OK   { param($m); Write-Host "OK: $m" -ForegroundColor Green }
function Write-ERR  { param($m); Write-Host "ERREUR: $m" -ForegroundColor Red }
function Write-WARN { param($m); Write-Host "WARN: $m" -ForegroundColor Yellow }

# --- STEP 1: TOKENS ---
Write-Step "LOGIN ADMIN + PRATICIEN"

$adminBody = @{email="admin@ivia.quebec";password="AdminIVIA2026!"} | ConvertTo-Json
$adminToken = (Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST -Body $adminBody -ContentType "application/json").access_token
Write-OK "Admin token OK"

$praticienBody = @{email="jean.beaumont@example.com";password="TestIVIA2026!"} | ConvertTo-Json
$praticienLogin = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST -Body $praticienBody -ContentType "application/json"
$praticienToken = $praticienLogin.access_token
$praticienUserId = $praticienLogin.user.id
Write-OK "Praticien OK (user_id=$praticienUserId)"

$praticienHeaders = @{"Authorization"="Bearer $praticienToken"}

# --- STEP 2: CLIENT MARIE TREMBLAY ---
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
    $marie = Invoke-RestMethod -Uri "$BASE_URL/api/v1/clients" -Method POST -Body $clientBody -ContentType "application/json" -Headers $praticienHeaders
    $marieId = $marie.id
    $mariePCC = $marie.public_client_code
    Write-OK "Marie creee: id=$marieId, code=$mariePCC"
} catch {
    Write-WARN "Deja existant ou erreur - recherche Marie..."
    $allClients = Invoke-RestMethod -Uri "$BASE_URL/api/v1/clients" -Method GET -Headers $praticienHeaders
    $marie = $allClients | Where-Object { $_.email -eq "marie.tremblay@example.com" } | Select-Object -First 1
    if ($marie) {
        $marieId = $marie.id
        $mariePCC = $marie.public_client_code
        Write-OK "Marie trouvee: id=$marieId, code=$mariePCC"
    } else {
        Write-ERR "Impossible de trouver Marie"
        exit 1
    }
}

# --- STEP 3: INTAKE REQUEST ---
Write-Step "CREER INTAKE REQUEST"

$intakeBody = @{
    client_id = $marieId
    first_name_or_alias = "Marie"
    email = "marie.tremblay@example.com"
    is_adult_confirmed = $true
    primary_need_code = "support"
    perceived_urgency_code = "non_urgent"
    requested_outcome_text = "Je traverse une periode difficile au travail et je cherche un espace pour en parler."
    entry_summary_text = "Pression professionnelle, fatigue emotionnelle, besoin d ecoute"
    consent_terms_accepted = $true
} | ConvertTo-Json

$intakeId = $null
try {
    $intake = Invoke-RestMethod -Uri "$BASE_URL/api/v1/intake-requests" -Method POST -Body $intakeBody -ContentType "application/json" -Headers $praticienHeaders
    $intakeId = $intake.id
    Write-OK "Intake cree: id=$intakeId"
} catch {
    Write-WARN "Erreur intake - on continue sans intake_request_id"
}

# --- STEP 4: SESSION ---
Write-Step "CREER SESSION"

$startTime = (Get-Date).ToUniversalTime().AddHours(-2).ToString("yyyy-MM-ddTHH:mm:ssZ")

$sessionData = @{
    client_id = $marieId
    praticien_id = $praticienUserId
    session_mode_code = "intake"
    session_channel_code = "audio_live"
    scheduled_start_at = $startTime
    session_status_code = "scheduled"
    data_sensitivity_class = "high"
    retention_class = "standard"
}
if ($intakeId) { $sessionData.intake_request_id = $intakeId }
$sessionBody = $sessionData | ConvertTo-Json

try {
    $session = Invoke-RestMethod -Uri "$BASE_URL/api/v1/sessions" -Method POST -Body $sessionBody -ContentType "application/json" -Headers $praticienHeaders
    $sessionId = $session.id
    Write-OK "Session creee: id=$sessionId"
} catch {
    Write-ERR "Echec session: $_"
    exit 1
}

# --- STEP 5: START SESSION ---
Write-Step "DEMARRER SESSION"

try {
    $startBody = @{actual_start_at = $startTime} | ConvertTo-Json
    $started = Invoke-RestMethod -Uri "$BASE_URL/api/v1/sessions/$sessionId/start" -Method POST -Body $startBody -ContentType "application/json" -Headers $praticienHeaders
    Write-OK "Session demarree (status=$($started.session_status_code))"
} catch {
    Write-WARN "Route /start echouee - on continue"
}

# --- STEP 6: NOTE DE SEANCE ---
Write-Step "AJOUTER NOTE DE SEANCE"

$noteBody = @{
    session_id = $sessionId
    client_id = $marieId
    note_sequence_number = 1
    summary_text = "Seance d ecoute initiale avec Marie Tremblay. Contexte professionnel charge."
    observations_text = "Marie exprime une fatigue profonde liee a une surcharge de travail depuis plusieurs mois. Perte de plaisir dans les activites habituelles."
    immediate_context_text = "Projet termine la semaine derniere avec beaucoup de pression. Vide ressenti apres sa cloture."
    coeur_summary_text = "Tristesse douce, sentiment d etre incomprise par son equipe, nostalgie d un travail plus creatif."
    corps_summary_text = "Tension dans les epaules, sommeil perturbe, appetit reduit."
    esprit_summary_text = "Questionnement sur l orientation professionnelle, doute sur ses capacites de leadership."
    etre_summary_text = "Recherche d un espace de validation et d ecoute sans jugement."
    follow_up_actions_text = "1. Tenir un court journal de 3 lignes par soir pendant 7 jours. 2. Observer les moments ou l energie remonte spontanement."
    next_session_focus_text = "Explorer les besoins fondamentaux non satisfaits dans le contexte professionnel."
    client_facing_summary_text = "Vous avez exprime avec clarte la fatigue accumulee et le besoin d etre entendue. Votre lucidite sur votre etat est deja une ressource importante."
    vigilance_level_code = "non_urgent"
} | ConvertTo-Json -Depth 3

$noteId = $null
try {
    $note = Invoke-RestMethod -Uri "$BASE_URL/api/v1/session-notes" -Method POST -Body $noteBody -ContentType "application/json" -Headers $praticienHeaders
    $noteId = $note.id
    Write-OK "Note creee: id=$noteId"
} catch {
    Write-ERR "Echec note: $_"
}

# --- STEP 7: CLOTURER SESSION ---
Write-Step "CLOTURER SESSION"

$endTime = (Get-Date).ToUniversalTime().AddMinutes(-30).ToString("yyyy-MM-ddTHH:mm:ssZ")

$closeBody = @{
    actual_start_at = $startTime
    actual_end_at = $endTime
    session_status_code = "completed"
    presenting_topic_text = "Fatigue professionnelle et besoin de retrouver un sens au quotidien."
    session_highlights_text = "Marie a pu nommer clairement ses emotions. Bonne ouverture au suivi."
    operator_assessment_text = "Marie presente un episode de burnout modere sans ideation. Suivi regulier recommande."
} | ConvertTo-Json -Depth 3

try {
    $closed = Invoke-RestMethod -Uri "$BASE_URL/api/v1/sessions/$sessionId/close" -Method POST -Body $closeBody -ContentType "application/json" -Headers $praticienHeaders
    Write-OK "Session cloturee (status=$($closed.session_status_code))"
} catch {
    Write-WARN "Erreur cloture: $_"
}

# --- STEP 8: DOCUMENT DERIVE ---
Write-Step "CREER DOCUMENT DERIVE"

$docId = $null
if ($noteId) {
    $docDate = (Get-Date).ToString("dd-MM-yyyy")
    $docText = "Seance d ecoute - Marie Tremblay`nDate: $docDate | Praticien: Jean Beaumont`n`nCe que vous avez apporte: Vous avez partage la fatigue accumulee. Vous avez nomme un sentiment de vide, une perte de plaisir.`n`nCe qui a ete entendu: Votre fatigue est reelle et legitime.`n`nPour la semaine: Tenez un court journal de 3 lignes le soir pendant 7 jours.`n`n---`nCe document vous appartient et est genere avec votre consentement."

    $docBody = @{
        client_id = $marieId
        session_id = $sessionId
        source_note_id = $noteId
        document_kind_code = "session_summary"
        audience_code = "client"
        title = "Compte rendu - Seance du $docDate"
        body_text = $docText
        client_visible = $true
        data_sensitivity_class = "high"
        retention_class = "standard"
    } | ConvertTo-Json -Depth 3

    try {
        $doc = Invoke-RestMethod -Uri "$BASE_URL/api/v1/derived-documents" -Method POST -Body $docBody -ContentType "application/json" -Headers $praticienHeaders
        $docId = $doc.id
        Write-OK "Document cree: id=$docId"
    } catch {
        Write-ERR "Echec document: $_"
    }
} else {
    Write-WARN "Pas de noteId - document non cree"
}

# --- RECAP ---
$sep = "=" * 55
Write-Host "`n$sep" -ForegroundColor Magenta
Write-Host "RECAP DU SEEDING" -ForegroundColor Magenta
Write-Host $sep -ForegroundColor Magenta
Write-Host "  Admin:       admin@ivia.quebec / AdminIVIA2026!" -ForegroundColor White
Write-Host "  Praticien:   jean.beaumont@example.com / TestIVIA2026!" -ForegroundColor White
Write-Host "  Client:      marie.tremblay@example.com / TestIVIA2026!" -ForegroundColor White
Write-Host "  Client ID:   $marieId" -ForegroundColor White
Write-Host "  Client Code: $mariePCC" -ForegroundColor White
if ($intakeId) { Write-Host "  Intake ID:   $intakeId" -ForegroundColor White }
Write-Host "  Session ID:  $sessionId" -ForegroundColor White
if ($noteId) { Write-Host "  Note ID:     $noteId" -ForegroundColor White }
if ($docId)  { Write-Host "  Document ID: $docId" -ForegroundColor White }
Write-Host ""
Write-Host "TEST URLs:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000/acces-client"
Write-Host "  http://localhost:3000/mon-espace"
Write-Host "  http://localhost:3000/espace-praticien"
$suviUrl = "http://localhost:3000/suivi?code=" + $mariePCC
Write-Host "  $suviUrl"
Write-Host ""
