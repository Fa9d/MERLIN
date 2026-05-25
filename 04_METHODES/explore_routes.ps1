# Lister toutes les routes pour derived-documents, sessions, clients
$resp = Invoke-RestMethod -Uri "http://localhost:8000/openapi.json" -Method GET
$routes = $resp.paths.PSObject.Properties.Name
Write-Host "=== DERIVED DOCUMENTS ===" -ForegroundColor Cyan
$routes | Where-Object { $_ -match "derived" } | Sort-Object | ForEach-Object { Write-Host $_ }
Write-Host "`n=== CLIENTS ===" -ForegroundColor Yellow
$routes | Where-Object { $_ -match "clients" } | Sort-Object | ForEach-Object { Write-Host $_ }
Write-Host "`n=== INTAKE ===" -ForegroundColor Green
$routes | Where-Object { $_ -match "intake" } | Sort-Object | ForEach-Object { Write-Host $_ }
Write-Host "`n=== DerivedDocumentCreate schema ===" -ForegroundColor Cyan
$resp.components.schemas.DerivedDocumentCreate | ConvertTo-Json -Depth 8
Write-Host "`n=== SessionClose schema ===" -ForegroundColor Yellow
$resp.components.schemas.SessionClose | ConvertTo-Json -Depth 8
Write-Host "`n=== SessionStart schema ===" -ForegroundColor Green
$resp.components.schemas.SessionStart | ConvertTo-Json -Depth 8
