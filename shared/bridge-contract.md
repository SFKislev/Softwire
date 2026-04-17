# Bridge Contract

All bridge scripts:

- run from the workspace root
- accept code through argv, `--stdin`, or `--file`
- return JSON on stdout for success
- return JSON on stderr with non-zero exit for failure
- connect to a running app by default
- launch only when `--allow-launch` is explicitly passed
- authenticate local HTTP eval endpoints with an unguessable per-session token
  that the shell bridge reads automatically from a user-scoped session file

Run context first:

```powershell
Get-Content <app>_adapter/examples/context.<jsx|py> -Raw | python <app>_adapter/<app>_bridge.py --stdin
```

For non-trivial scripts, prefer stdin over command-line quoting.

## API Discovery

For any call not already documented by the adapter or local examples, discover
the surface in this order. Do not trust pretraining for version-specific
features.

1. **Introspect the running app.** Write a read-only probe through the bridge
   and enumerate what this version actually exposes: method existence
   (`typeof obj.method === "function"`), available enum constants, `app.version`,
   menu command IDs via `stringIDToTypeID`, and object typenames. The running
   app is the authoritative source for what is callable right now.
2. **Consult the vendor's documentation.** Use web tools when a conceptual
   surface is not obvious from introspection. Match what you find against
   `app.version` before acting; documentation often describes the latest
   version, not the one the user is running.
3. **Search local adapter notes and examples.** Use `rg` for bridge-specific
   constraints, command shapes, and local gotchas. Search optional `docs/`
   only when that directory exists:

   ```powershell
   rg -i "<keyword>" <app>_adapter/APP.md <app>_adapter/examples
   ```
4. **Pretraining last, and flagged.** If you fall back on memory for an API
   name, say so explicitly and confirm it exists via introspection before
   mutating state. Do not invent plausible-sounding method names.

## ExtendScript Note

Do not assume ExtendScript has a global `JSON` object. Use the serializer
pattern from the app's `examples/context.jsx` when returning structured data.
