# Harness Support

Running `softwire setup` makes SoftWire discoverable by agentic frameworks. The following changes are made in order to make softwire discoverable.

## Supported Harnesses


| Harness               | File adjustments                                                                                                                              |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Codex                 | Installs`~/.codex/skills/softwire/` and upserts a SoftWire pointer block into `~/.codex/AGENTS.md`.                                           |
| Claude Code           | Installs`~/.claude/softwire.md`, upserts a SoftWire pointer block into `~/.claude/CLAUDE.md`, and also installs `~/.claude/skills/softwire/`. |
| Gemini CLI            | Installs`~/.gemini/softwire.md` and upserts a SoftWire pointer block into `~/.gemini/GEMINI.md`.                                              |
| Qwen CLI              | Installs`~/.qwen/softwire.md` and upserts a SoftWire pointer block into `~/.qwen/QWEN.md`.                                                    |
| Cursor                | Installs a global skill at`~/.cursor/skills/softwire/SKILL.md` (skill frontmatter enables discovery).                                         |
| Kilo CLI              | Installs a global skill at`~/.kilo/skills/softwire/SKILL.md`.                                                                                  |
| OpenCode              | Installs`~/.config/opencode/agents/softwire.md`.                                                                                              |
| OpenClaw              | Installs`~/.openclaw/skills/softwire/SKILL.md`.                                                                                               |
| Generic (`AGENTS.md`) | Installs generic instructions into`AGENTS.md` (defaults to the current directory unless `--path` is provided).                                |

## Notes

- Auto setup mode detects installed harnesses and registers all detected targets; if none are detected, it falls back to the generic `AGENTS.md` target.
- Use `softwire harnesses` to inspect detection reasons and expected global target paths.
- Use `softwire setup --agent <target>` for specific, single-harness registration.
