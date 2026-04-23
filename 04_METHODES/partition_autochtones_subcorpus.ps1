$ErrorActionPreference = "Stop"

$root = "C:\MERLIN\05_PREUVES_SOURCES\CORPUS\AUTOCHTONES"

$buckets = @(
  "EPISTEMOLOGIES_METHODES",
  "COSMOLOGIES_SPIRITUALITES",
  "TRAITES_SOUVERAINETE_WAMPUM",
  "LANGUES_TRANSMISSION",
  "HISTOIRE_COLONIALE_RUPTURES",
  "NATIONS_QC_ET_TERRITOIRES",
  "COMPARATIF_CIRCOMPOLAIRE_ET_AUTOCHTONE",
  "PEDAGOGIE_NOTES_PISTES"
)

foreach ($bucket in $buckets) {
  New-Item -ItemType Directory -Force -Path (Join-Path $root $bucket) | Out-Null
}

$duplicateDeletes = @(
  "AUTO__anon__native-american-testimony-alt__1999.txt",
  "AUTO__anon__visions-heart-indigenous-peoples-canada__nd.txt"
)

$deleted = New-Object System.Collections.Generic.List[Object]
foreach ($name in $duplicateDeletes) {
  $path = Join-Path $root $name
  if (Test-Path -LiteralPath $path) {
    Remove-Item -LiteralPath $path -Force
    $deleted.Add([PSCustomObject]@{
      file = $name
      action = "deleted_duplicate"
    }) | Out-Null
  }
}

$rules = @{
  "EPISTEMOLOGIES_METHODES" = @(
    "AUTO__cajete__native-science-interdependence__1999.txt",
    "AUTO__kovach__indigenous-methodologies__nd.txt",
    "AUTO__simpson-leanne__as-we-have-always-done__2017.txt",
    "AUTO__sioui__autohistoire-amerindiens__1989.txt",
    "AUTO__anon__aboriginal-history-reader__nd.txt",
    "AUTO__anon__cultures-native-north-americans__2000.txt",
    "AUTO__anon__indigenous-intellectuals-sovereignty-citizenship__nd.txt",
    "AUTO__anon__indigenous-peoples-canada-concise-history__nd.txt",
    "AUTO__anon__traditional-knowledge-canada__nd.txt",
    "AUTO__anon__remember-who-you-are__nd.txt",
    "AUTO__courchene__anishinaabeg-medicine-wheel-leadership__nd.txt"
  )
  "COSMOLOGIES_SPIRITUALITES" = @(
    "2026-01-18__la-spiritualite-des-indiens-d-amerique-la-voie-du-c-ur__pdf.pdf",
    "AUTO__anon__aboriginal-spirituality-unit-plan__nd.txt",
    "AUTO__anon__adisokan-religion__nd.txt",
    "AUTO__anon__american-indian-religious-traditions__nd.txt",
    "AUTO__anon__american-indians-spirit-world__nd.txt",
    "AUTO__anon__animaux-totems__nd.txt",
    "AUTO__anon__bear-ceremonialism-northern-hemisphere__1926.txt",
    "AUTO__anon__cosmogonia-indios-canada__nd.txt",
    "AUTO__anon__cultural-significance-traditional-foods__nd.txt",
    "AUTO__anon__deetkatoo-stories-little-people__nd.txt",
    "AUTO__anon__heritage-spirituel-amerindien-grand-mystere__nd.txt",
    "AUTO__anon__inuit-mythology__nd.txt",
    "AUTO__anon__native-american-culture__nd.txt",
    "AUTO__anon__native-american-myths__nd.txt",
    "AUTO__anon__native-american-religions__nd.txt",
    "AUTO__anon__origin-of-things__nd.txt",
    "AUTO__anon__origins-of-things__nd.txt",
    "AUTO__anon__saami-shaman-drum__1991.txt",
    "AUTO__anon__seven-fires-prophecy__nd.txt",
    "AUTO__anon__sexualite-amerindienne-inuit__nd.txt",
    "AUTO__anon__spiritualite-indiens-amerique__nd.txt",
    "AUTO__anon__traditional-plant-foods-indigenous-canada__nd.txt",
    "AUTO__black-elk-brown__sacred-pipe-seven-rites-oglala__nd.txt",
    "AUTO__blueotter__earth-mother-crying__nd.txt",
    "AUTO__brightman__grateful-prey-rock-cree__nd.txt",
    "AUTO__hill-susan__clay-we-are-made-of-haudenosaunee__2017.txt",
    "AUTO__leland__algonquin-legends__nd.txt",
    "AUTO__moore__dream-shall-have-name__2013.txt",
    "AUTO__neihardt__black-elk-speaks__1932.txt",
    "AUTO__wall-arden__wisdomkeepers-spiritual-elders__1990.txt"
  )
  "TRAITES_SOUVERAINETE_WAMPUM" = @(
    "AUTO__anon__holding-hands-with-wampum__nd.txt",
    "AUTO__anon__naskapi-law-lake-st-john-mistassini__nd.pdf",
    "AUTO__doxtator__tyendinaga-land-surrenders__nd.txt",
    "AUTO__hill-rick__fort-niagara-treaty-1764__nd.txt",
    "AUTO__lelievre__unsettling-mobility-mikmaw-sovereignty__nd.txt",
    "AUTO__rcap__kaswentha-royal-commission__nd.txt"
  )
  "LANGUES_TRANSMISSION" = @(
    "AUTO__anon__anishinaabe-language-workbook__nd.txt",
    "AUTO__anon__grammatical-studies-narragansett-language__nd.txt",
    "AUTO__anon__ha-shmla-dictionary__nd.txt",
    "AUTO__anon__innu-particles-thesis-oxford__2007.txt",
    "AUTO__anon__ojibwe-beginner-dictionary__nd.txt",
    "AUTO__anon__ojibwe-english-words-everyday-life__nd.txt",
    "AUTO__batchelor__ainu-english-japanese-dictionary__nd.txt",
    "AUTO__bugaeva__ainu-language-book-launch__2023.txt",
    "AUTO__lang__making-wawa-chinook-jargon__nd.txt",
    "AUTO__scott__phonological-sketch-mushuau-innu__2000.txt",
    "AUTO__swann__algonquian-spirit-native-literatures-americas__nd.txt",
    "AUTO__valentine__nishnaabemwin-reference-grammar__2001.txt"
  )
  "HISTOIRE_COLONIALE_RUPTURES" = @(
    "AUTO__alison__race-gender-colonialism__nd.txt",
    "AUTO__anon__esclavage-amerindiens__nd.txt",
    "AUTO__anon__expansion-et-metis__nd.txt",
    "AUTO__anon__formes-assimilation-chronologie__nd.txt",
    "AUTO__anon__indigenous-people-today__nd.txt",
    "AUTO__anon__native-americans-and-public__nd.txt",
    "AUTO__anon__residential-schools-report-english__nd.txt",
    "AUTO__anon__tensions-oka-kanesatake-xixe__2004.txt",
    "AUTO__anon__traduire-rupture-colonialite__nd.txt",
    "AUTO__fontaine__nauetakuan-silence-pour-bruit__2016.txt",
    "AUTO__miller__shingwauks-vision-residential-schools__1996.txt"
  )
  "NATIONS_QC_ET_TERRITOIRES" = @(
    "AUTO__anon__algonquin-history-ottawa-river__nd.txt",
    "AUTO__anon__algonquin-wolf-lake-eagle-village__nd.txt",
    "AUTO__anon__american-indian-tribes__nd.txt",
    "AUTO__anon__haudenosaunee-note__nd.txt",
    "AUTO__anon__hochelagans-and-mohawks__nd.txt",
    "AUTO__anon__innu__nd.txt",
    "AUTO__anon__native-nations-perspective__nd.txt",
    "AUTO__anon__toponymie-algonquins__nd.txt",
    "AUTO__anon__toponymie-cris__nd.txt",
    "AUTO__dorais__canadian-inuit__nd.txt",
    "AUTO__hawkes__labrador-eskimo__1916.txt",
    "AUTO__jean-michel__tiohtia-ke__nd.txt",
    "AUTO__jeanson__they-had-names-north-american-indigenous__nd.txt",
    "AUTO__leland__algonquin-legends-new-england__1884.txt",
    "AUTO__lighthall__hochelagan-burying-ground-westmount__1898.txt",
    "AUTO__pilling__bibliography-algonquian-languages__1891.txt",
    "AUTO__schoolcraft__archives-aboriginal-knowledge__nd.txt",
    "AUTO__speck__beothuk-and-micmac__1922.txt"
  )
  "COMPARATIF_CIRCOMPOLAIRE_ET_AUTOCHTONE" = @(
    "AUTO__anon__divining-ecology-sami-shamanism__nd.txt",
    "AUTO__anon__early-ethnography-american-arctic__nd.txt",
    "AUTO__bogoras__chukchee-mythology__nd.txt"
  )
  "PEDAGOGIE_NOTES_PISTES" = @(
    "AUTO__anon__haudenosaunee-note__nd.txt",
    "AUTO__anon__handbook-of-indians__nd.txt",
    "AUTO__nabokov__native-american-testimony__1999.txt",
    "AUTO__anon__visions-heart-indigenous-peoples-canada-5th__nd.txt",
    "AUTO__seattle__chief-seattle-speech__nd.txt",
    "AUTO__van-heerden__animal-totems__nd.txt"
  )
}

$assigned = @{}
$moves = New-Object System.Collections.Generic.List[Object]

foreach ($bucket in $rules.Keys) {
  foreach ($name in $rules[$bucket]) {
    $assigned[$name] = $bucket
  }
}

$files = Get-ChildItem -LiteralPath $root -File
foreach ($file in $files) {
  if (-not $assigned.ContainsKey($file.Name)) {
    throw "Fichier non mappe: $($file.Name)"
  }

  $bucket = $assigned[$file.Name]
  $destination = Join-Path (Join-Path $root $bucket) $file.Name
  Move-Item -LiteralPath $file.FullName -Destination $destination -Force

  $moves.Add([PSCustomObject]@{
    file = $file.Name
    category = $bucket
  }) | Out-Null
}

$remainingAtRoot = Get-ChildItem -LiteralPath $root -File

[PSCustomObject]@{
  deleted_duplicates = $deleted.Count
  moved = $moves.Count
  remaining_at_root = $remainingAtRoot.Count
} | Format-List

$moves | Group-Object category | Sort-Object Name | ForEach-Object {
  [PSCustomObject]@{
    category = $_.Name
    files = $_.Count
  }
} | Format-Table -AutoSize
