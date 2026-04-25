# Illustrator Adapter Prototype

This folder lets a coding agent drive the running Illustrator instance through
shell commands.

## Platform Bridge

| Platform | Mechanism |
|----------|-----------|
| Windows  | COM (`Illustrator.Application` ProgID) via `DoJavaScript` |
| macOS    | AppleScript `do javascript` — no addon or panel required |

On macOS the bridge auto-detects the running Illustrator process name via System
Events, so no hardcoded version year is needed.

## First Live Test

Open Illustrator first. From the workspace root:

**Windows:**
```powershell
Get-Content adapters/illustrator_adapter/examples/context.jsx -Raw | python adapters/illustrator_adapter/illustrator_bridge.py --stdin
```

**macOS:**
```bash
cat adapters/illustrator_adapter/examples/context.jsx | python adapters/illustrator_adapter/illustrator_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Adobe Illustrator", "...": "..."}}
```

## Directed Mutation Example

With one or more path items selected:

**Windows:**
```powershell
Get-Content adapters/illustrator_adapter/examples/set-selected-stroke-black-1pt.jsx -Raw | python adapters/illustrator_adapter/illustrator_bridge.py --stdin
```

**macOS:**
```bash
cat adapters/illustrator_adapter/examples/set-selected-stroke-black-1pt.jsx | python adapters/illustrator_adapter/illustrator_bridge.py --stdin
```

This sets selected path-like items to 1pt black stroke with no fill. Test on a
disposable document first.

## ExtendScript Notes

Illustrator runs ExtendScript (ES3-era JavaScript). `JSON.stringify` is not
available — use a manual serialisation helper for structured output:

```javascript
function jsonObject(obj) {
  var parts = [];
  for (var key in obj) {
    if (obj.hasOwnProperty(key)) {
      parts.push('"' + key + '":"' + String(obj[key]).replace(/"/g, '\\"') + '"');
    }
  }
  return "{" + parts.join(",") + "}";
}
```
