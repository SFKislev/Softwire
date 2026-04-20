# Illustrator Adapter Prototype

This folder lets a coding agent drive the running Illustrator instance through
Windows COM and ExtendScript using only shell commands.

## Portable Hook

The bridge uses the generic COM ProgID:

```text
Illustrator.Application
```

Do not hard-code the local Illustrator install path. Each Windows machine
resolves the ProgID through its own registry.

## First Live Test

Open Illustrator first, then open or create a document. From the workspace root:

```powershell
Get-Content adapters/illustrator_adapter/examples/context.jsx -Raw | python adapters/illustrator_adapter/illustrator_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Adobe Illustrator", "...": "..."}}
```

## Directed Mutation Example

With one or more path items selected:

```powershell
Get-Content adapters/illustrator_adapter/examples/set-selected-stroke-black-1pt.jsx -Raw | python adapters/illustrator_adapter/illustrator_bridge.py --stdin
```

This sets selected path-like items to 1pt black stroke with no fill. Test on a
disposable document first.
