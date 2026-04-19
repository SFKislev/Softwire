# InDesign Notes

Bridge:

```powershell
python indesign_adapter/indesign_bridge.py --stdin
```

Runtime: COM `InDesign.Application` -> `DoScript(JavaScript)`.

Context:

```powershell
Get-Content indesign_adapter/examples/context.jsx -Raw | python indesign_adapter/indesign_bridge.py --stdin
```

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
