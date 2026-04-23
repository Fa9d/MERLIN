$ErrorActionPreference = "Stop"

$root = "C:\MERLIN"
$targetRoot = Join-Path $root "05_PREUVES_SOURCES\CORPUS"
$aClasser = Join-Path $targetRoot "A_CLASSER"
$reviewRequired = Join-Path $aClasser "REVIEW_REQUIRED"

function Remove-Diacritics {
  param([string]$Text)

  if ([string]::IsNullOrWhiteSpace($Text)) {
    return ""
  }

  $normalized = $Text.Normalize([Text.NormalizationForm]::FormD)
  $builder = New-Object System.Text.StringBuilder

  foreach ($char in $normalized.ToCharArray()) {
    if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($char) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
      [void]$builder.Append($char)
    }
  }

  return $builder.ToString().Normalize([Text.NormalizationForm]::FormC)
}

function Convert-ToSlug {
  param([string]$Name)

  $baseName = [IO.Path]::GetFileNameWithoutExtension($Name)
  $slug = Remove-Diacritics $baseName
  $slug = $slug.ToLowerInvariant()
  $slug = $slug -replace '^\d+[-_ ]*', ''
  $slug = $slug -replace '\b(pdf|epub|scan|ocr|softcover|hardcover|edition|complete-work)\b', ' '
  $slug = $slug -replace '[^a-z0-9]+', '-'
  $slug = $slug.Trim('-')

  if ([string]::IsNullOrWhiteSpace($slug)) {
    return "document"
  }

  return $slug
}

function Get-TextSample {
  param([string]$Path)

  try {
    return Get-Content -LiteralPath $Path -TotalCount 120 -ErrorAction Stop | Out-String
  }
  catch {
    return ""
  }
}

function New-CanonicalName {
  param(
    [string]$OriginalName,
    [hashtable]$Rule
  )

  if ($Rule.ContainsKey("FileName")) {
    return $Rule["FileName"]
  }

  $extension = [IO.Path]::GetExtension($OriginalName).ToLowerInvariant()
  $prefix = $Rule["Prefix"]
  $author = $Rule["Author"]
  $year = $Rule["Year"]
  $slug = Convert-ToSlug $OriginalName

  return "{0}__{1}__{2}__{3}{4}" -f $prefix, $author, $slug, $year, $extension
}

function Get-ClassificationRule {
  param(
    [string]$FileName,
    [string]$Sample
  )

  $name = $FileName.ToLowerInvariant()
  $text = $Sample.ToLowerInvariant()

  $exactRules = @{
    "230637426-techqua-ikachi-newsletter.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__anon__techqua-ikachi-newsletter__nd.txt"
    }
    "2378258-archeological-expedition-to-arizona-in-1895seventeenth-annual-report-of-the-bureau-of-americanethnology-to-the-secretary-of-the-smithsonian-institutio.txt" = @{
      Destination = "AUTOCHTONES\ETHNOGRAPHIES_ARCHIVES"
      FileName = "AUTO__fewkes__archeological-expedition-arizona-1895__1895.txt"
    }
    "268722219-hopi-nation-book-2008.txt" = @{
      Destination = "AUTOCHTONES\NATIONS_AMERIQUES_TERRITOIRES"
      FileName = "AUTO__glenn-wunder-rollings-martin__hopi-nation-essays-art-culture-history-law__2008.txt"
    }
    "289341391-whorf.txt" = @{
      Destination = "AUTOCHTONES\LANGUES_TRANSMISSION"
      FileName = "AUTO__whorf__langage-pensee-realite-hopi__1969.txt"
    }
    "360003853-hopi-katsina-songs-pdf.txt" = @{
      Destination = "AUTOCHTONES\LANGUES_TRANSMISSION"
      FileName = "AUTO__sekaquaptewa__hopi-katsina-songs__nd.txt"
    }
    "360005399-hopi-katcinas-drawings-fewkes-pdf.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__fewkes__tusayan-katcinas-drawings__nd.txt"
    }
    "405391719-nursery-manual-for-native-plants-pdf.txt" = @{
      Destination = "AUTOCHTONES\EPISTEMOLOGIES_METHODES"
      FileName = "AUTO__dumroese-luna-landis__nursery-manual-native-plants-tribal-nurseries__2009.txt"
    }
    "474565525-tradiciones-hopi.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__fewkes__tusayan-katcinas__nd.txt"
    }
    "477681839-maasaw-profile-of-a-hopi-god.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__anon__maasaw-profile-hopi-god__nd.txt"
    }
    "514832253-voth-the-oraibi-summer-snake-ceremony.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__voth__oraibi-summer-snake-ceremony__nd.txt"
    }
    "52953420-native-american-folktales.txt" = @{
      Destination = "AUTOCHTONES\LANGUES_TRANSMISSION"
      FileName = "AUTO__green__native-american-folktales__2009.txt"
    }
    "567715469-hopi-earth-changes-prophecies-of-the-hopi.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__anon__hopi-earth-changes-prophecies__nd.txt"
    }
    "573795890-appendix-a-b-school-listing-profiles-508.txt" = @{
      Destination = "AUTOCHTONES\HISTOIRE_COLONIALE_RUPTURES"
      FileName = "AUTO__doi__federal-indian-boarding-schools-listing-profiles__nd.txt"
    }
    "680525661-chuckingit-com-techqua-ikachi-hopi-prophecies.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__anon__techqua-ikachi-hopi-prophecies__nd.txt"
    }
    "746425952-westerncolorado1011mcke.txt" = @{
      Destination = "AUTOCHTONES\ETHNOGRAPHIES_ARCHIVES"
      FileName = "AUTO__mckern__western-colorado-petroglyphs__nd.txt"
    }
    "798692796-secrets-of-mayan-science-religion-hunbatz-men-translated-by-diana-gubiseh-ayala-james-1990-softcover-autographed-2000-edition-santa-fe-new.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__hunbatz-men__secrets-mayan-science-religion__1990.txt"
    }
    "814242864-the-north-american-indians-a-selection-of-photographs-by-by-edward.txt" = @{
      Destination = "AUTOCHTONES\ETHNOGRAPHIES_ARCHIVES"
      FileName = "AUTO__curtis__north-american-indians-selection-photographs__nd.txt"
    }
    "884365896-unwritten-literature-of-the-hopi-by-hattie-greene-lockett.txt" = @{
      Destination = "AUTOCHTONES\LANGUES_TRANSMISSION"
      FileName = "AUTO__lockett__unwritten-literature-hopi__nd.txt"
    }
    "926126485-propheties-des-indiens-hopi.txt" = @{
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      FileName = "AUTO__anon__propheties-indiens-hopi__nd.txt"
    }
    "120876120-american-indian-ethnographic-art-skinner-auction-2536b.txt" = @{
      Destination = "AUTOCHTONES\ETHNOGRAPHIES_ARCHIVES"
      FileName = "AUTO__skinner__american-indian-ethnographic-art-auction-2636b__2013.txt"
    }
    "210747819-36194226-tribal-names-of-the-americas.txt" = @{
      Destination = "AUTOCHTONES\NATIONS_AMERIQUES_TERRITOIRES"
      FileName = "AUTO__clark__tribal-names-americas__2009.txt"
    }
    "118077178-love-is-the-way-to-ascend.txt" = @{
      Destination = "PENSEE_THEORIE"
      FileName = "PENS__namka__love-is-the-way-to-ascend__2011.txt"
    }
    "121375526-a-short-study-of-end-time-prophecies.txt" = @{
      Destination = "PENSEE_THEORIE"
      FileName = "PENS__anon__short-study-end-time-prophecies__2010.txt"
    }
    "307938176-drunvalo-melchizedek-spatiul-sacru-al-inimii.txt" = @{
      Destination = "PENSEE_THEORIE"
      FileName = "PENS__melchizedek__sacred-space-heart-ro__2005.txt"
    }
    "374446923-recuerdos-en-la-atlantida-de-itzen-caan.txt" = @{
      Destination = "PENSEE_THEORIE"
      FileName = "PENS__anon__recuerdos-atlantida-itzen-caan__nd.txt"
    }
    "386381023-37-1-31-july-2011-love-peace-and-harmony-journal.txt" = @{
      Destination = "PENSEE_THEORIE"
      FileName = "PENS__anon__love-peace-harmony-journal__2011.txt"
    }
    "509714969-el-ultimo-anasazi.txt" = @{
      Destination = "PENSEE_THEORIE"
      FileName = "PENS__alfaro__ultimo-anasazi__2015.txt"
    }
    "634182391-john-h-mcwhorter-the-language-hoax-why-the-world-looks-the-same-in-any-language-oxford-university-press-2014-pdf.txt" = @{
      Destination = "METHODES_CADRES"
      FileName = "METH__mcwhorter__language-hoax__2014.txt"
    }
    "779250149-drunvalo-melchizedek-zycie-w-przestrzeni-serca.txt" = @{
      Destination = "PENSEE_THEORIE"
      FileName = "PENS__melchizedek__sacred-space-heart-pl__nd.txt"
    }
    "962760722-the-shaman-s-path-michael-harner.txt" = @{
      Destination = "METHODES_CADRES"
      FileName = "METH__harner__shamans-path__1980.txt"
    }
  }

  if ($exactRules.ContainsKey($name)) {
    return $exactRules[$name]
  }

  $genericRules = @(
    @{
      Test = { ($name -match 'boarding-school|residential-school|school-listing') -or ($text -match 'boarding school|residential school') }
      Destination = "AUTOCHTONES\HISTOIRE_COLONIALE_RUPTURES"
      Prefix = "AUTO"
      Author = "anon"
      Year = "nd"
    },
    @{
      Test = { ($name -match 'whorf|language|grammar|song|songs|literature|folktale') -or ($text -match 'hopi creation of the world|native american folktales|hattie greene lockett|benjamin lee whorf') }
      Destination = "AUTOCHTONES\LANGUES_TRANSMISSION"
      Prefix = "AUTO"
      Author = "anon"
      Year = "nd"
    },
    @{
      Test = { ($name -match 'hopi|katsina|katcina|maasaw|massau|oraibi|prophec|techqua|snake-ceremony|snake') -or ($text -match 'thomas banyacya|dan katchongva|hopi prophecy|maasaw|massau') }
      Destination = "AUTOCHTONES\COSMOLOGIES_SPIRITUALITES"
      Prefix = "AUTO"
      Author = "anon"
      Year = "nd"
    },
    @{
      Test = { ($name -match 'petroglyph|photograph|ethnographic-art|auction|archeological|archaeological|fewkes|curtis') -or ($text -match 'bureau of american ethnology|edward s\. curtis|petroglyphs') }
      Destination = "AUTOCHTONES\ETHNOGRAPHIES_ARCHIVES"
      Prefix = "AUTO"
      Author = "anon"
      Year = "nd"
    },
    @{
      Test = { ($name -match 'tribal-names|nation-book|nation|territor') -or ($text -match 'tribal names of the americas|hopi nation: essays') }
      Destination = "AUTOCHTONES\NATIONS_AMERIQUES_TERRITOIRES"
      Prefix = "AUTO"
      Author = "anon"
      Year = "nd"
    },
    @{
      Test = { ($name -match 'nursery|tribal-nurser') -or ($text -match 'native plants: a guide for tribal nurseries') }
      Destination = "AUTOCHTONES\EPISTEMOLOGIES_METHODES"
      Prefix = "AUTO"
      Author = "anon"
      Year = "nd"
    },
    @{
      Test = { ($name -match 'harner|language-hoax') -or ($text -match 'michael harner|john h\. mcwhorter') }
      Destination = "METHODES_CADRES"
      Prefix = "METH"
      Author = "anon"
      Year = "nd"
    },
    @{
      Test = { ($name -match 'drunvalo|atlant|ascend|harmony-journal|anasazi|end-time') -or ($text -match 'drunvalo melchizedek|atlantida|love is the way to ascend|end time prophecies') }
      Destination = "PENSEE_THEORIE"
      Prefix = "PENS"
      Author = "anon"
      Year = "nd"
    }
  )

  foreach ($rule in $genericRules) {
    if (& $rule["Test"]) {
      return $rule
    }
  }

  return $null
}

if (-not (Test-Path $aClasser)) {
  throw "Dossier introuvable: $aClasser"
}

$bootstrapDirs = @(
  "AUTOCHTONES\ETHNOGRAPHIES_ARCHIVES",
  "AUTOCHTONES\NATIONS_AMERIQUES_TERRITOIRES"
)

foreach ($dir in $bootstrapDirs) {
  New-Item -ItemType Directory -Force -Path (Join-Path $targetRoot $dir) | Out-Null
}

New-Item -ItemType Directory -Force -Path $reviewRequired | Out-Null

$moved = New-Object System.Collections.Generic.List[Object]
$deleted = New-Object System.Collections.Generic.List[Object]
$review = New-Object System.Collections.Generic.List[Object]
$unmatched = New-Object System.Collections.Generic.List[Object]

$corpusFiles = Get-ChildItem -LiteralPath $targetRoot -File -Recurse | Where-Object {
  $_.FullName -notlike "$aClasser\*" -and $_.FullName -notlike "$reviewRequired\*"
}

$hashIndex = @{}
foreach ($file in $corpusFiles) {
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash
  if (-not $hashIndex.ContainsKey($hash)) {
    $hashIndex[$hash] = New-Object System.Collections.Generic.List[string]
  }
  $hashIndex[$hash].Add($file.FullName) | Out-Null
}

$incoming = Get-ChildItem -LiteralPath $aClasser -File

foreach ($file in $incoming) {
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash

  if ($hashIndex.ContainsKey($hash)) {
    Remove-Item -LiteralPath $file.FullName -Force
    $deleted.Add([PSCustomObject]@{
      file = $file.Name
      action = "deleted_duplicate"
      corpus = ($hashIndex[$hash] -join " || ")
    }) | Out-Null
    continue
  }

  $sample = Get-TextSample -Path $file.FullName
  $rule = Get-ClassificationRule -FileName $file.Name -Sample $sample

  if ($null -eq $rule) {
    $unmatched.Add([PSCustomObject]@{
      file = $file.Name
      action = "left_in_a_classer"
    }) | Out-Null
    continue
  }

  $relativeDirectory = $rule["Destination"]
  $targetDirectory = Join-Path $targetRoot $relativeDirectory
  New-Item -ItemType Directory -Force -Path $targetDirectory | Out-Null

  $targetName = New-CanonicalName -OriginalName $file.Name -Rule $rule
  $targetPath = Join-Path $targetDirectory $targetName

  if (Test-Path -LiteralPath $targetPath) {
    $existingHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $targetPath).Hash
    if ($existingHash -eq $hash) {
      Remove-Item -LiteralPath $file.FullName -Force
      $deleted.Add([PSCustomObject]@{
        file = $file.Name
        action = "deleted_duplicate"
        corpus = $targetPath
      }) | Out-Null
      continue
    }

    $reviewPath = Join-Path $reviewRequired $file.Name
    Move-Item -LiteralPath $file.FullName -Destination $reviewPath -Force
    $review.Add([PSCustomObject]@{
      file = $file.Name
      action = "review_required"
      destination = $reviewPath
      intended = $targetPath
    }) | Out-Null
    continue
  }

  Move-Item -LiteralPath $file.FullName -Destination $targetPath -Force
  $moved.Add([PSCustomObject]@{
    file = $file.Name
    destination = $targetPath
  }) | Out-Null
}

[PSCustomObject]@{
  moved = $moved.Count
  deleted_duplicates = $deleted.Count
  review_required = $review.Count
  unmatched = $unmatched.Count
} | Format-List

if ($moved.Count -gt 0) {
  $moved | Sort-Object destination, file | Format-Table -AutoSize
}

if ($unmatched.Count -gt 0) {
  $unmatched | Sort-Object file | Format-Table -AutoSize
}
