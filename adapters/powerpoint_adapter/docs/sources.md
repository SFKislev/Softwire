# Sources

- MicrosoftDocs/VBA-Docs repository (official PowerPoint VBA reference markdown):
  https://github.com/MicrosoftDocs/VBA-Docs
- PowerPoint object model overview page:
  https://learn.microsoft.com/en-us/office/vba/api/overview/powerpoint/object-model
- PowerPoint enumerations overview page:
  https://learn.microsoft.com/en-us/office/vba/api/powerpoint(enumerations)

## Extraction

- Date: 2026-04-21
- Method: downloaded VBA-Docs repo snapshot and mechanically parsed `api/PowerPoint*.md` via frontmatter `api_name`, titles, and section links.
- Normalization: one symbol per line, deduplicated, grep-friendly prefixes.

## Counts

- CLASS: 173
- ENUM: 127
- PROPERTY: 1816
- METHOD: 1042
- EVENT: 51
- CONSTANT: 1679
