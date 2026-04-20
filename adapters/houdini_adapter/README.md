# Houdini Adapter Prototype

Houdini exposes its scripting surface through in-process Python and the Houdini
Object Model (`hou`). This adapter installs a small startup bridge that runs
inside Houdini and exposes the same tokenized local HTTP eval contract used by
the other non-COM adapters.

## Shape

```text
Houdini
  uiready.py startup loader
    embedded Python bridge
    hou Python on Houdini's UI thread
    local eval endpoint + per-session token file

Shell
  python adapters/houdini_adapter/houdini_bridge.py --stdin
```

## Install Bridge

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/houdini_adapter/install_bridge.ps1
```

Restart Houdini after installing. When the bridge starts, it writes:

```text
%APPDATA%\creative-adapters\houdini.json
```

The shell bridge reads that file automatically and sends `X-Bridge-Token`.
Users should not need to copy or manage tokens or ports.

## First Live Test

```powershell
Get-Content adapters/houdini_adapter/examples/context.py -Raw | python adapters/houdini_adapter/houdini_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Houdini", "...": "..."}}
```

## Directed Mode

This first adapter implements the directed-mode floor: execute bounded Python
against the live Houdini session, read context, and mutate the current scene or
selection on request. Node graph query helpers and higher-level action commands
can be added later if the raw HOM bridge proves too broad for a workflow.
