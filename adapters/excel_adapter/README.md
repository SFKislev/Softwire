# Excel Adapter Prototype

This folder lets a coding agent drive a running Microsoft Excel instance
through Windows COM using only shell commands.

## Platform Support

**Windows only.** The bridge uses Windows COM automation (`pythoncom` /
`win32com`), which is not available on macOS. Running the bridge on Mac exits
immediately with a clear error. A macOS port would require a different
scripting surface (Office AppleScript dictionary or Office Add-in JS API).

## Portable Hook (Windows)

The bridge uses the generic COM ProgID:

```text
Excel.Application
```

Do not hard-code the local Office install path. Each Windows machine resolves
the ProgID through its own registry.

## First Live Test

Open Excel first, then open or create a workbook. From the workspace root:

```powershell
Get-Content adapters/excel_adapter/examples/context.py -Raw | python adapters/excel_adapter/excel_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Microsoft Excel", "...": "..."}}
```

## Script Shape

Excel does not provide a general script-eval method. The Excel bridge executes
Python code and exposes the live COM object as `app`. Set `_result` to a
JSON-serializable value:

```python
book = app.ActiveWorkbook if app.Workbooks.Count else None
sheet = book.ActiveSheet if book else None
_result = {
    "workbooks": app.Workbooks.Count,
    "workbook": book.Name if book else None,
    "sheet": sheet.Name if sheet else None,
}
```

Use `--stdin` for one-off scripts. If a file is required, keep it in a temp or
scratch directory, not in `examples/`.
