import argparse
import json
import subprocess
import sys
import traceback
import winreg

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


def error_payload(message, **extra):
    payload = {"ok": False, "error": message}
    payload.update(extra)
    return payload


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


def progid_candidates(default_progid):
    candidates = [default_progid]
    if "." not in default_progid:
        return candidates

    base, suffix = default_progid.rsplit(".", 1)
    if suffix.isdigit():
        base_progid = base
    else:
        base_progid = default_progid

    discovered = []
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "") as root:
            index = 0
            while True:
                try:
                    name = winreg.EnumKey(root, index)
                except OSError:
                    break
                index += 1
                if not name.startswith(base_progid + "."):
                    continue
                version = name[len(base_progid) + 1 :]
                if version.isdigit():
                    discovered.append((int(version), name))
    except OSError:
        discovered = []

    discovered.sort(reverse=True)
    for _version, progid in discovered:
        if progid not in candidates:
            candidates.append(progid)
    return candidates


def get_active_object_with_fallback(progid):
    errors = []
    for candidate in progid_candidates(progid):
        try:
            return win32com.client.GetActiveObject(candidate), candidate, errors
        except Exception as exc:
            errors.append((candidate, exc))
    raise RuntimeError("; ".join(f"{name}: {exc}" for name, exc in errors))


def connect_app(progid, app_name, process_name=None, allow_launch=False):
    attach_error = None
    try:
        app, _resolved_progid, _errors = get_active_object_with_fallback(progid)
        return app
    except Exception as exc:
        attach_error = exc
        if not allow_launch and process_name and not is_process_running(process_name):
            raise RuntimeError(
                f"Could not attach to {app_name} via COM ProgID {progid}. "
                f"Process check did not find {process_name}. "
                f"Original COM error: {attach_error}. "
                f"Open {app_name} first, or pass --allow-launch."
            )
        if not allow_launch and not process_name:
            raise RuntimeError(
                f"Could not attach to {app_name} via COM ProgID {progid}. "
                f"Original COM error: {attach_error}. "
                f"Open {app_name} first, or pass --allow-launch."
            )
        dispatch_errors = []
        for candidate in progid_candidates(progid):
            try:
                return win32com.client.Dispatch(candidate)
            except Exception as dispatch_exc:
                dispatch_errors.append(f"{candidate}: {dispatch_exc}")
        raise RuntimeError(
            f"Could not launch {app_name} via COM ProgID {progid}. "
            f"Attach errors: {attach_error}. "
            f"Dispatch attempts: {'; '.join(dispatch_errors)}"
        )


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


def run_child_with_timeout(args, code, timeout_seconds):
    command = [
        sys.executable,
        sys.argv[0],
        "--stdin",
        "--app-progid",
        args.app_progid,
        "--_com-child",
    ]
    if args.allow_launch:
        command.append("--allow-launch")

    try:
        proc = subprocess.run(
            command,
            input=code,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print(
            json.dumps(
                error_payload(
                    f"COM call timed out after {timeout_seconds} seconds.",
                    timeoutSeconds=timeout_seconds,
                    recovery=(
                        "The desktop app may be busy, modal, or blocked inside its "
                        "scripting runtime. The bridge subprocess was terminated; "
                        "check the app UI before retrying."
                    ),
                )
            ),
            file=sys.stderr,
        )
        return 1

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


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
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Maximum seconds for the COM call. Use 0 to disable the parent watchdog.",
    )
    parser.add_argument("--_com-child", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    com_initialized = False
    try:
        code = read_code(args)
        if not code.strip():
            raise ValueError(f"{script_name} input is empty.")

        if not args._com_child and args.timeout > 0:
            return run_child_with_timeout(args, code, args.timeout)

        pythoncom.CoInitialize()
        com_initialized = True
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
        if com_initialized:
            pythoncom.CoUninitialize()
