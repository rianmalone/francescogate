#!/usr/bin/env python3
"""Tiny static server: NO caching (so edits show immediately) + HTTP Range
support (so audio/video can seek — e.g. the football music starting at 1:30).
Local preview only."""
import http.server
import socketserver
import io
import os
import re

PORT = 4599


# Static media (images/audio/video/fonts) get cached so the browser fetches each
# file ONCE instead of re-downloading it every reload. Without this the map's ~40
# cloud <img>s each re-request cloud.png on every load and some fail under load.
# HTML/JS stay no-cache so edits always show immediately.
CACHEABLE = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp3", ".wav",
             ".m4a", ".ogg", ".mp4", ".webm", ".woff", ".woff2", ".ttf")


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        path = self.path.split("?")[0].lower()
        if path.endswith(CACHEABLE):
            self.send_header("Cache-Control", "public, max-age=86400")
        else:
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def send_head(self):
        rng = self.headers.get("Range")
        path = self.translate_path(self.path)
        if rng and os.path.isfile(path):
            m = re.match(r"bytes=(\d+)-(\d*)", rng)
            if m:
                try:
                    f = open(path, "rb")
                except OSError:
                    self.send_error(404); return None
                size = os.fstat(f.fileno()).st_size
                start = int(m.group(1))
                end = int(m.group(2)) if m.group(2) else size - 1
                end = min(end, size - 1)
                if 0 <= start <= end:
                    f.seek(start)
                    data = f.read(end - start + 1)
                    f.close()
                    self.send_response(206)
                    self.send_header("Content-Type", self.guess_type(path))
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    return io.BytesIO(data)
                f.close()
        return super().send_head()


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


with ThreadedServer(("", PORT), Handler) as httpd:
    print(f"Serving (no-cache + range, threaded) on http://localhost:{PORT}")
    httpd.serve_forever()
