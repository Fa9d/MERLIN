param(
    [string]$RepoRoot = "C:\MERLIN",
    [string]$MirrorPath = "C:\MERLIN_BACKUPS\git\MERLIN.git",
    [string]$BackupSourcePath = "C:\MERLIN_BACKUPS\payloads",
    [string]$ExternalDrivePath = ""
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $RepoRoot)) {
    throw "RepoRoot introuvable: $RepoRoot"
}

$mirrorParent = Split-Path -Parent $MirrorPath
if (-not (Test-Path $mirrorParent)) {
    New-Item -ItemType Directory -Path $mirrorParent -Force | Out-Null
}

if (-not (Test-Path $MirrorPath)) {
    git clone --mirror $RepoRoot $MirrorPath
} else {
    git --git-dir=$MirrorPath remote update --prune
}

if ($ExternalDrivePath -ne "") {
    if (-not (Test-Path $ExternalDrivePath)) {
        throw "ExternalDrivePath introuvable: $ExternalDrivePath"
    }

    $externalGitDir = Join-Path $ExternalDrivePath "MERLIN_BACKUP\git"
    $externalPayloadDir = Join-Path $ExternalDrivePath "MERLIN_BACKUP\payloads"

    New-Item -ItemType Directory -Path $externalGitDir -Force | Out-Null
    robocopy (Split-Path -Parent $MirrorPath) $externalGitDir (Split-Path -Leaf $MirrorPath) /MIR /R:1 /W:1 | Out-Null

    if (Test-Path $BackupSourcePath) {
        New-Item -ItemType Directory -Path $externalPayloadDir -Force | Out-Null
        robocopy $BackupSourcePath $externalPayloadDir /E /R:1 /W:1 | Out-Null
    }
}

Write-Host "git-mirror-ok mirror=$MirrorPath"
