from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridges.local_http_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="Houdini",
            session_name="houdini",
            script_name="Python",
            recovery_hint=(
                "Open Houdini with the Creative Adapter Bridge startup script "
                "installed."
            ),
        )
    )
