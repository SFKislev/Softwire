# Sources

- Adobe Audition help says Audition supports CEP extensions and that panels use
  HTML/JavaScript plus ExtendScript to communicate with Audition:
  https://helpx.adobe.com/audition/using/enabling-cep-extensions.html
- Adobe CEP Audition samples use host ID `AUDT`:
  https://github.com/Adobe-CEP/Samples/tree/master/Audition
- Audition type definitions used for mechanical symbol extraction:
  https://github.com/docsforadobe/Types-for-Adobe/tree/master/Audition/2018

## Extraction Notes

- Extraction date: 2026-04-21
- Adapter: `adapters/audition_adapter`
- Output: `docs/api-index.txt`
- Extraction process: parsed TypeScript declarations in
  `Types-for-Adobe/Audition/2018/index.d.ts` and emitted normalized records
- Output counts:
  - classes: 41
  - properties: 888
  - methods: 82

## Normalization Rules Used

- one symbol per line
- uppercase record types: `CLASS`, `INTERFACE`, `ENUMCLASS`, `ENUM`, `PROPERTY`, `METHOD`
- fully-qualified members where possible (for example `METHOD Application.openDocument(...)`)
- deduplicated repeated symbols
