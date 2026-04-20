# Creative Software Adapters

Before operating an app, read:

1. `shared/coexistence.md`
2. `shared/bridge-contract.md`
3. `adapters/<app>_adapter/APP.md`

Then run that app's context example before acting.

Read app-local `examples/` and optional `docs/` for scripting details. Treat
`examples/` as reference material, not a scratch directory.

Prefer passing one-off scripts through `--stdin`. If a script must be written to
disk for encoding, debugging, or host-runtime reasons, put it under a temp or
scratch path such as `.tmp/<app>/` or the OS temp directory, then remove it after
the run unless the user asks to keep it. Do not add task-specific scripts to
adapter source folders.

Keep edits scoped to the user's live app state and report bridge/app errors
directly.
