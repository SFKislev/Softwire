# Known Issues

- Some desktop apps can block inside their scripting runtime or COM dispatch.
  When that happens, the shell bridge may time out, but the host app can still
  remain busy or modal until the app finishes or is interrupted.
- For Windows apps with a known process name, `softwire modal <app>` can inspect
  top-level windows and `softwire modal <app> --dismiss` can attempt a bounded
  cancel-style dismissal outside the blocked scripting runtime.
- Modal dialogs and opaque app UI state are not fully inspectable through these
  adapters. Agents should report partial visibility honestly and avoid claiming
  success without runtime confirmation.
- A local `softwire` launcher may not be on `PATH` in every shell session.
  Prefer `py -m softwire.cli ...` when launch resolution is uncertain.
