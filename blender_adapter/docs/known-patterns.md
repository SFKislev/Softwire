# Blender Python Known Patterns

This file is intentionally small. Add tested snippets as the adapter is used.

## Context

Use `examples/context.py`.

## Create Mesh Objects

```python
import bpy

bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
obj = bpy.context.object
obj.name = "Named Cube"
```

## Materials

```python
mat = bpy.data.materials.new("Blue")
mat.diffuse_color = (0.0, 0.2, 1.0, 1.0)
obj.data.materials.append(mat)
```

## Undo

For bounded directed edits, push an undo marker after mutation:

```python
bpy.ops.ed.undo_push(message="Adapter action")
```

Not every data API mutation maps perfectly to Blender's undo stack. Report
honestly if a requested operation cannot be collapsed into one undo step.
