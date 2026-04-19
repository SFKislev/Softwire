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

Connection recovery:

If the bridge cannot connect, ask the user to open Photoshop and retry the
context command. This adapter connects to the running COM application by
default; do not launch Photoshop unless the user explicitly asks.

Photoshop-specific notes:

- Use `app.activeDocument.suspendHistory("<label>", "main()")` for multi-step
  edits that should undo as one step.
- `app.runMenuItem(stringIDToTypeID("<id>"))` is useful for menu commands.
- `app.doAction("<action name>", "<action set name>")` runs an installed
  Photoshop action.
- Modal filter internals are often opaque after the dialog opens; do not claim
  a setting was applied unless the script verified it.
