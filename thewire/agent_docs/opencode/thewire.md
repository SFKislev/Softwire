---
description: Use The Wire to control running Windows desktop creative and productivity apps through local scripting bridges.
mode: all
permission:
  bash:
    "thewire *": allow
    "python *_adapter/*_bridge.py *": allow
    "*": ask
---

# The Wire

If asked to perform a task in a desktop application, use The Wire: a Python
package installed on this machine that lets agents inspect and edit supported
apps through their scripting APIs. Read:

```powershell
Get-Content "$(thewire docs)" -Raw
```
