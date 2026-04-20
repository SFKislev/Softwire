# SoftWire

SoftWire gives agents shell access to the scripting APIs of large desktop
apps, so they can inspect live app state and make targeted edits without MCP
servers or UI automation.

## Required Workflow

1. Run `softwire path` to find the installed adapter root.
2. Read these files from that root before operating an app:
   - `shared/coexistence.md`
   - `shared/bridge-contract.md`
   - `adapters/<app>_adapter/APP.md`
3. Run context before acting:

```powershell
softwire context <app>
```

Run one-off scripts through stdin:

```powershell
Get-Content .\script.py -Raw | softwire run <app> --stdin
```

If context fails, read the app's `APP.md` and follow `Connection recovery`.

Do not launch, save, close, export, render, switch projects/files, or perform
destructive operations unless the user explicitly asks.

## Safety

Scripts run inside the desktop app. Poorly bounded scripts can make the app
slow, bloated, modal, or unstable even if the shell bridge times out. Keep
scripts small and targeted. Avoid unbounded enumeration, broad scans, expensive
layout/render/media work, full asset-library searches, and open-ended loops.
Prefer narrow probes, caps, filters, active selections, known object names, and
incremental verification.

For unknown APIs, introspect the running app with a small read-only probe, then
consult official app scripting/API docs for the detected version. Use model
memory last and verify uncertain API names before mutating live state.

If a task is large, complex, multi-step, or too autonomous to verify safely in
one script run, recommend 1-2 observable steps at a time. SoftWire usually
cannot visually inspect final results.

Report bridge and app errors directly. After a successful edit, run context or
a targeted verification script and summarize the important result.
