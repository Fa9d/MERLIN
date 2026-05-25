# Script de creation des comptes de test pour IVIA/MERLIN

$BASE_URL = "http://localhost:8000"

# 1. Login admin
Write-Host "=== STEP 1: Login admin ===" -ForegroundColor Cyan
$loginBody = '{"email":"admin@ivia.quebec","password":"AdminIVIA2026!"}'
try {
    $loginResp = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
    $adminToken = $loginResp.access_token
    Write-Host "Admin token: OK (length=$($adminToken.Length))" -ForegroundColor Green
} catch {
    Write-Host "ERREUR login admin: $_" -ForegroundColor Red
    exit 1
}

$headers = @{"Authorization"="Bearer $adminToken"}

# 2. Creer praticien Jean Beaumont
Write-Host "`n=== STEP 2: Creer praticien Jean Beaumont ===" -ForegroundColor Cyan
$praticienBody = @{
    email = "jean.beaumont@example.com"
    password = "TestIVIA2026!"
    role = "operator"
    display_name = "Jean Beaumont"
} | ConvertTo-Json
try {
    $praticienResp = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/register" -Method POST -Body $praticienBody -ContentType "application/json" -Headers $headers
    Write-Host "Praticien cree: $($praticienResp | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "ERREUR creation praticien: $_" -ForegroundColor Yellow
}

# 3. Verifier les utilisateurs en DB
Write-Host "`n=== STEP 3: Verifier les utilisateurs ===" -ForegroundColor Cyan
try {
    $usersResp = Invoke-RestMethod -Uri "$BASE_URL/api/v1/admin/users" -Method GET -Headers $headers
    $usersResp | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Route /admin/users indisponible: $_" -ForegroundColor Yellow
    Write-Host "Verification via login praticien..."
    try {
        $praticienLogin = Invoke-RestMethod -Uri "$BASE_URL/api/v1/auth/login" -Method POST -Body '{"email":"jean.beaumont@example.com","password":"TestIVIA2026!"}' -ContentType "application/json"
        Write-Host "Login praticien OK: $($praticienLogin | ConvertTo-Json -Depth 2)" -ForegroundColor Green
    } catch {
        Write-Host "ERREUR login praticien: $_" -ForegroundColor Red
    }
}
