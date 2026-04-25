import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

if sys.platform == "darwin":
    from bridges.applescript_bridge import run_bridge

    def _detect_app_name():
        import subprocess
        result = subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to get name of every process whose name contains "Photoshop"'],
            capture_output=True, text=True,
        )
        names = [n.strip() for n in result.stdout.strip().split(",") if n.strip()]
        return names[0] if names else "Adobe Photoshop"

    _kwargs = dict(
        app_name=_detect_app_name(),
        script_name="ExtendScript",
        recovery_hint="Open Adobe Photoshop and retry.",
    )
else:
    from bridges.com_bridge import run_bridge
    _kwargs = dict(
        app_name="Photoshop",
        default_progid="Photoshop.Application",
        process_name="Photoshop.exe",
        execute_method="DoJavaScript",
    )

if __name__ == "__main__":
    raise SystemExit(run_bridge(**_kwargs))
