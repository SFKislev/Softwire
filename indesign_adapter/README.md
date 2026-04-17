# InDesign Adapter Prototype

This folder lets a coding agent drive a running InDesign instance through
Windows COM and ExtendScript using only shell commands.

## Portable Hook

The bridge uses the generic COM ProgID:

```text
InDesign.Application
```

Do not hard-code the local InDesign install path. Each Windows machine resolves
the ProgID through its own registry.

The bridge uses InDesign's `DoScript` COM method with JavaScript language id
`1246973031`.

## First Live Test

Open InDesign first. From the workspace root:

```powershell
Get-Content indesign_adapter/examples/context.jsx -Raw | python indesign_adapter/indesign_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Adobe InDesign", "...": "..."}}
```

## Directed Mutation Example

With a disposable document open:

```powershell
Get-Content indesign_adapter/examples/set-margins-10mm.jsx -Raw | python indesign_adapter/indesign_bridge.py --stdin
```

This sets the active document's margin preferences to 10mm on all sides.
