# Word Notes

Bridge:

```powershell
python adapters/word_adapter/word_bridge.py --stdin
```

Runtime: Windows COM `Word.Application` controlled from Python.

Context:

```powershell
Get-Content adapters/word_adapter/examples/context.py -Raw | python adapters/word_adapter/word_bridge.py --stdin
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

If the bridge cannot connect, ask the user to open Word and retry the context
command. This adapter connects to the running COM application by default; do
not launch Word unless the user explicitly asks.

Word-specific notes:

- Word does not expose an arbitrary `DoScript` or `DoJavaScript` method through
  COM. The bridge executes Python code with the live `Word.Application` COM
  object available as `app`.
- Set `_result` in the submitted Python script to return structured JSON.
- Prefer structural Word object-model calls over UI automation: `Documents`,
  `ActiveDocument`, `Selection`, `Range`, `Tables`, `Styles`, `InlineShapes`,
  `Sections`, `Paragraphs`, and `ContentControls`.
- Do not save, close, print, export, mail-merge, or switch documents unless the
  user explicitly asks.
- Word uses 1-based COM collections. Use `.Count` and `.Item(index)` instead of
  Python indexing for most Word collections.
- Many Word constants are available through `constants`, for example
  `constants.wdCollapseEnd`, but verify constants at runtime if unsure.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `ENUM`, `PROPERTY`, `METHOD`, `EVENT`, `CONSTANT`).
