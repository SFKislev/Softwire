# Sources

- MicrosoftDocs/VBA-Docs repository (official Excel VBA reference markdown):
  https://github.com/MicrosoftDocs/VBA-Docs
- Excel object model overview page:
  https://learn.microsoft.com/en-us/office/vba/api/overview/Excel/object-model
- Excel enumerations overview page:
  https://learn.microsoft.com/en-us/office/vba/api/excel(enumerations)

## Extraction

- Date: 2026-04-21
- Method: downloaded VBA-Docs repo snapshot and mechanically parsed `api/excel*.md` filenames plus frontmatter titles/body headings.
- Normalization: one symbol per line, deduplicated, grep-friendly prefixes.

## Counts

- CLASS: 311
- ENUM: 307
- PROPERTY: 3730
- METHOD: 3447
- EVENT: 317
- CONSTANT: 2447
