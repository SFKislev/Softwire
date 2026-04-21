# Sources

- Unity ScriptReference index page:
  https://docs.unity3d.com/ScriptReference
- Unity ScriptReference machine-readable doc index (authoritative symbol catalog):
  https://docs.unity3d.com/ScriptReference/docdata/index.json
- Unity Editor namespace reference page:
  https://docs.unity3d.com/ScriptReference/UnityEditor.html

## Extraction

- Date: 2026-04-21
- Method: downloaded Unity `docdata/index.json` and mechanically parsed page symbol pairs (`pages`) into classes, constructors, methods, and properties.
- Normalization: one symbol per line, deduplicated, grep-friendly prefixes.

## Counts

- CLASS: 4312
- CONSTRUCTOR: 912
- METHOD: 17748
- PROPERTY: 11809
