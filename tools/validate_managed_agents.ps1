$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

python tools/validate_managed_agents.py
exit $LASTEXITCODE
