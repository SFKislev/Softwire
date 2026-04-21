# Source Links

- After Effects scripting guide: https://ae-scripting.docsforadobe.dev/
- Docs repository: https://github.com/docsforadobe/after-effects-scripting-guide
- Adobe CEP samples: https://github.com/Adobe-CEP/Samples
- Offline combined docs page: https://ae-scripting.docsforadobe.dev/print_page/
- Legacy Adobe CS6 scripting guide PDF:
  https://download.macromedia.com/pub/developer/aftereffects/scripting/After-Effects-CS6-Scripting-Guide.pdf

## Extraction Notes

- Extraction date: 2026-04-21
- Adapter: `adapters/after_effects_adapter`
- Output: `docs/api-index.txt`
- Source path pattern: `docs/**.md` (excluding `introduction`, `index`, `_global`, `matchnames`)
- Extraction process:
  - deterministic parse of markdown headings for `CLASS`, `PROPERTY`, `METHOD`
  - strict regex extraction for documented enum/constants (`EnumName.VALUE`) from
    print-page and legacy PDF text exports
  - targeted extraction of documented AE match names from `docs/matchnames/*`
    for retrieval terms like `shadow`, `vector`, and shape operations
- Output counts:
  - classes: 47
  - enums/constants: 330
  - properties: 398
  - methods: 264

## Normalization Rules Used

- one symbol per line
- uppercase record types: `CLASS`, `ENUM`, `PROPERTY`, `METHOD`, `MATCHNAME`
- fully-qualified members where possible (for example `METHOD app.open(...)`)
- deduplicated repeated symbols
