# Test e2e IVIA/MERLIN — v2  (répétable sans reset manuel)
# Usage: Set-Location C:\MERLIN\10_backend_merlin_api ; .\test_e2e.ps1
#
# Pré-requis :
#   - merlin-backend-1  UP  (port 8000)
#   - merlin-postgres-1 UP  (port 5432)
#   - Next.js           UP  (port 3000, optionnel)
#   - slot 609fc6d7 doit être 'available' (géré automatiquement via cancel)
#
$ErrorActionPreference = "Continue"
$BASE = "http://localhost:8000/api/v1"
$PASS = 0; $FAIL = 0
# Email unique par run — évite les collisions sur soumissions répétées
$RUN_ID = (Get-Date -Format "yyyyMMddHHmmss")
$BOT_EMAIL = "testbot_e2e_$RUN_ID@example.com"
$KNOWN_SLOT_ID = "609fc6d7-8002-4bcf-84c2-d033d8e4fdd8"
$AELIS_ID = "2c72a544-e324-45ec-bbf0-9d158b44953a"

function Pass($label) {
    Write-Host "  [PASS] $label" -ForegroundColor Green
    $script:PASS++
}
function Fail($label, $detail) {
    Write-Host "  [FAIL] $label : $detail" -ForegroundColor Red
    $script:FAIL++
}
function Info($msg) {
    Write-Host "        $msg" -ForegroundColor DarkGray
}

function Api($method, $path, $body, $token) {
    $uri = "$BASE$path"
    $headers = @{ "Content-Type" = "application/json" }
    if ($token) { $headers["Authorization"] = "Bearer $token" }
    try {
        if ($body) {
            $json = $body | ConvertTo-Json -Depth 10
            $resp = Invoke-RestMethod -Method $method -Uri $uri -Headers $headers -Body $json -ErrorAction Stop
        } else {
            $resp = Invoke-RestMethod -Method $method -Uri $uri -Headers $headers -ErrorAction Stop
        }
        return $resp
    } catch {
        return $null
    }
}

function Login($email, $pwd) {
    try {
        $body = "{`"email`":`"$email`",`"password`":`"$pwd`"}"
        $headers = @{ "Content-Type" = "application/json" }
        $resp = Invoke-RestMethod -Method POST -Uri "$BASE/auth/login" -Headers $headers -Body $body -ErrorAction Stop
        return $resp.access_token
    } catch { return $null }
}

Write-Host "`n=== 1. LOGINS ===" -ForegroundColor Cyan

$adminTok = Login "admin@ivia.quebec" "AdminIVIA2026!"
if ($adminTok) { Pass "Login admin" } else { Fail "Login admin" "null token" }

$aelisTok = Login "pilote.aelis@ivia.quebec" "IVIA2026!"
if ($aelisTok) { Pass "Login praticien Aelis" } else { Fail "Login praticien Aelis" "null token" }

$naelTok = Login "pilote.nael@ivia.quebec" "IVIA2026!"
if ($naelTok) { Pass "Login praticien Nael" } else { Fail "Login praticien Nael" "null token" }

$opTok = Login "jean.beaumont@example.com" "IVIA2026!"
if ($opTok) { Pass "Login operateur" } else { Fail "Login operateur" "null token" }

$marieTok = Login "marie.tremblay@example.com" "TestIVIA2026!"
if ($marieTok) { Pass "Login client Marie" } else { Fail "Login client Marie" "null token" }

Write-Host "`n=== 2. PROFILS ===" -ForegroundColor Cyan

$me = Api GET "/auth/me" $null $adminTok
if ($me.role -eq "admin_tech") { Pass "Profil admin role=admin_tech" } else { Fail "Profil admin" $me }

$meAelis = Api GET "/auth/me" $null $aelisTok
if ($meAelis.role -eq "practitioner") { Pass "Profil Aelis role=practitioner" } else { Fail "Profil Aelis" $meAelis }

$meMarie = Api GET "/auth/me" $null $marieTok
if ($meMarie.role -eq "public_client") { Pass "Profil Marie role=public_client" } else { Fail "Profil Marie" $meMarie }

Write-Host "`n=== 3. INTAKE PUBLIC ===" -ForegroundColor Cyan

# Email unique par run (déjà défini en haut : $BOT_EMAIL)
Info "Email run : $BOT_EMAIL"
$intakeBody = @{
    first_name_or_alias = "TestBot_$RUN_ID"
    email = $BOT_EMAIL
    is_adult_confirmed = $true
    consent_terms_accepted = $true
    primary_need_code = "support"
    perceived_urgency_code = "non_urgent"
    support_already_in_place = $false
    requested_outcome_text = "Test e2e automatique run=$RUN_ID"
}
$intake = Api POST "/public/intake/start" $intakeBody $null
if ($intake.intake_request_id) {
    Pass "Intake public soumis (id=$($intake.intake_request_id))"
} else {
    Fail "Intake public" ($intake | ConvertTo-Json)
}

Write-Host "`n=== 4. SLOTS ===" -ForegroundColor Cyan

$today = Get-Date -Format "yyyy-MM-dd"
$in14 = (Get-Date).AddDays(14).ToString("yyyy-MM-dd")

$slotsAll = Api GET "/schedules/available?praticien_id=$AELIS_ID&date_from=$today&date_to=$in14" $null $marieTok
if ($slotsAll -and $slotsAll.Count -gt 0) {
    Pass "Liste slots available ($($slotsAll.Count) total)"
} else {
    Fail "Liste slots available" "0 slots ou erreur"
}

$slotsUrl = "/schedules/available?praticien_id=$AELIS_ID&date_from=$today&date_to=$in14"
$slots = Api GET $slotsUrl $null $marieTok
if ($slots -and $slots.Count -gt 0) {
    $script:SLOT_ID = $slots[0].id
    Pass "Slots publics Aelis ($($slots.Count) dispo, first=$($script:SLOT_ID))"
} else {
    $script:SLOT_ID = $null
    Fail "Slots publics Aelis" "0 slots"
}

Write-Host "`n=== 5. HOLD + CONFIRM ===" -ForegroundColor Cyan

# Slot seeded pré-connu — répétable car cancel est fait en section 9
Info "Slot cible : $KNOWN_SLOT_ID"
$holdBody = @{ slot_id = $KNOWN_SLOT_ID }
$hold = Api POST "/bookings/hold" $holdBody $marieTok
if ($hold.id -or $hold.slot_id) {
    Pass "Hold slot ($KNOWN_SLOT_ID)"
    $script:BOOKING_SLOT_ID = $KNOWN_SLOT_ID
} else {
    Fail "Hold slot" ($hold | ConvertTo-Json -Compress)
    $script:BOOKING_SLOT_ID = $null
}

if ($script:BOOKING_SLOT_ID) {
    $confirmBody = @{ slot_id = $script:BOOKING_SLOT_ID }
    $confirm = Api POST "/bookings/confirm" $confirmBody $marieTok
    if ($confirm.status -eq "confirmed") {
        Pass "Confirm slot (status=confirmed)"
    } else {
        Fail "Confirm slot" ($confirm | ConvertTo-Json -Compress)
    }
}

Write-Host "`n=== 6. MES BOOKINGS ==" -ForegroundColor Cyan

$myBookings = Api GET "/bookings/my" $null $marieTok
if ($myBookings -ne $null) {
    Pass "Marie: mes bookings ($($myBookings.Count) total)"
} else {
    Fail "Mes bookings" "null"
}

Write-Host "`n=== 7. HEALTH ===" -ForegroundColor Cyan

$health = Invoke-RestMethod -Uri "http://localhost:8000/health" -ErrorAction SilentlyContinue
if ($health.status -eq "ok") { Pass "Health check" } else { Fail "Health check" ($health | ConvertTo-Json) }

Write-Host "`n=== 8. ADMIN INTAKES ===" -ForegroundColor Cyan

$intakes = Api GET "/intake-requests" $null $opTok
if ($intakes -ne $null) {
    Pass "Operateur: liste intakes ($($intakes.Count) intakes)"
} else {
    Fail "Operateur: liste intakes" "null"
}

Write-Host "`n=== 9. ENTITLEMENTS ==" -ForegroundColor Cyan

$ents = Api GET "/client-entitlements/me" $null $marieTok
if ($ents -ne $null) {
    Pass "Marie: mes entitlements ($($ents.Count) total)"
} else {
    $ents2 = Api GET "/client-entitlements" $null $opTok
    if ($ents2 -ne $null) { Pass "Operateur: client-entitlements ($($ents2.Count) total)" }
    else { Fail "Client-entitlements" "null" }
}

Write-Host "`n=== 10. TEARDOWN (cancel + reset slot) ==" -ForegroundColor Cyan

# Cancel le booking confirme pour que le test soit rejoutable sans reset manuel
if ($script:BOOKING_SLOT_ID) {
    $cancelBody = @{ slot_id = $script:BOOKING_SLOT_ID }
    $cancel = Api POST "/bookings/cancel" $cancelBody $marieTok
    if ($cancel.status -eq "available" -or $cancel.status -eq "cancelled") {
        Pass "Cancel booking (slot reset a disponible)"
    } else {
        # Fallback: cancel par l'operateur
        $cancel2 = Api POST "/bookings/cancel" $cancelBody $opTok
        if ($cancel2.status -eq "available" -or $cancel2.status -eq "cancelled") {
            Pass "Cancel booking via operateur"
        } else {
            Fail "Cancel booking" ($cancel | ConvertTo-Json -Compress)
            Info "ATTENTION: relancez ce script seulement apres un reset manuel du slot:"
            Info "  docker exec merlin-postgres-1 psql -U merlin -d merlin_v1 -c `"UPDATE booking_slots SET status='available', client_id=null, hold_expires_at=null, consumed_entitlement_id=null WHERE id='$KNOWN_SLOT_ID';`""
        }
    }
}

Write-Host "`n==============================" -ForegroundColor Cyan
Write-Host "  RESULTATS: $PASS PASS  /  $FAIL FAIL" -ForegroundColor White
if ($FAIL -eq 0) {
    Write-Host "  TOUT PASSE - systeme operationnel" -ForegroundColor Green
} else {
    Write-Host "  $FAIL test(s) en echec - voir details ci-dessus" -ForegroundColor Yellow
}
Write-Host "==============================`n" -ForegroundColor Cyan
