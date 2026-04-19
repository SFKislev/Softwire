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

Bounded scripting:

Writing scripts into a live desktop app is delicate. Any script you submit runs
inside the host application's own scripting runtime, and a poorly bounded script
can make the app slow, bloated, modal, or unstable even if the shell bridge times
out or exits. Keep scripts small and targeted. Avoid unbounded enumeration,
large cross-document scans, expensive layout/render calculations, broad media
analysis, full asset-library searches, or open-ended loops unless the user
explicitly asks and accepts the risk. Prefer narrow probes, caps, filters,
known object names, active selections, and incremental verification. Do not ask
the host app to perform complicated work beyond what its scripting/runtime
surface can reasonably handle in a short interactive step.

Prefer structural app APIs over UI automation. Use examples and local docs only
to find the relevant scripting surface; do not dump broad app state.
