# PowerPoint Notes

Bridge:

```powershell
python adapters/powerpoint_adapter/powerpoint_bridge.py --stdin
```

Runtime: Windows COM `PowerPoint.Application` controlled from Python.

Context:

```powershell
Get-Content adapters/powerpoint_adapter/examples/context.py -Raw | python adapters/powerpoint_adapter/powerpoint_bridge.py --stdin
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

If the bridge cannot connect, ask the user to open PowerPoint and retry the
context command. This adapter connects to the running COM application by
default; do not launch PowerPoint unless the user explicitly asks.

PowerPoint-specific notes:

- PowerPoint does not expose a general script-eval method through COM. The
  bridge executes Python code with the live `PowerPoint.Application` COM object
  available as `app`.
- Set `_result` in the submitted Python script to return structured JSON.
- Prefer structural PowerPoint object-model calls over UI automation:
  `Presentations`, `ActivePresentation`, `Slides`, `Shapes`, `TextFrame`,
  `TextFrame2`, `Tables`, `Chart`, `SlideMaster`, `CustomLayouts`, and
  `Selection`.
- Do not save, close, print, export, start a slideshow, or switch presentations
  unless the user explicitly asks.
- PowerPoint uses 1-based COM collections. Use `.Count` and `.Item(index)`
  instead of Python indexing for most collections.
- PowerPoint has both legacy `TextFrame` and newer `TextFrame2` APIs. Inspect
  a shape's capabilities before mutating text.
- Many PowerPoint/Office constants are available through `constants`, but
  verify constants at runtime if unsure.
- For visually judged slide layout or formatting changes, prefer the temporary
  preview-verification workflow in `shared/coexistence.md` instead of assuming
  the visible result.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `ENUM`, `PROPERTY`, `METHOD`, `EVENT`, `CONSTANT`).
