# Setup and Commands

SoftWire is currently packaged for Windows. The bridges connect to running desktop apps by default: it can launch apps when explicitly requested to. 

## Install from PyPI

```powershell
pip install softwire
```

The package installs `pywin32` on Windows for the COM-backed adapters. `pip install softwire` installs the bridge code, adapter assets, and modular agent-facing instructions.

Register SoftWire with your local agent harness:

```powershell
softwire setup
```

By default, setup detects local harnesses and registers SoftWire with all of them, so that the agents are aware of this ability. Use `--agent` when you want to target one harness explicitly.

For deterministic setup:

```powershell
softwire setup --agent codex
softwire setup --agent claude
softwire setup --agent gemini
softwire setup --agent qwen
softwire setup --agent cursor
softwire setup --agent kilo
softwire setup --agent opencode
softwire setup --agent openclaw
```

The `claude` target is for Claude Code. Claude Desktop/Cowork is not supported.
The `kilo` target installs a global skill at `~/.kilo/skills/softwire/SKILL.md`.

Harness-by-harness discoverability details are documented in [Harness support and discoverability](harenesses.md).

## Useful Commands

```powershell
softwire adapters
softwire path
softwire setup
softwire agent-docs-path
softwire install-agent-docs codex
softwire install-agent-docs claude
softwire install-agent-docs gemini
softwire install-agent-docs qwen
softwire install-agent-docs cursor
softwire install-agent-docs kilo
softwire install-agent-docs opencode
softwire install-agent-docs openclaw
softwire context houdini
softwire install blender
```

## Run a Context Smoke Test

Use the installed CLI when possible:

```powershell
softwire context photoshop
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
