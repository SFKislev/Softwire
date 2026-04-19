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

Collaboration scope:

If the user asks for a task that is too large, complex, multi-step, or
autonomous to verify safely as one script run, say so before acting. Recommend
working in 1-2 observable steps at a time so the user can inspect the live app,
keep control, and correct direction early. Remind the user that the bridge acts
through scripting APIs and usually cannot visually inspect the final result, so
this setup is best used as close collaboration rather than unattended operation.

Prefer structural app APIs over UI automation. Use examples and local docs only
to find the relevant scripting surface; do not dump broad app state.
