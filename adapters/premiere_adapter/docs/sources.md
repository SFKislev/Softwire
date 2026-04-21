# Source Links

- Premiere Pro scripting guide: https://ppro-scripting.docsforadobe.dev/
- Adobe CEP samples, including PProPanel: https://github.com/Adobe-CEP/Samples
- Premiere QE DOM typings (unsupported surface):
  https://github.com/aenhancers/types-for-adobe-extras/blob/master/Premiere/12.0/qeDom.d.ts

## Extraction Notes

- Extraction date: 2026-04-21
- Adapter: `adapters/premiere_adapter`
- Output: `docs/api-index.txt`
- Source repository: https://github.com/docsforadobe/premiere-scripting-guide
- Source page: https://ppro-scripting.docsforadobe.dev/print_page/
- Extraction process:
  - deterministic parse of print-page member headings (`### Class.member` /
    `### Class.method()`)
  - deterministic extraction of documented uppercase constant tokens from
    print-page content
- Output counts:
  - classes: 26
  - properties: 108
  - methods: 217
  - constants: 22
  - qe_interfaces: 17
  - qe_properties: 158
  - qe_methods: 243
  - qe_types: 2

## Normalization Rules Used

- one symbol per line
- uppercase record types: `CLASS`, `PROPERTY`, `METHOD`, `CONSTANT`,
  `QE_INTERFACE`, `QE_PROPERTY`, `QE_METHOD`, `QE_TYPE`
- fully-qualified members where possible (for example `METHOD Sequence.insertClip(...)`)
- deduplicated repeated symbols


## QE DOM Notes

- `qe` DOM is an unsupported internal surface exposed after `app.enableQE()`.
- QE symbols in `api-index.txt` are prefixed with `QE_` and sourced mechanically
  from `types-for-adobe-extras` Premiere `qeDom.d.ts`.
