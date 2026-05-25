# Script complet de seeding - comptes de test + donnees IVIA/MERLIN

$BASE_URL = "http://localhost:8000"

# ============================================================
# STEP 1 - Login admin
# ============================================================
Write-Host "`n=== LOGIN ADMIN ===" -ForegroundColor Cyan
$loginResp = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST -Body '{"email":"admin@ivia.quebec","password":"AdminIVIA2026!"}' -ContentType "application/json"
$adminToken = $loginResp.access_token
$adminHeaders = @{"Authorization"="Bearer $adminToken"}
Write-Host "OK - admin_tech (id=$($loginResp.user.id))" -ForegroundColor Green

# ============================================================
# STEP 2 - Login praticien Jean Beaumont
# ============================================================
Write-Host "`n=== LOGIN PRATICIEN ===" -ForegroundColor Cyan
$praticienResp = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST -Body '{"email":"jean.beaumont@example.com","password":"TestIVIA2026!"}' -ContentType "application/json"
$praticienToken = $praticienResp.access_token
$praticienId = $praticienResp.user.id
$praticienHeaders = @{"Authorization"="Bearer $praticienToken"}
Write-Host "OK - operator Jean Beaumont (id=$praticienId)" -ForegroundColor Green

# ============================================================
# STEP 3 - Creer client Marie Tremblay (inscription publique)
# ============================================================
Write-Host "`n=== CREER CLIENT MARIE TREMBLAY ===" -ForegroundColor Cyan
$clientBody = @{
    email = "marie.tremblay@example.com"
    password = "TestIVIA2026!"
    display_name = "Marie Tremblay"
} | ConvertTo-Json

try {
    $clientResp = Invoke-RestMethod -Uri "$BASE_URL/api/v1/register/client" -Method POST -Body $clientBody -ContentType "application/json"
    Write-Host "Client cree: $($clientResp | ConvertTo-Json -Depth 4)" -ForegroundColor Green
    $clientCode = $clientResp.public_code
    Write-Host "public_code: $clientCode" -ForegroundColor Yellow
} catch {
    Write-Host "ERREUR ou deja existant: $_" -ForegroundColor Yellow
    # Tenter de login
    try {
        $clientLogin = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST -Body '{"email":"marie.tremblay@example.com","password":"TestIVIA2026!"}' -ContentType "application/json"
        Write-Host "Client login OK: $($clientLogin | ConvertTo-Json -Depth 3)" -ForegroundColor Green
    } catch {
        Write-Host "Echec login client: $_" -ForegroundColor Red
    }
}

# ============================================================
# STEP 4 - Verifier le profil praticien
# ============================================================
Write-Host "`n=== PROFIL PRATICIEN ===" -ForegroundColor Cyan
try {
    $profil = Invoke-RestMethod -Uri "$BASE_URL/api/v1/operators/me" -Method GET -Headers $praticienHeaders
    Write-Host $($profil | ConvertTo-Json -Depth 4) -ForegroundColor White
} catch {
    Write-Host "Route /operators/me: $_" -ForegroundColor Yellow
    # Essayer d'autres routes
    try {
        $profil2 = Invoke-RestMethod -Uri "$BASE_URL/api/v1/practitioners/me" -Method GET -Headers $praticienHeaders
        Write-Host $($profil2 | ConvertTo-Json -Depth 4) -ForegroundColor White
    } catch {
        Write-Host "Route /practitioners/me: $_" -ForegroundColor Yellow
    }
}

# ============================================================
# STEP 5 - Lister les clients (vue praticien)
# ============================================================
Write-Host "`n=== LISTE CLIENTS (vue praticien) ===" -ForegroundColor Cyan
try {
    $clients = Invoke-RestMethod -Uri "$BASE_URL/api/v1/clients" -Method GET -Headers $praticienHeaders
    Write-Host "Clients: $($clients | ConvertTo-Json -Depth 3)" -ForegroundColor White
} catch {
    Write-Host "Erreur: $_" -ForegroundColor Yellow
}

Write-Host "`n=== SEEDING TERMINE ===" -ForegroundColor Green
