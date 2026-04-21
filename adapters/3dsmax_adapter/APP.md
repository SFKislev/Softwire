# 3ds Max Notes

Bridge:

```powershell
python adapters/3dsmax_adapter/3dsmax_bridge.py --stdin
```

Runtime: 3ds Max startup MAXScript -> embedded Python bridge -> tokenized
localhost eval endpoint -> `MaxPlus` / MAXScript.

Context:

```powershell
Get-Content adapters/3dsmax_adapter/examples/context.py -Raw | python adapters/3dsmax_adapter/3dsmax_bridge.py --stdin
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

1. Open 3ds Max.
2. Confirm the startup script is installed.
3. Restart 3ds Max if the bridge was installed after Max was already open.
4. Retry the context command above.

If the bridge is missing, install it:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/3dsmax_adapter/install_bridge.ps1
```

3ds Max-specific notes:

- Startup uses a MAXScript loader that calls `python.ExecuteFile(...)` to load
  the bridge during app startup.
- The bridge generates a random token on startup and writes it with the eval URL
  to `%APPDATA%\creative-adapters\3dsmax.json`. The Python bridge reads this
  file automatically and sends `X-Bridge-Token`.
- The bridge queues incoming scripts from the HTTP thread and uses a PySide2
  `QTimer` to execute them on Max's UI thread when PySide2 is available.
- Scripts run in a persistent namespace with `MaxPlus` imported. Set `_result`
  in the script to return structured data.
- For MAXScript calls from Python, prefer `MaxPlus.Core.EvalMAXScript(...)` and
  convert results to simple strings/numbers/lists before assigning `_result`.
- For bounded MAXScript edits, prefer `undo "<label>" on (...)`.
- Do not save, render, export, reset the scene, switch files, or alter the
  user's selection/viewport unless explicitly asked.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `MAX_COMMAND`, `MXS_FUNCTION`, `RUNTIME_DISCOVERY`).
