# Houdini Adapter Instructions

Before operating Houdini, read:

1. `../shared/coexistence.md`
2. `../shared/bridge-contract.md`
3. `APP.md`

Then run:

```powershell
Get-Content houdini_adapter/examples/context.py -Raw | python houdini_adapter/houdini_bridge.py --stdin
```

Use `examples/` as reference material only. Pass one-off scripts through
`--stdin` unless a temporary file is required.
