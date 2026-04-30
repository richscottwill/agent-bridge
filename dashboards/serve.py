#!/usr/bin/env python3
"""
serve.py — Dashboard server with feedback + refresh API endpoints.

Serves static files from the dashboards directory AND handles:
  - POST /api/feedback  — writes ledger actions from the browser to disk for DuckDB sync
  - POST /api/refresh   — kicks off generate-command-center.py in the background
  - GET  /api/refresh-status — reports background refresh state + current data mtime

This is what lets the Command Center stop being stale: the UI has a
visible "Refresh now" button wired to /api/refresh. No cron or hook
dependency required for Richard to get fresh data.
"""
import json, os, subprocess, sys, threading, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = int(os.environ.get("KIRO_DASH_PORT", "8080"))
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
CC_DATA = DATA_DIR / "command-center-data.json"
CC_GENERATOR = SCRIPT_DIR / "generate-command-center.py"

# Shared refresh state — single global lock so concurrent POSTs don't
# double-run the generator.
_refresh_lock = threading.Lock()
_refresh_state = {
    "running": False,
    "last_started": None,
    "last_finished": None,
    "last_ok": None,
    "last_error": None,
    "last_duration_s": None,
}


def _run_refresh():
    """Run generate-command-center.py and update refresh state.
    Called in a background thread so the POST returns immediately."""
    state = _refresh_state
    state["running"] = True
    state["last_started"] = time.time()
    state["last_error"] = None
    t0 = time.time()
    try:
        result = subprocess.run(
            [sys.executable, str(CC_GENERATOR)],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )
        state["last_ok"] = result.returncode == 0
        if result.returncode != 0:
            # Keep stderr compact — first 500 chars is plenty for a toast
            state["last_error"] = (result.stderr or result.stdout or "generator failed")[:500]
    except subprocess.TimeoutExpired:
        state["last_ok"] = False
        state["last_error"] = "Generator timed out after 120s"
    except Exception as e:
        state["last_ok"] = False
        state["last_error"] = f"{type(e).__name__}: {e}"[:500]
    finally:
        state["last_finished"] = time.time()
        state["last_duration_s"] = round(state["last_finished"] - t0, 1)
        state["running"] = False


class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/refresh-status"):
            # Current background-refresh state + data file mtime.
            try:
                mtime = CC_DATA.stat().st_mtime if CC_DATA.exists() else None
            except Exception:
                mtime = None
            body = {
                "running": _refresh_state["running"],
                "last_started": _refresh_state["last_started"],
                "last_finished": _refresh_state["last_finished"],
                "last_ok": _refresh_state["last_ok"],
                "last_error": _refresh_state["last_error"],
                "last_duration_s": _refresh_state["last_duration_s"],
                "data_mtime": mtime,
                "data_age_s": (time.time() - mtime) if mtime else None,
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())
            return
        return super().do_GET()

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
        elif self.path == "/api/refresh":
            # Kick off generate-command-center.py in a background thread.
            # If a refresh is already in flight, return 202 without starting a new one.
            with _refresh_lock:
                already_running = _refresh_state["running"]
                if not already_running:
                    threading.Thread(target=_run_refresh, daemon=True).start()
            self.send_response(202 if already_running else 200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "already_running": already_running,
                "message": "Refresh already in flight" if already_running else "Refresh started"
            }).encode())
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
