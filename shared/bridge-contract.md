# Bridge Contract

All bridge scripts:

- run from the workspace root
- accept code through argv, `--stdin`, or `--file`
- return JSON on stdout for success
- return JSON on stderr with non-zero exit for failure
- connect to a running app by default
- launch only when `--allow-launch` is passed
- authenticate local HTTP eval endpoints with an unguessable per-session token that the shell bridge reads automatically from a user-scoped session file

Run context first:

```powershell
Get-Content adapters/<app>_adapter/examples/context.<jsx|py> -Raw | python adapters/<app>_adapter/<app>_bridge.py --stdin
```

For non-trivial scripts, prefer stdin over command-line quoting.

## Scratch Scripts

Adapter `examples/` directories are reference material, not a place for generated task scripts. Do not add one-off scripts to `adapters/<app>_adapter/examples/` unless the user explicitly asks for a reusable example.

If a bridge script must be materialized as a file, write it to a temp or scratch location such as `.tmp/<app>/` or the OS temp directory, run it with `--file`, and remove it after a successful run unless the user asks to keep it.

## Stuck Bridge Processes

A bridge process can remain alive if the host app blocks inside its scripting runtime or COM dispatch. Do not kill arbitrary Python processes to recover. 

Use the cleanup tool to list and stop only Python processes that are running known adapter bridge scripts from this repo:

```powershell
python tools/cleanup_bridges.py --list
python tools/cleanup_bridges.py --kill stale --older-than 60
python tools/cleanup_bridges.py --app indesign --kill all
```

The cleanup tool matches checked-in `*_bridge.py` paths and ignores unrelated Python processes.

COM-backed bridges run the app call in a watchdog subprocess by default. If the host app blocks inside COM, the bridge should return JSON timeout failure instead of hanging indefinitely. Use `--timeout <seconds>` on the app bridge to adjust the watchdog, or `--timeout 0` only when deliberately allowing a long COM operation.

## API Discovery

For any call not already documented by the adapter or local examples, discover the surface in this order. Do not trust pretraining for version-specific features.

1. **Search the local API index first.** If `adapters/<app>_adapter/docs/api-index.txt` exists, search it with `rg` for relevant symbols before relying on memory. Treat it as a grep-friendly symbol index, not a full manual.

   ```powershell
   rg -i "<keyword>" adapters/<app>_adapter/docs/api-index.txt
   ```

2. **Introspect the running app.** Write a read-only probe through the bridge and enumerate what this version actually exposes: method existence
   (`typeof obj.method === "function"`), available enum constants, `app.version`, menu command IDs via `stringIDToTypeID`, and object typenames. The running app is the authoritative source for what is callable right now.
3. **Consult the vendor's documentation.** Use web tools when a conceptual surface is not obvious from introspection. Match what you find against `app.version` before acting; documentation often describes the latest version, not the one the user is running.
4. **Search local adapter notes and examples.** Use `rg` for bridge-specific constraints, command shapes, and local gotchas. Search optional `docs/` only when that directory exists:

   ```powershell
   rg -i "<keyword>" adapters/<app>_adapter/APP.md adapters/<app>_adapter/examples adapters/<app>_adapter/docs
   ```
5. **Pretraining last, and flagged.** If you fall back on memory for an API name, say so explicitly and confirm it exists via introspection before mutating state. Do not invent plausible-sounding method names.

## ExtendScript Note

Do not assume ExtendScript has a global `JSON` object. Use the serializer pattern from the app's `examples/context.jsx` when returning structured data.
