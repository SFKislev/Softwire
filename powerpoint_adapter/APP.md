# PowerPoint Notes

Bridge:

```powershell
python powerpoint_adapter/powerpoint_bridge.py --stdin
```

Runtime: Windows COM `PowerPoint.Application` controlled from Python.

Context:

```powershell
Get-Content powerpoint_adapter/examples/context.py -Raw | python powerpoint_adapter/powerpoint_bridge.py --stdin
```

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
