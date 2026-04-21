# Sources

- MicrosoftDocs/VBA-Docs repository (official Word VBA reference markdown):
  https://github.com/MicrosoftDocs/VBA-Docs
- Word object model overview page:
  https://learn.microsoft.com/en-us/office/vba/api/overview/word/object-model
- Word enumerations overview page:
  https://learn.microsoft.com/en-us/office/vba/api/word(enumerations)

## Extraction

- Date: 2026-04-21
- Method: downloaded VBA-Docs repo snapshot and mechanically parsed `api/Word*.md` via frontmatter `api_name`, titles, and section links.
- Normalization: one symbol per line, deduplicated, grep-friendly prefixes.

## Counts

- CLASS: 260
- ENUM: 351
- PROPERTY: 4144
- METHOD: 2151
- EVENT: 119
- CONSTANT: 3380
