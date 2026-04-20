$ErrorActionPreference = "Stop"

$sourceBridge = Join-Path $PSScriptRoot "inprocess\creative_adapter_bridge.py"
$sourceLoader = Join-Path $PSScriptRoot "inprocess\creative_adapter_loader.py"

if (!(Test-Path $sourceBridge)) {
  throw "Bridge source not found: $sourceBridge"
}
if (!(Test-Path $sourceLoader)) {
  throw "Loader source not found: $sourceLoader"
}

$documents = [Environment]::GetFolderPath("MyDocuments")
$prefs = @()

if (Test-Path $documents) {
  $prefs += Get-ChildItem -Path $documents -Directory -Filter "houdini*" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "^houdini\d+(\.\d+)?$" }
}

$installRoots = @(
  "$env:ProgramFiles\Side Effects Software",
  "${env:ProgramFiles(x86)}\Side Effects Software"
) | Where-Object { $_ -and (Test-Path $_) }

foreach ($root in $installRoots) {
  Get-ChildItem -Path $root -Directory -Filter "Houdini*" -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.Name -match "Houdini\s+(\d+\.\d+)") {
      $prefPath = Join-Path $documents ("houdini" + $Matches[1])
      if (!($prefs | Where-Object { $_.FullName -eq $prefPath })) {
        New-Item -ItemType Directory -Force -Path $prefPath | Out-Null
        $prefs += Get-Item -LiteralPath $prefPath
      }
    }
  }
}

if ($prefs.Count -eq 0) {
  $fallback = Join-Path $documents "houdini21.0"
  New-Item -ItemType Directory -Force -Path $fallback | Out-Null
  $prefs += Get-Item -LiteralPath $fallback
}

$pythonLibDirs = @("python3.9libs", "python3.10libs", "python3.11libs", "python3.12libs", "python3.13libs")
$begin = "# >>> Creative Adapter Bridge >>>"
$end = "# <<< Creative Adapter Bridge <<<"
$loaderBlock = @"
$begin
try:
    import creative_adapter_loader
except Exception:
    import traceback
    traceback.print_exc()
$end
"@

$targets = @()

foreach ($pref in ($prefs | Sort-Object FullName -Unique)) {
  foreach ($pythonLibDir in $pythonLibDirs) {
    $targetDir = Join-Path $pref.FullName $pythonLibDir
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

    Copy-Item -LiteralPath $sourceBridge -Destination (Join-Path $targetDir "creative_adapter_bridge.py") -Force
    Copy-Item -LiteralPath $sourceLoader -Destination (Join-Path $targetDir "creative_adapter_loader.py") -Force

    $uiReady = Join-Path $targetDir "uiready.py"
    $content = ""
    if (Test-Path $uiReady) {
      $content = Get-Content -LiteralPath $uiReady -Raw
    }

    if ($content.Contains($begin) -and $content.Contains($end)) {
      $pattern = [regex]::Escape($begin) + "(?s).*?" + [regex]::Escape($end)
      $content = [regex]::Replace($content, $pattern, $loaderBlock)
    } else {
      if ($content.Trim().Length -gt 0) {
        $content = $content.TrimEnd() + "`r`n`r`n" + $loaderBlock
      } else {
        $content = $loaderBlock
      }
    }

    Set-Content -LiteralPath $uiReady -Value $content -Encoding UTF8
    $targets += $uiReady
  }
}

[PSCustomObject]@{
  Installed = $true
  Source = $sourceBridge
  Targets = ($targets -join "; ")
}
