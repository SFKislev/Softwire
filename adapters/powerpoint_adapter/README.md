# PowerPoint Adapter Prototype

This folder lets a coding agent drive a running Microsoft PowerPoint instance
through Windows COM using only shell commands.

## Platform Support

**Windows only.** The bridge uses Windows COM automation (`pythoncom` /
`win32com`), which is not available on macOS. Running the bridge on Mac exits
immediately with a clear error. A macOS port would require a different
scripting surface (Office AppleScript dictionary or Office Add-in JS API).

## Portable Hook (Windows)

The bridge uses the generic COM ProgID:

```text
PowerPoint.Application
```

Do not hard-code the local Office install path. Each Windows machine resolves
the ProgID through its own registry.

## First Live Test

Open PowerPoint first, then open or create a presentation. From the workspace
root:

```powershell
Get-Content adapters/powerpoint_adapter/examples/context.py -Raw | python adapters/powerpoint_adapter/powerpoint_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Microsoft PowerPoint", "...": "..."}}
```

## Script Shape

PowerPoint does not provide a general script-eval method. The PowerPoint bridge
executes Python code and exposes the live COM object as `app`. Set `_result` to
a JSON-serializable value:

```python
presentation = app.ActivePresentation if app.Presentations.Count else None
_result = {
    "presentations": app.Presentations.Count,
    "presentation": presentation.Name if presentation else None,
}
```

Use `--stdin` for one-off scripts. If a file is required, keep it in a temp or
scratch directory, not in `examples/`.
