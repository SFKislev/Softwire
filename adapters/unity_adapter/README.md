# Unity Adapter Prototype

Unity exposes its automation surface through Editor scripting. This adapter is
a project-local Unity package plus the standard shell bridge wrapper.

## Shape

```text
Unity Editor
  Creative Adapter Bridge package
    UnityEditor / UnityEngine C# on the Editor main thread
    local command endpoint + per-session token file

Shell
  python adapters/unity_adapter/unity_bridge.py --stdin
```

## Install Into a Unity Project

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/unity_adapter/install_package.ps1 -ProjectPath "C:\Path\To\UnityProject"
```

Then open or refocus that Unity project. The package starts automatically and
writes:

```text
%APPDATA%\creative-adapters\unity.json
```

The shell bridge reads that file automatically and sends `X-Bridge-Token`.
Users should not need to copy or manage tokens or ports.

## First Live Test

```powershell
Get-Content adapters/unity_adapter/examples/context.json -Raw | python adapters/unity_adapter/unity_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Unity", "...": "..."}}
```

Create a cube:

```powershell
Get-Content adapters/unity_adapter/examples/create-blue-cube.json -Raw | python adapters/unity_adapter/unity_bridge.py --stdin
```

## Command Surface

The initial directed-mode bridge supports:

- `context`
- `createPrimitive`
- `createGameObject`
- `setTransform`
- `setSelection`
- `addComponent`
- `executeMenuItem`

Unity does not provide a built-in arbitrary C# string `eval`, so this adapter
does not claim one. Expand the command surface in
`package/Editor/CreativeAdapterBridge.cs` or add project-local Editor scripts
for deeper game-specific workflows.
