# Explorer les schemas et routes pour les sessions/intakes
$resp = Invoke-RestMethod -Uri "http://localhost:8000/openapi.json" -Method GET

# Lister les schemas disponibles
Write-Host "=== SCHEMAS ===" -ForegroundColor Cyan
$resp.components.schemas.PSObject.Properties.Name | Sort-Object | ForEach-Object { Write-Host $_ }

Write-Host "`n=== ROUTES PUBLIC INTAKE ===" -ForegroundColor Cyan
$route = $resp.paths.'/api/v1/public/intake/start'.post
$route | ConvertTo-Json -Depth 8

Write-Host "`n=== CLIENTS/ME ===" -ForegroundColor Cyan  
$clientsMe = $resp.paths.'/api/v1/clients/me'.get
$clientsMe | ConvertTo-Json -Depth 6

Write-Host "`n=== INTAKE-REQUESTS ===" -ForegroundColor Cyan
$intakeReq = $resp.paths.'/api/v1/intake-requests'.post
$intakeReq | ConvertTo-Json -Depth 8
