# Blender Notes

Bridge:

```bash
python adapters/blender_adapter/blender_bridge.py --stdin
```

Runtime: Blender addon -> tokenized localhost eval endpoint -> `bpy` Python on
Blender's main thread.

Context:

Windows:

```powershell
Get-Content adapters/blender_adapter/examples/context.py -Raw | python adapters/blender_adapter/blender_bridge.py --stdin
```

macOS:

```bash
cat adapters/blender_adapter/examples/context.py | python adapters/blender_adapter/blender_bridge.py --stdin
```

## Local Memory

If `APP.local.md` exists in this directory, review it before performing an
operation when local installation details, prior failures, or version-specific
behavior may matter.

After completing an operation, if you encountered a repeatable issue or
verified something worth remembering about this local installation, add a short
note to `APP.local.md`.

Keep notes concise and factual. Record only local, reusable insights such as
verified quirks, recovery steps, version-specific gaps, or runtime-discovered
details. Do not copy general guidance from `APP.md`, and do not add temporary
task-specific notes.

API lookup workflow:

- Use `docs/api-index.txt` as the primary operation index.
- Workflow for every task:
  1. Understand the user's intent.
  2. Search (`rg`) `docs/api-index.txt` for matching operations.
  3. If needed, introspect the live app/runtime to resolve ambiguity.
  4. If still needed, search official documentation online.
  5. Avoid over-relying on training, as it's fragile and can break. Do not directly read the index file, which can be heavy.

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

On macOS, install `adapters/blender_adapter/addon/creative_adapter_bridge.py`
through Blender's add-on installer, then enable `Creative Adapter Bridge`.

Blender-specific notes:

- Blender has no out-of-process `bpy`; Python runs inside Blender. This adapter therefore installs an in-process addon.
- If the human asks you for a model, it's often better to find an existing model online than you start modeling, which can be difficult.
- The addon generates a random token on startup and writes it with the eval URL to a user-scoped session file: `%APPDATA%\creative-adapters\blender.json` on Windows or `~/creative-adapters/blender.json` on macOS. The Python bridge reads this file automatically and sends `X-Bridge-Token`.
- Scripts run in a persistent namespace with `bpy` already imported. Set `_result` in the script to return structured data.
- For user-visible edits, include an undo label and call `bpy.ops.ed.undo_push(message="<label>")` after the mutation when Blender's
  undo system supports the operation.
- For visually judged scene, material, lighting, or camera changes, prefer the temporary review-verification workflow in `shared/coexistence.md` instead of assuming the visible result.
- Do not save, render, export, change files, switch scenes, or alter the user's selection/viewport unless explicitly asked.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with `MODULE`, `CLASS`, `OPERATOR`, `METHOD`, `PROPERTY`).
