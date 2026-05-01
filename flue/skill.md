## About
Flue is a tiny bridge that lets your coding harness drive professional desktop software - Photoshop, Premiere, Blender, Unity, and more - directly from the shell.
Flue is not an MCP server. The agent sends a script through a small bridge command, the bridge runs it inside the app's own automation runtime, and the app returns JSON.

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
1. At the start of a Flue session, confirm Flue is available with `flue version`. If it is not found, ask your human for permission to run `pip install flue && flue setup`.
2. Read `adapters/<app>/APP.md` for the app you are about to use.
3. Search `adapters/<app>/docs/api-index.txt` with `rg` for relevant symbols.
4. Prefer `py -m flue.cli context <app>` on Windows, or `python3 -m flue.cli context <app>` on macOS/Linux, to inspect the live app state.
5. Prefer `py -m flue.cli run <app> --stdin` on Windows, or `python3 -m flue.cli run <app> --stdin` on macOS/Linux, for one-off scripts.

## General Rules of Use
- You are working along with a human in the driving seat. Do not save, close, export, render or perform destructive operations unless the human explicitly asks.
- Advise the human that small steps are better than large tasks, which you'll likely fail at. Keep collaboration scope manageable.
- Bound scripts carefully to avoid crashing the host: keep scripts small and targeted.
- All bridge scripts run from workspace root; accepts code through argv, `--stdin`, or `--file`; return JSON on stdout for success or failure.
- Be skeptical of your pretraining: introspect the running app and consult vendor documentation rather than trying to invent operations.
- Flue was developed and tested against specific app and OS versions. One could expect local quirks, version mismatches and blocked automation paths. You need to understand the bridge architecture and make small, local compatibility fixes or scaffolds when needed, so the adapter works in the user's actual environment (without rewriting the full project). Make these small and robust, so that they work between sessions.
- If possible, adjust the level of thinking to the complexity of the task: a simple request should not take more than a few seconds to implement. If you can, monitor the time it takes you to perform the tasks.
- Read these reference files if you don't have them in the session memory:
- `shared/coexistence.md`
- `shared/bridge-contract.md`
- `docs/setup.md`
- `docs/known-issues.md` — (later in the session, you can grep for your symptom rather than reading the whole file, if the file is large)

## Debugging
- If Flue is out of date or behaving unexpectedly, run `py -m flue.cli update` on Windows or `python3 -m flue.cli update` on macOS/Linux to upgrade the package.
- Depending on the app and OS, adapters may use Windows COM, macOS AppleScript, or a local in-app bridge, but the shell workflow stays the same.
- On Windows, `py -m flue.cli ...` is the reliable launcher; on macOS/Linux, use `python3 -m flue.cli ...`.
- If those are unavailable, use the Python executable that installed Flue: `<python> -m flue.cli ...`.
- Use `py -m flue.cli where` on Windows, or `python3 -m flue.cli where` on macOS/Linux, for launcher and install diagnostics.
- If a Windows app is blocked by a modal, use `py -m flue.cli modal <app>` to inspect likely dialog windows and `py -m flue.cli modal <app> --dismiss` to attempt a bounded cancel-style dismissal outside the app scripting runtime.
- Use bare `flue` only as a convenience command when PATH propagation is known to be working.
