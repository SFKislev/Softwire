# After Effects Adapter Prototype

After Effects does not expose the same local COM script dispatch surface as
Photoshop, InDesign, and Illustrator. This adapter uses a tiny CEP panel inside
After Effects to expose ExtendScript evaluation through a tokenized local
bridge.

## Shape

```text
After Effects
  CEP panel
    window.__adobe_cep__.evalScript(...)
    local eval endpoint + per-session token file

Shell
  python adapters/after_effects_adapter/after_effects_bridge.py --stdin
```

## Install CEP Panel

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/after_effects_adapter/install_cep_bridge.ps1
```

Restart After Effects, then open the bridge once:

```text
Window > Extensions > Creative Adapter Bridge
```

Leave the panel open or docked while using the shell bridge.

The extension manifest uses `AutoVisible`, and the panel attempts
`app.setExtensionPersistent(...)`. After this one-time setup, After Effects may
reopen the bridge automatically in later sessions. If it does not, open
`Window > Extensions > Creative Adapter Bridge` manually.

## Local Session File

When the panel starts, it writes:

```text
%APPDATA%\creative-adapters\after_effects.json
```

The Python bridge reads that file automatically and sends `X-Bridge-Token`.
Users should not need to copy or manage tokens or ports.

## First Live Test

```powershell
Get-Content adapters/after_effects_adapter/examples/context.jsx -Raw | python adapters/after_effects_adapter/after_effects_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "After Effects", "...": "..."}}
```
