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
from datetime import datetime, timezone
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
    def _json(self, status, body):
        """Small helper — send a JSON response with status + CORS."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

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
        if self.path == "/api/wbr-note":
            # Research report #066 — per-week WBR note persistence.
            # Writes to ~/shared/context/active/wbr-notes.md. Append-or-update semantics:
            # one block per (market, week) keyed by an HTML-style marker so re-saves replace
            # rather than duplicate. Same-file, same-format every call so the file stays diffable.
            #
            # Expected JSON: {"market": "US", "week": "2026-W17", "note": "..."}
            #   market: uppercase market code (US/UK/MX/WW/etc.)
            #   week:   ISO week key like "2026-W17"
            #   note:   free text; strips CRLF, preserves LF; empty string deletes the block
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
            except Exception as e:
                self._json(400, {"ok": False, "error": f"bad json: {e}"})
                return

            market = (payload.get("market") or "").strip().upper()
            week = (payload.get("week") or "").strip()
            note = (payload.get("note") or "").replace("\r\n", "\n").replace("\r", "\n")

            # Minimal validation — market must be alnum, week must match YYYY-WNN
            import re as _re
            if not _re.match(r"^[A-Z0-9]{2,5}$", market):
                self._json(400, {"ok": False, "error": "market must match /^[A-Z0-9]{2,5}$/"})
                return
            if not _re.match(r"^\d{4}-W\d{1,2}$", week):
                self._json(400, {"ok": False, "error": "week must match /^\\d{4}-W\\d{1,2}$/"})
                return
            if len(note) > 10000:
                self._json(400, {"ok": False, "error": "note exceeds 10000 chars"})
                return

            notes_path = Path.home() / "shared" / "context" / "active" / "wbr-notes.md"
            notes_path.parent.mkdir(parents=True, exist_ok=True)
            existing = notes_path.read_text() if notes_path.exists() else (
                "# WBR notes\n\n"
                "One block per (market, week). Written by weekly-review.html via /api/wbr-note.\n"
                "Re-saving the same (market, week) replaces the existing block; empty note deletes it.\n\n"
            )

            # Block delimiter uses HTML comments so the file stays valid markdown in a viewer
            # and the blocks are unambiguously parseable. Marker format matches what the WR
            # dashboard reads back on load.
            marker_start = f"<!-- wbr-note:{market}:{week} -->"
            marker_end = f"<!-- /wbr-note:{market}:{week} -->"
            block_re = _re.compile(
                _re.escape(marker_start) + r"[\s\S]*?" + _re.escape(marker_end) + r"\n?",
                _re.MULTILINE,
            )
            stripped = block_re.sub("", existing)

            if note.strip():
                ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                block = (
                    f"{marker_start}\n"
                    f"## {market} · {week}\n\n"
                    f"_updated {ts}_\n\n"
                    f"{note.strip()}\n"
                    f"{marker_end}\n\n"
                )
                new_content = stripped.rstrip() + "\n\n" + block
            else:
                # Empty note = delete this block
                new_content = stripped.rstrip() + "\n"

            notes_path.write_text(new_content)
            self._json(200, {"ok": True, "market": market, "week": week, "deleted": not note.strip()})
            return
        elif self.path == "/api/wbr-note/get":
            # Companion GET-via-POST so the dashboard can fetch a specific note by key
            # without exposing the whole file over a GET (the file may contain other markets'
            # notes the current view doesn't care about). Payload: {"market", "week"}.
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
            except Exception as e:
                self._json(400, {"ok": False, "error": f"bad json: {e}"})
                return
            market = (payload.get("market") or "").strip().upper()
            week = (payload.get("week") or "").strip()
            notes_path = Path.home() / "shared" / "context" / "active" / "wbr-notes.md"
            if not notes_path.exists():
                self._json(200, {"ok": True, "note": "", "exists": False})
                return
            import re as _re
            marker_start = f"<!-- wbr-note:{market}:{week} -->"
            marker_end = f"<!-- /wbr-note:{market}:{week} -->"
            block_re = _re.compile(
                _re.escape(marker_start) + r"\s*\n(?:## [^\n]*\n\n_updated [^_]+_\n\n)?([\s\S]*?)\n?"
                + _re.escape(marker_end)
            )
            m = block_re.search(notes_path.read_text())
            self._json(200, {
                "ok": True,
                "note": (m.group(1).strip() if m else ""),
                "exists": bool(m),
            })
            return
        elif self.path == "/api/feedback":
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
        elif self.path == "/api/query-log/append":
            # Path B commit 4: append-then-trim ring buffer of the last 20 wiki
            # query+filter states. Unblocks Bucket A #022 "query log pane"
            # consumer on wiki-search.html. Storage is local-only at
            # dashboards/data/query-log.json — no auth, no cross-user sharding.
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
            except Exception as e:
                self._json(400, {"ok": False, "error": f"bad json: {e}"})
                return

            query = (payload.get("query") or "").strip()
            filters = payload.get("filters") or {}
            if not query:
                self._json(400, {"ok": False, "error": "query must be non-empty"})
                return
            if not isinstance(filters, dict):
                self._json(400, {"ok": False, "error": "filters must be an object"})
                return

            ql_path = DATA_DIR / "query-log.json"
            existing: list = []
            if ql_path.exists():
                try:
                    payload_existing = json.loads(ql_path.read_text())
                    if isinstance(payload_existing, dict):
                        existing = payload_existing.get("entries", [])
                    elif isinstance(payload_existing, list):
                        # Back-compat for older plain-array format
                        existing = payload_existing
                except Exception:
                    existing = []

            entry = {
                "query": query[:500],
                "filters": {k: v for k, v in filters.items() if isinstance(k, str)},
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            # Dedupe: if the immediately-previous entry has the same query+filters
            # don't add a new row (user hit reload or re-ran the same search).
            if existing and existing[-1].get("query") == entry["query"] and existing[-1].get("filters") == entry["filters"]:
                existing[-1] = entry  # refresh timestamp
            else:
                existing.append(entry)
                if len(existing) > 20:
                    existing = existing[-20:]  # ring-buffer trim

            ql_path.write_text(json.dumps({"entries": existing}, indent=2))
            self._json(200, {"ok": True, "count": len(existing)})
            return
        elif self.path == "/api/query-log/get":
            # Path B commit 4: return the ring buffer, newest-last (oldest-first
            # for chronological display). Empty array when no log exists.
            ql_path = DATA_DIR / "query-log.json"
            if not ql_path.exists():
                self._json(200, {"ok": True, "entries": []})
                return
            try:
                payload = json.loads(ql_path.read_text())
                entries = payload.get("entries", []) if isinstance(payload, dict) else payload
            except Exception as e:
                self._json(200, {"ok": True, "entries": [], "warning": f"parse error: {e}"})
                return
            self._json(200, {"ok": True, "entries": entries or []})
            return
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
        elif self.path == "/api/agent-drafts/commit":
            # WS-M11 (2026-04-30): commit an agent-authored draft to a feature branch.
            # Safety:
            #   1. Path must resolve under wiki/staging/, context/intake/, or wiki/agent-created/.
            #   2. Branch name is derived server-side from the path slug — client-supplied branch
            #      is advisory only, ignored if it tries to write to main/master.
            #   3. No force-push. Regular push with tracking.
            #   4. Subprocess with list args, never shell=True.
            #   5. Global feature flag WIKI_AGENTIC_COMMIT_ENABLED must be true; otherwise returns
            #      a 503 with an explanation. Default is DISABLED until Richard flips it.
            import subprocess, re
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
            except Exception as e:
                self._json(400, {"ok": False, "error": f"bad json: {e}"})
                return

            if not os.environ.get("WIKI_AGENTIC_COMMIT_ENABLED") == "1":
                self._json(503, {
                    "ok": False,
                    "error": "agentic commits disabled",
                    "hint": "set env WIKI_AGENTIC_COMMIT_ENABLED=1 to enable; see .kiro/steering/dashboard-redesign-naming.md",
                })
                return

            rel_path = (payload.get("path") or "").strip()
            author = (payload.get("author") or "agent").strip()[:60]
            message = (payload.get("message") or "").strip()[:240]
            if not rel_path or not message:
                self._json(400, {"ok": False, "error": "path and message are required"})
                return

            # Normalize + resolve under repo root
            repo_root = Path(__file__).parent.parent  # /shared/user
            try:
                full = (repo_root / rel_path).resolve()
                full.relative_to(repo_root)  # raises if escaped
            except Exception:
                self._json(400, {"ok": False, "error": "path escapes repo root"})
                return

            # Whitelist
            allowed_prefixes = ("wiki/staging/", "context/intake/", "wiki/agent-created/")
            if not rel_path.startswith(allowed_prefixes):
                self._json(400, {
                    "ok": False,
                    "error": f"path must start with one of {allowed_prefixes}",
                })
                return

            if not full.exists() or not full.is_file():
                self._json(404, {"ok": False, "error": "file not found"})
                return

            # Branch name — server-derived; reject client-supplied branches that look like main
            slug = re.sub(r"[^a-z0-9]+", "-", rel_path.lower()).strip("-")[:60]
            branch = f"wiki/{slug}"
            if branch in ("wiki/main", "wiki/master", "wiki/"):
                self._json(400, {"ok": False, "error": "computed branch invalid"})
                return

            def git(*args):
                return subprocess.run(
                    ["git", "-C", str(repo_root), *args],
                    capture_output=True, text=True, timeout=30,
                )

            try:
                # Create + checkout feature branch (no-op if it exists)
                r = git("checkout", "-B", branch)
                if r.returncode != 0:
                    self._json(500, {"ok": False, "error": f"checkout failed: {r.stderr.strip()[:400]}"})
                    return
                # Stage only this specific path — never git add -A from this endpoint
                r = git("add", rel_path)
                if r.returncode != 0:
                    self._json(500, {"ok": False, "error": f"add failed: {r.stderr.strip()[:400]}"})
                    return
                # Commit with trailer
                trailer = f"\n\nAuthor-agent: {author}\nTriggered-by: wiki-search UI"
                r = git("commit", "-m", message + trailer)
                if r.returncode != 0:
                    # Could be "nothing to commit" — return a clean 200 for that case
                    if "nothing to commit" in (r.stdout + r.stderr).lower():
                        self._json(200, {
                            "ok": True,
                            "branch": branch,
                            "no_changes": True,
                            "message": "nothing to commit for this path",
                        })
                        return
                    self._json(500, {"ok": False, "error": f"commit failed: {r.stderr.strip()[:400]}"})
                    return
                sha_r = git("rev-parse", "HEAD")
                sha = sha_r.stdout.strip() if sha_r.returncode == 0 else ""
                # Push (regular, no force)
                r = git("push", "-u", "origin", branch)
                if r.returncode != 0:
                    self._json(500, {
                        "ok": False,
                        "commit_sha": sha,
                        "branch": branch,
                        "error": f"push failed: {r.stderr.strip()[:400]}",
                    })
                    return
                # Return to main — don't leave the serve.py on a feature branch
                git("checkout", "main")
                self._json(200, {
                    "ok": True,
                    "commit_sha": sha[:10],
                    "branch": branch,
                    "path": rel_path,
                    "author": author,
                })
            except subprocess.TimeoutExpired:
                self._json(504, {"ok": False, "error": "git command timed out"})
            except Exception as e:
                self._json(500, {"ok": False, "error": f"{type(e).__name__}: {e}"[:400]})
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
