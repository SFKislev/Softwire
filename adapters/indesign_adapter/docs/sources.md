# Source Links

- Adobe InDesign developer hub: https://developer.adobe.com/indesign/
- Adobe InDesign DOM/API reference entry points (via developer hub navigation)

## Extraction Notes

- Extraction date: 2026-04-21
- Adapter: `adapters/indesign_adapter`
- Output: `docs/api-index.txt`
- Source repository: https://github.com/AdobeDocs/indesign-18-dom
- Source path pattern: `src/pages/api/**/index.md`
- Extraction process: deterministic parse of markdown signatures
- Output counts:
  - classes: 1079
  - enums/class constants: 2396
  - properties: 16388
  - methods: 7993

## Normalization Rules Used

- one symbol per line
- uppercase record types: `CLASS`, `ENUM`, `PROPERTY`, `METHOD`
- fully-qualified members where possible (for example `PROPERTY Document.pages`)
- deduplicated repeated symbols

For a larger searchable reference, add Adobe's InDesign JavaScript scripting
reference text to this folder as `indesign-scripting-reference.txt`.
