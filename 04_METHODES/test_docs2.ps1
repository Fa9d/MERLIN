# Test direct de la route docs publics
$url = "http://localhost:8000/api/v1/derived-documents/public/client/CLI-68E7023A24?intake_request_id=0198a43e-1bc6-434f-bcb2-ffaa0da86c11"
$resp = Invoke-WebRequest -Uri $url -Method GET
Write-Host "Status: $($resp.StatusCode)"
Write-Host "Body: $($resp.Content)"
