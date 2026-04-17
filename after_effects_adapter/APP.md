# After Effects Notes

Bridge:

```powershell
python after_effects_adapter/after_effects_bridge.py --stdin
```

Runtime: local CEP panel -> `window.__adobe_cep__.evalScript(...)` -> After
Effects ExtendScript.

Context:

```powershell
Get-Content after_effects_adapter/examples/context.jsx -Raw | python after_effects_adapter/after_effects_bridge.py --stdin
```

Connection recovery:

If the bridge says the session file is missing or the local eval endpoint is
unreachable, ask the user to:

1. Open After Effects.
2. Open the target project.
3. Open `Window > Extensions > Creative Adapter Bridge`.
4. Leave the panel open or docked.

Then retry the context command above.

If `Creative Adapter Bridge` is missing from the Extensions menu, reinstall the
panel:

```powershell
powershell -ExecutionPolicy Bypass -File after_effects_adapter/install_cep_bridge.ps1
```

Restart After Effects after reinstalling.

After Effects-specific notes:

- Local probing did not find a practical `AfterFX.Application` COM automation
  object, so this adapter uses CEP rather than the Photoshop-style COM bridge.
- The CEP panel generates a random token on startup and writes it with the eval
  URL to `%APPDATA%\creative-adapters\after_effects.json`. The Python bridge
  reads this file automatically and sends `X-Bridge-Token`.
- The manifest uses `AutoVisible`, and the panel attempts
  `app.setExtensionPersistent(...)`. After Effects may auto-open it in later
  sessions after one-time setup. If it does not, instruct the user to open
  `Window > Extensions > Creative Adapter Bridge`.
- Do not render, export, collect files, relink footage, save, or close projects
  unless the user explicitly asks.
