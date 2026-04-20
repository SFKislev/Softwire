from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridges.local_http_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="Blender",
            session_name="blender",
            script_name="Python",
            recovery_hint="Open Blender and enable the Creative Adapter Bridge addon.",
        )
    )
