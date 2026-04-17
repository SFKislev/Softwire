# After Effects ExtendScript Known Patterns

This file is intentionally small. Add tested snippets as the adapter is used.

## Context

Use `examples/context.jsx`.

## Active Project

```jsx
var project = app.project;
```

## Active Item

```jsx
var item = app.project ? app.project.activeItem : null;
```

`activeItem` is commonly a composition, footage item, or folder. Resolve
"current comp" and "this layer" through context before mutating.

## Caution

Render, export, collect, relink, save, and close operations affect large amounts
of work. Re-read context before changing project state and keep each user
request bounded.
