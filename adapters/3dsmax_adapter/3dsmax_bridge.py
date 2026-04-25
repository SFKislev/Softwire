from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bridges.local_http_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="3ds Max",
            session_name="3dsmax",
            script_name="Python",
            recovery_hint="Open 3ds Max with the Creative Adapter Bridge startup script installed.",
        )
    )
