# Coding Agents Can Control Photoshop Now
 
**A tiny bridge that lets your coding harness drive professional creative software — Photoshop, Premiere, Blender, Unity, and more — directly from the shell.**
 
A shell-based coding agent like Codex, Claude Code, or Gemini CLI can run commands, but it can't reach into a running Photoshop, Blender, or Premiere. Those apps expose automation through their own scripting runtime (ExtendScript, `bpy`, MAXScript, the Unity C# Editor API), not the shell.
 
This repo is the wire between them. A small bridge per app, around 120 lines and mostly shared, takes code on stdin, runs it inside the live application, and returns JSON. The agent reads the JSON and iterates.
 
```text
agent (shell)  →  bridge  →  app's scripting runtime  →  JSON result
```
 
No screenshots, no UI automation, no MCP server, no schemas to maintain. The scripting runtimes have existed for 20 to 30 years. This is the missing wire.
 
## Why this matters
 
Coding agents are already good at editing code, running commands, and orchestrating tools. What they can't do, out of the box, is act inside the large legacy applications where most professional creative work actually happens. Photoshop, Premiere, Blender, 3ds Max, Unity: decades of irreplaceable software that a shell-based agent has no hands in.
 
This bridge gives it hands. It runs locally on your machine, with no cloud service and no complicated setup, and lets the agent drive the app you're already working in. Restructure a layered Photoshop file. Fix timecode drift across a Premiere project. Rewire a Blender scene graph. Refactor a Unity scene. Whatever the scripting API can do (which is most of what the app itself can do), the agent can now do with you.
 
Two things happen at once. The agent becomes a real working partner inside the app. It reads the live state, edits structure, and responds to "undo that and try the other approach" the way it would in a codebase. And the find-it-in-the-menu tax disappears. You say what you want; the agent finds the right object-model call, wraps it in `suspendHistory` so Ctrl+Z still works, and runs it. No ExtendScript, no menu hunt, no 2017 forum thread about a dialog that's been renamed three times since.
 
Scripting APIs, unlike UIs, are stable across versions. Their original audience was plugin developers and studio TDs who were willing to read the reference because they'd reuse the script a hundred times. That assumption doesn't hold anymore. An agent reads the reference on demand, composes the call, handles the error, tries again. The back door that was built for power users turns out to work fine as a front door.
 
## Generalizability
 
The pattern works for any app with a scripting surface the shell can reach, which covers most professional software: Adobe Creative Cloud, the DCC stack (Blender, Maya, Houdini, C4D, 3ds Max), CAD (Fusion 360, Rhino, SolidWorks), audio (Reaper, Ableton, Logic), game engines (Unity, Unreal, Godot), GIS and science tools (QGIS, MATLAB, ImageJ), and Office via COM/VBA.
 
When the app exposes `DoJavaScript` or `DoScript` over COM, which is most Adobe apps on Windows, the bridge is `creative_adapters/com_bridge.py`. When it needs in-app execution (Premiere, After Effects, Audition, Blender, Unity, 3ds Max), the adapter ships a tiny in-app extension and uses `creative_adapters/local_http_bridge.py` with a tokenized localhost transport. The shell contract is the same either way: stdin/file/argv in, JSON out.
 
Apps without a scripting layer (most consumer SaaS, mobile apps, most games) are out of scope.
 
## Isn't this MCP?
 
No. MCP exposes a fixed catalog of named tools with declared schemas, served by a tool server. This repo has no server, no catalog, no schemas. The agent already has a shell; it calls a small local CLI the same way it calls `git`, and everything else happens inside the app's own scripting runtime.
 
| | MCP tool server | Adapter (this repo) |
|---|---|---|
| Surface area | Pre-named tools | The app's entire scripting API |
| Tool logic written by | You, per tool | The agent, per request |
| Adding a new app | Build server, define every tool | Copy a 10-line wrapper, write `APP.md` |
| Version churn | Re-sync schemas when vendors change things | Scripting APIs rarely break |
| Audit and allowlist | Built in | Not built in; full API access by design |
 
MCP is the right answer when you need a small, auditable tool surface with policy on top, which is usually an enterprise requirement. Adapters are the right answer when you want full coverage of an existing scripting API without maintaining schemas for it. The two can coexist: an MCP server can wrap an adapter to expose a curated subset with policy on top.
 
## Architecture
 
Each adapter has a small bridge script, an `APP.md` with app-specific context, and an `examples/` smoke test. Adapters may also include `docs/sources.md` when there are useful reference links. Shared, app-agnostic rules live in `shared/coexistence.md` (how to behave around a live human operator) and `shared/bridge-contract.md` (how every bridge is invoked). Shared bridge code lives in `creative_adapters/`. App wrappers only declare the app name, COM ProgID or alternate transport, Windows process name, and script execution method. Full spec in `ADAPTER_SPEC.md`.
 
## Current adapters
 
| App | Bridge | Runtime |
|---|---|---|
| Photoshop | `photoshop_adapter/` | COM → `DoJavaScript` |
| InDesign | `indesign_adapter/` | COM → `DoScript(JavaScript)` |
| Illustrator | `illustrator_adapter/` | COM → `DoJavaScript` |
| Word | `word_adapter/` | COM → Python object model |
| Excel | `excel_adapter/` | COM → Python object model |
| Premiere Pro | `premiere_adapter/` | CEP localhost → `evalScript` |
| After Effects | `after_effects_adapter/` | CEP localhost → `evalScript` |
| Audition | `audition_adapter/` | CEP localhost → `evalScript` |
| Blender | `blender_adapter/` | Addon localhost → `bpy` |
| Unity | `unity_adapter/` | Editor package localhost → `UnityEditor`/`UnityEngine` |
| 3ds Max | `3dsmax_adapter/` | Startup Python localhost → MAXScript |
 
## Install and first test
 
Prerequisites (Windows):
 
```powershell
pip install pywin32
```
 
Open the target app yourself. Bridges connect to running instances and won't launch apps unless you pass `--allow-launch`.
 
To see which Adobe COM adapters are registered on your machine:
 
```powershell
powershell -ExecutionPolicy Bypass -File tools/probe_adobe_com.ps1
```
 
Smoke-test any adapter by piping its example context script to its bridge. The pattern is the same for all of them:
 
```powershell
Get-Content <adapter>/examples/context.<ext> -Raw | python <adapter>/<n>_bridge.py --stdin
```
 
The CEP-backed adapters (Premiere, After Effects, Audition) need the bridge panel installed and open first. Blender needs the addon enabled. Unity needs the package installed into the target project. 3ds Max needs the startup bridge installed and Max restarted. Each adapter's `README.md` has the details.
 
## Coexistence
 
You're working in the app while the agent acts through the bridge, so the agent has to behave. Full rules in `shared/coexistence.md`. The short version: read live context before acting; only touch the active document, current selection, or an explicitly named object; never save, close, export, relink, or switch documents unless asked; prefer structural API writes over UI automation.
 
## Where this is going
 
The immediate goal of this repo is to let an agent do real work inside one creative app without a lot of setup. The broader observation behind it is that most of the heavy software on a professional's machine already has a stable, well-documented automation surface. It was built for plugin developers, it mostly got left alone, and now it turns out to be exactly what a coding agent needs to be useful inside that software.
