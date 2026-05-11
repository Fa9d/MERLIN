param(
    [string]$Fixture = "managed_agents/evals/fixtures/telescope_minimal_fake_run.json"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

python tools/run_telescope_minimal.py --fixture $Fixture
exit $LASTEXITCODE
