# Creative Software Adapters

This repo proves a simple pattern:

```text
coding agent + shell + local app scripting bridge = live creative software control
```

No MCP server, custom agent runtime, or app-specific tool schema is required.
Each adapter is a small folder that exposes the app's native scripting runtime
through the shell.

## Architecture

Each app adapter has:

- A tiny bridge script that connects to the running creative app.
- An `APP.md` file for app-specific bridge notes and gotchas.
- Local docs and examples that the agent can search with `rg`.

Shared interaction rules live in:

```text
shared/coexistence.md
shared/bridge-contract.md
```

Shared Windows COM bridge code lives in:

```text
creative_adapters/com_bridge.py
```

The app-specific bridge wrappers only declare:

- app name
- COM ProgID
- Windows process name
- script execution method
- optional script language id

## Current Adapters

| App | Folder / Bridge | Runtime |
|---|---|---|
| Photoshop | `photoshop_adapter/photoshop_bridge.py` | COM `Photoshop.Application` -> `DoJavaScript` |
| InDesign | `indesign_adapter/indesign_bridge.py` | COM `InDesign.Application` -> `DoScript(JavaScript)` |
| Illustrator | `illustrator_adapter/illustrator_bridge.py` | COM `Illustrator.Application` -> `DoJavaScript` |

## Install

Windows prerequisites:

```powershell
pip install pywin32
```

Then open the creative app yourself. The bridges connect to running instances by
default and do not launch apps unless `--allow-launch` is explicitly passed.

## Probe Local Machine

Check which Adobe COM adapters are registered:

```powershell
powershell -ExecutionPolicy Bypass -File tools/probe_adobe_com.ps1
```

## First Tests

Photoshop:

```powershell
Get-Content photoshop_adapter/examples/context.jsx -Raw | python photoshop_adapter/photoshop_bridge.py --stdin
```

InDesign:

```powershell
Get-Content indesign_adapter/examples/context.jsx -Raw | python indesign_adapter/indesign_bridge.py --stdin
```

Illustrator:

```powershell
Get-Content illustrator_adapter/examples/context.jsx -Raw | python illustrator_adapter/illustrator_bridge.py --stdin
```

## Coexistence Rules

See `shared/coexistence.md`.
