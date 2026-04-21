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

## Local Memory

If `APP.local.md` exists in this directory, review it before performing an
operation when local installation details, prior failures, or version-specific
behavior may matter.

After completing an operation, if you encountered a repeatable issue or
verified something worth remembering about this local installation, add a short
note to `APP.local.md`.

Keep notes concise and factual. Record only local, reusable insights such as
verified quirks, recovery steps, version-specific gaps, or runtime-discovered
details. Do not copy general guidance from `APP.md`, and do not add temporary
task-specific notes.

API lookup workflow:

- Use `docs/api-index.txt` as the primary operation index.
- Workflow for every task:
  1. Understand the user's intent.
  2. Search (`rg`) `docs/api-index.txt` for matching operations.
  3. If needed, introspect the live app/runtime to resolve ambiguity.
  4. If still needed, search official documentation online.
  5. Avoid over-relying on training, as it's fragile and can break. Do not directly read the index file, which can be heavy.


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
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `FUNCTION`, `MODULE`, `PACKAGE`, `ENUM`, `METHOD`).
