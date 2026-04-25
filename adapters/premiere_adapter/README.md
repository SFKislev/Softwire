# Premiere Pro Adapter Prototype

Premiere Pro does not expose the same local COM or AppleScript script dispatch
surface as Photoshop, InDesign, and Illustrator. This adapter uses a tiny CEP
panel inside Premiere to expose ExtendScript evaluation on localhost.

## Shape

```text
Premiere Pro
  CEP panel
    window.__adobe_cep__.evalScript(...)
    local eval endpoint + per-session token file

Shell
  python adapters/premiere_adapter/premiere_bridge.py --stdin
```

## Platform Support

| Platform | Status |
|----------|--------|
| Windows  | Fully supported |
| macOS (Premiere ≤ 25.x) | Supported — see macOS install below |
| macOS (Premiere 26+) | **Not supported** — CEP panel UI removed in this version |

## Install CEP Panel

**Windows** — from the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/premiere_adapter/install_cep_bridge.ps1
```

For unsigned local development panels, enable CEP debug mode:

```powershell
reg add HKCU\Software\Adobe\CSXS.9 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.10 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.11 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.12 /v PlayerDebugMode /t REG_SZ /d 1 /f
reg add HKCU\Software\Adobe\CSXS.13 /v PlayerDebugMode /t REG_SZ /d 1 /f
```

**macOS** — copy the panel manually:

```bash
mkdir -p ~/Library/Application\ Support/Adobe/CEP/extensions
cp -r adapters/premiere_adapter/cep/com.creativeadapters.premiere \
  ~/Library/Application\ Support/Adobe/CEP/extensions/
```

Enable CEP debug mode:

```bash
defaults write com.adobe.CSXS.9  PlayerDebugMode 1
defaults write com.adobe.CSXS.10 PlayerDebugMode 1
defaults write com.adobe.CSXS.11 PlayerDebugMode 1
defaults write com.adobe.CSXS.12 PlayerDebugMode 1
defaults write com.adobe.CSXS.13 PlayerDebugMode 1
defaults write com.adobe.CSXS.14 PlayerDebugMode 1
defaults write com.adobe.CSXS.15 PlayerDebugMode 1
```

Restart Premiere, **open or create a project** (the Extensions menu is not
available on the start screen), then open the bridge:

```text
Window > Extensions > Creative Adapter Bridge
```

On macOS the panel appears directly in the Window menu, not under a submenu.

Leave the panel open or docked while using the shell bridge.

## Local Session File

When the panel starts, it writes a per-session connection file:

```text
Windows : %APPDATA%\creative-adapters\premiere.json
macOS   : ~/creative-adapters/premiere.json
```

The Python bridge reads it automatically and sends `X-Bridge-Token`. Users
should not need to copy or manage the token.

If the session file is missing or stale, open `Window > Extensions > Creative
Adapter Bridge` again.

## First Live Test

**Windows:**
```powershell
Get-Content adapters/premiere_adapter/examples/context.jsx -Raw | python adapters/premiere_adapter/premiere_bridge.py --stdin
```

**macOS:**
```bash
cat adapters/premiere_adapter/examples/context.jsx | python adapters/premiere_adapter/premiere_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "Adobe Premiere Pro", "...": "..."}}
```

## ExtendScript Notes

- Premiere runs ExtendScript (ES3-era JavaScript). `JSON.stringify` is not
  available — use a manual serialisation helper for structured output.
- `app.project.createNewSequence(name, id)` works but the second argument
  (preset path) is ignored by the ExtendScript API; the sequence is created
  with default settings.
- A project must be open before the bridge can be used. The Extensions menu
  does not appear on the Premiere start screen.
