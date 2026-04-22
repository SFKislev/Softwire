# Illustrator Notes

Bridge:

```powershell
python adapters/illustrator_adapter/illustrator_bridge.py --stdin
```

Runtime: COM `Illustrator.Application` -> `DoJavaScript`.

Context:

```powershell
Get-Content adapters/illustrator_adapter/examples/context.jsx -Raw | python adapters/illustrator_adapter/illustrator_bridge.py --stdin
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

If the bridge cannot connect, ask the user to open Illustrator and retry the
context command. This adapter connects to the running COM application by
default; do not launch Illustrator unless the user explicitly asks.

Illustrator-specific notes:

- Selection can contain `PathItem`, `GroupItem`, `CompoundPathItem`, text,
  placed art, or plugin items. Check `typename` before applying properties.
- Recursive handling is usually needed for grouped or compound path edits.
- Many visual edits are direct object-model writes: fill, stroke, opacity,
  artboard, layer, swatch, and path geometry.
- Many appearance effects live in Illustrator Live Effects rather than direct
  DOM properties. Discover available effect names at runtime with
  `app.liveEffectsList`, then apply via `PageItem.applyEffect(liveEffectXML)`.
- For visually judged edits, prefer the temporary preview-verification workflow
  in `shared/coexistence.md` instead of assuming the result looks correct.
- Do not save, close documents, export, package, relink assets, or change the
  active document unless the user explicitly asks.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `ENUM`, `PROPERTY`, `METHOD`, and live-effect guidance).
