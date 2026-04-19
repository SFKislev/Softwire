# Illustrator Notes

Bridge:

```powershell
python illustrator_adapter/illustrator_bridge.py --stdin
```

Runtime: COM `Illustrator.Application` -> `DoJavaScript`.

Context:

```powershell
Get-Content illustrator_adapter/examples/context.jsx -Raw | python illustrator_adapter/illustrator_bridge.py --stdin
```

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
