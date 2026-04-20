# Audition Adapter Prototype

Audition does not expose the same local COM script dispatch surface as
Photoshop, InDesign, and Illustrator. This adapter uses a tiny CEP panel inside
Audition to expose ExtendScript evaluation through a tokenized local bridge.

## Shape

```text
Audition
  CEP panel
    window.__adobe_cep__.evalScript(...)
    local eval endpoint + per-session token file

Shell
  python adapters/audition_adapter/audition_bridge.py --stdin
```

## Install CEP Panel

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/audition_adapter/install_cep_bridge.ps1
```

Restart Audition, then open the bridge once:

```text
Window > Extensions > Creative Adapter Bridge
```

Leave the panel open or docked while using the shell bridge.

## Local Session File

When the panel starts, it writes:

```text
%APPDATA%\creative-adapters\audition.json
```

The Python bridge reads that file automatically and sends `X-Bridge-Token`.
Users should not need to copy or manage tokens or ports.

## First Live Test

```powershell
Get-Content adapters/audition_adapter/examples/context.jsx -Raw | python adapters/audition_adapter/audition_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Audition", "...": "..."}}
```
