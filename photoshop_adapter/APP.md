# Photoshop Notes

Bridge:

```powershell
python photoshop_adapter/photoshop_bridge.py --stdin
```

Runtime: COM `Photoshop.Application` -> `DoJavaScript`.

Context:

```powershell
Get-Content photoshop_adapter/examples/context.jsx -Raw | python photoshop_adapter/photoshop_bridge.py --stdin
```

Photoshop-specific notes:

- Use `app.activeDocument.suspendHistory("<label>", "main()")` for multi-step
  edits that should undo as one step.
- `app.runMenuItem(stringIDToTypeID("<id>"))` is useful for menu commands.
- `app.doAction("<action name>", "<action set name>")` runs an installed
  Photoshop action.
- Modal filter internals are often opaque after the dialog opens; do not claim
  a setting was applied unless the script verified it.
