# Blender Adapter Prototype

Blender exposes its scripting surface through in-process Python (`bpy`), so the
adapter is a small Blender addon rather than a COM or CEP bridge.

## Shape

```text
Blender
  Creative Adapter Bridge addon
    bpy Python on Blender's main thread
    local eval endpoint + per-session token file

Shell
  python blender_adapter/blender_bridge.py --stdin
```

## Install Addon

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File blender_adapter/install_addon.ps1
```

Then open Blender and enable:

```text
Edit > Preferences > Add-ons > Creative Adapter Bridge
```

When the addon starts, it writes:

```text
%APPDATA%\creative-adapters\blender.json
```

The shell bridge reads that file automatically and sends `X-Bridge-Token`.
Users should not need to copy or manage tokens or ports.

## First Live Test

```powershell
Get-Content blender_adapter/examples/context.py -Raw | python blender_adapter/blender_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Blender", "...": "..."}}
```

## Directed Mode

This first adapter intentionally implements the directed-mode floor: execute
bounded Python against the active Blender session, read context, and mutate the
current scene/selection on request. Exploratory endpoints such as object
filters, spatial queries, viewport projection, snapshots, and change deltas are
the next tier.
