import argparse
import contextlib
import io
import json
import sys
import traceback
from pathlib import Path

import pythoncom
import win32com.client


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridges.com_bridge import connect_app


def read_code(args):
    if args.stdin:
        return sys.stdin.read()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as handle:
            return handle.read()
    if args.code:
        return args.code
    raise ValueError("No Python code provided. Use --stdin, --file, or a code argument.")


def jsonable(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    return str(value)


def run_bridge():
    parser = argparse.ArgumentParser(
        description="Run Python code against a live Microsoft Word COM instance."
    )
    parser.add_argument("code", nargs="?", help="Python code to execute.")
    parser.add_argument("--stdin", action="store_true", help="Read Python code from stdin.")
    parser.add_argument("--file", help="Read Python code from a file.")
    parser.add_argument(
        "--app-progid",
        default="Word.Application",
        help="Word COM ProgID. Defaults to Word.Application.",
    )
    parser.add_argument(
        "--allow-launch",
        action="store_true",
        help="Launch Word if no running process is available.",
    )
    args = parser.parse_args()

    pythoncom.CoInitialize()
    try:
        code = read_code(args)
        if not code.strip():
            raise ValueError("Python input is empty.")

        app = connect_app(
            args.app_progid,
            "Word",
            process_name="WINWORD.EXE",
            allow_launch=args.allow_launch,
        )
        namespace = {
            "app": app,
            "constants": win32com.client.constants,
            "__builtins__": __builtins__,
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(compile(code, "<word_bridge>", "exec"), namespace, namespace)
        payload = {"ok": True, "result": jsonable(namespace.get("_result"))}
        if stdout.getvalue():
            payload["stdout"] = stdout.getvalue()
        if stderr.getvalue():
            payload["stderr"] = stderr.getvalue()
        print(json.dumps(payload, ensure_ascii=False))
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


if __name__ == "__main__":
    raise SystemExit(run_bridge())
