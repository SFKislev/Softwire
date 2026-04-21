# Unity Notes

Bridge:

```powershell
python adapters/unity_adapter/unity_bridge.py --stdin
```

Runtime: Unity Editor package -> tokenized localhost command endpoint ->
`UnityEditor` / `UnityEngine` C# code on the Editor main thread.

Context:

```powershell
Get-Content adapters/unity_adapter/examples/context.json -Raw | python adapters/unity_adapter/unity_bridge.py --stdin
```

## Local Memory

If `APP.local.md` exists in this directory, review it before performing an
operation when local installation details, prior failures, or version-specific
behavior may matter.

After completing an operation, if you encountered a repeatable issue or
verified something worth remembering about this local installation, add a short
note to `APP.local.md`.

Keep notes concise and factual. Record only local, reusable insights such as
verified quirks, recovery steps, version-specific gaps, or runtime-discovered
details. Do not copy general guidance from `APP.md`, and do not add temporary
task-specific notes.

API lookup workflow:

- Use `docs/api-index.txt` as the primary operation index.
- Workflow for every task:
  1. Understand the user's intent.
  2. Search (`rg`) `docs/api-index.txt` for matching operations.
  3. If needed, introspect the live app/runtime to resolve ambiguity.
  4. If still needed, search official documentation online.
  5. Avoid over-relying on training, as it's fragile and can break. Do not directly read the index file, which can be heavy.

Connection recovery:

If the bridge says the session file is missing or the local eval endpoint is
unreachable, ask the user to open a Unity project that has the Creative Adapter
Bridge package installed. If the package is not installed, install it into the
target Unity project:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/unity_adapter/install_package.ps1 -ProjectPath "C:\Path\To\UnityProject"
```

Unity-specific notes:

- Unity Editor scripting is C#, but Unity does not expose an arbitrary C#
  string `eval` API. This adapter accepts command JSON for tested Editor
  actions.
- For deeper project-specific behavior, add explicit actions to the package or
  create project-local Editor scripts. Do not pretend arbitrary C# was executed.
- The package generates a random token on Editor startup and writes it with the
  eval URL to `%APPDATA%\creative-adapters\unity.json`. The Python bridge reads
  this file automatically and sends `X-Bridge-Token`.
- Commands run on Unity's main Editor thread.
- Do not enter/exit Play Mode, save scenes, build, import large assets, edit
  project settings, or change scenes unless explicitly asked.
- Prefer undo-backed commands. The included create/transform/component actions
  use Unity's `Undo` API where applicable.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `CONSTRUCTOR`, `METHOD`, `PROPERTY`).

Supported command actions:

- `createPrimitive`: creates a Unity primitive. `primitiveType` uses Unity's
  `PrimitiveType` names, including `Cube`, `Sphere`, `Capsule`, `Cylinder`,
  `Plane`, and `Quad`. Optional fields include `name`, position fields
  (`x`, `y`, `z`), scale fields (`scaleX`, `scaleY`, `scaleZ`), `color`, and
  `undoLabel`.
- `setTransform`: changes the target object's position and/or scale. Targets
  resolve by `path`, then `name`, then the active selected GameObject. Use
  `setPosition` and `setScale` to choose which values apply.
- `executeMenuItem`: runs a Unity menu item by path, such as
  `GameObject/Light/Directional Light`.
- `addComponent`: adds a component to the target GameObject by `componentType`.
