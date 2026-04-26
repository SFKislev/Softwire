from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bridges.local_http_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="Audition",
            session_name="audition",
            recovery_hint="Open Audition and open Window > Extensions > Creative Adapter Bridge.",
        )
    )
