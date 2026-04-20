# Premiere Pro Adapter Prototype

Premiere Pro does not expose the same local COM script dispatch surface as
Photoshop, InDesign, and Illustrator. This adapter therefore
uses a tiny CEP panel inside Premiere to expose ExtendScript evaluation on
localhost.

## Shape

```text
Premiere Pro
  CEP panel
    window.__adobe_cep__.evalScript(...)
    local eval endpoint + per-session token file

Shell
  python adapters/premiere_adapter/premiere_bridge.py --stdin
```

## Install CEP Panel

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/premiere_adapter/install_cep_bridge.ps1
```

Manual equivalent:

Copy this folder:

```text
adapters/premiere_adapter/cep/com.creativeadapters.premiere
```

to the user CEP extensions directory:

```text
%APPDATA%\Adobe\CEP\extensions\com.creativeadapters.premiere
```

For unsigned local development panels, enable CEP debug mode:

```powershell
reg add HKCU\Software\Adobe\CSXS.9 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.10 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.11 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.12 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.13 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.14 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.15 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.16 /v PlayerDebugMode /t REG_SZ /d 1 /f
```

Restart Premiere, then open the bridge once:

```text
Window > Extensions > Creative Adapter Bridge
```

Leave the panel open or docked while using the shell bridge.

The extension manifest uses `AutoVisible`, and the panel asks Premiere to keep
it loaded via `app.setExtensionPersistent(...)`. After this one-time setup,
Premiere may reopen the bridge automatically in later sessions. If it does not,
open `Window > Extensions > Creative Adapter Bridge` manually; no token or port
setup is required.

## Local Session File

When the panel starts, it writes a per-session connection file:

```text
%APPDATA%\creative-adapters\premiere.json
```

The file contains the current localhost URL and a random bridge token. The
Python bridge reads it automatically and sends `X-Bridge-Token`; users should
not need to copy or manage the token.

This prevents unrelated webpages or local HTTP clients from posting arbitrary
scripts into the open Premiere project without the token. If the session file
is missing or stale, open `Window > Extensions > Creative Adapter Bridge` again.

## First Live Test

From the workspace root:

```powershell
Get-Content adapters/premiere_adapter/examples/context.jsx -Raw | python adapters/premiere_adapter/premiere_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Adobe Premiere Pro", "...": "..."}}
```

## Notes

This connector is intentionally different from the COM adapters. The bridge
process is inside Premiere because that is where `evalScript` is available.
