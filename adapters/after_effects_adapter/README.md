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

**Windows** — from the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/after_effects_adapter/install_cep_bridge.ps1
```

**macOS** — copy the panel manually:

```bash
mkdir -p ~/Library/Application\ Support/Adobe/CEP/extensions
cp -r adapters/after_effects_adapter/cep/com.creativeadapters.aftereffects \
  ~/Library/Application\ Support/Adobe/CEP/extensions/
```

Enable CEP debug mode (if not already set):

```bash
defaults write com.adobe.CSXS.11 PlayerDebugMode 1
defaults write com.adobe.CSXS.12 PlayerDebugMode 1
defaults write com.adobe.CSXS.13 PlayerDebugMode 1
defaults write com.adobe.CSXS.14 PlayerDebugMode 1
defaults write com.adobe.CSXS.15 PlayerDebugMode 1
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
Windows : %APPDATA%\creative-adapters\after_effects.json
macOS   : ~/creative-adapters/after_effects.json
```

The Python bridge reads that file automatically and sends `X-Bridge-Token`.
Users should not need to copy or manage tokens or ports.

## First Live Test

**Windows:**
```powershell
Get-Content adapters/after_effects_adapter/examples/context.jsx -Raw | python adapters/after_effects_adapter/after_effects_bridge.py --stdin
```

**macOS:**
```bash
cat adapters/after_effects_adapter/examples/context.jsx | python adapters/after_effects_adapter/after_effects_bridge.py --stdin
```

Expected result:

```json
{"ok": true, "result": {"app": "After Effects", "...": "..."}}
```
