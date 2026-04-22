# After Effects Notes

Bridge:

```powershell
python adapters/after_effects_adapter/after_effects_bridge.py --stdin
```

Runtime: local CEP panel -> `window.__adobe_cep__.evalScript(...)` -> After
Effects ExtendScript.

Context:

```powershell
Get-Content adapters/after_effects_adapter/examples/context.jsx -Raw | python adapters/after_effects_adapter/after_effects_bridge.py --stdin
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

1. Open After Effects.
2. Open the target project.
3. Open `Window > Extensions > Creative Adapter Bridge`.
4. Leave the panel open or docked.

Then retry the context command above.

If `Creative Adapter Bridge` is missing from the Extensions menu, reinstall the
panel:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/after_effects_adapter/install_cep_bridge.ps1
```

Restart After Effects after reinstalling.

After Effects-specific notes:

- This adapter uses a CEP panel rather than a COM automation bridge.
- The CEP panel generates a random token on startup and writes it with the eval
  URL to `%APPDATA%\creative-adapters\after_effects.json`. The Python bridge
  reads this file automatically and sends `X-Bridge-Token`.
- The manifest uses `AutoVisible`, and the panel attempts
  `app.setExtensionPersistent(...)`. The panel may auto-open in later sessions.
  If it does not, instruct the user to open
  `Window > Extensions > Creative Adapter Bridge`.
- For visually judged comp changes, prefer the temporary preview-verification
  workflow in `shared/coexistence.md` instead of assuming the visible result.
- Do not render, export, collect files, relink footage, save, or close projects
  unless the user explicitly asks.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `PROPERTY`, `METHOD`).
