presentation = app.ActivePresentation if app.Presentations.Count else None

active_window = None
active_slide = None
selection_type = None
selection_count = None
try:
    active_window = app.ActiveWindow
    try:
        active_slide = active_window.View.Slide
    except Exception:
        active_slide = None
    try:
        selection = active_window.Selection
        selection_type = selection.Type
        if hasattr(selection, "ShapeRange"):
            try:
                selection_count = selection.ShapeRange.Count
            except Exception:
                selection_count = None
    except Exception:
        pass
except Exception:
    active_window = None

slides = None
if presentation is not None:
    try:
        slides = presentation.Slides.Count
    except Exception:
        slides = None

_result = {
    "app": app.Name,
    "version": app.Version,
    "presentations": app.Presentations.Count,
    "presentation": presentation.Name if presentation else None,
    "path": presentation.Path if presentation else None,
    "saved": bool(presentation.Saved) if presentation else None,
    "slides": slides,
    "activeSlideIndex": active_slide.SlideIndex if active_slide else None,
    "activeSlideName": active_slide.Name if active_slide else None,
    "selectionType": selection_type,
    "selectionCount": selection_count,
}
