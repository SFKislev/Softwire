# InDesign ExtendScript Known Patterns

This file is the curated high-signal reference for the first InDesign adapter
test. Add the full InDesign scripting reference later, but prefer these patterns
when they match the request.

## Context

Use `examples/context.jsx`. It does not depend on a global `JSON` object.

## Active Document

```jsx
var doc = app.documents.length ? app.activeDocument : null;
```

## Selection

```jsx
var selectionCount = app.selection ? app.selection.length : 0;
var selected = selectionCount ? app.selection[0] : null;
```

## Margins To 10mm

```jsx
var doc = app.activeDocument;
var oldUnits = app.scriptPreferences.measurementUnit;
app.scriptPreferences.measurementUnit = MeasurementUnits.MILLIMETERS;

doc.marginPreferences.top = 10;
doc.marginPreferences.bottom = 10;
doc.marginPreferences.left = 10;
doc.marginPreferences.right = 10;

app.scriptPreferences.measurementUnit = oldUnits;
```

InDesign undo behavior differs from Photoshop. Prefer one `DoScript` call per
user request so the operation appears as a single script action in the undo
stack where possible.
