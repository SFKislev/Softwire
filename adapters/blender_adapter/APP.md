# Blender Notes

Bridge:

```powershell
python adapters/blender_adapter/blender_bridge.py --stdin
```

Runtime: Blender addon -> tokenized localhost eval endpoint -> `bpy` Python on
Blender's main thread.

Context:

```powershell
Get-Content adapters/blender_adapter/examples/context.py -Raw | python adapters/blender_adapter/blender_bridge.py --stdin
```

Connection recovery:

If the bridge says the session file is missing or the local eval endpoint is
unreachable, ask the user to:

1. Open Blender.
2. Enable the `Creative Adapter Bridge` addon.
3. Retry the context command above.

If the addon is missing, install it:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/blender_adapter/install_addon.ps1
```

Then restart Blender or use `Edit > Preferences > Add-ons` to enable
`Creative Adapter Bridge`.

Blender-specific notes:

- Blender has no out-of-process `bpy`; Python runs inside Blender. This adapter
  therefore installs an in-process addon.
- The addon generates a random token on startup and writes it with the eval URL
  to `%APPDATA%\creative-adapters\blender.json`. The Python bridge reads this
  file automatically and sends `X-Bridge-Token`.
- Scripts run in a persistent namespace with `bpy` already imported. Set
  `_result` in the script to return structured data.
- For user-visible edits, include an undo label and call
  `bpy.ops.ed.undo_push(message="<label>")` after the mutation when Blender's
  undo system supports the operation.
- Do not save, render, export, change files, switch scenes, or alter the user's
  selection/viewport unless explicitly asked.
