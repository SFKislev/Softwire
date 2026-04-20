$ErrorActionPreference = "Stop"

$source = Join-Path $PSScriptRoot "cep\com.creativeadapters.premiere"
$targetRoot = Join-Path $env:APPDATA "Adobe\CEP\extensions"
$target = Join-Path $targetRoot "com.creativeadapters.premiere"

if (!(Test-Path $source)) {
  throw "CEP source folder not found: $source"
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

if (Test-Path $target) {
  Remove-Item -LiteralPath $target -Recurse -Force
}

Copy-Item -LiteralPath $source -Destination $target -Recurse

$csxsVersions = @("CSXS.9", "CSXS.10", "CSXS.11", "CSXS.12", "CSXS.13", "CSXS.14", "CSXS.15", "CSXS.16")
foreach ($version in $csxsVersions) {
  $key = "HKCU:\Software\Adobe\$version"
  New-Item -Path $key -Force | Out-Null
  New-ItemProperty -Path $key -Name "PlayerDebugMode" -Value "1" -PropertyType String -Force | Out-Null
}

[PSCustomObject]@{
  Installed = $true
  Source = $source
  Target = $target
  DebugKeys = ($csxsVersions -join ", ")
}
