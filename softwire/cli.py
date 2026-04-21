import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ALIASES = {
    "3dsmax": "3dsmax",
    "3ds-max": "3dsmax",
    "max": "3dsmax",
    "aftereffects": "after_effects",
    "after-effects": "after_effects",
    "ae": "after_effects",
    "audition": "audition",
    "blender": "blender",
    "excel": "excel",
    "houdini": "houdini",
    "illustrator": "illustrator",
    "indesign": "indesign",
    "photoshop": "photoshop",
    "powerpoint": "powerpoint",
    "premiere": "premiere",
    "premierepro": "premiere",
    "premiere-pro": "premiere",
    "unity": "unity",
    "word": "word",
}

BRIDGES = {
    "3dsmax": "3dsmax_bridge.py",
    "after_effects": "after_effects_bridge.py",
    "audition": "audition_bridge.py",
    "blender": "blender_bridge.py",
    "excel": "excel_bridge.py",
    "houdini": "houdini_bridge.py",
    "illustrator": "illustrator_bridge.py",
    "indesign": "indesign_bridge.py",
    "photoshop": "photoshop_bridge.py",
    "powerpoint": "powerpoint_bridge.py",
    "premiere": "premiere_bridge.py",
    "unity": "unity_bridge.py",
    "word": "word_bridge.py",
}

CONTEXT_EXAMPLES = {
    "3dsmax": "context.py",
    "after_effects": "context.jsx",
    "audition": "context.jsx",
    "blender": "context.py",
    "excel": "context.py",
    "houdini": "context.py",
    "illustrator": "context.jsx",
    "indesign": "context.jsx",
    "photoshop": "context.jsx",
    "powerpoint": "context.py",
    "premiere": "context.jsx",
    "unity": "context.json",
    "word": "context.py",
}

AGENT_DOC_TARGETS = ("codex", "claude", "gemini", "qwen", "cursor", "cline", "kilo", "opencode", "openclaw", "generic", "all")

HARNESS_CONFIGS = {
    "codex": {
        "commands": ["codex"],
        "config_dir": Path(".codex"),
        "global_targets": [
            Path(".codex") / "skills" / "softwire" / "SKILL.md",
            Path(".codex") / "AGENTS.md",
        ],
    },
    "claude": {
        "commands": ["claude"],
        "config_dir": Path(".claude"),
        "global_targets": [
            Path(".claude") / "CLAUDE.md",
            Path(".claude") / "skills" / "softwire" / "SKILL.md",
        ],
    },
    "gemini": {
        "commands": ["gemini"],
        "config_dir": Path(".gemini"),
        "global_targets": [
            Path(".gemini") / "GEMINI.md",
            Path(".gemini") / "softwire.md",
        ],
    },
    "qwen": {
        "commands": ["qwen"],
        "config_dir": Path(".qwen"),
        "global_targets": [
            Path(".qwen") / "QWEN.md",
            Path(".qwen") / "softwire.md",
        ],
    },
    "cursor": {
        "commands": ["cursor"],
        "config_dir": Path(".cursor"),
        "global_targets": [
            Path(".cursor") / "skills" / "softwire" / "SKILL.md",
        ],
    },
    "cline": {
        "commands": ["cline"],
        "config_dir": Path(".cline"),
        "global_targets": [
            Path(".cline") / "skills" / "softwire" / "SKILL.md",
        ],
    },
    "kilo": {
        "commands": ["kilo"],
        "config_dir": Path(".kilo"),
        "global_targets": [
            Path(".kilo") / "skills" / "softwire" / "SKILL.md",
        ],
    },
    "opencode": {
        "commands": ["opencode"],
        "config_dir": Path(".config") / "opencode",
        "global_targets": [
            Path(".config") / "opencode" / "agents" / "softwire.md",
        ],
    },
    "openclaw": {
        "commands": ["openclaw"],
        "config_dir": Path(".openclaw"),
        "global_targets": [
            Path(".openclaw") / "skills" / "softwire" / "SKILL.md",
        ],
    },
}


def adapter_name(value):
    key = value.lower().replace("_", "-")
    try:
        return ALIASES[key]
    except KeyError:
        choices = ", ".join(sorted(set(ALIASES)))
        raise argparse.ArgumentTypeError(f"unknown adapter '{value}'. Choices: {choices}")


def adapter_dir(name):
    path = ROOT / "adapters" / f"{name}_adapter"
    if not path.exists():
        raise FileNotFoundError(f"Adapter directory not found: {path}")
    return path


def bridge_path(name):
    path = adapter_dir(name) / BRIDGES[name]
    if not path.exists():
        raise FileNotFoundError(f"Bridge script not found: {path}")
    return path


def run_process(args, *, input_text=None):
    proc = subprocess.run(
        args,
        cwd=str(ROOT),
        input=input_text,
        text=True,
        check=False,
    )
    return proc.returncode


def normalize_path_key(path):
    text = str(path)
    return text.lower() if os.name == "nt" else text


def unique_paths(paths):
    seen = set()
    result = []
    for path in paths:
        key = normalize_path_key(path)
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result


def home_candidates():
    candidates = [Path.home()]
    userprofile = os.environ.get("USERPROFILE")
    if userprofile:
        candidates.append(Path(userprofile))

    if os.name == "nt":
        username = os.environ.get("USERNAME")
        if username:
            candidates.append(Path("C:/Users") / username)
        homedrive = os.environ.get("HOMEDRIVE")
        homepath = os.environ.get("HOMEPATH")
        if homedrive and homepath:
            candidates.append(Path(homedrive + homepath))

    result = []
    for index, path in enumerate(unique_paths(candidates)):
        if index == 0 or path.exists():
            result.append(path)
    return result


def scripts_dir():
    executable_dir = Path(sys.executable).resolve().parent
    if os.name != "nt":
        return executable_dir
    if executable_dir.name.lower() == "scripts":
        return executable_dir
    return executable_dir / "Scripts"


def path_entries():
    return [Path(item) for item in os.environ.get("PATH", "").split(os.pathsep) if item]


def is_scripts_dir_on_path():
    scripts = normalize_path_key(scripts_dir())
    return any(normalize_path_key(path) == scripts for path in path_entries())


def installed_command(name):
    return shutil.which(name)


def module_command():
    return [sys.executable, "-m", "softwire.cli"]


def format_command_for_display(parts):
    return subprocess.list2cmdline([str(part) for part in parts])


def powershell_command_literal(parts):
    quoted = []
    for part in parts:
        text = str(part).replace("'", "''")
        quoted.append(f"'{text}'")
    return "& " + " ".join(quoted)


def packaged_skill_source():
    candidates = [
        ROOT / "skill.md",
        ROOT / "softwire" / "skill.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("SoftWire skill source not found.")


def packaged_known_issues_source():
    candidates = [
        ROOT / "docs" / "known-issues.md",
        ROOT / "softwire" / "known-issues.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("SoftWire known-issues source not found.")


def softwire_install_info():
    return {
        "root": str(ROOT),
        "pythonExecutable": str(Path(sys.executable).resolve()),
        "scriptsDir": str(scripts_dir()),
        "docsPath": str(packaged_skill_source()),
        "softwireCommandPath": installed_command("softwire"),
        "softwireOnPath": installed_command("softwire") is not None,
        "scriptsDirOnPath": is_scripts_dir_on_path(),
        "preferredCommand": "softwire" if installed_command("softwire") else format_command_for_display(module_command()),
        "fallbackCommand": format_command_for_display(module_command()),
        "homeCandidates": [str(path) for path in home_candidates()],
    }


def cmd_path(_args):
    print(ROOT)
    return 0


def cmd_where(_args):
    print(json.dumps(softwire_install_info(), indent=2))
    return 0


def cmd_adapters(_args):
    for name in sorted(BRIDGES):
        print(name)
    return 0


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(path)
    return True


def copy_file(source, target, *, force):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        print(f"File already exists: {target}. Use --force to replace it.", file=sys.stderr)
        return False
    shutil.copy2(source, target)
    print(target)
    return True


def copy_dir(source, target, *, force):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if not force:
            print(f"Directory already exists: {target}. Use --force to replace it.", file=sys.stderr)
            return False
        shutil.rmtree(target)
    shutil.copytree(source, target)
    print(target)
    return True


def remove_file(path):
    if not path.exists():
        return False
    path.unlink()
    print(path)
    return True


def remove_dir(path):
    if not path.exists():
        return False
    shutil.rmtree(path)
    print(path)
    return True


def upsert_marked_block(path, begin, end, block):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    if begin in content and end in content:
        start = content.index(begin)
        finish = content.index(end, start) + len(end)
        content = content[:start] + block + content[finish:]
    else:
        separator = "\n\n" if content.strip() else ""
        content = content.rstrip() + separator + block
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def remove_marked_block(path, begin, end):
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    if begin not in content or end not in content:
        return False
    start = content.index(begin)
    finish = content.index(end, start) + len(end)
    new_content = (content[:start] + content[finish:]).strip()
    if new_content:
        path.write_text(new_content + "\n", encoding="utf-8")
        print(path)
    else:
        path.unlink()
        print(path)
    return True


def remove_if_matches(path, source):
    if not path.exists():
        return False
    if path.read_text(encoding="utf-8") != source.read_text(encoding="utf-8"):
        print(f"Skipping modified file: {path}", file=sys.stderr)
        return False
    path.unlink()
    print(path)
    return True


def adapter_docs_sources():
    items = []
    for adapter_path in sorted((ROOT / "adapters").glob("*_adapter")):
        app_md = adapter_path / "APP.md"
        if not app_md.exists():
            continue
        name = adapter_path.name.removesuffix("_adapter")
        adapter_files = [("APP.md", app_md)]
        api_index = adapter_path / "docs" / "api-index.txt"
        if api_index.exists():
            adapter_files.append(("docs/api-index.txt", api_index))
        items.append((name, adapter_files))
    return items


def pointer_note_text(relative_entry):
    return f"""# SoftWire

If asked to perform a task in a desktop application, use SoftWire: a Python
package installed on this machine that lets agents inspect and edit supported
apps through their scripting APIs.

Read `{relative_entry}` first.
"""


def installed_skill_text(description):
    body = packaged_skill_source().read_text(encoding="utf-8").rstrip()
    return f"""---
name: softwire
description: {description}
---

{body}
"""


def install_local_docs_bundle(bundle_dir, *, entry_filename, entry_text, force):
    ok = True
    if bundle_dir.exists():
        if not force:
            print(f"Directory already exists: {bundle_dir}. Use --force to replace it.", file=sys.stderr)
            return False
        for stale_file in ("SKILL.md", "INDEX.md", "AGENTS.md", "common.md"):
            stale_path = bundle_dir / stale_file
            if stale_file != entry_filename:
                remove_file(stale_path)
        remove_dir(bundle_dir / "shared")
        remove_dir(bundle_dir / "docs")
        remove_dir(bundle_dir / "adapters")
    bundle_dir.mkdir(parents=True, exist_ok=True)
    ok = write_text(bundle_dir / entry_filename, entry_text) and ok

    shared_dir = bundle_dir / "shared"
    ok = copy_file(ROOT / "shared" / "coexistence.md", shared_dir / "coexistence.md", force=True) and ok
    ok = copy_file(ROOT / "shared" / "bridge-contract.md", shared_dir / "bridge-contract.md", force=True) and ok

    docs_dir = bundle_dir / "docs"
    ok = copy_file(packaged_known_issues_source(), docs_dir / "known-issues.md", force=True) and ok

    adapters_dir = bundle_dir / "adapters"
    for name, files in adapter_docs_sources():
        for relative_path, source in files:
            ok = copy_file(source, adapters_dir / name / relative_path, force=True) and ok
    return ok


def softwire_pointer_block(entry_path):
    begin = "<!-- SOFTWIRE START -->"
    end = "<!-- SOFTWIRE END -->"
    block = (
        f"{begin}\n"
        "# SoftWire\n\n"
        "SoftWire is installed on this machine. It lets agents communicate with "
        "supported desktop software directly through local scripting bridges, "
        "without MCP servers.\n\n"
        "When requested to operate supported desktop software, read:\n\n"
        f"`{entry_path}`\n"
        f"{end}"
    )
    return begin, end, block


def cmd_agent_docs_path(_args):
    print(packaged_skill_source())
    return 0


def cmd_docs(_args):
    print(packaged_skill_source())
    return 0


def harness_report():
    homes = home_candidates()
    report = []
    for name, config in HARNESS_CONFIGS.items():
        commands = []
        for command in config["commands"]:
            commands.append({"name": command, "path": installed_command(command)})

        config_dirs = []
        targets = []
        for home in homes:
            config_dir = home / config["config_dir"]
            config_dirs.append({"home": str(home), "path": str(config_dir), "exists": config_dir.exists()})
            for target in config["global_targets"]:
                path = home / target
                targets.append({"home": str(home), "path": str(path), "exists": path.exists()})

        command_on_path = any(item["path"] for item in commands)
        detection_reasons = []
        if command_on_path:
            detection_reasons.append("command")
        if any(item["exists"] for item in config_dirs):
            detection_reasons.append("config_dir")

        detected = bool(detection_reasons)
        report.append(
            {
                "harness": name,
                "commandOnPath": command_on_path,
                "commands": commands,
                "homes": [str(home) for home in homes],
                "configDir": config_dirs[0]["path"],
                "configDirExists": config_dirs[0]["exists"],
                "configDirs": config_dirs,
                "detectionReasons": detection_reasons,
                "detected": detected,
                "globalTargets": targets,
            }
        )
    return report


def detect_agent_targets():
    targets = []
    for item in harness_report():
        if item["detected"]:
            targets.append(item["harness"])
    return targets


def cmd_harnesses(_args):
    if getattr(_args, "json", False):
        print(json.dumps(harness_report(), indent=2))
        return 0

    rows = []
    for item in harness_report():
        status = "yes" if item["detected"] else "no"
        targets = []
        for target in item["globalTargets"]:
            if target["exists"]:
                targets.append(target["path"])
        target_text = "; ".join(targets) if targets else "-"
        rows.append(
            {
                "Harness": item["harness"],
                "Detected": status,
                "Targets": target_text,
            }
        )

    headers = ["Harness", "Detected", "Targets"]
    widths = {header: len(header) for header in headers}
    for row in rows:
        for header in headers:
            widths[header] = max(widths[header], len(row[header]))

    header_line = "  ".join(header.ljust(widths[header]) for header in headers)
    divider = "  ".join("-" * widths[header] for header in headers)
    print(header_line)
    print(divider)
    for row in rows:
        print("  ".join(row[header].ljust(widths[header]) for header in headers))
    return 0


def install_codex_docs(args):
    ok = True
    if args.path:
            bundle_dir = Path(args.path).expanduser() / "softwire"
            ok = install_local_docs_bundle(
                bundle_dir,
                entry_filename="SKILL.md",
                entry_text=installed_skill_text(
                    "Use when Codex needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
                ),
                force=args.force,
        ) and ok
    else:
        for home in home_candidates():
            bundle_dir = home / ".codex" / "skills" / "softwire"
            ok = install_local_docs_bundle(
                bundle_dir,
                entry_filename="SKILL.md",
                entry_text=installed_skill_text(
                    "Use when Codex needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
                ),
                force=args.force,
            ) and ok
            begin, end, block = softwire_pointer_block(bundle_dir / "SKILL.md")
            agents = home / ".codex" / "AGENTS.md"
            upsert_marked_block(agents, begin, end, block)
            print(agents)
    return ok


def install_claude_docs(args):
    ok = True
    if args.path:
        target_root = Path(args.path).expanduser()
        bundle_dir = target_root / "skills" / "softwire"
        ok = install_local_docs_bundle(
            bundle_dir,
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Claude needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
        remove_file(target_root / "softwire.md")
        begin, end, block = softwire_pointer_block(bundle_dir / "SKILL.md")
        memory = target_root / "CLAUDE.md"
        upsert_marked_block(memory, begin, end, block)
        print(memory)
    else:
        for home in home_candidates():
            target_root = home / ".claude"
            bundle_dir = target_root / "skills" / "softwire"
            ok = install_local_docs_bundle(
                bundle_dir,
                entry_filename="SKILL.md",
                entry_text=installed_skill_text(
                    "Use when Claude needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
                ),
                force=args.force,
            ) and ok
            remove_file(target_root / "softwire.md")
            begin, end, block = softwire_pointer_block(bundle_dir / "SKILL.md")
            memory = target_root / "CLAUDE.md"
            upsert_marked_block(memory, begin, end, block)
            print(memory)
    return ok


def install_gemini_docs(args):
    ok = True
    if args.path:
        target_root = Path(args.path).expanduser()
        bundle_dir = target_root / "softwire"
        ok = install_local_docs_bundle(
            bundle_dir,
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Gemini needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
        remove_file(target_root / "softwire.md")
        begin, end, block = softwire_pointer_block(bundle_dir / "SKILL.md")
        memory = target_root / "GEMINI.md"
        upsert_marked_block(memory, begin, end, block)
        print(memory)
    else:
        for home in home_candidates():
            target_root = home / ".gemini"
            bundle_dir = target_root / "softwire"
            ok = install_local_docs_bundle(
                bundle_dir,
                entry_filename="SKILL.md",
                entry_text=installed_skill_text(
                    "Use when Gemini needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
                ),
                force=args.force,
            ) and ok
            remove_file(target_root / "softwire.md")
            begin, end, block = softwire_pointer_block(bundle_dir / "SKILL.md")
            memory = target_root / "GEMINI.md"
            upsert_marked_block(memory, begin, end, block)
            print(memory)
    return ok


def install_cursor_docs(args):
    ok = True
    if args.path:
        return install_local_docs_bundle(
            Path(args.path).expanduser() / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Cursor needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        )
    for home in home_candidates():
        ok = install_local_docs_bundle(
            home / ".cursor" / "skills" / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Cursor needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
    return ok


def install_kilo_docs(args):
    ok = True
    if args.path:
        return install_local_docs_bundle(
            Path(args.path).expanduser() / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Kilo needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        )
    for home in home_candidates():
        ok = install_local_docs_bundle(
            home / ".kilo" / "skills" / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Kilo needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
    return ok


def install_cline_docs(args):
    ok = True
    if args.path:
        return install_local_docs_bundle(
            Path(args.path).expanduser() / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Cline needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        )
    for home in home_candidates():
        ok = install_local_docs_bundle(
            home / ".cline" / "skills" / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Cline needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
    return ok


def install_qwen_docs(args):
    ok = True
    if args.path:
        target_root = Path(args.path).expanduser()
        bundle_dir = target_root / "softwire"
        ok = install_local_docs_bundle(
            bundle_dir,
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when Qwen needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
        remove_file(target_root / "softwire.md")
        begin, end, block = softwire_pointer_block(bundle_dir / "SKILL.md")
        memory = target_root / "QWEN.md"
        upsert_marked_block(memory, begin, end, block)
        print(memory)
    else:
        for home in home_candidates():
            target_root = home / ".qwen"
            bundle_dir = target_root / "softwire"
            ok = install_local_docs_bundle(
                bundle_dir,
                entry_filename="SKILL.md",
                entry_text=installed_skill_text(
                    "Use when Qwen needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
                ),
                force=args.force,
            ) and ok
            remove_file(target_root / "softwire.md")
            begin, end, block = softwire_pointer_block(bundle_dir / "SKILL.md")
            memory = target_root / "QWEN.md"
            upsert_marked_block(memory, begin, end, block)
            print(memory)
    return ok


def install_opencode_docs(args):
    ok = True
    if args.path:
        target_root = Path(args.path).expanduser()
        ok = install_local_docs_bundle(
            target_root / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when OpenCode needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
        ok = write_text(target_root / "softwire.md", pointer_note_text("softwire/SKILL.md")) and ok
        return ok
    for home in home_candidates():
        target_root = home / ".config" / "opencode" / "agents"
        ok = install_local_docs_bundle(
            target_root / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when OpenCode needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
        ok = write_text(target_root / "softwire.md", pointer_note_text("softwire/SKILL.md")) and ok
    return ok


def install_openclaw_docs(args):
    ok = True
    if args.path:
        return install_local_docs_bundle(
            Path(args.path).expanduser() / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when OpenClaw needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        )
    for home in home_candidates():
        ok = install_local_docs_bundle(
            home / ".openclaw" / "skills" / "softwire",
            entry_filename="SKILL.md",
            entry_text=installed_skill_text(
                "Use when OpenClaw needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
            ),
            force=args.force,
        ) and ok
    return ok


def install_generic_docs(args):
    target = Path(args.path).expanduser() if args.path else Path.cwd() / "AGENTS.md"
    bundle_dir = target.parent / "softwire"
    ok = install_local_docs_bundle(
        bundle_dir,
        entry_filename="SKILL.md",
        entry_text=installed_skill_text(
            "Use when an agent needs to inspect, install, test, or run SoftWire adapters to control supported Windows desktop apps through local scripting bridges.",
        ),
        force=args.force,
    )
    ok = write_text(target, pointer_note_text("softwire/SKILL.md")) and ok
    return ok


def uninstall_codex_docs(args):
    removed = False
    begin, end, _block = softwire_pointer_block("softwire")
    if args.path:
        removed = remove_dir(Path(args.path).expanduser() / "softwire") or removed
    else:
        for home in home_candidates():
            removed = remove_dir(home / ".codex" / "skills" / "softwire") or removed
            removed = remove_marked_block(home / ".codex" / "AGENTS.md", begin, end) or removed
    return removed


def uninstall_claude_docs(args):
    removed = False
    begin, end, _block = softwire_pointer_block("softwire")
    if args.path:
        target_root = Path(args.path).expanduser()
        removed = remove_file(target_root / "softwire.md") or removed
        removed = remove_dir(target_root / "skills" / "softwire") or removed
        removed = remove_marked_block(target_root / "CLAUDE.md", begin, end) or removed
    else:
        for home in home_candidates():
            target_root = home / ".claude"
            removed = remove_file(target_root / "softwire.md") or removed
            removed = remove_dir(target_root / "skills" / "softwire") or removed
            removed = remove_marked_block(target_root / "CLAUDE.md", begin, end) or removed
    return removed


def uninstall_gemini_docs(args):
    removed = False
    begin, end, _block = softwire_pointer_block("softwire")
    if args.path:
        target_root = Path(args.path).expanduser()
        removed = remove_file(target_root / "softwire.md") or removed
        removed = remove_dir(target_root / "softwire") or removed
        removed = remove_marked_block(target_root / "GEMINI.md", begin, end) or removed
    else:
        for home in home_candidates():
            target_root = home / ".gemini"
            removed = remove_file(target_root / "softwire.md") or removed
            removed = remove_dir(target_root / "softwire") or removed
            removed = remove_marked_block(target_root / "GEMINI.md", begin, end) or removed
    return removed


def uninstall_cursor_docs(args):
    removed = False
    if args.path:
        return remove_dir(Path(args.path).expanduser() / "softwire")
    for home in home_candidates():
        removed = remove_dir(home / ".cursor" / "skills" / "softwire") or removed
    return removed


def uninstall_kilo_docs(args):
    removed = False
    if args.path:
        return remove_dir(Path(args.path).expanduser() / "softwire")
    for home in home_candidates():
        removed = remove_dir(home / ".kilo" / "skills" / "softwire") or removed
    return removed


def uninstall_cline_docs(args):
    removed = False
    if args.path:
        return remove_dir(Path(args.path).expanduser() / "softwire")
    for home in home_candidates():
        removed = remove_dir(home / ".cline" / "skills" / "softwire") or removed
    return removed


def uninstall_qwen_docs(args):
    removed = False
    begin, end, _block = softwire_pointer_block("softwire")
    if args.path:
        target_root = Path(args.path).expanduser()
        removed = remove_file(target_root / "softwire.md") or removed
        removed = remove_dir(target_root / "softwire") or removed
        removed = remove_marked_block(target_root / "QWEN.md", begin, end) or removed
    else:
        for home in home_candidates():
            target_root = home / ".qwen"
            removed = remove_file(target_root / "softwire.md") or removed
            removed = remove_dir(target_root / "softwire") or removed
            removed = remove_marked_block(target_root / "QWEN.md", begin, end) or removed
    return removed


def uninstall_opencode_docs(args):
    removed = False
    if args.path:
        target_root = Path(args.path).expanduser()
        removed = remove_file(target_root / "softwire.md") or removed
        removed = remove_dir(target_root / "softwire") or removed
        return removed
    for home in home_candidates():
        target_root = home / ".config" / "opencode" / "agents"
        removed = remove_file(target_root / "softwire.md") or removed
        removed = remove_dir(target_root / "softwire") or removed
    return removed


def uninstall_openclaw_docs(args):
    removed = False
    if args.path:
        return remove_dir(Path(args.path).expanduser() / "softwire")
    for home in home_candidates():
        removed = remove_dir(home / ".openclaw" / "skills" / "softwire") or removed
    return removed


def uninstall_generic_docs(args):
    target = Path(args.path).expanduser() if args.path else Path.cwd() / "AGENTS.md"
    removed = remove_file(target) or False
    removed = remove_dir(target.parent / "softwire") or removed
    return removed


def cmd_install_agent_docs(args):
    targets = ("codex", "claude", "gemini", "qwen", "cursor", "cline", "kilo", "opencode", "openclaw", "generic") if args.target == "all" else (args.target,)
    ok = True
    for target in targets:
        if target == "codex":
            ok = install_codex_docs(args) and ok
        elif target == "claude":
            ok = install_claude_docs(args) and ok
        elif target == "gemini":
            ok = install_gemini_docs(args) and ok
        elif target == "qwen":
            ok = install_qwen_docs(args) and ok
        elif target == "cursor":
            ok = install_cursor_docs(args) and ok
        elif target == "cline":
            ok = install_cline_docs(args) and ok
        elif target == "kilo":
            ok = install_kilo_docs(args) and ok
        elif target == "opencode":
            ok = install_opencode_docs(args) and ok
        elif target == "openclaw":
            ok = install_openclaw_docs(args) and ok
        elif target == "generic":
            ok = install_generic_docs(args) and ok
    return 0 if ok else 1


def cmd_uninstall(args):
    if args.agent == "auto":
        targets = detect_agent_targets()
        if not targets:
            targets = ["generic"]
    elif args.agent == "all":
        targets = ["codex", "claude", "gemini", "qwen", "cursor", "cline", "kilo", "opencode", "openclaw", "generic"]
    else:
        targets = [args.agent]

    print("Removing SoftWire agent instructions for: " + ", ".join(targets))
    removed_any = False
    for target in targets:
        if target == "codex":
            removed_any = uninstall_codex_docs(args) or removed_any
        elif target == "claude":
            removed_any = uninstall_claude_docs(args) or removed_any
        elif target == "gemini":
            removed_any = uninstall_gemini_docs(args) or removed_any
        elif target == "qwen":
            removed_any = uninstall_qwen_docs(args) or removed_any
        elif target == "cursor":
            removed_any = uninstall_cursor_docs(args) or removed_any
        elif target == "cline":
            removed_any = uninstall_cline_docs(args) or removed_any
        elif target == "kilo":
            removed_any = uninstall_kilo_docs(args) or removed_any
        elif target == "opencode":
            removed_any = uninstall_opencode_docs(args) or removed_any
        elif target == "openclaw":
            removed_any = uninstall_openclaw_docs(args) or removed_any
        elif target == "generic":
            removed_any = uninstall_generic_docs(args) or removed_any
    return 0 if removed_any else 1


def cmd_setup(args):
    if args.agent == "auto":
        targets = detect_agent_targets()
        if not targets:
            print("No AI harness found. SoftWire needs a harness in order to work.", file=sys.stderr)
            return 1
        chosen = targets
    elif args.agent == "all":
        chosen = ["codex", "claude", "gemini", "qwen", "cursor", "cline", "kilo", "opencode", "openclaw"]
    else:
        chosen = [args.agent]

    print("Registering SoftWire agent instructions for: " + ", ".join(chosen))
    homes = home_candidates()
    if len(homes) > 1:
        print("Detected multiple home directories:")
        for home in homes:
            print(f"  {home}")

    ok = True
    for target in chosen:
        setup_args = argparse.Namespace(target=target, path=None, force=args.force)
        ok = (cmd_install_agent_docs(setup_args) == 0) and ok

    info = softwire_install_info()
    print("")
    print("SoftWire is installed. New agent sessions should discover it through the registered global instructions.")
    print(f"Use SoftWire with: {info['preferredCommand']}")
    if not info["softwireOnPath"]:
        print("The 'softwire' command is not on PATH in this shell. Agents should use the Python module fallback.")
        print(f"Fallback command: {info['fallbackCommand']}")
    elif not info["scriptsDirOnPath"]:
        print("Warning: the current Python Scripts directory is not on PATH for this shell session.")
        print(f"Fallback command: {info['fallbackCommand']}")
    print("Verify the bridge runtime with: " + info["preferredCommand"] + " adapters")
    return 0 if ok else 1


def cmd_context(args):
    name = args.adapter
    context = adapter_dir(name) / "examples" / CONTEXT_EXAMPLES[name]
    if not context.exists():
        raise FileNotFoundError(f"Context example not found: {context}")
    return run_process(
        [sys.executable, str(bridge_path(name)), "--stdin"],
        input_text=context.read_text(encoding="utf-8-sig"),
    )


def cmd_run(args):
    command = [sys.executable, str(bridge_path(args.adapter))]
    input_text = None
    if args.stdin:
        command.append("--stdin")
        input_text = sys.stdin.read()
    elif args.file:
        command.extend(["--file", args.file])
    elif args.code:
        command.append(args.code)
    else:
        command.append("--stdin")
        input_text = sys.stdin.read()
    return run_process(command, input_text=input_text)


def cmd_install(args):
    if os.name != "nt":
        print("Adapter installers are currently Windows-only.", file=sys.stderr)
        return 1

    script = None
    for candidate in (
        "install_bridge.ps1",
        "install_addon.ps1",
        "install_cep_bridge.ps1",
        "install_package.ps1",
    ):
        path = adapter_dir(args.adapter) / candidate
        if path.exists():
            script = path
            break

    if script is None:
        print(f"{args.adapter} has no installer. Open the app and run context.", file=sys.stderr)
        return 1

    return run_process(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
            *args.installer_args,
        ]
    )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="softwire",
        description="Run software adapter bridge commands.",
    )
    subparsers = parser.add_subparsers(dest="command")

    path_parser = subparsers.add_parser("path", help=argparse.SUPPRESS)
    path_parser.set_defaults(func=cmd_path)

    where_parser = subparsers.add_parser("where", help="Show install location and launcher details.")
    where_parser.set_defaults(func=cmd_where)

    adapters_parser = subparsers.add_parser("adapters", help="List available adapters.")
    adapters_parser.set_defaults(func=cmd_adapters)

    harnesses_parser = subparsers.add_parser(
        "harnesses",
        help="Detect known agent harnesses and their global instruction targets.",
    )
    harnesses_parser.add_argument("--json", action="store_true", help="Print the harness report as JSON.")
    harnesses_parser.set_defaults(func=cmd_harnesses)

    setup_parser = subparsers.add_parser(
        "setup",
        help="Do this first so detected agents can discover SoftWire.",
    )
    setup_parser.add_argument(
        "--agent",
        choices=AGENT_DOC_TARGETS + ("auto",),
        default="auto",
        help="Agent harness to register. Defaults to auto.",
    )
    setup_parser.add_argument(
        "--all-detected",
        action="store_true",
        help="Deprecated compatibility flag. Auto setup now registers every detected harness.",
    )
    setup_parser.add_argument("--force", action="store_true", help="Replace existing SoftWire docs.")
    setup_parser.set_defaults(func=cmd_setup)

    uninstall_parser = subparsers.add_parser(
        "uninstall",
        help="Remove SoftWire registrations from detected agent locations.",
    )
    uninstall_parser.add_argument(
        "--agent",
        choices=AGENT_DOC_TARGETS + ("auto",),
        default="auto",
        help="Agent harness to remove. Defaults to auto.",
    )
    uninstall_parser.add_argument(
        "--path",
        help="Target directory/file. Defaults depend on the selected agent.",
    )
    uninstall_parser.set_defaults(func=cmd_uninstall)

    agent_docs_path_parser = subparsers.add_parser(
        "agent-docs-path",
        help=argparse.SUPPRESS,
    )
    agent_docs_path_parser.set_defaults(func=cmd_agent_docs_path)

    docs_parser = subparsers.add_parser(
        "docs",
        help=argparse.SUPPRESS,
    )
    docs_parser.set_defaults(func=cmd_docs)

    skill_path_parser = subparsers.add_parser(
        "skill-path",
        help=argparse.SUPPRESS,
    )
    skill_path_parser.set_defaults(func=cmd_agent_docs_path)

    install_agent_docs_parser = subparsers.add_parser(
        "install-agent-docs",
        help=argparse.SUPPRESS,
    )
    install_agent_docs_parser.add_argument("target", choices=AGENT_DOC_TARGETS)
    install_agent_docs_parser.add_argument(
        "--path",
        help="Target directory/file. Defaults depend on the selected agent.",
    )
    install_agent_docs_parser.add_argument("--force", action="store_true", help="Replace existing files.")
    install_agent_docs_parser.set_defaults(func=cmd_install_agent_docs)

    install_skill_parser = subparsers.add_parser(
        "install-skill",
        help=argparse.SUPPRESS,
    )
    install_skill_parser.add_argument("--path", help="Target Codex skills directory. Defaults to ~/.codex/skills.")
    install_skill_parser.add_argument("--force", action="store_true", help="Replace an existing skill.")
    install_skill_parser.set_defaults(func=lambda args: cmd_install_agent_docs(argparse.Namespace(target="codex", path=args.path, force=args.force)))

    context_parser = subparsers.add_parser("context", help="Run a context smoke test for an adapter.")
    context_parser.add_argument("adapter", type=adapter_name, help="Adapter name, for example: photoshop")
    context_parser.set_defaults(func=cmd_context)

    run_parser = subparsers.add_parser("run", help="Run code through an adapter bridge.")
    run_parser.add_argument("adapter", type=adapter_name, help="Adapter name, for example: photoshop")
    run_parser.add_argument("code", nargs="?")
    run_parser.add_argument("--stdin", action="store_true", help="Read code from stdin.")
    run_parser.add_argument("--file", help="Read code from a file.")
    run_parser.set_defaults(func=cmd_run)

    install_parser = subparsers.add_parser("install", help="Run an adapter-specific installer.")
    install_parser.add_argument("adapter", type=adapter_name, help="Adapter name, for example: photoshop")
    install_parser.add_argument("installer_args", nargs=argparse.REMAINDER)
    install_parser.set_defaults(func=cmd_install)

    return parser


def print_start_summary():
    info = softwire_install_info()
    print("SoftWire is installed.")
    print(f"Use: {info['preferredCommand']}")
    if not info["softwireOnPath"] or not info["scriptsDirOnPath"]:
        print(f"Fallback: {info['fallbackCommand']}")
    print("")
    print("Start here:")
    print("  setup      Do this first so detected agents can discover SoftWire.")
    print("  where      Show install location and launcher details.")
    print("  harnesses  List detected agent harnesses and their target locations.")
    print("  adapters   List supported adapters.")
    print("  context    Run a context smoke test for an adapter.")
    print("  run        Run code through an adapter bridge.")
    print("  install    Run an adapter-specific installer.")
    print("  uninstall  Remove SoftWire registrations from detected agent locations.")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv in (["-h"], ["--help"]):
        print_start_summary()
        return 0
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        print_start_summary()
        return 0
    try:
        return args.func(args)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
