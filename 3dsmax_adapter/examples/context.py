import MaxPlus


def mxs(expr, default=None):
    try:
        value = MaxPlus.Core.EvalMAXScript(expr)
        try:
            return value.Get()
        except Exception:
            return str(value)
    except Exception:
        return default


_result = {
    "app": "3ds Max",
    "version": mxs("maxVersion()", None),
    "file": mxs("maxFilePath + maxFileName", None),
    "sceneName": mxs("maxFileName", None),
    "objectCount": mxs("objects.count", None),
    "selectionCount": mxs("selection.count", None),
    "selectedObjects": mxs("for o in selection collect o.name", None),
    "frame": mxs("sliderTime as string", None),
}
