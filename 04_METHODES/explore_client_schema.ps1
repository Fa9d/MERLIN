# Verifier le schema ClientCreate et la route POST /api/v1/clients
$resp = Invoke-RestMethod -Uri "http://localhost:8000/openapi.json" -Method GET
Write-Host "=== ClientCreate ===" -ForegroundColor Cyan
$resp.components.schemas.ClientCreate | ConvertTo-Json -Depth 8
Write-Host "`n=== POST /api/v1/clients ===" -ForegroundColor Yellow
$resp.paths.'/api/v1/clients'.post | ConvertTo-Json -Depth 6
