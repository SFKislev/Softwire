# 3ds Max Notes

Bridge:

```powershell
python 3dsmax_adapter/3dsmax_bridge.py --stdin
```

Runtime: 3ds Max startup MAXScript -> embedded Python bridge -> tokenized
localhost eval endpoint -> `MaxPlus` / MAXScript.

Context:

```powershell
Get-Content 3dsmax_adapter/examples/context.py -Raw | python 3dsmax_adapter/3dsmax_bridge.py --stdin
```

Connection recovery:

If the bridge says the session file is missing or the local eval endpoint is
unreachable, ask the user to:

1. Open 3ds Max.
2. Confirm the startup script is installed.
3. Restart 3ds Max if the bridge was installed after Max was already open.
4. Retry the context command above.

If the bridge is missing, install it:

```powershell
powershell -ExecutionPolicy Bypass -File 3dsmax_adapter/install_bridge.ps1
```

3ds Max-specific notes:

- Local probing did not find a practical COM automation ProgID, so this adapter
  installs an in-process bridge.
- 3ds Max 2020 embeds Python 2.7. Keep in-app bridge code Python 2-compatible.
- Startup uses a MAXScript file in the user profile that calls
  `python.ExecuteFile(...)`.
- The bridge generates a random token on startup and writes it with the eval URL
  to `%APPDATA%\creative-adapters\3dsmax.json`. The Python bridge reads this
  file automatically and sends `X-Bridge-Token`.
- The bridge queues incoming scripts from the HTTP thread and uses a PySide2
  `QTimer` to execute them on Max's UI thread when PySide2 is available.
- Scripts run in a persistent namespace with `MaxPlus` imported. Set `_result`
  in the script to return structured data.
- For MAXScript calls from Python, prefer `MaxPlus.Core.EvalMAXScript(...)` and
  convert results to simple strings/numbers/lists before assigning `_result`.
- Do not save, render, export, reset the scene, switch files, or alter the
  user's selection/viewport unless explicitly asked.
