# InDesign Notes

Bridge:

```powershell
python adapters/indesign_adapter/indesign_bridge.py --stdin
```

Runtime: COM `InDesign.Application` -> `DoScript(JavaScript)`.

Context:

```powershell
Get-Content adapters/indesign_adapter/examples/context.jsx -Raw | python adapters/indesign_adapter/indesign_bridge.py --stdin
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

If the bridge cannot connect, ask the user to open InDesign and retry the
context command. This adapter connects to the running COM application by
default; do not launch InDesign unless the user explicitly asks.

InDesign-specific notes:

- JavaScript language id is `1246973031`.
- Layout tasks often live under document, page, margin, grid, style, layer, and
  selection objects.
- For measurements, set and restore `app.scriptPreferences.measurementUnit`
  inside the script.
- Prefer one bounded `DoScript` call per requested edit.
- Grep-friendly operation index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `ENUM`, `PROPERTY`, `METHOD`).
