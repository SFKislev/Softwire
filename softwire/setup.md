# Setup and Commands

SoftWire connects agents to running desktop apps through local bridge commands.
The bridges connect to running apps by default and launch only when an adapter
explicitly supports it and the user asks for it.

## Install from PyPI

```powershell
pip install softwire
softwire setup
```

The package installs the bridge code, adapter assets, and modular
agent-facing instructions. On Windows, it also installs `pywin32` for
COM-backed adapters.

By default, setup detects local harnesses and registers SoftWire with all of
them. It also installs a local SoftWire docs bundle into each detected harness
directory so the agent can read the docs directly from its own skill or rules
area.

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

Harness-by-harness discoverability details are documented in
[Harness support and discoverability](harenesses.md).

## Useful Commands

```powershell
softwire adapters
softwire where
softwire harnesses
softwire setup
py -m softwire.cli update
softwire uninstall
softwire context houdini
softwire modal photoshop
softwire modal photoshop --dismiss
softwire install blender
```

## Update SoftWire

Use the module form to upgrade the Python package. If the package version
changes, it also refreshes the installed agent-facing docs bundles:

```powershell
py -m softwire.cli update
```

This runs `pip install --upgrade softwire`, compares the installed version
before and after the upgrade, then runs `softwire setup --force` from a fresh
Python process only when the package changed. Use
`py -m softwire.cli update --force-docs` to refresh docs even when the package is already
current.

On Windows, avoid running package updates through `softwire update`; the
`softwire.exe` launcher can be locked while pip tries to replace it.

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

## Recover a Blocking Modal

When an app is stuck behind a modal dialog, the scripting bridge may time out
while the host app is still waiting for UI input. Inspect the app's current
top-level windows with:

```powershell
softwire modal photoshop
```

To attempt a safe cancel-style dismissal of the most likely blocking dialog:

```powershell
softwire modal photoshop --dismiss
```

Use `--action escape` to send only Escape, or `--action close` when you
explicitly want to try a direct window close request.

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
