book = app.ActiveWorkbook if app.Workbooks.Count else None
sheet = book.ActiveSheet if book else None

selection_address = None
selection_type = None
try:
    selection = app.Selection
    selection_type = str(selection.__class__.__name__)
    selection_address = selection.Address(False, False)
except Exception:
    pass

used_range = None
if sheet is not None:
    try:
        used = sheet.UsedRange
        used_range = {
            "address": used.Address(False, False),
            "rows": used.Rows.Count,
            "columns": used.Columns.Count,
        }
    except Exception:
        used_range = None

_result = {
    "app": app.Name,
    "version": app.Version,
    "workbooks": app.Workbooks.Count,
    "workbook": book.Name if book else None,
    "path": book.Path if book else None,
    "saved": bool(book.Saved) if book else None,
    "activeSheet": sheet.Name if sheet else None,
    "selectionType": selection_type,
    "selectionAddress": selection_address,
    "usedRange": used_range,
}
