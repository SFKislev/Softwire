# Premiere Pro ExtendScript Known Patterns

This file is intentionally small. Add full local scripting docs later.

## Context

Use `examples/context.jsx`.

## Active Project

```jsx
var projectName = app.project ? app.project.name : null;
```

## Active Sequence

```jsx
var sequence = app.project ? app.project.activeSequence : null;
var sequenceName = sequence ? sequence.name : null;
```

## Caution

Project, sequence, track, clip, render, export, and relink operations can affect
large amounts of work. Re-read context before changing them and keep each user
request bounded.
