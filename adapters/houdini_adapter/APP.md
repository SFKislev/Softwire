# Houdini Notes

Bridge:

```powershell
python adapters/houdini_adapter/houdini_bridge.py --stdin
```

Runtime: Houdini startup Python -> embedded Python bridge -> tokenized
localhost eval endpoint -> Houdini Object Model (`hou`).

Context:

```powershell
Get-Content adapters/houdini_adapter/examples/context.py -Raw | python adapters/houdini_adapter/houdini_bridge.py --stdin
```

Install:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/houdini_adapter/install_bridge.ps1
```

Restart Houdini after installing. The installer adds a marked loader block to
the user's `pythonX.Ylibs/uiready.py` startup file and copies the bridge module
beside it.

Connection recovery:

If the bridge says the session file is missing or the local eval endpoint is
unreachable, ask the user to:

1. Open Houdini.
2. Confirm the startup bridge is installed.
3. Restart Houdini if the bridge was installed after Houdini was already open.
4. Retry the context command above.

Houdini-specific notes:

- Scripts run in a persistent namespace with `hou` imported. Set `_result` to
  return structured data.
- The bridge queues HTTP requests and executes them from
  `hou.ui.addEventLoopCallback(...)`, so scene edits happen on Houdini's UI
  thread.
- Prefer HOM node APIs (`hou.node`, `createNode`, `parm().set`,
  `setInput`) over UI automation.
- Houdini does not expose a universal Python undo wrapper for arbitrary HOM
  edits. Keep edits bounded and report script errors directly.
- Do not save, render, export, change desktops, or switch files unless
  explicitly asked.
