# Unity Notes

Bridge:

```powershell
python unity_adapter/unity_bridge.py --stdin
```

Runtime: Unity Editor package -> tokenized localhost command endpoint ->
`UnityEditor` / `UnityEngine` C# code on the Editor main thread.

Context:

```powershell
Get-Content unity_adapter/examples/context.json -Raw | python unity_adapter/unity_bridge.py --stdin
```

Connection recovery:

If the bridge says the session file is missing or the local eval endpoint is
unreachable, ask the user to open a Unity project that has the Creative Adapter
Bridge package installed. If the package is not installed, install it into the
target Unity project:

```powershell
powershell -ExecutionPolicy Bypass -File unity_adapter/install_package.ps1 -ProjectPath "C:\Path\To\UnityProject"
```

Unity-specific notes:

- Unity Editor scripting is C#, but Unity does not expose an arbitrary C#
  string `eval` API. This adapter accepts command JSON for tested Editor
  actions.
- For deeper project-specific behavior, add explicit actions to the package or
  create project-local Editor scripts. Do not pretend arbitrary C# was executed.
- The package generates a random token on Editor startup and writes it with the
  eval URL to `%APPDATA%\creative-adapters\unity.json`. The Python bridge reads
  this file automatically and sends `X-Bridge-Token`.
- Commands run on Unity's main Editor thread.
- Do not enter/exit Play Mode, save scenes, build, import large assets, edit
  project settings, or change scenes unless explicitly asked.
- Prefer undo-backed commands. The included create/transform/component actions
  use Unity's `Undo` API where applicable.
