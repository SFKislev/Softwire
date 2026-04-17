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

Illustrator-specific notes:

- Selection can contain `PathItem`, `GroupItem`, `CompoundPathItem`, text,
  placed art, or plugin items. Check `typename` before applying properties.
- Recursive handling is usually needed for grouped or compound path edits.
- Many visual edits are direct object-model writes: fill, stroke, opacity,
  artboard, layer, swatch, and path geometry.
