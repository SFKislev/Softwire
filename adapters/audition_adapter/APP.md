# Audition Notes

Bridge:

```powershell
python adapters/audition_adapter/audition_bridge.py --stdin
```

Runtime: local CEP panel -> `window.__adobe_cep__.evalScript(...)` -> Audition
ExtendScript.

Context:

```powershell
Get-Content adapters/audition_adapter/examples/context.jsx -Raw | python adapters/audition_adapter/audition_bridge.py --stdin
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
unreachable, ask the user to:

1. Open Audition.
2. Open the target file or multitrack session.
3. Open `Window > Extensions > Creative Adapter Bridge`.
4. Leave the panel open or docked.

Then retry the context command above.

If `Creative Adapter Bridge` is missing from the Extensions menu, reinstall the
panel:

```powershell
powershell -ExecutionPolicy Bypass -File adapters/audition_adapter/install_cep_bridge.ps1
```

Restart Audition after reinstalling.

Audition-specific notes:

- This adapter uses a CEP panel rather than a COM automation bridge.
- Adobe documents Audition CEP support: panels use HTML/JavaScript and
  ExtendScript to communicate with Audition.
- Adobe's CEP samples use Audition host ID `AUDT`.
- The CEP panel generates a random token on startup and writes it with the eval
  URL to `%APPDATA%\creative-adapters\audition.json`. The Python bridge reads
  this file automatically and sends `X-Bridge-Token`.
- Do not save, export, mix down, batch process, relink media, close sessions, or
  overwrite audio files unless the user explicitly asks.
- Grep-friendly API index: `docs/api-index.txt` (records are prefixed with
  `CLASS`, `INTERFACE`, `ENUMCLASS`, `ENUM`, `PROPERTY`, `METHOD`).
