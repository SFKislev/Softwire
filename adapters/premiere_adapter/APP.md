# Premiere Pro Notes

Bridge:

```bash
python adapters/premiere_adapter/premiere_bridge.py --stdin
```

Runtime: local CEP panel -> `window.__adobe_cep__.evalScript(...)` ->
Premiere Pro ExtendScript.

Context:

Windows:

```powershell
Get-Content adapters/premiere_adapter/examples/context.jsx -Raw | python adapters/premiere_adapter/premiere_bridge.py --stdin
```

macOS:

```bash
cat adapters/premiere_adapter/examples/context.jsx | python adapters/premiere_adapter/premiere_bridge.py --stdin
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

If `premiere_bridge.py` says the local eval endpoint is unreachable, the CEP
panel is not running in Premiere or the session file points at an old panel
session.

If it says the session file is missing, the fix is the same: open the CEP panel
so it can write the session file. Do not ask the user to create or copy the
token manually.

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

On macOS, follow the manual CEP install steps in
`adapters/premiere_adapter/README.md`. Premiere Pro 26+ on macOS does not load
CEP panels; see `docs/known-issues.md`.

Restart Premiere after reinstalling.

Premiere-specific notes:

- This adapter uses a CEP panel rather than a COM automation bridge.
- The CEP panel must be open inside Premiere before the shell bridge can read
  the session file and reach the local eval endpoint.
- The manifest uses `AutoVisible`, and the panel calls
  `app.setExtensionPersistent(...)`. The panel may auto-open in later sessions.
  If it does not, instruct the user to open
  `Window > Extensions > Creative Adapter Bridge`; do not ask them to manage
  ports or tokens.
- The CEP panel generates a random token on startup and writes it with the eval
  URL to a user-scoped session file: `%APPDATA%\creative-adapters\premiere.json`
  on Windows or `~/creative-adapters/premiere.json` on macOS. The Python bridge
  reads this file automatically and sends `X-Bridge-Token`.
- The panel calls `app.setExtensionPersistent("com.creativeadapters.premiere.panel", 1)`
  when loaded. This keeps it in memory during the current Premiere session, but
  does not guarantee automatic opening after a full app restart.
- Timeline/project operations can be version-sensitive. Check local examples and
  docs before editing sequences, tracks, clips, exports, or project settings.
- Premiere exposes a QE (Quality Engineering) DOM via `app.enableQE()`. QE is an
  internal, unsupported surface: methods can change between versions and may be
  unstable. Use QE only when the supported ExtendScript DOM does not provide the
  required operation.
- Typical QE flow: call `app.enableQE()`, access `qe.project` / `qe.sequence`
  objects, perform the minimal required action, then re-validate project state.
- For visually judged sequence or frame changes, prefer the temporary
  preview-verification workflow in `shared/coexistence.md` instead of assuming
  the visible result.
- Do not render, export, relink, transcode, or change project files unless the
  user explicitly asks.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `PROPERTY`, `METHOD`; QE records use `QE_INTERFACE`, `QE_PROPERTY`,
  `QE_METHOD`, `QE_TYPE`).
