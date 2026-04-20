# 3ds Max Adapter Prototype

3ds Max exposes scripting through MAXScript and an embedded Python runtime, not
through a simple COM automation object on this machine. This adapter installs a
small in-process Python bridge loaded by a MAXScript startup shim.

## Shape

```text
3ds Max
  startup MAXScript
    python.ExecuteFile(...)
  embedded Python bridge
    MaxPlus / MAXScript
    local eval endpoint + per-session token file
    PySide2 timer dispatch onto Max's UI thread

Shell
  python adapters/3dsmax_adapter/3dsmax_bridge.py --stdin
```

## Install Bridge

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/3dsmax_adapter/install_bridge.ps1
```

Restart 3ds Max after installing. The startup shim loads the bridge.

When the bridge starts, it writes:

```text
%APPDATA%\creative-adapters\3dsmax.json
```

The shell bridge reads that file automatically and sends `X-Bridge-Token`.
Users should not need to copy or manage tokens or ports.

## First Live Test

```powershell
Get-Content adapters/3dsmax_adapter/examples/context.py -Raw | python adapters/3dsmax_adapter/3dsmax_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "3ds Max", "...": "..."}}
```

## Directed Mode

This first adapter implements the directed-mode floor: execute bounded Python
against the live 3ds Max session, read context, and mutate the current scene on
request. Exploratory endpoints such as object filters, spatial queries,
viewport projection, snapshots, and change deltas are the next tier.
