Translation into a grounded Flue plan
Priority	Action	Why this is grounded	Concrete Flue version
1	Bring PyPI README fully in sync with GitHub README	Claude Code’s assessment is right. PyPI keywords are minor; the PyPI landing page matters when people arrive from Google, package links, or pip context. PyPI’s docs explicitly say README content can be used as the project description.	Make README_PYPI.md show: what Flue is, install, one demo, supported apps, supported harnesses, “no MCP server,” limitations.
2	Create one canonical video demo	Context Mode benefited from video later, and Flue is more visual than Context Mode. Text alone is weaker for “agent controls desktop software.”	Split-screen: Claude Code/Codex terminal on one side, Blender or Photoshop responding on the other. 30–60 seconds.
3	Add an agent-skill surface	The current direction of discovery is not only package managers. GitHub is explicitly pushing gh skill as a way to discover/install portable agent skills across hosts.	Add a /skills or equivalent agent-skill package: “Use Flue to control desktop apps from coding agents.” Include Claude Code/Codex/OpenCode instructions.
4	Submit to catalogues/awesome lists	Context Mode did this via awesome-claude-code; it creates legitimate indexed references without Reddit spam.	Submit Flue to relevant lists with one neutral sentence: “CLI bridge for coding agents to control desktop software such as Blender, Photoshop, Unity, and 3ds Max without MCP servers.”
5	Write one short technical note	Context Mode had an explanatory blog/page immediately after the HN moment.	Title: “CLI-first desktop automation for coding agents.” Keep it technical. Explain when Flue is better than MCP and when MCP is better.
6	One HN post	HN was a real concentrated surface for Context Mode. It is not guaranteed, but it is still the cleanest non-social launch surface.	Post only after PyPI + demo + examples are aligned.
7	Reddit only after proof exists	Context Mode’s Reddit presence looks secondary, not origin.	One technical build report only. No repeated comments, no link-dropping.
My revised judgment

For Flue, PyPI keywords are not the issue. They are maintenance hygiene. The real pre-launch gaps are:

Area	Importance	Why
PyPI README parity	High	Someone landing there must not see a weaker version of the project.
Demo video	Very high	Flue’s claim is behavioral and visual; it needs proof.
Agent-skill packaging	High	This may become the actual discovery/install layer for tools meant for Claude Code/Codex/Cursor/Gemini-style agents.
Awesome-list/catalogue PRs	Medium-high	Legitimate low-stigma external references.
HN	Medium	Potential burst, not dependable.
X/LinkedIn	Low	Context Mode’s visible examples do not justify treating these as causal.
Reddit from a fresh account	Low / risky	Use only after there is a strong artifact and only as a build report.