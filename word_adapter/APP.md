# Word Notes

Bridge:

```powershell
python word_adapter/word_bridge.py --stdin
```

Runtime: Windows COM `Word.Application` controlled from Python.

Context:

```powershell
Get-Content word_adapter/examples/context.py -Raw | python word_adapter/word_bridge.py --stdin
```

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
