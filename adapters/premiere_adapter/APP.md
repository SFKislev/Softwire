# Premiere Pro Notes

Bridge:

```powershell
python adapters/premiere_adapter/premiere_bridge.py --stdin
```

Runtime: local CEP panel -> `window.__adobe_cep__.evalScript(...)` ->
Premiere Pro ExtendScript.

Context:

```powershell
Get-Content adapters/premiere_adapter/examples/context.jsx -Raw | python adapters/premiere_adapter/premiere_bridge.py --stdin
```

Connection recovery:

If `premiere_bridge.py` says the local eval endpoint is unreachable, the CEP
panel is not running in Premiere or the session file points at an old panel
session.

If it says the session file is missing, the fix is the same: open the CEP panel
so it can write `%APPDATA%\creative-adapters\premiere.json`. Do not ask the user
to create or copy the token manually.

Ask the user to:

1. Open Premiere Pro.
2. Open the target project.
3. Open `Window > Extensions > Creative Adapter Bridge`.
4. Leave the panel open or docked.

Then retry the context command above.

If `Creative Adapter Bridge` is missing from the Extensions menu, reinstall the
panel:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/premiere_adapter/install_cep_bridge.ps1
```

Restart Premiere after reinstalling.

Premiere-specific notes:

- This adapter is not COM-only. Premiere exposes file-type ProgIDs on Windows,
  but not a practical `Premiere.Application` automation object for this bridge.
- The CEP panel must be installed and opened once inside Premiere before the
  shell bridge can read the session file and reach the local eval endpoint.
- After one-time setup, Premiere may auto-open the panel in later sessions
  because the manifest uses `AutoVisible` and the panel calls
  `app.setExtensionPersistent(...)`. If it does not auto-open, instruct the user
  to open `Window > Extensions > Creative Adapter Bridge`; do not ask them to
  manage ports or tokens.
- The CEP panel generates a random token on startup and writes it with the eval
  URL to `%APPDATA%\creative-adapters\premiere.json`. The Python bridge reads
  this file automatically and sends `X-Bridge-Token`.
- The panel calls `app.setExtensionPersistent("com.creativeadapters.premiere.panel", 1)`
  when loaded. This keeps it in memory during the current Premiere session, but
  does not guarantee automatic opening after a full app restart.
- Timeline/project operations can be version-sensitive. Check local examples and
  docs before editing sequences, tracks, clips, exports, or project settings.
- Do not render, export, relink, transcode, or change project files unless the
  user explicitly asks.
