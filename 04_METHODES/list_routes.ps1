# Explorer routes sessions
$resp = Invoke-RestMethod -Uri "http://localhost:8000/openapi.json" -Method GET
$routes = $resp.paths.PSObject.Properties.Name
$routes | Where-Object { $_ -match "session" } | Sort-Object | ForEach-Object { Write-Host $_ }
