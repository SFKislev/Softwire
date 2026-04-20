# Why Shell Adapters

CLI coding harnesses allow agents to edit files, run commands, search a repository, and iterate on failures. They cannot, however, act inside a running desktop application, because those apps expose automation through their own internal runtime: ExtendScript, `bpy`, MAXScript, the Unity Editor API, COM object models, or a similar scripting surface. These surfaces have been maintained for decades, and are very often featured packed: they can do most of what the software can.

SoftWire connects those two worlds. The agent keeps using the shell; the bridge
takes code on stdin, passes it into the live application, and returns structured
JSON. The agent can inspect the result, adjust the script, and iterate.

## Why This Matters

Professional work still happens in large desktop applications: Photoshop, Premiere Pro, Blender, Unity, 3ds Max, Houdini, Illustrator, InDesign, Office, and so forth. These tools already have stable automation APIs, but using those APIs directly has historically required a specialist who knows the app's object model.

Agents can use this evolved legacy automation layer. They can read adapter notes, inspect the live document, search examples, compose one-off scripts, run them, and handle errors. The user asks for an outcome in natural language; the agent finds the object-model calls.

SoftWire runs locally, with no cloud service and no complicated setup, and lets the agent drive the app you're already working in. From restructuring a layered Photoshop file to rewriting a Blender scene graph: whatever the scripting API can do (which is most of what the app itself can do), the agent can now do with you.

Through a simple pip install and set of tiny bridges, the agent becomes a working partner inside the app. It reads the live state, edits structure, and responds to "undo that and try the other approach" the way it would in a codebase. You no longer have to find that function in that submenu. You say what you want; the agent finds the right object-model call, wraps it in `suspendHistory` (so Ctrl+Z still works), and runs it. Without ExtendScript and without a menu hunt.

Scripting APIs, unlike UIs, are stable across versions. Their original audience was plugin developers and studio TDs who were willing to read the reference because they'd reuse the script a hundred times. Agents can read the reference on demand and compose a one-time call. They write a piece of code to run that one-time operation, and gladly throw it away.

The back door that was built for power users turns out to work fine as a front door.

## General Pattern

The pattern works for apps with a scripting surface the shell can reach. That means practically all creative software: Adobe Creative Cloud apps through COM or CEP, DCC tools such as Blender, Houdini, Maya, Cinema 4D, and 3ds Max, CAD and design tools with local scripting APIs, game engines such as Unity or Unreal, GIS and scientific tools such as QGIS, and Office apps through COM or VBA. Exposing the internal automation layer is a simple and semi-universal solution for cli-to-software communication.

## Transport Choices

When an app exposes `DoJavaScript`, `DoScript`, or an object model over COM, the
adapter can use `bridges/com_bridge.py`. This is the simplest communication path.

When an app requires in-process execution, the adapter can ship a small in-app
extension and use `bridges/local_http_bridge.py` with a tokenized
localhost transport. This is the pattern used by apps such as Premiere Pro,
After Effects, Audition, Blender, Unity, 3ds Max, and Houdini.

The shell contract stays the same: script in through argv, `--stdin`, or`--file`; JSON out on success; JSON error on failure.

## MCP vs. SoftWire

SoftWire is not an MCP server.


|                    | MCP tool server                             | Shell adapter                                                                |
| -------------------- | --------------------------------------------- | ------------------------------------------------------------------------------ |
| Runtime model      | Run a dedicated MCP server process per app  | No MCP server; run a local bridge command (`*_bridge.py`) on demand          |
| Transport note     | Tool calls route through the MCP server     | COM/direct dispatch or in-app localhost bridge endpoint                      |
| Installation model | Install/configure server stack per app/tool | Single `pip install softwire` provides one CLI usable across many app adapters |
| Surface area       | Predefined tools                            | The app's full scripting API                                                 |
| Tool logic         | Written ahead of time                       | Composed by the agent per task                                               |
| New app support    | Build a server and schemas                  | Add a bridge and adapter notes                                               |
| Version churn      | Keep schemas in sync                        | Rely on stable scripting APIs                                                |
| Policy layer       | Built in by design                          | Not built in; full API access                                                |

MCP is a good fit for a small, audited, policy-controlled tool surface. Shell adapters are better when the goal is broad access to an existing local app API without maintaining a catalog of every possible operation.

For apps that need in-process execution, the shell adapter may use a tiny local HTTP endpoint exposed by an in-app extension. That endpoint is transport, not an MCP tool server: the agent still invokes a normal shell command and sends script code through the same bridge contract.

The two approaches can coexist. An MCP server can wrap an adapter and expose a curated subset of actions when policy or auditability matters.
