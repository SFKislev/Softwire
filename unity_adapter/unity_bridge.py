from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from creative_adapters.local_http_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="Unity",
            session_name="unity",
            script_name="Unity command JSON",
            recovery_hint=(
                "Open a Unity project with the Creative Adapter Bridge package "
                "installed. See unity_adapter/README.md."
            ),
        )
    )
