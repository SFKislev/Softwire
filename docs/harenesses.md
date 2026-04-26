# Harness Support

Running `softwire setup` makes SoftWire discoverable by agentic frameworks.
Setup now installs a local SoftWire docs bundle into each harness location, then
adds a small pointer so the harness can read those docs directly from its own
skill or rules directory.

## Supported Harnesses

| Harness               | File adjustments                                                                                                                              |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Codex                 | Installs `~/.codex/skills/softwire/` with `SKILL.md`, `shared/*`, `docs/*`, and `adapters/*/APP.md`, then upserts a SoftWire pointer block into `~/.codex/AGENTS.md`. |
| Claude Code           | Installs `~/.claude/skills/softwire/` with the local docs bundle and upserts a SoftWire pointer block into `~/.claude/CLAUDE.md`. |
| Gemini CLI            | Installs `~/.gemini/softwire/` with the local docs bundle and upserts a SoftWire pointer block into `~/.gemini/GEMINI.md`. |
| Qwen CLI              | Installs `~/.qwen/softwire/` with the local docs bundle and upserts a SoftWire pointer block into `~/.qwen/QWEN.md`. |
| GitHub Copilot        | Installs `~/.copilot/skills/softwire/` with the local docs bundle and writes global Copilot instruction files so Copilot can discover the skill outside any single repository. |
| Cursor                | Installs a global skill at `~/.cursor/skills/softwire/` with `SKILL.md`, `shared/*`, `docs/*`, and `adapters/*/APP.md`. |
| Cline                 | Installs a global skill at `~/.cline/skills/softwire/` with the local docs bundle. |
| Kilo CLI              | Installs a global skill at `~/.kilo/skills/softwire/` with the local docs bundle. |
| OpenCode              | Installs `~/.config/opencode/agents/softwire/` with the local docs bundle and writes `~/.config/opencode/agents/softwire.md`. |
| OpenClaw              | Installs `~/.openclaw/skills/softwire/` with the local docs bundle. |
| Generic (`AGENTS.md`) | Installs `./softwire/` with the local docs bundle plus a pointer from `AGENTS.md` in the target directory (defaults to the current directory unless `--path` is provided). |

## Notes

- Auto setup mode detects installed harnesses and registers all detected targets.
- If no supported harness is detected, `softwire setup` stops and reports that SoftWire needs a harness in order to work.
- Use `softwire harnesses` to inspect detected harnesses.
- Use `softwire setup --agent <target>` for specific, single-harness registration.
- Use `softwire uninstall` to remove the installed SoftWire docs bundle and pointer files from detected harnesses.
