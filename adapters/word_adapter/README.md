# Word Adapter Prototype

This folder lets a coding agent drive a running Microsoft Word instance through
Windows COM using only shell commands.

## Portable Hook

The bridge uses the generic COM ProgID:

```text
Word.Application
```

Do not hard-code the local Office install path. Each Windows machine resolves
the ProgID through its own registry.

## First Live Test

Open Word first, then open or create a document. From the workspace root:

```powershell
Get-Content adapters/word_adapter/examples/context.py -Raw | python adapters/word_adapter/word_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Microsoft Word", "...": "..."}}
```

## Script Shape

Unlike Adobe COM adapters, Word does not provide a general script-eval method.
The Word bridge executes Python code and exposes the live COM object as `app`.
Set `_result` to a JSON-serializable value:

```python
doc = app.ActiveDocument if app.Documents.Count else None
_result = {
    "documents": app.Documents.Count,
    "doc": doc.Name if doc else None,
}
```

Use `--stdin` for one-off scripts. If a file is required, keep it in a temp or
scratch directory, not in `examples/`.
