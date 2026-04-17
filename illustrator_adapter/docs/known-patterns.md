# Illustrator ExtendScript Known Patterns

This file is the curated high-signal reference for the first Illustrator adapter
test. Add the full Illustrator scripting reference later, but prefer these
patterns when they match the request.

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

## Set Selected Path Stroke

```jsx
var black = new RGBColor();
black.red = 0;
black.green = 0;
black.blue = 0;

var item = app.selection[0];
item.stroked = true;
item.strokeColor = black;
item.strokeWidth = 1;
item.filled = false;
```

Illustrator selection can contain groups, compound paths, text frames, placed
items, and plugin items. Check `typename` before applying path-only properties.
