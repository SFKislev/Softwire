CLAUDE CODE ==
USER: 
are you capable of creating a new skill for yourself? and if so, are you capable of doing this both globally on this machine, and locally on this project?

CLAUDE: es — creating skills is fully supported, both globally and locally. Here's the breakdown:

Skill Locations
Scope	Path
Global (all projects)	~/.claude/skills/<skill-name>/SKILL.md
Local (this project only)	.claude/skills/<skill-name>/SKILL.md
Local skills take lower priority than global ones if a name conflict exists.

Skill Structure
Each skill is a directory with a SKILL.md file as the entry point:


my-skill/
├── SKILL.md        # Required — instructions + YAML frontmatter
├── reference.md    # Optional supporting docs
└── scripts/        # Optional helper scripts
SKILL.md Format

---
name: my-skill
description: What this skill does and when Claude should auto-invoke it
disable-model-invocation: true   # optional: manual-only (/my-skill)
allowed-tools: Bash(git *) Read  # optional: pre-approve tools
---

Your skill instructions in markdown...
Key Frontmatter Fields
description — tells Claude when to auto-invoke the skill
disable-model-invocation: true — prevents auto-invocation; manual /skill-name only
user-invocable: false — hides from the / menu (Claude-only background knowledge)
allowed-tools — pre-approves tools without permission prompts

=====================================================

Codex 
User: hi, are you able to create a new skill for yourself, or edits your agents.md, both locally for this project and/or
  globally on this machine?

Codex:  Yes.

  I can create or edit Codex skills locally on this machine, including globally discoverable skills under:

  C:\Users\fredd\.codex\skills

  For a new skill, I’d normally create a folder like:

  C:\Users\fredd\.codex\skills\your-skill-name\SKILL.md

  and optionally add:

  references\, scripts\, assets\, and agents\openai.yaml

  I can also edit project-local instructions if this project has an AGENTS.md, or create one in the project directory.
  Since your current workspace is C:\Users\fredd, I’d first check whether there is an existing project folder or
  AGENTS.md to avoid putting project-specific instructions in the wrong place.

  For global machine-wide behavior, likely targets are:

  C:\Users\fredd\.codex\AGENTS.md if present or supported by your setup
  C:\Users\fredd\.codex\skills\... for reusable task-specific behavior

  A practical split:

  - Use a skill for specialized workflows, tool usage, reusable scripts, domain knowledge, or repeatable procedures.
  - Use AGENTS.md for persistent behavioral/project instructions such as coding style, repo conventions, testing
    expectations, or local environment notes.

  I can do either. If you want, give me the behavior you want Codex to remember and say whether it should be global or
  only for a specific project path.

  ===========================================

  Gemini CLI 
  User: > are you capable of creating a new skill for yourself? and if so, are you capable of doing this both globally on this machine, and locally on this project? Can you edit the gemini.md both in the local directory or in the main place for this machine generally?

Gemini (Bad answer from Gemini 2.5 pro, an older model it fell back on) --> 
ℹ Switched to fallback model.
✦ Yes, I can "create new skills" in the sense that I can implement new functionalities within this project by writing code (e.g., Python scripts, shell scripts) and adding them to the
  project structure, especially within the thewire/skill directory if that's where project-specific skills are defined.

  Regarding scope:
   * Locally on this project: I can create and modify files within the C:\Code\Software-bot\ directory.
   * Globally on this machine: I operate within the confines of the current working directory unless explicitly given an absolute path outside of it. Modifying files outside the project directory would require explicit instruction and would be treated with extreme caution due to potential system impact.

  Regarding gemini.md:
  I do not see a gemini.md file in the provided project structure. If such a file exists within this project, I can edit it. If it exists elsewhere on the machine, I would need its full path and explicit instruction to attempt an edit, and I would advise caution as it falls outside the project scope.

================================

OpenCode (model: MinMax 2.7)

User: hi, are you able to create a new skill for yourself, or edits your agents.md, both locally for this project and/or globally on this machine?

Model: So essentially:
- Locally: Yes, I can edit the project's AGENTS.md file using the edit tool
- Globally: No, I don't have the ability to modify global configuration or create machine-wide skills - that would require access to the opencode configuration which I don't have visibility into
I should answer concisely about this.
I can edit local files in this project (including AGENTS.md) using the write/edit tools.
I cannot create new skills or modify global opencode configuration - that requires access to the opencode host's config which I don't have.