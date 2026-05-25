# Explorer les schemas cles: PublicIntakeStartIn et SessionCreate
$resp = Invoke-RestMethod -Uri "http://localhost:8000/openapi.json" -Method GET

Write-Host "=== PublicIntakeStartIn ===" -ForegroundColor Cyan
$resp.components.schemas.PublicIntakeStartIn | ConvertTo-Json -Depth 8

Write-Host "`n=== PublicIntakeStartOut ===" -ForegroundColor Yellow
$resp.components.schemas.PublicIntakeStartOut | ConvertTo-Json -Depth 8

Write-Host "`n=== SessionCreate ===" -ForegroundColor Cyan
$resp.components.schemas.SessionCreate | ConvertTo-Json -Depth 8

Write-Host "`n=== SessionNoteCreate ===" -ForegroundColor Yellow
$resp.components.schemas.SessionNoteCreate | ConvertTo-Json -Depth 6

Write-Host "`n=== SessionClose ===" -ForegroundColor Cyan
$resp.components.schemas.SessionClose | ConvertTo-Json -Depth 6

Write-Host "`n=== DerivedDocumentCreate ===" -ForegroundColor Yellow
$resp.components.schemas.DerivedDocumentCreate | ConvertTo-Json -Depth 6

Write-Host "`n=== Routes Sessions ===" -ForegroundColor Cyan
$resp.paths.PSObject.Properties.Name | Where-Object { $_ -match '/sessions' } | ForEach-Object { Write-Host $_ }
