# Excel Notes

Bridge:

```powershell
python excel_adapter/excel_bridge.py --stdin
```

Runtime: Windows COM `Excel.Application` controlled from Python.

Context:

```powershell
Get-Content excel_adapter/examples/context.py -Raw | python excel_adapter/excel_bridge.py --stdin
```

Excel-specific notes:

- Excel does not expose a general script-eval method through COM. The bridge
  executes Python code with the live `Excel.Application` COM object available as
  `app`.
- Set `_result` in the submitted Python script to return structured JSON.
- Prefer structural Excel object-model calls over UI automation: `Workbooks`,
  `ActiveWorkbook`, `Worksheets`, `Range`, `Cells`, `ListObjects`, `PivotTables`,
  `Charts`, `Names`, `UsedRange`, and `Selection`.
- Do not save, close, print, export, refresh external data, run macros, or switch
  workbooks unless the user explicitly asks.
- Excel uses 1-based COM collections. Use `.Count` and `.Item(index)` instead
  of Python indexing for most Excel collections.
- Excel COM calls can be slow across large ranges. Read or write rectangular
  ranges in batches through `.Value` / `.Value2` instead of looping cell by
  cell whenever possible.
- Many Excel constants are available through `constants`, for example
  `constants.xlUp`, but verify constants at runtime if unsure.
