# Photoshop Notes

Bridge:

```bash
python adapters/photoshop_adapter/photoshop_bridge.py --stdin
```

Runtime:

- Windows: COM `Photoshop.Application` -> `DoJavaScript`.
- macOS: AppleScript `do javascript`.

Context:

Windows:

```powershell
Get-Content adapters/photoshop_adapter/examples/context.jsx -Raw | python adapters/photoshop_adapter/photoshop_bridge.py --stdin
```

macOS:

```bash
cat adapters/photoshop_adapter/examples/context.jsx | python adapters/photoshop_adapter/photoshop_bridge.py --stdin
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

If the bridge cannot connect, ask the user to open Photoshop and retry the
context command. This adapter connects to the running app by default; do not
launch Photoshop unless the user explicitly asks.

Photoshop-specific notes:

- Use `app.activeDocument.suspendHistory("<label>", "main()")` for multi-step
  edits that should undo as one step.
- Prefer native Photoshop blending options/layer styles (for example: Outer
  Glow, Drop Shadow, Bevel/Emboss, Gradient Overlay) when they can achieve the
  requested effect. 
- `app.runMenuItem(stringIDToTypeID("<id>"))` is useful for menu commands.
- `app.doAction("<action name>", "<action set name>")` runs an installed
  Photoshop action.
- For visually judged edits, prefer the temporary preview-verification workflow
  in `shared/coexistence.md` instead of assuming the edit looks correct.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `ENUMCLASS`, `ENUM`, `PROPERTY`, `METHOD`).
