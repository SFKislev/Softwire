# Source Links

- Adobe Photoshop scripting overview: https://helpx.adobe.com/photoshop/using/scripting.html
- Photoshop scripting reference mirror: https://theiviaxx.github.io/photoshop-docs/Photoshop/
- Adobe CEP Photoshop scripting PDFs:
  https://github.com/Adobe-CEP/CEP-Resources/tree/master/Documentation/Product%20specific%20Documentation/Photoshop%20Scripting

## Extraction Notes

- Extraction date: 2026-04-21
- Adapter: `adapters/photoshop_adapter`
- Output: `docs/api-index.txt`
- Extraction process:
  - class and enumeration URL extraction from Photoshop index listing
  - per-class symbol extraction from mirror class pages (method summaries,
    signatures, and property listing tokens)
  - per-enum page value extraction for `EnumName.VALUE` entries
- Output counts:
  - classes: 93
  - enum classes: 133
  - enums: 725
  - properties: 2157
  - methods: 67

## Normalization Rules Used

- one symbol per line
- uppercase record types: `CLASS`, `ENUMCLASS`, `ENUM`, `PROPERTY`, `METHOD`
- fully-qualified members where possible (for example `METHOD Document.save(...)`)
- deduplicated repeated symbols

For a larger searchable reference, add Adobe's Photoshop JavaScript scripting
reference text to this folder as `photoshop-scripting-reference.txt`.
