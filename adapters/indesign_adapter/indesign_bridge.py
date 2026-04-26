import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

if sys.platform == "darwin":
    from bridges.applescript_bridge import run_bridge

    def _detect_app_name():
        import subprocess
        result = subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to get name of every process whose name contains "InDesign"'],
            capture_output=True, text=True,
        )
        names = [n.strip() for n in result.stdout.strip().split(",") if n.strip()]
        return names[0] if names else "Adobe InDesign"

    _kwargs = dict(
        app_name=_detect_app_name(),
        script_name="JavaScript",
        recovery_hint="Open Adobe InDesign and retry.",
        execute_line="do script {content} language JavaScript",
    )
else:
    from bridges.com_bridge import run_bridge
    _kwargs = dict(
        app_name="InDesign",
        default_progid="InDesign.Application",
        process_name="InDesign.exe",
        execute_method="DoScript",
        language_id=1246973031,
    )

if __name__ == "__main__":
    raise SystemExit(run_bridge(**_kwargs))
