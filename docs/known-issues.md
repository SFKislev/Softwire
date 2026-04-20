# Known Issues

## Stale or Mismatched Bridge Sessions

**Symptom:** One agent harness (e.g. Codex) can reach the app; another (e.g. Claude Code) gets an `EvalScript error` or "endpoint unreachable" on the same machine.

**Cause:** CEP-backed adapters (Premiere Pro, After Effects, Audition) write a session file containing the eval URL and a random token when the panel loads. If the panel was reloaded or the app restarted since the agent last connected, the session file on disk has a new token. The agent's bridge is reading a stale or cached path.

**Fix:**
1. Start a new agent session. A fresh session will read the current session file on its first bridge call, which is often enough to recover.
2. If that doesn't help, close and reopen the adapter panel in the app (`Window > Extensions > Creative Adapter Bridge`). This forces the panel to write a fresh session file, then retry the context command.

If context still fails after both steps, check that the session file exists and is recent:

```powershell
Get-Item "$env:APPDATA\creative-adapters\premiere.json" | Select LastWriteTime
```

The timestamp should be within the last few minutes.

## App Becomes Sluggish or Unresponsive After Scripting

**Symptom:** The app slows down noticeably during or after a bridge run — menus respond slowly, playback stutters, the UI feels heavy.

**Cause:** A script submitted too much work to the app's scripting runtime: an unbounded enumeration, a broad scan across many items, an expensive layout or render calculation, or a loop that didn't exit cleanly. Even if the shell bridge timed out, the script may still be running inside the app.

**Fix:**
1. Stop any pending bridge processes:
   ```powershell
   python tools/cleanup_bridges.py --kill stale --older-than 30
   ```
2. If the app is still sluggish after that, recommend the user save their work and restart the app. Do not attempt further bridge calls until the app is responsive.
3. When scripting resumes, keep scripts narrow and targeted. Avoid the patterns that caused the slowdown.

Recommend a restart to the user honestly — do not retry the same heavy operation hoping it will finish faster.

## Agents Inventing API Calls Instead of Using Official Ones

**Symptom:** A task works, but the approach is inefficient, fragile, or visually incorrect — for example, a drop shadow applied by manually compositing layers rather than using the app's built-in Drop Shadow effect; a color change achieved by iterating pixels rather than adjusting a fill layer.

**Cause:** The agent used pretraining memory or general reasoning instead of consulting the app's official scripting API. The app almost always has a direct, optimised call for common operations. Hand-rolled workarounds are slower, harder to undo, and often produce subtly different results.

**Rule:** For any operation that sounds like a named feature in the app (drop shadow, gaussian blur, color balance, smart object, sequence marker, keyframe easing), assume the official API has a direct call for it. Introspect the running app or check official docs before inventing a workaround. If you used a workaround and later discover the official call, say so and offer to redo it correctly.

Refer to the API Discovery order in `shared/bridge-contract.md`: introspect first, then official vendor docs, then local notes, pretraining last.
