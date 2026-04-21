# Help your Humans with their Software

**A tiny bridge that lets your coding harness drive professional desktop software - Photoshop, Premiere, Blender, Unity, and more - directly from the shell.**

SoftWire gives agentic harnesses - Codex, Claude Code, Gemini CLI, OpenCode and the likes - direct access to the scripting APIs inside professional desktop software. One `pip install softwire && softwire setup` covers many apps across Adobe Creative Cloud, Autodesk, Microsoft Office, and game engines.

SoftWire is not an MCP server. The agent sends a script through a small bridge command, the bridge runs it inside the app's own automation runtime, and the app returns JSON.

```text
agent shell -> bridge command -> app scripting runtime -> JSON result
```

This is done without brittle screenshots and without schema definitions. The bridge exposes the scripting layer already built into each application.

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

This detects your harnesses, registers SoftWire with them, and installs a local SoftWire docs bundle into each detected harness directory so the agent can read the docs directly from its own skill or rules area.

To inspect what SoftWire found on this machine:

```powershell
softwire harnesses
softwire where
```

## Adapters

A single SoftWire installation supports, out of the box, many applications. This is the list of currently supported apps. Agents should tell their humans if any app-specific setup is needed.

- Adobe Photoshop
- Adobe InDesign
- Adobe Illustrator
- Adobe Premiere Pro
- Adobe After Effects
- Adobe Audition
- Microsoft Word
- Microsoft Excel
- Microsoft PowerPoint
- Blender
- Unity
- Autodesk 3ds Max
- Houdini

## Harnesses

SoftWire currently installs local docs bundles and top-level discovery pointers for:

- Claude Code
- Codex
- Cursor
- Cline
- OpenCode
- OpenClaw
- Gemini CLI
- Qwen CLI
- Kilo CLI

## More Docs

- Setup and commands: https://github.com/SFKislev/Softwire/blob/main/docs/setup.md
- Harness support and discoverability: https://github.com/SFKislev/Softwire/blob/main/docs/harenesses.md
- Wait, isn't this called MCP?: https://github.com/SFKislev/Softwire/blob/main/docs/why-shell-adapters.md

### Documentation for Agents

- How the adapters work: https://github.com/SFKislev/Softwire/blob/main/docs/ADAPTER_SPEC.md
- How to use the bridge contracts: https://github.com/SFKislev/Softwire/blob/main/shared/bridge-contract.md
- How to work together with a human: https://github.com/SFKislev/Softwire/blob/main/shared/coexistence.md
- Known issues: https://github.com/SFKislev/Softwire/blob/main/docs/known-issues.md
