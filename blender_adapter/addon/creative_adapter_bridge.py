bl_info = {
    "name": "Creative Adapter Bridge",
    "author": "Creative Adapters",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "Preferences > Add-ons",
    "description": "Tokenized local bridge for running bounded bpy scripts from a shell agent.",
    "category": "System",
}

import contextlib
import io
import json
import os
import queue
import secrets
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import bpy


MAX_BODY_BYTES = 1024 * 1024
SESSION_NAME = "blender"
SESSION_FILE = "blender.json"
HOST = "127.0.0.1"

_server = None
_server_thread = None
_token = None
_tasks = queue.Queue()
_timer_registered = False
_namespace = {"bpy": bpy}


class EvalTask:
    def __init__(self, code):
        self.code = code
        self.event = threading.Event()
        self.payload = None


def _session_dir():
    root = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(root, "creative-adapters")


def _session_path():
    return os.path.join(_session_dir(), SESSION_FILE)


def _write_session_file(port):
    os.makedirs(_session_dir(), exist_ok=True)
    payload = {
        "app": SESSION_NAME,
        "url": f"http://{HOST}:{port}/eval",
        "host": HOST,
        "port": port,
        "token": _token,
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    temp_path = _session_path() + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    os.replace(temp_path, _session_path())


def _remove_session_file():
    with contextlib.suppress(FileNotFoundError):
        os.remove(_session_path())


def _json_response(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _run_code(code):
    stdout = io.StringIO()
    stderr = io.StringIO()
    local_ns = _namespace
    local_ns["_result"] = None

    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                compiled = compile(code, "<creative-adapter>", "eval")
                result = eval(compiled, local_ns, local_ns)
            except SyntaxError:
                compiled = compile(code, "<creative-adapter>", "exec")
                exec(compiled, local_ns, local_ns)
                result = local_ns.get("_result")

        return {
            "ok": True,
            "result": result,
            "stdout": stdout.getvalue(),
            "stderr": stderr.getvalue(),
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "stdout": stdout.getvalue(),
            "stderr": stderr.getvalue(),
        }


def _process_tasks():
    while True:
        try:
            task = _tasks.get_nowait()
        except queue.Empty:
            break
        task.payload = _run_code(task.code)
        task.event.set()
    return 0.05


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "CreativeAdapterBlender/0.1"

    def log_message(self, format, *args):
        return

    def do_OPTIONS(self):
        _json_response(self, 403, {"ok": False, "error": "CORS preflight is not supported."})

    def do_POST(self):
        if self.path != "/eval":
            _json_response(self, 404, {"ok": False, "error": "Not found"})
            return

        if self.headers.get("X-Bridge-Token") != _token:
            _json_response(self, 403, {"ok": False, "error": "Invalid bridge token"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            _json_response(self, 400, {"ok": False, "error": "Invalid Content-Length"})
            return
        if length <= 0 or length > MAX_BODY_BYTES:
            _json_response(self, 413, {"ok": False, "error": "Invalid request size"})
            return

        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            _json_response(self, 400, {"ok": False, "error": "Invalid JSON request"})
            return

        code = payload.get("script")
        if not isinstance(code, str) or not code.strip():
            _json_response(self, 400, {"ok": False, "error": "Missing script"})
            return

        task = EvalTask(code)
        _tasks.put(task)
        if not task.event.wait(timeout=30):
            _json_response(self, 504, {"ok": False, "error": "Blender script timed out"})
            return

        if task.payload.get("ok"):
            _json_response(self, 200, task.payload)
        else:
            _json_response(self, 500, task.payload)


def start_bridge():
    global _server, _server_thread, _token, _timer_registered
    if _server:
        return

    _token = secrets.token_hex(32)
    _server = ThreadingHTTPServer((HOST, 0), BridgeHandler)
    _server_thread = threading.Thread(target=_server.serve_forever, name="CreativeAdapterBridge", daemon=True)
    _server_thread.start()
    _write_session_file(_server.server_address[1])

    if not _timer_registered:
        bpy.app.timers.register(_process_tasks, persistent=True)
        _timer_registered = True


def stop_bridge():
    global _server, _server_thread, _token
    if _server:
        _server.shutdown()
        _server.server_close()
        _server = None
    _server_thread = None
    _token = None
    _remove_session_file()


def register():
    start_bridge()


def unregister():
    stop_bridge()
