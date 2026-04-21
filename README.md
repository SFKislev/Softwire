<p>
  <img src="docs/images/logo.svg" alt="Softwire logo" width="350" />
</p>

<h1>Agents Running Software</h1>

**A tiny bridge that lets your coding harness drive professional desktop software — Photoshop, Premiere, Blender, Unity, and more — directly from the shell.**

SoftWire gives agentic harnesses — Codex, Claude Code, Gemini CLI, OpenCode and the likes — direct access to the scripting APIs inside professional desktop software. One `pip install softwire && softwire setup` covers many apps across Adobe Creative Cloud, Autodesk, Microsoft Office, and game engines.

[SoftWire is not an MCP server](https://github.com/SFKislev/Softwire/blob/main/docs/mcp.md). The agent sends a script through a small bridge command, the bridge runs it inside the app's own automation runtime, and the app returns JSON.

```text
agent shell -> bridge command -> app scripting runtime -> JSON result
```

This is done without brittle screenshots and without schema definitions. The bridge exposes the scripting layer already built into each application.

<img src="docs/softwire_1.gif" alt="Softwire demo" width="50%" />

## Installation

```powershell
pip install softwire
```

Confirm the installation and see the available commands:

```powershell
softwire
```

If `softwire` is not on PATH in the current shell, use:

```powershell
py -m softwire.cli where
```

Then register SoftWire with your local agent harness:

```powershell
softwire setup
```

This detects your harnesses and informs them that SoftWire exists. For first-run checks, source checkout commands, and app-specific prerequisites, see [Setup and commands](https://github.com/SFKislev/Softwire/blob/main/docs/setup.md).

## Current Adapters


| App           | Adapter                  | Runtime                                          |
| --------------- | -------------------------- | -------------------------------------------------- |
| Photoshop     | `photoshop_adapter/`     | COM to ExtendScript                              |
| InDesign      | `indesign_adapter/`      | COM to ExtendScript                              |
| Illustrator   | `illustrator_adapter/`   | COM to ExtendScript                              |
| Word          | `word_adapter/`          | COM object model                                 |
| Excel         | `excel_adapter/`         | COM object model                                 |
| PowerPoint    | `powerpoint_adapter/`    | COM object model                                 |
| Premiere Pro  | `premiere_adapter/`      | CEP localhost to ExtendScript                    |
| After Effects | `after_effects_adapter/` | CEP localhost to ExtendScript                    |
| Audition      | `audition_adapter/`      | CEP localhost to ExtendScript                    |
| Blender       | `blender_adapter/`       | Addon localhost to `bpy`                          |
| Unity         | `unity_adapter/`         | Editor package to `UnityEditor` and `UnityEngine` |
| 3ds Max       | `3dsmax_adapter/`        | Startup Python localhost to MAXScript             |
| Houdini       | `houdini_adapter/`       | Startup Python localhost to `hou`                 |

## More Docs

- [Full documentation and source](https://github.com/SFKislev/Softwire)
- [Setup and commands](https://github.com/SFKislev/Softwire/blob/main/docs/setup.md)
- [Harness support and discoverability](https://github.com/SFKislev/Softwire/blob/main/docs/harenesses.md)
- [Wait, isn't this called MCP?](https://github.com/SFKislev/Softwire/blob/main/docs/why-shell-adapters.md)

### Documentation for Agents

- [How the Adapters work](https://github.com/SFKislev/Softwire/blob/main/docs/ADAPTER_SPEC.md)
- [How to use the Bridge Contracts](https://github.com/SFKislev/Softwire/blob/main/shared/bridge-contract.md)
- [How to Work Together with a Human](https://github.com/SFKislev/Softwire/blob/main/shared/coexistence.md)
- [Known Issues](https://github.com/SFKislev/Softwire/blob/main/docs/known-issues.md)
