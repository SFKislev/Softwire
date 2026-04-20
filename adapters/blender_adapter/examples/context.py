import bpy

scene = bpy.context.scene
active = bpy.context.view_layer.objects.active
selected = list(bpy.context.selected_objects)

_result = {
    "app": "Blender",
    "version": bpy.app.version_string,
    "file": bpy.data.filepath or None,
    "scene": scene.name if scene else None,
    "mode": bpy.context.mode,
    "activeObject": active.name if active else None,
    "activeObjectType": active.type if active else None,
    "selectedObjects": [{"name": obj.name, "type": obj.type} for obj in selected],
    "frame": scene.frame_current if scene else None,
    "objectCount": len(bpy.data.objects),
}
