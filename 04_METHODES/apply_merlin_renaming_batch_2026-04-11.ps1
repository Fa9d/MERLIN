$ErrorActionPreference = 'Stop'

$root = 'C:\MERLIN'
$src = Join-Path $root '06_IMPORTS_MESANGE\2026-04-11'

$map = @(
    @{ Old='MERLIN_01_PHILOSOPHIE_CERCLE_ET_DEMARRAGE_EMPLOI_CV.md'; New='01_FONDEMENTS\MERLIN_FOND_CHARTE_PHILOSOPHIE_CERCLE_EMPLOI_v1.0.md' }
    @{ Old='MERLIN_02_CONCEPTS_REALITES_AUTOCHTONES_ET_SPIRITUALITES.md'; New='02_NATIONS_QC\MERLIN_NATQ_CADRE_CONCEPTS_REALITES_SPIRITUALITES_v1.0.md' }
    @{ Old='MERLIN_03_METHODE_11_NATIONS_QUEBEC_ET_INTERNATIONALISATION.md'; New='04_METHODES\MERLIN_METH_CADRE_METHODE_11_NATIONS_QC_INTL_v1.0.md' }
    @{ Old='MERLIN_04_PROTOCOLE_REFERENCEMENT_11_NATIONS_QUEBEC.md'; New='04_METHODES\MERLIN_METH_PLAYBOOK_PROTOCOLE_REFERENCEMENT_11_NATIONS_v1.0.md' }
    @{ Old='MERLIN_05_CADRE_FONDATEUR_11_NATIONS_ET_DEMOCRATIE_DU_VIVANT.md'; New='01_FONDEMENTS\MERLIN_FOND_CADRE_11_NATIONS_DEMOCRATIE_DU_VIVANT_v1.0.md' }
    @{ Old='MERLIN_06_FICHE_CADRE_11_NATIONS_QUEBEC.md'; New='02_NATIONS_QC\MERLIN_NATQ_FICHE_CADRE_11_NATIONS_QUEBEC_v1.0.md' }
    @{ Old='MERLIN_07_FICHE_NATION_KANIENKEHAKA_MOHAWKS.md'; New='02_NATIONS_QC\MERLIN_NATQ_FICHE_KANIENKEHAKA_v1.0.md' }
    @{ Old='MERLIN_PROMPT_2_FULL_AUGMENTED_MEMORY_LAYER.md'; New='04_METHODES\MERLIN_METH_SPEC_PROMPT_2_AUGMENTED_MEMORY_LAYER_v1.0.md' }
    @{ Old='MERLIN_PROMPT_2_LITE_MEMORY_LAYER.md'; New='04_METHODES\MERLIN_METH_SPEC_PROMPT_2_LITE_MEMORY_LAYER_v1.0.md' }
)

foreach ($item in $map) {
    $from = Join-Path $src $item.Old
    $to = Join-Path $root $item.New
    $toDir = Split-Path $to -Parent

    if (-not (Test-Path $from)) {
        Write-Warning "Source missing: $from"
        continue
    }

    if (-not (Test-Path $toDir)) {
        New-Item -ItemType Directory -Path $toDir -Force | Out-Null
    }

    if (Test-Path $to) {
        Write-Warning "Target exists, skipped: $to"
        continue
    }

    Copy-Item -Path $from -Destination $to
    Write-Host "COPIED: $($item.Old) -> $($item.New)"
}
