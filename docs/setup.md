# Setup and Commands

The Wire is currently packaged for Windows. The bridges connect to running desktop apps by default: it can launch apps when explicitly requested to. 

## Install from PyPI

```powershell
pip install thewire
```

The package installs `pywin32` on Windows for the COM-backed adapters. pip install thewire` installs the bridge code, adapter assets, and modular agent-facing instructions.

Register The Wire with your local agent harness:

```powershell
thewire setup
```

By default, setup detects local harnesses and registers The Wire with all of them, so that the agents are aware of this ability. Use `--agent` when you want to target one harness explicitly.

For deterministic setup:

```powershell
thewire setup --agent codex
thewire setup --agent claude
thewire setup --agent gemini
thewire setup --agent opencode
thewire setup --agent openclaw
```

The `claude` target is shared by Claude Code and Claude Desktop/Cowork. Auto detection still checks them separately.

## Useful Commands

```powershell
thewire adapters
thewire path
thewire setup
thewire agent-docs-path
thewire install-agent-docs codex
thewire install-agent-docs claude
thewire install-agent-docs gemini
thewire install-agent-docs opencode
thewire install-agent-docs openclaw
thewire context houdini
thewire install blender
```

## Run a Context Smoke Test

Use the installed CLI when possible:

```powershell
thewire context photoshop
```

Or run a bridge directly from a source checkout:

```powershell
Get-Content <adapter>/examples/context.<ext> -Raw | python <adapter>/<app>_bridge.py --stdin
```

Open the target app yourself before running the command. Bridges connect to
running instances and will not launch apps unless you pass `--allow-launch`.

## Probe Adobe COM Registration

To see which Adobe COM adapters are registered on your machine:

```powershell
powershell -ExecutionPolicy Bypass -File tools/probe_adobe_com.ps1
```

## Adapter-Specific Setup

Some adapters need an in-app component before the shell bridge can reach the app:

- Premiere Pro, After Effects, and Audition need the CEP bridge panel installed
  and open.
- Blender needs the addon installed and enabled.
- Unity needs the editor package installed into the target project.
- 3ds Max and Houdini need their startup bridges installed and the app
  restarted.

Each adapter's `README.md` has the exact setup details.
