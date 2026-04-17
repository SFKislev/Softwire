# Audition Notes

Bridge:

```powershell
python audition_adapter/audition_bridge.py --stdin
```

Runtime: local CEP panel -> `window.__adobe_cep__.evalScript(...)` -> Audition
ExtendScript.

Context:

```powershell
Get-Content audition_adapter/examples/context.jsx -Raw | python audition_adapter/audition_bridge.py --stdin
```

Connection recovery:

If the bridge says the session file is missing or the local eval endpoint is
unreachable, ask the user to:

1. Open Audition.
2. Open the target file or multitrack session.
3. Open `Window > Extensions > Creative Adapter Bridge`.
4. Leave the panel open or docked.

Then retry the context command above.

If `Creative Adapter Bridge` is missing from the Extensions menu, reinstall the
panel:

```powershell
powershell -ExecutionPolicy Bypass -File audition_adapter/install_cep_bridge.ps1
```

Restart Audition after reinstalling.

Audition-specific notes:

- Local probing did not find a practical `Audition.Application` COM automation
  object, so this adapter uses CEP rather than the Photoshop-style COM bridge.
- Adobe documents Audition CEP support: panels use HTML/JavaScript and
  ExtendScript to communicate with Audition.
- Adobe's CEP samples use Audition host ID `AUDT`.
- The CEP panel generates a random token on startup and writes it with the eval
  URL to `%APPDATA%\creative-adapters\audition.json`. The Python bridge reads
  this file automatically and sends `X-Bridge-Token`.
- Do not save, export, mix down, batch process, relink media, close sessions, or
  overwrite audio files unless the user explicitly asks.
