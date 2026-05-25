# Test docs publics
$url = "http://localhost:8000/api/v1/derived-documents/public/client/CLI-68E7023A24?intake_request_id=0198a43e-1bc6-434f-bcb2-ffaa0da86c11"
try {
    $docs = Invoke-RestMethod -Uri $url -Method GET
    $docs | ConvertTo-Json -Depth 4
} catch {
    Write-Host "ERREUR: $_"
    docker logs merlin-backend-1 --tail 10
}
