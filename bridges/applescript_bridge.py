import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile
import traceback


def read_code(args, script_name):
    if args.stdin:
        return sys.stdin.read()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as handle:
            return handle.read()
    if args.code:
        return args.code
    raise ValueError(f"No {script_name} provided. Use --stdin, --file, or a code argument.")


def run_bridge(*, app_name, script_name="ExtendScript", recovery_hint=None, execute_line=None):
    parser = argparse.ArgumentParser(
        description=f"Run {script_name} in {app_name} via AppleScript on macOS."
    )
    parser.add_argument("code", nargs="?", help=f"{script_name} code to execute.")
    parser.add_argument("--stdin", action="store_true", help=f"Read {script_name} from stdin.")
    parser.add_argument("--file", help=f"Read {script_name} from a file.")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds.")
    args = parser.parse_args()

    try:
        code = read_code(args, script_name)
        if not code.strip():
            raise ValueError(f"{script_name} input is empty.")

        # Write the script to a temp file to avoid any quoting issues when
        # embedding arbitrary ExtendScript inside an AppleScript string literal.
        with tempfile.NamedTemporaryFile(suffix=".jsx", mode="w", encoding="utf-8", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            # `do shell script "cat <path>"` returns the file contents as an
            # AppleScript string, which is then passed directly to the execute
            # command. This avoids having to escape the JSX code inside AppleScript.
            content_expr = f'(do shell script "cat {shlex.quote(tmp_path)}")'
            exec_line = execute_line.format(content=content_expr) if execute_line else f"do javascript {content_expr}"
            apple_script = (
                f'tell application "{app_name}"\n'
                f'    {exec_line}\n'
                f'end tell\n'
            )
            result = subprocess.run(
                ["osascript", "-"],
                input=apple_script,
                capture_output=True,
                text=True,
                timeout=args.timeout,
            )
        finally:
            os.unlink(tmp_path)

        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip()
            hint = recovery_hint or f"Open {app_name} and retry."
            print(
                json.dumps({"ok": False, "error": err, "hint": hint}),
                file=sys.stderr,
            )
            return 1

        output = result.stdout.strip()
        try:
            parsed = json.loads(output)
        except Exception:
            parsed = output or None

        print(json.dumps({"ok": True, "result": parsed}))
        return 0

    except subprocess.TimeoutExpired:
        hint = recovery_hint or f"Check that {app_name} is open and responsive."
        print(
            json.dumps({"ok": False, "error": f"Script timed out after {args.timeout}s. {hint}"}),
            file=sys.stderr,
        )
        return 1
    except Exception as exc:
        print(
            json.dumps({"ok": False, "error": str(exc), "traceback": traceback.format_exc()}),
            file=sys.stderr,
        )
        return 1
