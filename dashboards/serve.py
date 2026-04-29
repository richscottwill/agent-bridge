#!/usr/bin/env python3
"""
serve.py — Dashboard server with feedback API endpoint.

Serves static files from the dashboards directory AND handles POST /api/feedback
to write ledger actions from the browser to disk for DuckDB sync.
"""
import json, os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8080
DATA_DIR = Path(__file__).parent / "data"


class DashboardHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/feedback":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
                actions = payload.get("actions", [])
                
                # Merge into existing ledger-actions.json
                actions_path = DATA_DIR / "ledger-actions.json"
                existing = {"actions": []}
                if actions_path.exists():
                    try:
                        existing = json.loads(actions_path.read_text())
                    except:
                        pass
                
                # Dedup by text_hash — newer wins
                existing_map = {a["text_hash"]: a for a in existing.get("actions", [])}
                for a in actions:
                    existing_map[a["text_hash"]] = a
                
                existing["actions"] = list(existing_map.values())
                actions_path.write_text(json.dumps(existing, indent=2))
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "synced": len(actions)}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        # Log to file instead of stderr
        pass


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    DATA_DIR.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), DashboardHandler)
    server.daemon_threads = True
    print(f"Dashboard server on port {PORT} (threaded, with feedback API)")
    server.serve_forever()
