import bpy

bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cube = bpy.context.object
cube.name = "Creative Adapter Blue Cube"

mat = bpy.data.materials.new("Creative Adapter Blue")
mat.diffuse_color = (0.0, 0.2, 1.0, 1.0)
cube.data.materials.append(mat)

bpy.ops.ed.undo_push(message="Add blue cube")

_result = {
    "created": cube.name,
    "location": list(cube.location),
    "material": mat.name,
}
