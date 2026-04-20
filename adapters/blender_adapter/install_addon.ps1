$ErrorActionPreference = "Stop"

$source = Join-Path $PSScriptRoot "addon\creative_adapter_bridge.py"
if (!(Test-Path $source)) {
  throw "Addon source not found: $source"
}

$blenderRoot = Join-Path $env:APPDATA "Blender Foundation\Blender"
$versions = @()
if (Test-Path $blenderRoot) {
  $versions += Get-ChildItem -Path $blenderRoot -Directory | Select-Object -ExpandProperty Name
}

if ($versions.Count -eq 0) {
  $installed = Get-ChildItem "C:\Program Files\Blender Foundation" -Recurse -Filter blender.exe -ErrorAction SilentlyContinue |
    Select-Object -First 1
  if ($installed -and $installed.FullName -match "Blender\s+([0-9]+\.[0-9]+)") {
    $versions += $Matches[1]
  }
}

if ($versions.Count -eq 0) {
  $versions += "5.0"
}

$targets = @()
foreach ($version in ($versions | Sort-Object -Unique)) {
  $targetDir = Join-Path $blenderRoot "$version\scripts\addons"
  New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
  $target = Join-Path $targetDir "creative_adapter_bridge.py"
  Copy-Item -LiteralPath $source -Destination $target -Force
  $targets += $target
}

[PSCustomObject]@{
  Installed = $true
  Source = $source
  Targets = ($targets -join "; ")
}
