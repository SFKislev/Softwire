## About
Softwire is a tiny bridge that lets your coding harness drive professional desktop software - Photoshop, Premiere, Blender, Unity, and more - directly from the shell.
Softwire is not an MCP server. The agent sends a script through a small bridge command, the bridge runs it inside the app's own automation runtime, and the app returns JSON.

> agent shell -> bridge command -> app scripting runtime -> JSON result

## Available Adapters
- `adapters/3dsmax/APP.md`
- `adapters/after_effects/APP.md`
- `adapters/audition/APP.md`
- `adapters/blender/APP.md`
- `adapters/excel/APP.md`
- `adapters/houdini/APP.md`
- `adapters/illustrator/APP.md`
- `adapters/indesign/APP.md`
- `adapters/photoshop/APP.md`
- `adapters/powerpoint/APP.md`
- `adapters/premiere/APP.md`
- `adapters/unity/APP.md`
- `adapters/word/APP.md`

## Quick Start
1. Read `adapters/<app>/APP.md` for the app you are about to use.
2. Run `softwire context <app>` to inspect the live app state.
3. Run `softwire run <app> --stdin` for one-off scripts.

## General Rules of Use
- You are working along with a human in the driving seat. Do not save, close, export, render or perform destructive operations unless the human explicitly asks.
- Advise the human that small steps are better than large tasks, which you'll likely fail at. Keep collaboration scope manageable.
- Bound scripts carefully to avoid crashing the host: keep scripts small and targeted.
- All bridge scripts run from workspace root; accepts code through argv, `--stdin`, or `--file`; return JSON on stdout for success or failure.
- Be skeptical of your pretraining: introspect the running app and consult vendor documentation rather than trying to invent operations.
- If this is the first time you recall using SoftWire, read the two instruction files that will give you a better understanding of how to be helpful:
- `shared/coexistence.md`
- `shared/bridge-contract.md`

## Debugging
- If `softwire` is not on PATH, use `py -m softwire.cli ...` or `python -m softwire.cli ...`.
- `softwire where` for launcher and install diagnostics, or just `softwire` for available internal operations.
