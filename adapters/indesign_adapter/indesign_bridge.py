import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridges.com_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="InDesign",
            default_progid="InDesign.Application",
            process_name="InDesign.exe",
            execute_method="DoScript",
            language_id=1246973031,
        )
    )
