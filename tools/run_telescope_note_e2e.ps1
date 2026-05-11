param(
    [string]$Fixture = "managed_agents/evals/fixtures/merlin_note_e2e_fake_cases.json"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

python tools/run_telescope_note_e2e.py --fixture $Fixture
exit $LASTEXITCODE
