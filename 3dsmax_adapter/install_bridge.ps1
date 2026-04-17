$ErrorActionPreference = "Stop"

$sourcePy = Join-Path $PSScriptRoot "inprocess\creative_adapter_bridge.py"
$sourceStartup = Join-Path $PSScriptRoot "inprocess\creative_adapter_bridge_startup.ms"

if (!(Test-Path $sourcePy)) {
  throw "Bridge source not found: $sourcePy"
}
if (!(Test-Path $sourceStartup)) {
  throw "Startup source not found: $sourceStartup"
}

$profilesRoot = Join-Path $env:LOCALAPPDATA "Autodesk\3dsMax"
$profiles = @()
if (Test-Path $profilesRoot) {
  $profiles = Get-ChildItem -Path $profilesRoot -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "* - 64bit" }
}

if ($profiles.Count -eq 0) {
  throw "No 3ds Max user profiles found under $profilesRoot. Open 3ds Max once, then rerun this installer."
}

$targets = @()
foreach ($profile in $profiles) {
  $enu = Join-Path $profile.FullName "ENU"
  if (!(Test-Path $enu)) {
    continue
  }

  $scriptsDir = Join-Path $enu "scripts"
  $startupDir = Join-Path $scriptsDir "startup"
  New-Item -ItemType Directory -Force -Path $startupDir | Out-Null

  $targetPy = Join-Path $scriptsDir "creative_adapter_bridge.py"
  $targetStartup = Join-Path $startupDir "creative_adapter_bridge_startup.ms"

  Copy-Item -LiteralPath $sourcePy -Destination $targetPy -Force
  $startup = Get-Content -LiteralPath $sourceStartup -Raw
  $startup = $startup.Replace("__BRIDGE_PY__", $targetPy)
  Set-Content -LiteralPath $targetStartup -Value $startup -Encoding ASCII
  $targets += $targetStartup
}

if ($targets.Count -eq 0) {
  throw "No ENU 3ds Max profiles found under $profilesRoot."
}

[PSCustomObject]@{
  Installed = $true
  Source = $sourcePy
  Targets = ($targets -join "; ")
}
