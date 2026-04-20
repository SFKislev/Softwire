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

AGENT_DOC_TARGETS = ("codex", "claude", "gemini", "opencode", "openclaw", "generic", "all")

HARNESS_CONFIGS = {
    "codex": {
        "commands": ["codex"],
        "config_dir": Path(".codex"),
        "global_targets": [
            Path(".codex") / "skills" / "thewire" / "SKILL.md",
            Path(".codex") / "AGENTS.md",
        ],
    },
    "claude": {
        "commands": ["claude"],
        "config_dir": Path(".claude"),
        "desktop_markers": [
            Path("AppData") / "Local" / "Programs" / "Claude" / "Claude.exe",
            Path("AppData") / "Local" / "Microsoft" / "WindowsApps" / "Claude.exe",
            Path("AppData") / "Local" / "Packages" / "Claude_*",
            Path("/Applications") / "Claude.app",
            Path("Library") / "Application Support" / "Claude",
        ],
        "global_targets": [
            Path(".claude") / "CLAUDE.md",
            Path(".claude") / "skills" / "thewire" / "SKILL.md",
        ],
    },
    "gemini": {
        "commands": ["gemini"],
        "config_dir": Path(".gemini"),
        "global_targets": [
            Path(".gemini") / "GEMINI.md",
            Path(".gemini") / "thewire.md",
        ],
    },
    "opencode": {
        "commands": ["opencode"],
        "config_dir": Path(".config") / "opencode",
        "global_targets": [
            Path(".config") / "opencode" / "agents" / "thewire.md",
        ],
    },
    "openclaw": {
        "commands": ["openclaw"],
        "config_dir": Path(".openclaw"),
        "global_targets": [
            Path(".openclaw") / "skills" / "thewire" / "SKILL.md",
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
    path = ROOT / f"{name}_adapter"
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


def cmd_path(_args):
    print(ROOT)
    return 0


def cmd_adapters(_args):
    for name in sorted(BRIDGES):
        print(name)
    return 0


def agent_docs_dir():
    return ROOT / "thewire" / "agent_docs"


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


def thewire_pointer_block():
    begin = "<!-- THEWIRE START -->"
    end = "<!-- THEWIRE END -->"
    block = (
        f"{begin}\n"
        "# The Wire\n\n"
        "The Wire is installed on this machine. It lets agents communicate with "
        "supported desktop software directly through local scripting bridges, "
        "without MCP servers.\n\n"
        "When requested to operate supported desktop software, read:\n\n"
        "```powershell\n"
        "Get-Content \"$(thewire docs)\" -Raw\n"
        "```\n"
        f"{end}"
    )
    return begin, end, block


def cmd_agent_docs_path(_args):
    print(agent_docs_dir())
    return 0


def cmd_docs(_args):
    print(agent_docs_dir() / "common.md")
    return 0


def installed_command(name):
    return shutil.which(name)


def existing_home_markers(markers):
    home = Path.home()
    found = []
    for marker in markers:
        path = marker if marker.is_absolute() else home / marker
        if any(char in str(path) for char in "*?["):
            found.extend(str(item) for item in path.parent.glob(path.name))
        elif path.exists():
            found.append(str(path))
    return found


def harness_report():
    home = Path.home()
    report = []
    for name, config in HARNESS_CONFIGS.items():
        commands = []
        for command in config["commands"]:
            commands.append({"name": command, "path": installed_command(command)})
        config_dir = home / config["config_dir"]
        command_on_path = any(item["path"] for item in commands)
        targets = []
        for target in config["global_targets"]:
            path = home / target
            targets.append({"path": str(path), "exists": path.exists()})
        desktop_markers = existing_home_markers(config.get("desktop_markers", []))
        claude_code_detected = False
        claude_desktop_detected = False
        detection_reasons = []

        if command_on_path:
            detection_reasons.append("command")
        if config_dir.exists():
            detection_reasons.append("config_dir")
        if desktop_markers:
            detection_reasons.append("desktop_app")

        if name == "claude":
            claude_code_detected = command_on_path
            claude_desktop_detected = bool(desktop_markers)
            detection_reasons = []
            if claude_code_detected:
                detection_reasons.append("claude_code")
            if claude_desktop_detected:
                detection_reasons.append("claude_desktop")

        detected = bool(detection_reasons)
        report.append(
            {
                "harness": name,
                "commandOnPath": command_on_path,
                "commands": commands,
                "configDir": str(config_dir),
                "configDirExists": config_dir.exists(),
                "detectionReasons": detection_reasons,
                "claudeCodeDetected": claude_code_detected,
                "claudeDesktopDetected": claude_desktop_detected,
                "desktopAppDetected": bool(desktop_markers),
                "desktopMarkers": desktop_markers,
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
    print(json.dumps(harness_report(), indent=2))
    return 0


def install_codex_docs(args):
    source = agent_docs_dir() / "codex"
    target_root = Path(args.path).expanduser() if args.path else Path.home() / ".codex" / "skills"
    ok = copy_dir(source, target_root / "thewire", force=args.force)
    if args.path is None:
        begin, end, block = thewire_pointer_block()
        agents = Path.home() / ".codex" / "AGENTS.md"
        upsert_marked_block(agents, begin, end, block)
        print(agents)
    return ok


def install_claude_docs(args):
    source = agent_docs_dir() / "claude" / "thewire.md"
    target_root = Path(args.path).expanduser() if args.path else Path.home() / ".claude"
    target = target_root / "thewire.md"
    if not copy_file(source, target, force=args.force):
        return False

    memory = target_root / "CLAUDE.md"
    import_path = target.resolve().as_posix()
    begin = "<!-- THEWIRE START -->"
    end = "<!-- THEWIRE END -->"
    block = f"{begin}\n@{import_path}\n{end}"
    upsert_marked_block(memory, begin, end, block)
    print(memory)
    skill_source = agent_docs_dir() / "claude_skill"
    if skill_source.exists() and args.path is None:
        copy_dir(skill_source, target_root / "skills" / "thewire", force=True)
    return True


def install_gemini_docs(args):
    target_root = Path(args.path).expanduser() if args.path else Path.home() / ".gemini"
    target = target_root / "thewire.md"
    source = agent_docs_dir() / "common.md"
    if not copy_file(source, target, force=args.force):
        return False

    memory = target_root / "GEMINI.md"
    import_path = target.resolve().as_posix()
    begin = "<!-- THEWIRE START -->"
    end = "<!-- THEWIRE END -->"
    block = f"{begin}\n@{import_path}\n{end}"
    upsert_marked_block(memory, begin, end, block)
    print(memory)
    return True


def install_opencode_docs(args):
    target_root = Path(args.path).expanduser() if args.path else Path.home() / ".config" / "opencode" / "agents"
    source = agent_docs_dir() / "opencode" / "thewire.md"
    return copy_file(source, target_root / "thewire.md", force=args.force)


def install_openclaw_docs(args):
    source = agent_docs_dir() / "openclaw"
    target_root = Path(args.path).expanduser() if args.path else Path.home() / ".openclaw" / "skills"
    return copy_dir(source, target_root / "thewire", force=args.force)


def install_generic_docs(args):
    source = agent_docs_dir() / "generic" / "AGENTS.md"
    target = Path(args.path).expanduser() if args.path else Path.cwd() / "AGENTS.md"
    return copy_file(source, target, force=args.force)


def cmd_install_agent_docs(args):
    targets = ("codex", "claude", "gemini", "opencode", "openclaw", "generic") if args.target == "all" else (args.target,)
    ok = True
    for target in targets:
        if target == "codex":
            ok = install_codex_docs(args) and ok
        elif target == "claude":
            ok = install_claude_docs(args) and ok
        elif target == "gemini":
            ok = install_gemini_docs(args) and ok
        elif target == "opencode":
            ok = install_opencode_docs(args) and ok
        elif target == "openclaw":
            ok = install_openclaw_docs(args) and ok
        elif target == "generic":
            ok = install_generic_docs(args) and ok
    return 0 if ok else 1


def cmd_setup(args):
    if args.agent == "auto":
        targets = detect_agent_targets()
        if not targets:
            targets = ["generic"]
        chosen = targets
    elif args.agent == "all":
        chosen = ["codex", "claude", "gemini", "opencode", "openclaw", "generic"]
    else:
        chosen = [args.agent]

    print("Registering The Wire agent instructions for: " + ", ".join(chosen))
    ok = True
    for target in chosen:
        setup_args = argparse.Namespace(target=target, path=None, force=args.force)
        ok = (cmd_install_agent_docs(setup_args) == 0) and ok

    print("")
    print("The Wire is installed. New agent sessions should discover it through the registered global instructions.")
    print("Verify the bridge runtime with: thewire adapters")
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
        prog="thewire",
        description="Run Creative Software Adapter bridge commands.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    path_parser = subparsers.add_parser("path", help="Print the installed adapter root.")
    path_parser.set_defaults(func=cmd_path)

    adapters_parser = subparsers.add_parser("adapters", help="List available adapters.")
    adapters_parser.set_defaults(func=cmd_adapters)

    harnesses_parser = subparsers.add_parser(
        "harnesses",
        help="Detect known agent harnesses and their global instruction targets.",
    )
    harnesses_parser.set_defaults(func=cmd_harnesses)

    setup_parser = subparsers.add_parser(
        "setup",
        help="Register The Wire with global agent instruction locations.",
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
    setup_parser.add_argument("--force", action="store_true", help="Replace existing The Wire docs.")
    setup_parser.set_defaults(func=cmd_setup)

    agent_docs_path_parser = subparsers.add_parser(
        "agent-docs-path",
        help="Print the packaged agent documentation path.",
    )
    agent_docs_path_parser.set_defaults(func=cmd_agent_docs_path)

    docs_parser = subparsers.add_parser(
        "docs",
        help="Print the canonical agent instructions file.",
    )
    docs_parser.set_defaults(func=cmd_docs)

    skill_path_parser = subparsers.add_parser(
        "skill-path",
        help="Compatibility alias for agent-docs-path.",
    )
    skill_path_parser.set_defaults(func=cmd_agent_docs_path)

    install_agent_docs_parser = subparsers.add_parser(
        "install-agent-docs",
        help="Install modular agent instructions for Codex, Claude, OpenClaw, or generic AGENTS.md users.",
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
        help="Compatibility alias for install-agent-docs codex.",
    )
    install_skill_parser.add_argument("--path", help="Target Codex skills directory. Defaults to ~/.codex/skills.")
    install_skill_parser.add_argument("--force", action="store_true", help="Replace an existing skill.")
    install_skill_parser.set_defaults(func=lambda args: cmd_install_agent_docs(argparse.Namespace(target="codex", path=args.path, force=args.force)))

    context_parser = subparsers.add_parser("context", help="Run an adapter context smoke test.")
    context_parser.add_argument("adapter", type=adapter_name)
    context_parser.set_defaults(func=cmd_context)

    run_parser = subparsers.add_parser("run", help="Run code through an adapter bridge.")
    run_parser.add_argument("adapter", type=adapter_name)
    run_parser.add_argument("code", nargs="?")
    run_parser.add_argument("--stdin", action="store_true", help="Read code from stdin.")
    run_parser.add_argument("--file", help="Read code from a file.")
    run_parser.set_defaults(func=cmd_run)

    install_parser = subparsers.add_parser("install", help="Run an adapter installer.")
    install_parser.add_argument("adapter", type=adapter_name)
    install_parser.add_argument("installer_args", nargs=argparse.REMAINDER)
    install_parser.set_defaults(func=cmd_install)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
