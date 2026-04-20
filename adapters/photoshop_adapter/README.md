# Photoshop Adapter Prototype

This folder lets a coding agent drive a running Photoshop instance through
Windows COM and ExtendScript using only shell commands.

## Portable Hook

The bridge uses the generic COM ProgID:

```text
Photoshop.Application
```

Do not hard-code the local Photoshop install path. Each Windows machine resolves
the ProgID through its own registry.

## First Live Test

Open Photoshop first, then open a document. From the workspace root:

```powershell
Get-Content adapters/photoshop_adapter/examples/context.jsx -Raw | python adapters/photoshop_adapter/photoshop_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Adobe Photoshop", "...": "..."}}
```

## Directed Mutation Tests

With a disposable document open and a layer selected:

```powershell
Get-Content adapters/photoshop_adapter/examples/set-layer-opacity-multiply.jsx -Raw | python adapters/photoshop_adapter/photoshop_bridge.py --stdin
```

This should set the active layer to 40% opacity and Multiply in one history
step.

```powershell
Get-Content adapters/photoshop_adapter/examples/create-retouch-layer.jsx -Raw | python adapters/photoshop_adapter/photoshop_bridge.py --stdin
```

This should create a new layer named `Retouch` above the previously active layer
in one history step.

```powershell
Get-Content adapters/photoshop_adapter/examples/open-liquify.jsx -Raw | python adapters/photoshop_adapter/photoshop_bridge.py --stdin
```

This should open Liquify. Brush state inside the modal dialog may not be
scriptable on the installed Photoshop version; report that limitation honestly.
