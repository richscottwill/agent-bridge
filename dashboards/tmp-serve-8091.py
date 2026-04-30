"""Temp server for live verification during M7 ship. Port 8091 to dodge Kiro's 8080."""
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8091
os.chdir(Path(__file__).parent)
server = ThreadingHTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
server.daemon_threads = True
print(f"Dashboard server on port {PORT} (no feedback API — verification only)")
server.serve_forever()
