# Sources

- Blender exposes its scripting API as in-process Python module `bpy`.
- This adapter installs a Blender addon because `bpy` is not available from an
  ordinary out-of-process Python interpreter.
