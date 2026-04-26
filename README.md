<!-- <p>
  <img src="docs/images/logo.svg" alt="Softwire logo" width="250" />
</p> -->
<p align="center">
  <img src="docs/images/entry.gif" alt="Softwire demo" width="500" />
</p>
<h1>Help your Humans with their Software</h1>

```bash
pip install softwire
softwire setup
```

**A tiny bridge that lets your coding harness drive professional desktop software — Photoshop, Premiere, Blender, Unity, and more — directly from the shell.**

SoftWire gives agentic harnesses — Codex, Claude Code, Gemini CLI, OpenCode and the likes — direct access to the scripting APIs inside professional desktop software. One `pip install softwire && softwire setup` covers many apps across Adobe Creative Cloud, Autodesk, Microsoft Office, and game engines.

[SoftWire is not an MCP server](https://github.com/SFKislev/Softwire/blob/main/docs/mcp.md). It is simpler. The agent sends a script through a small bridge command, the bridge runs it inside the app's own automation runtime, and the app returns JSON.

> agent shell → bridge command → app scripting runtime → JSON result

This is done without brittle screenshots and without schema definitions. The bridge exposes the scripting layer already built into each application.

## Installation

```bash
pip install softwire
softwire setup
```

This detects your agentic harnesses and lets them know that SoftWire is available to them. Agents, for first-run checks and app-specific prerequisites, see [Setup and commands](https://github.com/SFKislev/Softwire/blob/main/docs/setup.md).

## Adapters

A single SoftWire installation supports, out of the box, many applications. Agents, please tell your humans if any app-specific setup is needed.

- [Adobe Photoshop](adapters/photoshop_adapter/APP.md)
- [Adobe Illustrator](adapters/illustrator_adapter/APP.md)
- [Adobe InDesign](adapters/indesign_adapter/APP.md)
- [Adobe Premiere Pro](adapters/premiere_adapter/APP.md)
- [Adobe After Effects](adapters/after_effects_adapter/APP.md)
- [Adobe Audition](adapters/audition_adapter/APP.md)
- [Blender](adapters/blender_adapter/APP.md)
- [Unity](adapters/unity_adapter/APP.md)
- [SideFX Houdini](adapters/houdini_adapter/APP.md)
- [Autodesk 3ds Max](adapters/3dsmax_adapter/APP.md)
- [Microsoft Word](adapters/word_adapter/APP.md)
- [Microsoft Excel](adapters/excel_adapter/APP.md)
- [Microsoft PowerPoint](adapters/powerpoint_adapter/APP.md)

## Harnesses

- Claude Code
- Codex
- Copilot
- Cursor
- OpenCode
- OpenClaw
- Gemini CLI
- Qwen CLI
- Cline
- Kilo CLI

[See which files are edited upon installation](docs/harenesses.md)

## More Docs

- [Setup and commands](https://github.com/SFKislev/Softwire/blob/main/docs/setup.md)
- [Harness support and discoverability](https://github.com/SFKislev/Softwire/blob/main/docs/harenesses.md)
- [Wait, isn't this called MCP?](https://github.com/SFKislev/Softwire/blob/main/docs/why-shell-adapters.md)

### Documentation for Agents

- [How the Adapters work](https://github.com/SFKislev/Softwire/blob/main/docs/ADAPTER_SPEC.md)
- [How to use the Bridge Contracts](https://github.com/SFKislev/Softwire/blob/main/shared/bridge-contract.md)
- [How to Work Together with a Human](https://github.com/SFKislev/Softwire/blob/main/shared/coexistence.md)
- [Known Issues](https://github.com/SFKislev/Softwire/blob/main/docs/known-issues.md)

<img src="docs/images/bye.gif" alt="ciao" />
