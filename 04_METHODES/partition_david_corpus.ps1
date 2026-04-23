param(
  [switch]$SkipSemanticPass
)

$ErrorActionPreference = "Stop"

$root = "C:\MERLIN"
$source = Join-Path $root "DAVID_CORPUS"
$targetRoot = Join-Path $root "05_PREUVES_SOURCES\CORPUS"

$map = @{
  "AUTO__"  = "AUTOCHTONES"
  "CONST__" = "CONSTITUTION_DROIT"
  "CULT__"  = "CULTURE_IDENTITE_QC"
  "GENE__"  = "GENEALOGIES_LIGNEES"
  "HIST__"  = "HISTOIRE_QC_CANADA"
  "METH__"  = "METHODES_CADRES"
  "PENS__"  = "PENSEE_THEORIE"
  "POLQ__"  = "POLITIQUE_QC_CANADA"
}

$fallback = "A_CLASSER"
$reviewRequired = "A_CLASSER\REVIEW_REQUIRED"

if (-not (Test-Path $source)) {
  throw "Source introuvable: $source"
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
foreach ($dir in ($map.Values + $fallback | Select-Object -Unique)) {
  New-Item -ItemType Directory -Force -Path (Join-Path $targetRoot $dir) | Out-Null
}
New-Item -ItemType Directory -Force -Path (Join-Path $targetRoot $reviewRequired) | Out-Null

$moved = New-Object System.Collections.Generic.List[Object]
$deleted = New-Object System.Collections.Generic.List[Object]
$review = New-Object System.Collections.Generic.List[Object]

$existing = Get-ChildItem -Recurse -File -LiteralPath $targetRoot
$existingByName = @{}
foreach ($file in $existing) {
  $existingByName[$file.Name] = $file.FullName
}

Get-ChildItem -LiteralPath $source -File | ForEach-Object {
  $name = $_.Name
  $bucket = $fallback

  foreach ($prefix in $map.Keys) {
    if ($name.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
      $bucket = $map[$prefix]
      break
    }
  }

  switch -Regex ($name) {
    '^Brunet-histoire-litte-canadienne-francaise\.txt$' { $bucket = "CULTURE_IDENTITE_QC"; break }
    '^Frechette-Louis-La-Noel-au-Canada\.txt$' { $bucket = "CULTURE_IDENTITE_QC"; break }
    '^2026-01-18__92resolutions__pdf\.pdf$' { $bucket = "CONSTITUTION_DROIT"; break }
    '^2026-01-18__act-d-union-1840__pdf\.pdf$' { $bucket = "CONSTITUTION_DROIT"; break }
    '^2026-01-18__l-evolution-du-canada-francais__pdf\.pdf$' { $bucket = "CULTURE_IDENTITE_QC"; break }
    '^2026-01-18__la-spiritualite-des-indiens-d-amerique-la-voie-du-c-ur__pdf\.pdf$' { $bucket = "AUTOCHTONES"; break }
    '^Frechette-originaux\.pdf$' { $bucket = "CULTURE_IDENTITE_QC"; break }
    '^LABELLE-Discours\.pdf$' { $bucket = "POLITIQUE_QC_CANADA"; break }
    '^Le Canadien 20 fevrier 1839\.pdf$' { $bucket = "HISTOIRE_QC_CANADA"; break }
  }

  if ($existingByName.ContainsKey($name)) {
    $existingPath = $existingByName[$name]
    $currentHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash
    $existingHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $existingPath).Hash

    if ($currentHash -eq $existingHash) {
      Remove-Item -LiteralPath $_.FullName -Force
      $deleted.Add([PSCustomObject]@{
        file = $name
        action = "deleted_duplicate"
        corpus = $existingPath
      }) | Out-Null
      return
    }

    $reviewDestination = Join-Path (Join-Path $targetRoot $reviewRequired) $name
    Move-Item -LiteralPath $_.FullName -Destination $reviewDestination -Force
    $review.Add([PSCustomObject]@{
      file = $name
      action = "review_required"
      destination = $reviewDestination
      corpus = $existingPath
    }) | Out-Null
    return
  }

  $destination = Join-Path (Join-Path $targetRoot $bucket) $name
  Move-Item -LiteralPath $_.FullName -Destination $destination -Force

  $moved.Add([PSCustomObject]@{
    file = $name
    category = $bucket
    destination = $destination
  }) | Out-Null
}

$remaining = Get-ChildItem -LiteralPath $source -File

[PSCustomObject]@{
  moved = $moved.Count
  deleted_duplicates = $deleted.Count
  review_required = $review.Count
  remaining = $remaining.Count
} | Format-List

$moved | Sort-Object category, file | Format-Table -AutoSize

if (-not $SkipSemanticPass) {
  $semanticScript = Join-Path $root "04_METHODES\reclasser_a_classer_semantic.ps1"
  $aClasserPath = Join-Path $targetRoot $fallback
  $reviewPath = Join-Path $targetRoot $reviewRequired
  $needsSemanticPass = @(
    Get-ChildItem -LiteralPath $aClasserPath -File | Where-Object { $_.DirectoryName -ne $reviewPath }
  ).Count -gt 0

  if ($needsSemanticPass -and (Test-Path $semanticScript)) {
    Write-Host ""
    Write-Host "Semantic pass on A_CLASSER..."
    & $semanticScript
  }
}
