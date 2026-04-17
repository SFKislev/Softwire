# Coexistence

The user is working in the app while the agent acts through the bridge.

Required loop:

1. Read live context at the start of each request.
2. Resolve references like "this", "current", "selected", and named documents
   from context before acting.
3. Act only on the active document, current selection, or an explicitly named
   document/object.
4. Do not save, close, export, package, relink, switch documents, or launch apps
   unless explicitly asked.
5. Re-read context before destructive or multi-step changes.
6. Keep failures in the terminal; do not hide scripting errors.
7. Report partial support honestly, especially for modal dialogs or opaque app
   UI state.

Prefer structural app APIs over UI automation. Use examples and local docs only
to find the relevant scripting surface; do not dump broad app state.
