import csv
import io
import subprocess
import time

import pywintypes
import win32api
import win32con
import win32gui
import win32process


def process_ids_by_name(process_name):
    result = subprocess.run(
        ["tasklist", "/FO", "CSV", "/NH", "/FI", f"IMAGENAME eq {process_name}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"Failed to query process list for {process_name}.")

    rows = csv.reader(io.StringIO(result.stdout))
    process_ids = []
    for row in rows:
        if not row:
            continue
        if len(row) < 2:
            continue
        image_name = row[0].strip()
        if image_name.upper() == "INFO:":
            continue
        if image_name.lower() != process_name.lower():
            continue
        try:
            process_ids.append(int(row[1]))
        except ValueError:
            continue
    return process_ids


def _window_snapshot(hwnd):
    _thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
    try:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    except pywintypes.error:
        left = top = right = bottom = 0

    owner = win32gui.GetWindow(hwnd, win32con.GW_OWNER)
    title = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    visible = bool(win32gui.IsWindowVisible(hwnd))
    enabled = bool(win32gui.IsWindowEnabled(hwnd))

    return {
        "hwnd": hwnd,
        "processId": process_id,
        "title": title,
        "className": class_name,
        "visible": visible,
        "enabled": enabled,
        "ownerHwnd": owner or None,
        "rect": {
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom,
            "width": max(0, right - left),
            "height": max(0, bottom - top),
        },
        "isForeground": hwnd == win32gui.GetForegroundWindow(),
        "isDialogLike": class_name == "#32770" or bool(owner),
    }


def list_process_windows(process_name):
    process_ids = process_ids_by_name(process_name)
    windows = []
    process_set = set(process_ids)

    def callback(hwnd, _lparam):
        if not win32gui.IsWindow(hwnd):
            return True
        _thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid in process_set:
            windows.append(_window_snapshot(hwnd))
        return True

    win32gui.EnumWindows(callback, None)
    windows.sort(
        key=lambda item: (
            not item["isForeground"],
            not item["isDialogLike"],
            not item["visible"],
            item["hwnd"],
        )
    )
    return {"processName": process_name, "processIds": process_ids, "windows": windows}


def _choose_modal_candidate(windows):
    for window in windows:
        if window["isForeground"] and window["isDialogLike"] and window["visible"] and window["enabled"]:
            return window
    for window in windows:
        if window["isDialogLike"] and window["visible"] and window["enabled"]:
            return window
    return None


def _focus_window(hwnd):
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    except pywintypes.error:
        return False
    return True


def _send_escape(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)


def _send_cancel(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_COMMAND, win32con.IDCANCEL, 0)
    _send_escape(hwnd)


def _send_close(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def dismiss_process_modal(process_name, action="cancel", settle_ms=400):
    snapshot = list_process_windows(process_name)
    candidate = _choose_modal_candidate(snapshot["windows"])
    if candidate is None:
        return {
            "ok": False,
            "error": f"No dialog-like top-level window found for {process_name}.",
            "processName": process_name,
            "processIds": snapshot["processIds"],
            "windows": snapshot["windows"],
        }

    hwnd = candidate["hwnd"]
    focused = _focus_window(hwnd)
    if action == "cancel":
        _send_cancel(hwnd)
    elif action == "escape":
        _send_escape(hwnd)
    elif action == "close":
        _send_close(hwnd)
    else:
        raise ValueError(f"Unsupported modal action: {action}")

    time.sleep(max(settle_ms, 0) / 1000.0)
    refreshed = list_process_windows(process_name)
    remaining = any(window["hwnd"] == hwnd for window in refreshed["windows"])

    return {
        "ok": not remaining,
        "action": action,
        "focused": focused,
        "processName": process_name,
        "processIds": refreshed["processIds"],
        "target": candidate,
        "dismissed": not remaining,
        "windows": refreshed["windows"],
    }
