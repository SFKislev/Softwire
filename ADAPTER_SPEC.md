# Adapter Spec

This is the reusable shape for connecting a coding agent to a local creative
application.

## Goal

Make a running creative app legible and mutable through shell commands, so a
coding agent can use its existing tools to read context, search docs, compose a
script, execute it, inspect errors, and iterate.

## Non-Goals

- No custom agent runtime.
- No MCP server requirement.
- No app takeover or headless batch mode.
- No screen scraping when a structural scripting API exists.

## Folder Shape

```text
<app>_adapter/
  <app>_bridge.py
  APP.md
  README.md
  docs/
    known-patterns.md
    sources.md
  examples/
    context.jsx
```

All app adapters should use this folder shape. Root-level bridge files, if
present, should only be backwards-compatible wrappers.

The root `CLAUDE.md` is a small router to shared rules and app notes. Adapter
`CLAUDE.md` files, if present, should only point to shared rules and `APP.md`.

## Bridge Contract

The bridge must:

- Accept script code through argv, `--stdin`, or `--file`.
- Return JSON on stdout for success.
- Return JSON on stderr and non-zero exit for failure.
- Connect to a running app by default.
- Avoid launching the app unless `--allow-launch` is explicitly passed.
- Avoid hard-coded install paths.

## Windows COM Adapter Template

Use `creative_adapters.com_bridge.run_bridge`:

```python
from creative_adapters.com_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="Illustrator",
            default_progid="Illustrator.Application",
            process_name="Illustrator.exe",
            execute_method="DoJavaScript",
        )
    )
```

For InDesign JavaScript:

```python
run_bridge(
    app_name="InDesign",
    default_progid="InDesign.Application",
    process_name="InDesign.exe",
    execute_method="DoScript",
    language_id=1246973031,
)
```

## Context Script Requirements

The first example for each app should be a read-only context script. It should
return:

- app name
- app version
- document count
- active document name
- active layer/page/selection where relevant

Do not depend on a global `JSON` object. Older ExtendScript runtimes may not
provide it. Use a tiny local serializer.

## Portability Rules

- Use generic ProgIDs like `Photoshop.Application`, `InDesign.Application`, and
  `Illustrator.Application`.
- Never hard-code `C:\Program Files\Adobe\...` paths in bridge code.
- Keep local install paths out of required commands.
- Put app-version-specific notes in docs, not in bridge logic.
- Make the failure mode useful when an app is not installed or not running.

## Agent-Facing Instructions

Put reusable behavior in:

```text
shared/coexistence.md
shared/bridge-contract.md
```

Put only app-specific, non-obvious facts in `<app>_adapter/APP.md`: bridge
command, execution method, undo behavior, measurement quirks, selection object
quirks, or known modal/API limitations.

## Non-COM Apps

If an app does not expose an OS-level script dispatch surface, the adapter can
ship an in-app bridge extension. Keep the same shell contract: the external
bridge command still accepts code through stdin/file/argv and returns JSON. The
in-app bridge is only the transport into the app runtime.
