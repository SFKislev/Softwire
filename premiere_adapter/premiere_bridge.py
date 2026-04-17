import argparse
import json
import os
import sys
import urllib.error
import urllib.request


SESSION_FILE = os.path.join(
    os.environ.get("APPDATA") or os.path.expanduser("~"),
    "creative-adapters",
    "premiere.json",
)


def read_code(args):
    if args.stdin:
        return sys.stdin.read()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as handle:
            return handle.read()
    if args.code:
        return args.code
    raise ValueError("No ExtendScript provided. Use --stdin, --file, or a code argument.")


def main():
    parser = argparse.ArgumentParser(
        description="Run ExtendScript in Premiere Pro through the local CEP bridge."
    )
    parser.add_argument("code", nargs="?", help="ExtendScript code to execute.")
    parser.add_argument("--stdin", action="store_true", help="Read ExtendScript from stdin.")
    parser.add_argument("--file", help="Read ExtendScript from a file.")
    parser.add_argument(
        "--url",
        help=(
            "Premiere CEP bridge eval URL. Defaults to the URL in the hidden "
            "session file."
        ),
    )
    parser.add_argument(
        "--token",
        help="Bridge token override. Defaults to the hidden session file token.",
    )
    parser.add_argument(
        "--session-file",
        default=SESSION_FILE,
        help=f"Bridge session file. Defaults to {SESSION_FILE}.",
    )
    args = parser.parse_args()

    try:
        code = read_code(args)
        if not code.strip():
            raise ValueError("ExtendScript input is empty.")

        url = args.url
        token = args.token
        if not url or not token:
            session_url, session_token = read_session_file(args.session_file)
            url = url or session_url
            token = token or session_token
        if not url:
            raise ValueError(
                "No Premiere bridge URL is available. Open the Creative "
                "Adapter Bridge panel in Premiere and retry."
            )
        if not token:
            raise ValueError(
                "No Premiere bridge token is available. Open the Creative "
                "Adapter Bridge panel in Premiere and retry."
            )

        payload = json.dumps({"script": code}).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Bridge-Token": token,
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            print(body)
            return 0
    except FileNotFoundError:
        error = (
            "Premiere bridge session file was not found. Open Premiere Pro and "
            "open Window > Extensions > Creative Adapter Bridge, then retry."
        )
        print(
            json.dumps({"ok": False, "error": error, "sessionFile": args.session_file}),
            file=sys.stderr,
        )
        return 1
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Premiere bridge returned HTTP {exc.code}",
                    "detail": detail,
                }
            ),
            file=sys.stderr,
        )
        return 1
    except urllib.error.URLError as exc:
        error = (
            "Premiere CEP bridge is not reachable. Open Premiere Pro, install "
            "the CEP bridge panel, and open the panel once from Window > "
            "Extensions."
        )
        print(json.dumps({"ok": False, "error": error, "detail": str(exc)}), file=sys.stderr)
        return 1
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


def read_session_file(session_file):
    with open(session_file, "r", encoding="utf-8") as handle:
        session = json.load(handle)
    url = session.get("url")
    token = session.get("token")
    if not url or not token:
        raise ValueError(f"Premiere bridge session file is incomplete: {session_file}")
    return url, token


if __name__ == "__main__":
    raise SystemExit(main())
