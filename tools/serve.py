"""Local preview that behaves like GitHub Pages for this project site:
the repo is served under /mixreveal-site/, directories serve index.html, and any
unknown path returns 404.html with HTTP status 404.

    python3 tools/serve.py [port]      # default 8765, 127.0.0.1 only
"""
import http.server
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "/mixreveal-site/"
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css", ".png": "image/png", ".js": "text/javascript"}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == "/mixreveal-site":
            self.send_response(301)
            self.send_header("Location", PREFIX)
            self.end_headers()
            return
        status, f = 404, ROOT / "404.html"
        if path.startswith(PREFIX):
            rel = path[len(PREFIX):]
            cand = (ROOT / rel).resolve()
            if ROOT in cand.parents or cand == ROOT:
                if cand.is_dir() and (cand / "index.html").is_file():
                    status, f = 200, cand / "index.html"
                elif cand.is_file() and not rel.startswith((".git", "tools")):
                    status, f = 200, cand
        body = f.read_bytes()
        self.send_response(status)
        self.send_header("Content-Type", TYPES.get(f.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
print(f"http://127.0.0.1:{port}{PREFIX}")
http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
