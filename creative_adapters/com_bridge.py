import argparse
import json
import subprocess
import sys
import traceback

import pythoncom
import win32com.client


def read_code(args):
    if args.stdin:
        return sys.stdin.read()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as handle:
            return handle.read()
    if args.code:
        return args.code
    raise ValueError("No script provided. Use --stdin, --file, or a code argument.")


def is_process_running(process_name):
    if not process_name:
        return False

    result = subprocess.run(
        ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
        capture_output=True,
        text=True,
        check=False,
    )
    return process_name.lower() in result.stdout.lower()


def connect_app(progid, app_name, process_name=None, allow_launch=False):
    try:
        return win32com.client.GetActiveObject(progid)
    except Exception:
        if not allow_launch and process_name and not is_process_running(process_name):
            raise RuntimeError(
                f"No running {app_name} process found for {progid}. "
                f"Open {app_name} first, or pass --allow-launch."
            )
        if not allow_launch and not process_name:
            raise RuntimeError(
                f"No running {app_name} COM instance found for {progid}. "
                f"Open {app_name} first, or pass --allow-launch."
            )
        return win32com.client.Dispatch(progid)


def normalize_result(result):
    if result is None:
        return None

    text = str(result)
    try:
        return json.loads(text)
    except Exception:
        return text


def execute_script(app, method_name, code, language_id=None):
    method = getattr(app, method_name)
    if language_id is None:
        return method(code)
    return method(code, language_id)


def run_bridge(
    *,
    app_name,
    default_progid,
    process_name,
    execute_method,
    language_id=None,
    script_name="ExtendScript",
):
    parser = argparse.ArgumentParser(
        description=f"Run {script_name} in a live {app_name} instance through COM."
    )
    parser.add_argument("code", nargs="?", help=f"{script_name} code to execute.")
    parser.add_argument("--stdin", action="store_true", help=f"Read {script_name} from stdin.")
    parser.add_argument("--file", help=f"Read {script_name} from a file.")
    parser.add_argument(
        "--app-progid",
        default=default_progid,
        help=f"{app_name} COM ProgID. Defaults to {default_progid}.",
    )
    parser.add_argument(
        "--allow-launch",
        action="store_true",
        help=f"Launch {app_name} if no running process is available.",
    )
    args = parser.parse_args()

    pythoncom.CoInitialize()
    try:
        code = read_code(args)
        if not code.strip():
            raise ValueError(f"{script_name} input is empty.")

        app = connect_app(
            args.app_progid,
            app_name,
            process_name=process_name,
            allow_launch=args.allow_launch,
        )
        result = execute_script(app, execute_method, code, language_id=language_id)
        print(json.dumps({"ok": True, "result": normalize_result(result)}))
        return 0
    except Exception as exc:
        payload = {
            "ok": False,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
        print(json.dumps(payload), file=sys.stderr)
        return 1
    finally:
        pythoncom.CoUninitialize()
