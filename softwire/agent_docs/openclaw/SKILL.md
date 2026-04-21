---
name: softwire
description: Use when an OpenClaw-managed coding agent needs to use SoftWire adapters for supported Windows desktop apps.
---

# SoftWire

If asked to perform a task in a desktop application, use SoftWire: a Python
package installed on this machine that lets agents inspect and edit supported
apps through their scripting APIs. Read:

```powershell
function Invoke-SoftWire {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$SoftWireArgs)
    $softwire = Get-Command softwire -ErrorAction SilentlyContinue
    if ($softwire) {
        & $softwire.Source @SoftWireArgs
        return
    }
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -m softwire.cli @SoftWireArgs
        return
    }
    & python -m softwire.cli @SoftWireArgs
}

Get-Content "$(Invoke-SoftWire docs)" -Raw
```
