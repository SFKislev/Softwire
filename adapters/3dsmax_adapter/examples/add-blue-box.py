import MaxPlus


script = r'''
undo "Add blue box" on
(
    mat = StandardMaterial name:"Creative Adapter Blue"
    mat.diffuse = color 0 60 255
    obj = box name:"Creative Adapter Blue Box" length:40 width:40 height:40 pos:[0,0,20]
    obj.material = mat
    select obj
    obj.name
)
'''

value = MaxPlus.Core.EvalMAXScript(script)
try:
    created = value.Get()
except Exception:
    created = str(value)

_result = {
    "created": created,
}
