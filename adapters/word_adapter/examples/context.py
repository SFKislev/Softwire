doc = app.ActiveDocument if app.Documents.Count else None

selection_text = None
selection_start = None
selection_end = None
try:
    selection = app.Selection
    selection_text = selection.Text
    selection_start = selection.Start
    selection_end = selection.End
except Exception:
    pass

_result = {
    "app": app.Name,
    "version": app.Version,
    "documents": app.Documents.Count,
    "doc": doc.Name if doc else None,
    "path": doc.Path if doc else None,
    "saved": bool(doc.Saved) if doc else None,
    "selectionText": selection_text,
    "selectionStart": selection_start,
    "selectionEnd": selection_end,
}
