# Audition ExtendScript Known Patterns

This file is intentionally small. Add tested snippets as the adapter is used.

## Context

Use `examples/context.jsx`.

## Caution

Audition operations can alter audio destructively or export large files. Re-read
context before edits and keep each request bounded.

Do not save, export, mix down, batch process, relink, close, or overwrite audio
unless the user explicitly asks.
