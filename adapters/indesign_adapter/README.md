# InDesign Adapter Prototype

This folder lets a coding agent drive a running InDesign instance through
shell commands.

## Platform Bridge

| Platform | Mechanism |
|----------|-----------|
| Windows  | COM (`InDesign.Application` ProgID) via `DoScript` with JavaScript language id `1246973031` |
| macOS    | AppleScript `do script ... language JavaScript` — no addon or panel required |

On macOS the bridge auto-detects the running InDesign process name via System
Events, so no hardcoded version year is needed.

## First Live Test

Open InDesign first. From the workspace root:

**Windows:**
```powershell
Get-Content adapters/indesign_adapter/examples/context.jsx -Raw | python adapters/indesign_adapter/indesign_bridge.py --stdin
```

**macOS:**
```bash
cat adapters/indesign_adapter/examples/context.jsx | python adapters/indesign_adapter/indesign_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Adobe InDesign", "...": "..."}}
```

## Directed Mutation Example

With a disposable document open:

**Windows:**
```powershell
Get-Content adapters/indesign_adapter/examples/set-margins-10mm.jsx -Raw | python adapters/indesign_adapter/indesign_bridge.py --stdin
```

**macOS:**
```bash
cat adapters/indesign_adapter/examples/set-margins-10mm.jsx | python adapters/indesign_adapter/indesign_bridge.py --stdin
```

This sets the active document's margin preferences to 10mm on all sides.

## ExtendScript Notes

InDesign runs ExtendScript (ES3-era JavaScript). `JSON.stringify` is not
available — use a manual serialisation helper for structured output.
