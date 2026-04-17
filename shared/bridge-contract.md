# Bridge Contract

All bridge scripts:

- run from the workspace root
- accept code through argv, `--stdin`, or `--file`
- return JSON on stdout for success
- return JSON on stderr with non-zero exit for failure
- connect to a running app by default
- launch only when `--allow-launch` is explicitly passed

Run context first:

```powershell
Get-Content <app>_adapter/examples/context.jsx -Raw | python <app>_adapter/<app>_bridge.py --stdin
```

For non-trivial scripts, prefer stdin over command-line quoting.

Search app-local references before unfamiliar calls:

```powershell
rg -i "<keyword>" <app>_adapter/docs <app>_adapter/examples
```

Do not assume ExtendScript has a global `JSON` object. Use the serializer pattern
from the app's `examples/context.jsx` when returning structured data.
