import hou


def node_summary(node):
    if node is None:
        return None
    return {
        "name": node.name(),
        "path": node.path(),
        "type": node.type().name() if node.type() else None,
    }


hip = hou.hipFile
selected = hou.selectedNodes()
current = hou.pwd()

_result = {
    "app": "Houdini",
    "version": hou.applicationVersionString(),
    "file": hip.path() if hip.hasUnsavedChanges() or hip.name() else None,
    "sceneName": hip.basename() if hip.name() else None,
    "currentNode": node_summary(current),
    "selectedNodes": [node_summary(node) for node in selected],
    "frame": hou.frame(),
    "rootChildren": [child.name() for child in hou.node("/").children()],
}
