$apps = @(
  @{ Name = "Photoshop"; ProgId = "Photoshop.Application"; Process = "Photoshop.exe" },
  @{ Name = "InDesign"; ProgId = "InDesign.Application"; Process = "InDesign.exe" },
  @{ Name = "Illustrator"; ProgId = "Illustrator.Application"; Process = "Illustrator.exe" },
  @{ Name = "Premiere Pro"; ProgId = "Premiere.Application"; Process = "Adobe Premiere Pro.exe" }
)

foreach ($app in $apps) {
  $registered = Test-Path "Registry::HKEY_CLASSES_ROOT\$($app.ProgId)"
  $versioned = Get-ChildItem 'Registry::HKEY_CLASSES_ROOT' -ErrorAction SilentlyContinue |
    Where-Object { $_.PSChildName -like "$($app.ProgId).*" } |
    Select-Object -ExpandProperty PSChildName
  $process = Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -eq [System.IO.Path]::GetFileNameWithoutExtension($app.Process) } |
    Select-Object -First 1
  $appPath = Get-ChildItem 'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths' -ErrorAction SilentlyContinue |
    Where-Object { $_.PSChildName -eq $app.Process } |
    ForEach-Object { (Get-ItemProperty $_.PSPath).'(default)' }

  [PSCustomObject]@{
    App = $app.Name
    ProgId = $app.ProgId
    Registered = $registered
    VersionedProgIds = ($versioned -join ", ")
    Running = [bool]$process
    Path = $appPath
  }
}
