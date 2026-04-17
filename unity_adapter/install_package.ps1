param(
  [string]$ProjectPath = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($ProjectPath)) {
  if ((Test-Path "Assets") -and (Test-Path "ProjectSettings")) {
    $ProjectPath = (Get-Location).Path
  } else {
    throw "Pass -ProjectPath <Unity project root>, or run this from a Unity project folder."
  }
}

$project = Resolve-Path -LiteralPath $ProjectPath
$assets = Join-Path $project "Assets"
$settings = Join-Path $project "ProjectSettings"
if (!(Test-Path $assets) -or !(Test-Path $settings)) {
  throw "Not a Unity project root: $project"
}

$source = Join-Path $PSScriptRoot "package"
$target = Join-Path $project "Packages\com.creativeadapters.unity-bridge"
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null

if (Test-Path $target) {
  Remove-Item -LiteralPath $target -Recurse -Force
}
Copy-Item -LiteralPath $source -Destination $target -Recurse -Force

[PSCustomObject]@{
  Installed = $true
  Source = $source
  Target = $target
}
