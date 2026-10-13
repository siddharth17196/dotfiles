#!/usr/bin/env python3
"""Shared local Markdown previews. Requires only markdown-it-py."""

import argparse
import hashlib
import html
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urlsplit
from urllib.request import Request, urlopen
import webbrowser

try:
    from markdown_it import MarkdownIt
    from markdown_it.token import Token
except ImportError:
    sys.exit("markdown-it-py is required. Run this script with the Python environment that has it installed.")

HERE = Path(__file__).resolve().parent
APP = "mdview-1"
MARKDOWN = {".md", ".markdown"}
ASSETS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".avif", ".pdf"}


def project_root(path):
    for parent in path.parents:
        if (parent / ".git").exists():
            return parent
    return path.parent


def render_front_matter(text):
    """Display a conservative subset of front matter, without parsing full YAML."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != "---":
        return "", text
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if end is None:
        return "", text
    metadata = lines[1:end]
    field = re.compile(r"^([A-Za-z_][\w.-]*):(?:[ \t]+(.*))?$")
    if not any(field.fullmatch(line.rstrip()) for line in metadata):
        return "", text

    fallback = '<pre class="front-matter"><code>' + html.escape("".join(lines[:end + 1])) + '</code></pre>\n'
    body = "".join(lines[end + 1:])
    rows, keys = [], set()
    for line in metadata:
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = field.fullmatch(line)
        if not match or match[1] in keys:
            return fallback, body
        key, value = match[1], match[2] or ""
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError:
                return fallback, body
        elif value.startswith("'"):
            if not re.fullmatch(r"'(?:[^']|'')*'", value):
                return fallback, body
            value = value[1:-1].replace("''", "'")
        elif value.startswith(("[", "{", "|", ">", "!", "&", "*", "- ")) or re.search(r"(?:^|\s)#|:\s", value):
            return fallback, body
        keys.add(key)
        rows.append(f'<tr><th scope="row">{html.escape(key)}</th><td>{html.escape(value)}</td></tr>')
    return '<table class="front-matter" aria-label="File metadata"><tbody>' + "".join(rows) + '</tbody></table>\n', body


def render_markdown(parser, text):
    metadata, text = render_front_matter(text)
    tokens = parser.parse(text)
    slugs = {}
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            inline = tokens[i + 1]
            title = "".join(t.content for t in inline.children or [] if t.type in {"text", "code_inline"})
            slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-") or "section"
            count = slugs.get(slug, 0)
            slugs[slug] = count + 1
            token.attrSet("id", slug if count == 0 else f"{slug}-{count}")
        # Task lists without a separate plugin dependency.
        if token.type == "inline" and i >= 2 and tokens[i - 2].type == "list_item_open":
            children = token.children or []
            if children and children[0].type == "text":
                match = re.match(r"^\[([ xX])\]\s+", children[0].content)
                if match:
                    children[0].content = children[0].content[match.end():]
                    checkbox = Token("html_inline", "", 0)
                    checked = " checked" if match[1].lower() == "x" else ""
                    checkbox.content = f'<input type="checkbox" disabled{checked}> '
                    children.insert(0, checkbox)
    return metadata + parser.renderer.render(tokens, parser.options, {})


class Workspace:
    def __init__(self):
        self.lock = threading.RLock()
        self.roots = {}
        self.files = {}
        self.cache = {}
        self.parser = MarkdownIt("commonmark", {"html": False}).enable(["table", "strikethrough"])

    def add(self, paths, root=None):
        # Validate the whole batch before changing the shared workspace.
        selected = []
        for name in paths:
            path = Path(name).expanduser().resolve(strict=True)
            if not path.is_file() or path.suffix.lower() not in MARKDOWN:
                raise ValueError(f"Not a Markdown file: {path}")
            base = Path(root).expanduser().resolve(strict=True) if root else project_root(path)
            if not base.is_dir():
                raise ValueError(f"Not a directory: {base}")
            path.relative_to(base)
            selected.append((path, base))
        with self.lock:
            for path, base in selected:
                if any(item["path"] == str(path) for item in self.files.values()):
                    continue
                mount = hashlib.sha256(str(base).encode()).hexdigest()[:16]
                self.roots[mount] = base
                url = f"/files/{mount}/{quote(path.relative_to(base).as_posix(), safe='/')}"
                self.files[url] = {"url": url, "name": path.name, "path": str(path),
                                   "label": f"{base.name}/{path.relative_to(base).as_posix()}"}
            return list(self.files.values())

    def resolve(self, url):
        parts = urlsplit(url)
        if parts.scheme or parts.netloc:
            raise ValueError("Expected a local preview URL")
        prefix, mount, relative = unquote(parts.path).split("/", 3)[1:]
        if prefix != "files":
            raise ValueError("Expected a preview URL")
        with self.lock:
            base = self.roots[mount]
        path = (base / relative).resolve()
        path.relative_to(base)  # Also blocks symlinks that escape the mount.
        if not path.is_file():
            raise FileNotFoundError(path)
        return path, base

    def document(self, path):
        stat = path.stat()
        stamp = (stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size, stat.st_ino)
        with self.lock:
            cached = self.cache.get(path)
            if cached and cached[0] == stamp:
                return cached[1]
            content = path.read_text(encoding="utf-8-sig")
            result = {"html": render_markdown(self.parser, content),
                      "revision": hashlib.sha256(content.encode()).hexdigest()}
            self.cache[path] = (stamp, result)
            return result


class Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, port):
        self.workspace = Workspace()
        super().__init__(("127.0.0.1", port), Handler)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def trusted(self):
        host = f"127.0.0.1:{self.server.server_port}"
        origin = self.headers.get("Origin")
        return self.headers.get("Host") == host and (not origin or origin == f"http://{host}")

    def reply(self, body, mime="application/json", status=200, asset=False):
        if mime == "application/json":
            body = json.dumps(body).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        policy = ("default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; sandbox" if asset else
                  "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
                  "img-src 'self' data: https: http:; frame-src 'self'; object-src 'none'; "
                  "base-uri 'self'; frame-ancestors 'self'")
        self.send_header("Content-Security-Policy", policy)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self.trusted():
            return self.reply({"error": "Untrusted origin or host"}, status=403)
        route = urlsplit(self.path).path
        try:
            if route == "/api/state":
                with self.server.workspace.lock:
                    return self.reply({"app": APP, "files": list(self.server.workspace.files.values())})
            if route in {"/", "/style.css", "/theme.js"}:
                file = HERE / ("index.html" if route == "/" else "style.css")
                mime = "text/html; charset=utf-8" if route == "/" else "text/css; charset=utf-8"
                if route == "/theme.js":
                    file, mime = HERE / "theme.js", "text/javascript; charset=utf-8"
                return self.reply(file.read_bytes(), mime)
            path, _ = self.server.workspace.resolve(self.path)
            if path.suffix.lower() in MARKDOWN:
                query = parse_qs(urlsplit(self.path).query)
                if query.get("render") == ["1"]:
                    result = self.server.workspace.document(path)
                    if query.get("revision") == [result["revision"]]:
                        result = {"revision": result["revision"]}
                    return self.reply(result)
                return self.reply((HERE / "preview.html").read_bytes(), "text/html; charset=utf-8")
            if path.suffix.lower() in ASSETS:
                return self.reply(path.read_bytes(), mimetypes.guess_type(path.name)[0] or "application/octet-stream", asset=True)
            self.reply({"error": "This file type is not served"}, status=403)
        except (KeyError, ValueError, FileNotFoundError, PermissionError) as exc:
            self.reply({"error": str(exc)}, status=404)
        except (OSError, UnicodeError) as exc:
            self.reply({"error": str(exc)}, status=400)

    def do_POST(self):
        if not self.trusted() or self.headers.get("Content-Type") != "application/json":
            return self.reply({"error": "Expected same-origin JSON request"}, status=403)
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 65536:
                raise ValueError("Invalid request size")
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")
            if self.path in {"/api/open-link", "/api/close"} and not isinstance(data.get("url"), str):
                raise ValueError("Expected a preview URL")
            if self.path == "/api/open":
                paths, root = data.get("paths"), data.get("root")
                if not isinstance(paths, list) or not paths or not all(isinstance(p, str) for p in paths):
                    raise ValueError("Expected a nonempty list of file paths")
                if root is not None and not isinstance(root, str):
                    raise ValueError("Expected a root path")
                files = self.server.workspace.add(paths, root)
                return self.reply({"files": files})
            if self.path == "/api/open-link":
                path, base = self.server.workspace.resolve(data["url"])
                files = self.server.workspace.add([str(path)], str(base))
                url = next(item["url"] for item in files if item["path"] == str(path))
                return self.reply({"files": files, "url": url})
            if self.path == "/api/close":
                with self.server.workspace.lock:
                    item = self.server.workspace.files.pop(data["url"], None)
                    if item:
                        self.server.workspace.cache.pop(Path(item["path"]), None)
                return self.reply({"ok": True})
            if self.path == "/api/stop":
                self.reply({"ok": True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            self.reply({"error": "Unknown endpoint"}, status=404)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            self.reply({"error": str(exc)}, status=400)


def request(port, route, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = Request(f"http://127.0.0.1:{port}{route}", data=body,
                  headers={"Content-Type": "application/json"} if body else {})
    with urlopen(req, timeout=2) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="Markdown files to add to the shared page")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--root", help="Base directory for relative links (default: Git root, otherwise file directory)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open a browser when starting the server")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--stop", action="store_true", help="Stop the shared server")
    mode.add_argument("--serve", action="store_true", help="Run the server in the foreground")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if args.serve:
        server = Server(args.port)
        try:
            if args.files:
                server.workspace.add(args.files, args.root)
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
        return
    try:
        # Validate before starting a background process.
        if args.files:
            Workspace().add(args.files, args.root)
        state = request(args.port, "/api/state")
    except HTTPError:
        parser.exit(1, "This port is occupied by another application. Choose --port.\n")
    except URLError:
        if args.stop:
            parser.exit(1, "No mdview server is running.\n")
        log = Path(os.environ.get("TMPDIR", "/tmp")) / f"mdview-{os.getuid()}-{args.port}.log"
        with log.open("a") as stream:
            child = subprocess.Popen([sys.executable, str(HERE / "mdview.py"), "--serve", "--port", str(args.port)],
                                     stdin=subprocess.DEVNULL, stdout=stream, stderr=stream, start_new_session=True)
        for _ in range(50):
            try:
                state = request(args.port, "/api/state")
                break
            except URLError:
                time.sleep(0.1)
        else:
            parser.exit(1, f"Server did not start; see {log}\n")
        started = child.poll() is None
    except (ValueError, OSError) as exc:
        parser.exit(1, f"{exc}\n")
    else:
        started = False
    if state.get("app") != APP:
        parser.exit(1, "This port is occupied by another application. Choose --port.\n")
    if args.stop:
        request(args.port, "/api/stop", {})
        print("Stopped mdview.")
        return
    if args.files:
        request(args.port, "/api/open", {"paths": [str(Path(p).expanduser().resolve()) for p in args.files], "root": str(Path(args.root).expanduser().resolve()) if args.root else None})
    url = f"http://127.0.0.1:{args.port}/"
    print(url)
    if not args.no_browser and (started or not args.files):
        webbrowser.open(url)


if __name__ == "__main__":
    main()
