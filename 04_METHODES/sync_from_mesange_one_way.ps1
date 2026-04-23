param(
  [string]$SourceRoot = "C:\MÉSANGE",
  [string]$DestinationRoot = "C:\MERLIN"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $SourceRoot)) { throw "SourceRoot introuvable: $SourceRoot" }
if (!(Test-Path $DestinationRoot)) { throw "DestinationRoot introuvable: $DestinationRoot" }

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$runRoot = Join-Path $DestinationRoot ("06_IMPORTS_MESANGE\" + $timestamp)
$manifestPath = Join-Path $runRoot "manifest.csv"

New-Item -ItemType Directory -Force -Path $runRoot | Out-Null

$exactFiles = @(
  "MESANGE_MASTER_PLAN.md",
  "MESANGE_ORGANIGRAMME.md",
  "MÉSANGE.code-workspace"
)

$recursiveFolders = @(
  "00_PIVOT",
  "01_ROMAN\\CANON",
  "01_ROMAN\\00_INDEX",
  "01_ROMAN\\METHODO",
  "NOTES"
)

$copied = New-Object System.Collections.Generic.List[Object]

function Copy-IfExists {
  param([string]$src, [string]$dst)
  if (Test-Path $src) {
    New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
    Copy-Item $src $dst -Force
    $item = Get-Item $dst
    $copied.Add([PSCustomObject]@{
      source = $src
      destination = $dst
      length = $item.Length
      lastWriteTime = $item.LastWriteTime.ToString("s")
    }) | Out-Null
  }
}

foreach ($f in $exactFiles) {
  $src = Join-Path $SourceRoot $f
  $dst = Join-Path $runRoot $f
  Copy-IfExists -src $src -dst $dst
}

foreach ($folder in $recursiveFolders) {
  $srcFolder = Join-Path $SourceRoot $folder
  if (Test-Path $srcFolder) {
    Get-ChildItem -Path $srcFolder -Recurse -File -Include *.md,*.txt,*.csv,*.code-workspace | ForEach-Object {
      $relative = $_.FullName.Substring($SourceRoot.Length).TrimStart('\\')
      $dst = Join-Path $runRoot $relative
      Copy-IfExists -src $_.FullName -dst $dst
    }
  }
}

$copied | Export-Csv -Path $manifestPath -NoTypeInformation -Encoding UTF8

$summary = [PSCustomObject]@{
  run = $timestamp
  sourceRoot = $SourceRoot
  destinationRoot = $runRoot
  filesCopied = $copied.Count
  manifest = $manifestPath
}

$summary | Format-List
