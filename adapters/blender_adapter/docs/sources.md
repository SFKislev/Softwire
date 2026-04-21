# Sources

- Blender Python API `genindex-all` (authoritative symbol index):
  https://docs.blender.org/api/current/genindex-all.html
- Blender Python API `bpy.types` (type catalog):
  https://docs.blender.org/api/current/bpy.types.html
- Blender Python API `bpy.ops` (operator catalog):
  https://docs.blender.org/api/current/bpy.ops.html

## Extraction

- Date: 2026-04-21
- Method: downloaded official Blender docs pages and mechanically parsed index patterns for modules, classes, operators, methods, and properties.
- Normalization: one symbol per line, deduplicated, grep-friendly prefixes.

## Counts

- MODULE: 49
- CLASS: 2038
- OPERATOR: 1896
- METHOD: 573
- PROPERTY: 1041
