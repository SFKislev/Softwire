from __future__ import print_function

import BaseHTTPServer
import contextlib
import json
import os
import Queue
import random
import SocketServer
import string
import sys
import threading
import time
import traceback

try:
    import MaxPlus
except Exception:
    MaxPlus = None

try:
    from PySide2 import QtCore
except Exception:
    QtCore = None


MAX_BODY_BYTES = 1024 * 1024
SESSION_NAME = "3dsmax"
SESSION_FILE = "3dsmax.json"
HOST = "127.0.0.1"

_server = None
_server_thread = None
_token = None
_tasks = Queue.Queue()
_timer = None
_namespace = {"MaxPlus": MaxPlus}


class EvalTask(object):
    def __init__(self, code):
        self.code = code
        self.event = threading.Event()
        self.payload = None


class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    daemon_threads = True


def _session_dir():
    root = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(root, "creative-adapters")


def _session_path():
    return os.path.join(_session_dir(), SESSION_FILE)


def _random_token():
    alphabet = string.hexdigits.lower()
    return "".join(random.SystemRandom().choice(alphabet) for _ in range(64))


def _write_session_file(port):
    if not os.path.isdir(_session_dir()):
        os.makedirs(_session_dir())
    payload = {
        "app": SESSION_NAME,
        "url": "http://%s:%s/eval" % (HOST, port),
        "host": HOST,
        "port": port,
        "token": _token,
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    temp_path = _session_path() + ".tmp"
    with open(temp_path, "w") as handle:
        json.dump(payload, handle, indent=2)
    if os.path.exists(_session_path()):
        os.remove(_session_path())
    os.rename(temp_path, _session_path())


def _remove_session_file():
    with contextlib.closing(open(os.devnull, "w")):
        try:
            os.remove(_session_path())
        except OSError:
            pass


def _json_response(handler, status, payload):
    body = json.dumps(_make_json_safe(payload)).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _make_json_safe(value):
    if value is None or isinstance(value, (bool, int, long, float, basestring)):
        return value
    if isinstance(value, (list, tuple)):
        return [_make_json_safe(item) for item in value]
    if isinstance(value, dict):
        safe = {}
        for key, item in value.items():
            safe[str(key)] = _make_json_safe(item)
        return safe
        return str(value)


def _process_tasks():
    while True:
        try:
            task = _tasks.get_nowait()
        except Queue.Empty:
            break
        task.payload = _run_code(task.code)
        task.event.set()


def _ensure_timer():
    global _timer
    if _timer is not None or QtCore is None:
        return
    _timer = QtCore.QTimer()
    _timer.timeout.connect(_process_tasks)
    _timer.start(50)


class _Capture(object):
    def __init__(self):
        self.parts = []

    def write(self, value):
        self.parts.append(value)

    def flush(self):
        pass

    def getvalue(self):
        return "".join(self.parts)


def _run_code(code):
    stdout = _Capture()
    stderr = _Capture()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    _namespace["_result"] = None
    try:
        sys.stdout = stdout
        sys.stderr = stderr
        try:
            compiled = compile(code, "<creative-adapter>", "eval")
            result = eval(compiled, _namespace, _namespace)
        except SyntaxError:
            compiled = compile(code, "<creative-adapter>", "exec")
            exec(compiled, _namespace, _namespace)
            result = _namespace.get("_result")
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
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


class BridgeHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "CreativeAdapter3dsMax/0.1"

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
        if not isinstance(code, basestring) or not code.strip():
            _json_response(self, 400, {"ok": False, "error": "Missing script"})
            return

        if QtCore is None:
            result = _run_code(code)
        else:
            task = EvalTask(code)
            _tasks.put(task)
            if not task.event.wait(30):
                _json_response(self, 504, {"ok": False, "error": "3ds Max script timed out"})
                return
            result = task.payload
        if result.get("ok"):
            _json_response(self, 200, result)
        else:
            _json_response(self, 500, result)


def start_bridge():
    global _server, _server_thread, _token
    if _server:
        return
    _token = _random_token()
    _server = ThreadingHTTPServer((HOST, 0), BridgeHandler)
    _server_thread = threading.Thread(target=_server.serve_forever)
    _server_thread.daemon = True
    _server_thread.start()
    _ensure_timer()
    _write_session_file(_server.server_address[1])
    if MaxPlus:
        try:
            MaxPlus.Core.WriteLine("Creative Adapter Bridge listening on %s" % _server.server_address[1])
        except Exception:
            pass


def stop_bridge():
    global _server, _server_thread, _token, _timer
    if _server:
        _server.shutdown()
        _server.server_close()
        _server = None
    if _timer is not None:
        _timer.stop()
        _timer = None
    _server_thread = None
    _token = None
    _remove_session_file()


start_bridge()
