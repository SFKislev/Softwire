# Creative Software Adapters

Professional software has been shipping rich internal scripting layers for
decades: ExtendScript in Adobe apps, Python in Blender / Maya / Resolve,
MAXScript in 3ds Max, AppleScript in macOS apps, COM in Office. These runtimes
were built as a back door for developers automating batch workflows. They are
now the best front door for an LLM.

This repo proves a small, sharp claim:

```text
coding agent (Claude Code, Codex, Cursor, Opencode)
  + shell
  + a ~120-line local bridge into the app's own scripting runtime
  = natural-language control of a live, running professional app.
```

No MCP server, no custom agent runtime, no per-app tool schema, no plugin
marketplace. Each adapter is a small folder that exposes the app's native
scripting runtime through the shell. The agent composes scripts itself, runs
them through the bridge, reads JSON back, and iterates.

## Why This Is Useful

Most time inside professional software is not spent *doing* the work. It is
spent *finding* where the work lives:

- "Where is Liquify in this version again?"
- "How do I sync all four margins to 10mm in InDesign?"
- "What's the exact blend mode dropdown path?"
- "Where did they move the gradient-to-transparent tool?"

The dominant UX of creative software is a whack-a-mole game against menu
reshuffles, renamed panels, and forum threads from 2017 that no longer apply.
Power users maintain private snippet libraries just to short-circuit this.

The scripting API, by contrast, is stable across versions. A coding agent
pointed at that API collapses the find-it loop into a single turn:

```text
User:  "Set the active Photoshop layer to 40% opacity, multiply blend mode."
Agent: reads live context, finds the object-model call, wraps it in
       suspendHistory so Ctrl+Z still works, runs it, reports what happened.
```

The user never learns ExtendScript, never opens a menu, never leaves the app.

## What's Actually Novel

Scripting hosts like ExtendScript, Blender's `bpy`, Maya Python, and
AppleScript have existed for 20-30 years. Their audience was plugin developers
and studio TDs: people who already read the reference and were willing to pay
the cost of writing a script for a task they'd do a hundred times.

What changed is who can pull that door open. An LLM in an agent harness reads
the reference on demand, composes the call from a natural-language request,
handles the JSON error on failure, and iterates. A 30-year-old back door built
for devs automating 100x workflows has just become the best front door for end
users doing 1x tasks.

The contribution of this repo is the minimal proof of that claim:

- The bridge is disproportionately small (~120 lines, shared across apps)
  because the hard work was pre-paid by decades of vendor investment in
  scripting APIs.
- The adapter shape is three files: a bridge wrapper, an `APP.md` of
  non-obvious facts, and a few curated examples the agent can `rg` against.
- The agent harness is unmodified. Any agent with a shell and file tools works.

## Generalizability

The pattern applies to any application that exposes a scripting surface the
shell can reach. That set is large, and it covers most of what professionals
use all day:

- Design: Photoshop, Illustrator, InDesign, Figma (via plugin bridge), Sketch
- Video: Premiere Pro, After Effects, DaVinci Resolve, Final Cut (AppleScript)
- 3D / DCC: Blender, Maya, Houdini, Cinema 4D, 3ds Max, Modo
- CAD: Fusion 360, SolidWorks, Rhino, FreeCAD
- Audio: Audition, Reaper, Ableton Live (via Max / Remote Scripts), Logic (AppleScript)
- GIS / science: QGIS, ArcGIS, MATLAB, Mathematica, ImageJ/Fiji, ParaView
- Office / productivity: Word, Excel, PowerPoint, Outlook (COM/VBA)

When the app exposes `DoJavaScript` / `DoScript` over COM (many Adobe apps on
Windows), the bridge is the shared COM wrapper in
`creative_adapters/com_bridge.py`. When it needs in-app execution (Premiere Pro,
After Effects, Audition, Blender, 3ds Max), the adapter ships a tiny in-app
extension/addon/startup script and uses `creative_adapters/local_http_bridge.py`
for the external tokenized shell client. The same shell contract remains:
stdin/file/argv in, JSON out. The agent-facing interface does not change.

Apps that do not expose a scripting layer (most consumer SaaS, most mobile
apps, many games) are out of scope for this pattern. That's an honest limit,
not a hidden one.

## Isn't This Called MCP?

No, and the distinction matters.

MCP (Model Context Protocol) is a protocol for a model to talk to a **tool
server** that exposes a **fixed catalog of named tools** with declared
schemas. You write a server, register tools, the agent picks from them.

This repo does not do that. There is no tool server, no tool catalog, and no
schema registration. The agent already has a shell; it calls a small local CLI
the same way it would call `git` or `rg`, and everything else happens inside
the app's own scripting runtime.

Practical differences:

| | MCP tool server | Adapter (this repo) |
|---|---|---|
| Surface area | Handful of pre-named tools | The app's entire scripting API |
| Who writes tool logic | You, per tool, in the server | The agent, per request, in the app's script language |
| Effort to add a new app | Build a server, define every tool, keep schemas current | Copy a 10-line bridge wrapper, write an `APP.md` |
| Effort to add a new capability | Add a tool, redeploy | Already there; the agent just calls the API |
| Version churn | You re-sync schemas when the vendor changes things | Vendors rarely break scripting APIs; UI churn is irrelevant |
| Audit / allowlist | Built into the server | Not built in; the agent has full API access by design |
| Runtime dependency | MCP client in the agent | `python` and a shell |

MCP is the right answer when you want a small, enforceable, auditable tool
surface (enterprise deployments, hosted agents, policy boundaries). The
adapter pattern is the right answer when you want **full coverage of an
existing scripting API with zero schema maintenance**, which is exactly what
individual professionals working in their own apps want.

The two can coexist: an MCP server could wrap an adapter and expose a
curated subset of its capabilities with policy on top. But for a solo
operator driving their own Photoshop, the MCP layer is ceremony around
something the shell already does.

## Architecture

Each app adapter has:

- A tiny bridge script that connects to the running app and executes code.
- An `APP.md` with app-specific bridge notes and known quirks.
- `docs/` and `examples/` that the agent searches with `rg` before acting.

Shared, app-agnostic rules for agents live in:

```text
shared/coexistence.md       # how to behave around a live human operator
shared/bridge-contract.md   # how every bridge is invoked
```

Shared Windows COM bridge code lives in:

```text
creative_adapters/com_bridge.py
```

Shared tokenized localhost bridge client code for CEP-backed adapters lives in:

```text
creative_adapters/local_http_bridge.py
```

App-specific bridge wrappers only declare:

- app name
- COM ProgID (or alternate transport)
- Windows process name
- script execution method
- optional script language id

The full adapter spec, including the non-COM case, is in `ADAPTER_SPEC.md`.

## Current Adapters

| App | Folder / Bridge | Runtime |
|---|---|---|
| Photoshop | `photoshop_adapter/photoshop_bridge.py` | COM `Photoshop.Application` -> `DoJavaScript` |
| InDesign | `indesign_adapter/indesign_bridge.py` | COM `InDesign.Application` -> `DoScript(JavaScript)` |
| Illustrator | `illustrator_adapter/illustrator_bridge.py` | COM `Illustrator.Application` -> `DoJavaScript` |
| Premiere Pro | `premiere_adapter/premiere_bridge.py` | CEP localhost bridge -> `evalScript` |
| After Effects | `after_effects_adapter/after_effects_bridge.py` | CEP localhost bridge -> `evalScript` |
| Audition | `audition_adapter/audition_bridge.py` | CEP localhost bridge -> `evalScript` |
| Blender | `blender_adapter/blender_bridge.py` | Blender addon localhost bridge -> `bpy` |
| 3ds Max | `3dsmax_adapter/3dsmax_bridge.py` | startup Python localhost bridge -> `MaxPlus` / MAXScript |

Premiere, After Effects, and Audition are included specifically because they do **not**
expose the same practical `DoJavaScript` over COM bridge as Photoshop,
InDesign, and Illustrator. Their adapters ship small in-app CEP extensions, and
the external bridge commands keep the same shell contract. Same agent
interface, different transport.

## Install

Windows prerequisites:

```powershell
pip install pywin32
```

Then open the creative app yourself. The bridges connect to running instances
by default and do not launch apps unless `--allow-launch` is explicitly
passed.

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

Premiere Pro:

```powershell
Get-Content premiere_adapter/examples/context.jsx -Raw | python premiere_adapter/premiere_bridge.py --stdin
```

Premiere requires installing and opening the CEP bridge panel first; see
`premiere_adapter/README.md`.

After Effects:

```powershell
Get-Content after_effects_adapter/examples/context.jsx -Raw | python after_effects_adapter/after_effects_bridge.py --stdin
```

After Effects requires installing and opening the CEP bridge panel first; see
`after_effects_adapter/README.md`.

Audition:

```powershell
Get-Content audition_adapter/examples/context.jsx -Raw | python audition_adapter/audition_bridge.py --stdin
```

Audition requires installing and opening the CEP bridge panel first; see
`audition_adapter/README.md`.

Blender:

```powershell
Get-Content blender_adapter/examples/context.py -Raw | python blender_adapter/blender_bridge.py --stdin
```

Blender requires installing and enabling the addon first; see
`blender_adapter/README.md`.

3ds Max:

```powershell
Get-Content 3dsmax_adapter/examples/context.py -Raw | python 3dsmax_adapter/3dsmax_bridge.py --stdin
```

3ds Max requires installing the startup bridge and restarting Max first; see
`3dsmax_adapter/README.md`.

## Coexistence Rules

The user is working in the app while the agent acts through the bridge. See
`shared/coexistence.md` for the full rules. The short version:

- Read live context before acting.
- Act only on the active document, current selection, or an explicitly named
  object.
- Do not save, close, export, package, relink, switch documents, or launch
  apps unless asked.
- Prefer structural API writes over UI automation.
- Keep errors in the terminal and report scripting limitations honestly.
