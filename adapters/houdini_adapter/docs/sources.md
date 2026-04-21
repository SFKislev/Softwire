# Sources

- SideFX Houdini Python scripting overview:
  https://www.sidefx.com/docs/houdini/hom/index.html
- SideFX `hou` package reference index (authoritative symbol listing):
  https://www.sidefx.com/docs/houdini/hom/hou/index.html
- SideFX `hou.ui` reference (bridge/event-loop-relevant UI callbacks):
  https://www.sidefx.com/docs/houdini/hom/hou/ui.html

## Extraction

- Date: 2026-04-21
- Method: downloaded `hou` package reference index HTML and mechanically parsed labeled symbol entries (`homclass`, `homfunction`, `hommodule`, `pypackage`), then crawled class pages to extract member signatures from Methods/Attributes sections.
- Normalization: one symbol per line, deduplicated, grep-friendly prefixes.

## Counts

- CLASS: 259
- FUNCTION: 231
- MODULE: 193
- PACKAGE: 5
- ENUM: 92
- METHOD: 10285
- PROPERTY: 0
