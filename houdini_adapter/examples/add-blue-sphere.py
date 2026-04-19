import hou


obj = hou.node("/obj")
geo = obj.createNode("geo", node_name="creative_adapter_blue_sphere")

for child in geo.children():
    child.destroy()

sphere = geo.createNode("sphere", node_name="sphere")
sphere.parm("type").set(2)
sphere.parm("radx").set(1.5)
sphere.parm("rady").set(1.5)
sphere.parm("radz").set(1.5)

normal = geo.createNode("normal", node_name="smooth_normals")
normal.setInput(0, sphere)

material = hou.node("/mat").createNode("principledshader", node_name="creative_adapter_blue")
material.parm("basecolorr").set(0.02)
material.parm("basecolorg").set(0.18)
material.parm("basecolorb").set(1.0)

assign = geo.createNode("material", node_name="assign_blue_material")
assign.setInput(0, normal)
assign.parm("shop_materialpath1").set(material.path())
assign.setDisplayFlag(True)
assign.setRenderFlag(True)

geo.layoutChildren()
hou.clearAllSelected()
geo.setSelected(True)

_result = {
    "created": geo.path(),
    "displayNode": assign.path(),
    "material": material.path(),
}
