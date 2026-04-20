## Why The Wire is Not MCP


|                    | MCP tool server                             | Shell adapter                                                                |
| -------------------- | --------------------------------------------- | ------------------------------------------------------------------------------ |
| Runtime model      | Run a dedicated MCP server process per app  | No MCP server; run a local bridge command (`*_bridge.py`) on demand          |
| Transport note     | Tool calls route through the MCP server     | COM/direct dispatch or in-app localhost bridge endpoint                      |
| Installation model | Install/configure server stack per app/tool | Single`pip install thewire` provides one CLI usable across many app adapters |
| Surface area       | Predefined tools                            | The app's full scripting API                                                 |
| Tool logic         | Written ahead of time                       | Composed by the agent per task                                               |
| New app support    | Build a server and schemas                  | Add a bridge and adapter notes                                               |
| Version churn      | Keep schemas in sync                        | Rely on stable scripting APIs                                                |
| Policy layer       | Built in by design                          | Not built in; full API access                                                |

MCP is a good fit for a small, audited, policy-controlled tool surface. Shell adapters are better when the goal is broad access to an existing local app API without maintaining a catalog of every possible operation.

For apps that need in-process execution, the shell adapter may use a tiny local HTTP endpoint exposed by an in-app extension. That endpoint is transport, not an MCP tool server: the agent still invokes a normal shell command and sends script code through the same bridge contract.

The two approaches can coexist. An MCP server can wrap an adapter and expose a curated subset of actions when policy or auditability matters.
