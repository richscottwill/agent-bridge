#!/usr/bin/env python3
"""Refresh contributions dashboard data.

For each of Richard's 3 official 2026 goals, pull contribution signals from
FOUR sources and blend them into a single per-goal timeline:

  1. Asana  — completed tasks (assignee=Richard, 2026 YTD)
  2. Slack  — messages Richard authored mentioning goal-keywords
  3. Quip   — Richard's edits/comments on the Outbound Marketing Internal doc + children
  4. Email  — messages in Sent Items where Richard originated a decision

Design:
  - Source-agnostic record shape: {source, date, text, url, people, confidence, goal}
  - Keyword taxonomy per goal (shared with downstream consumers)
  - Dedupe across sources using a normalized text-hash (same idea surfaced in
    multiple channels collapses to one entry with source-list)
  - Output JSON: { goals: [{goal_title, markets, contributions: [...], counts_by_source}] }

IMPORTANT:
  This script cannot call MCP tools directly (they're agent-exposed). It writes
  a MANIFEST with search specs, and the orchestrating agent executes the queries
  and writes raw results to /tmp/contrib-inputs/. This script then consolidates.

  Run order:
    1. Agent calls MCP tools per the manifest (Asana search, Slack search,
       Quip read, Outlook search) and writes JSON results to /tmp/contrib-inputs/.
    2. python3 refresh-contributions.py → reads /tmp/contrib-inputs/*.json
       → writes data/contributions-data.json.

  For unattended runs, refresh-contributions.py falls back to the existing
  inputs on disk if the manifest says they're fresh enough (<24h).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path.home()
OUT = ROOT / "shared" / "dashboards" / "data" / "contributions-data.json"
INPUT_DIR = Path("/tmp/contrib-inputs")
MANIFEST_OUT = INPUT_DIR / "MANIFEST.json"

RICHARD_NAME = "Richard Williams"
RICHARD_LOGIN = "prichwil"
RICHARD_EMAIL = "prichwil@amazon.com"
RICHARD_ASANA_GID = "1212732742544167"
RICHARD_QUIP_ID = "YAT9EAkZs9f"  # author_id for Richard in Quip (used for creator-match)

QUIP_URL = "https://quip-amazon.com/UZ3VOhztKN4s/Outbound-Marketing-Internal"

# SharePoint attribution tiers — see soul.md § contribution-pipeline-rules.
# Tier 1: native Richard-authored files → credit Richard, confidence=high.
# Tier 2: script-generated (python-docx/openpyxl) → credit only if source is Richard.
# Tier 3: co-authored native files → credit with co_authors.
# Tier 4: shared team docs → content-extract-only; skip at doc level.
# Tier 5: Quip docs Richard created → credit Richard.
SCRIPT_GENERATED_MARKERS = ("python-docx", "openpyxl", "python-pptx")
SHARED_TEAM_DOC_HINTS = (
    "WBR Callouts", "MBR ", "Brandon 1:1", "Richard/Brandon", "Deep Dive",
    "AU transition", "OCI Handoff", "Outbound Marketing Internal",
)

# ---------------------------------------------------------------------------
# Goal keyword taxonomy. These drive both the search queries (Slack/email/Quip)
# and the downstream bucketing of Asana task names into the right goal.
# ---------------------------------------------------------------------------

GOALS = [
    {
        "title": "Globalized Cross-Market Testing",
        "markets": ["ww"],
        "keywords": [
            "email overlay", "weblab", "polaris brand", "baloo",
            "bfcm promo", "cross-market test", "cross market test",
            "non-standard integration", "testing approach", "enhanced match",
            "liveramp", "ww testing", "ww rollout", "workstream",
            "ai max", "ad copy", "modern search", "algorithmic ads",
            "testing framework", "testing playbook",
        ],
        "negative_keywords": [],
    },
    {
        "title": "MX/AU Paid Search Registrations",
        "markets": ["mx", "au"],
        "keywords": [
            "mx registration", "mx regs", "au registration", "au regs",
            "mx cpa", "au cpa", "ie%ccp", "ieccp", "iescp",
            "op2 pacing mx", "op2 pacing au", "mx forecast", "au forecast",
            "mx budget", "au budget", "mx spend", "au spend",
            "mx r&o", "au r&o", "mx pacing", "au pacing",
            "lorena", "kingpin for mx", "mx po", "au invoice",
        ],
        "negative_keywords": [],
    },
    {
        "title": "MX + AU Market Testing",
        "markets": ["mx", "au"],
        "keywords": [
            "mx test", "au test", "mx landing page", "au landing page",
            "polaris au", "polaris mx", "mx lp", "au lp",
            "adobe au", "adobe mx", "keyword mx", "keyword au",
            "mx automotive", "au brand lp", "mx beauty",
            "negative keyword mx", "negative keyword au",
            "au keyword", "au nb", "mx nb", "au paid search",
            "mx paid search", "refmarker au", "au lp switch",
            "au meetings", "mx lp", "au polaris", "mx polaris",
        ],
        "negative_keywords": [],
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def text_hash(s: str) -> str:
    return hashlib.md5(norm(s).encode("utf-8")).hexdigest()[:12]


def bucket_by_keywords(text: str, goals=GOALS):
    """Return list of goal titles whose keywords or market tokens appear in text.

    Rules:
      1. Explicit keyword hit anywhere in the text.
      2. Market-token hit via word-boundary regex — catches AU/MX/WW as
         standalone words even next to em-dashes/punctuation.
      3. Every goal that matches is returned (a task can fund multiple goals).
    """
    t = norm(text)
    matches = []
    # Build a market-token regex once per call; cheap enough for this scale.
    for g in goals:
        hit = False
        if any(kw.lower() in t for kw in g["keywords"]):
            hit = True
        else:
            # Market-token check — word boundary around the market code.
            for m in g.get("markets", []):
                if m == "ww":
                    # WW goals also catch pan-market terms and workstreams.
                    continue
                if re.search(rf"\b{m}\b", t):
                    hit = True
                    break
        if hit:
            matches.append(g["title"])
    return matches


def load_json_if_fresh(path: Path, max_age_hours: int = 48):
    if not path.exists():
        return None
    age_s = (datetime.now().timestamp() - path.stat().st_mtime)
    if age_s > max_age_hours * 3600:
        return None
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"warn: failed to parse {path}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Manifest — written to /tmp/contrib-inputs/MANIFEST.json so the agent knows
# what MCP calls to run before invoking this script.
# ---------------------------------------------------------------------------

def write_manifest():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    ytd_start = "2026-01-01"
    today = datetime.now().date().isoformat()

    spec = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "purpose": "Agent-callable spec for contribution signal collection.",
        "run_when": "Before refresh-contributions.py. Outputs land in /tmp/contrib-inputs/.",
        "inputs": [
            {
                "name": "asana_completed.json",
                "tool": "asana___SearchTasksInWorkspace",
                "params": {
                    "assignee_any": RICHARD_ASANA_GID,
                    "completed": "true",
                    "completed_on_before": today,
                    "sort_by": "completed_at",
                },
                "follow_up": (
                    "For each task in data[], call asana___GetTaskDetails with "
                    "opt_fields='name,completed_at,notes,projects.name,permalink_url,"
                    "memberships.project.name,memberships.section.name' to enrich."
                ),
                "notes": "API returns completed YTD; cap at ~200 for volume control.",
            },
            {
                "name": "slack_messages.json",
                "tool": "slack-mcp_search",
                "queries": [
                    f'from:@{RICHARD_LOGIN} "{kw}" after:2026-01-01'
                    for g in GOALS for kw in g["keywords"][:6]  # top 6 kw per goal
                ],
                "notes": (
                    "Slack search is rate-limited — prioritise the first 6 keywords "
                    "per goal. Write {query, results: [...]} objects one per line "
                    "(JSONL) or a single list."
                ),
            },
            {
                "name": "quip_outbound_marketing_internal.json",
                "tool": "ReadInternalWebsites",
                "params": {"inputs": [QUIP_URL + "?includeComments=true"]},
                "follow_up": (
                    "Also fetch quip-amazon.com/search?query=RICHARD&count=30 to find "
                    "any Outbound Marketing child threads Richard authored or commented on."
                ),
                "notes": "Read the main doc + comments to capture Richard's edits/comments.",
            },
            {
                "name": "quip_docs.json",
                "tool": "ReadInternalWebsites",
                "params": {
                    "inputs": [
                        "https://quip-amazon.com/explore/list_created?startDate=2026-01-01&endDate=" + today,
                        "https://quip-amazon.com/explore/list_commented?startDate=2026-01-01&endDate=" + today,
                    ]
                },
                "notes": (
                    "Quip explore routes return docs where Richard is creator or commenter. "
                    "The normalizer credits Richard as creator (tier 5) and filters shared_team_doc=true "
                    "from commented docs. Write as {richard_quip_author_id, created:[...], commented:[...]}."
                ),
            },
            {
                "name": "sharepoint_artifacts.json",
                "tool": "sharepoint_search",
                "queries": [
                    "Author:\"Richard Williams\" (paid search OR testing OR polaris OR overlay OR weblab OR regs OR OCI OR baloo)",
                    "Author:\"Richard Williams\" (MX OR AU) (test OR keyword OR registration OR landing)",
                    "Author:\"Richard Williams\" (email overlay OR weblab OR polaris OR baloo OR enhanced match OR liveramp)",
                ],
                "notes": (
                    "Run each KQL query via sharepoint_search with rowLimit=50; dedupe on path; "
                    "retain the most-recent instance of each title. Write as "
                    "{artifacts: [{title, path, author, author_email, last_modified, "
                    "last_modified_by, file_type, co_authors?, summary}]}. "
                    "Filter: skip titles matching SHARED_TEAM_DOC_HINTS; "
                    "skip author=python-docx/openpyxl unless verified."
                ),
            },
            {
                "name": "email_sent.json",
                "tool": "outlook-mcp_email_folders + email_search",
                "params_per_goal": {
                    g["title"]: {
                        "folder": "sentitems",
                        "startDate": ytd_start,
                        "endDate": today,
                        "query_options": [kw for kw in g["keywords"][:5]],
                        "limit": 50,
                    }
                    for g in GOALS
                },
                "notes": (
                    "For each goal, run email_search(folder='sentitems', query=kw, "
                    "startDate, endDate) for the top 5 keywords. Store results keyed "
                    "by goal-title to simplify downstream bucketing."
                ),
            },
        ],
    }
    MANIFEST_OUT.write_text(json.dumps(spec, indent=2))
    print(f"wrote manifest: {MANIFEST_OUT}")


# ---------------------------------------------------------------------------
# Per-source normalizers — each turns a raw MCP response into the common record
# shape: {source, date, title, text, url, people, confidence}
# ---------------------------------------------------------------------------

def normalize_asana(raw):
    """raw = {'data': [{gid,name,completed_at,notes,permalink_url, memberships:[{project:{name}}]}]}"""
    records = []
    if not raw:
        return records
    items = raw.get("data") or raw.get("APIOutput", {}).get("Response", {}).get("data") or []
    for t in items:
        name = t.get("name") or ""
        if not name:
            continue
        completed = t.get("completed_at") or t.get("created_at") or ""
        projects = []
        for m in (t.get("memberships") or []):
            p = (m.get("project") or {}).get("name")
            if p:
                projects.append(p)
        if t.get("projects"):
            for p in t["projects"]:
                if isinstance(p, dict) and p.get("name"):
                    projects.append(p["name"])
        buckets = bucket_by_keywords(name + " " + " ".join(projects))
        records.append({
            "source": "asana",
            "date": completed[:10] if completed else "",
            "title": name,
            "text": (t.get("notes") or "")[:400],
            "url": t.get("permalink_url") or "",
            "people": [RICHARD_NAME],
            "projects": projects,
            "confidence": "high",  # Richard is the assignee — direct evidence
            "goals": buckets,
            "hash": text_hash(name),
        })
    return records


def normalize_slack(raw):
    """raw = [{query, results:[{text, permalink, ts, channel_name, user_name}]}] or the flat mcp search shape.
    
    Filters out Kiro-generated system messages (daily briefs, AM triage summaries)
    since those are agent outputs, not Richard's contributions.
    """
    records = []
    if not raw:
        return records
    queries = raw if isinstance(raw, list) else [raw]
    # Patterns that indicate a system-generated brief rather than a Richard contribution.
    SYSTEM_PATTERNS = [
        r"Daily Brief",
        r"AM Triage Complete",
        r"AM Frontend Complete",
        r"Wednesday Brief",
        r"Friday Brief",
        r"Monday Brief",
        r"Thursday Brief",
        r"Tuesday Brief",
        r"TRAINER CHECK-IN",
        r"Streak:\s*\d",
        r"Engine Room Cap Enforcement",
        r"Hard Thing:",
    ]
    sys_re = re.compile("|".join(SYSTEM_PATTERNS), re.IGNORECASE)

    for q in queries:
        # Accept either {query, messages:{matches:[...]}} (mcp search shape) or
        # {query, results:[...]} (our normalized shape).
        results = []
        if isinstance(q.get("messages"), dict):
            results = q["messages"].get("matches") or []
        else:
            results = q.get("results") or q.get("messages") or []
        for m in results:
            text = m.get("text") or m.get("message") or ""
            if not text:
                continue
            # Skip Kiro-generated briefs
            if sys_re.search(text):
                continue
            # Date extraction — prefer ts_iso (already ISO), else unix ts
            ts_iso = m.get("ts_iso")
            if ts_iso:
                date = ts_iso[:10]
            else:
                ts = m.get("ts") or m.get("timestamp") or ""
                if isinstance(ts, (int, float)) or (isinstance(ts, str) and ts.replace(".", "").isdigit()):
                    try:
                        date = datetime.fromtimestamp(float(ts), tz=timezone.utc).date().isoformat()
                    except Exception:
                        date = ""
                else:
                    date = str(ts)[:10]
            url = m.get("permalink") or m.get("url") or ""
            ch_obj = m.get("channel") or {}
            if isinstance(ch_obj, dict):
                ch = ch_obj.get("name") or ""
            else:
                ch = m.get("channel_name") or str(ch_obj)
            # Build a snippet title from the message text itself (first sentence,
            # stripped of markdown artifacts) — more useful than "Slack in #foo".
            clean = re.sub(r"<https?://[^|>]+\|([^>]+)>", r"\1", text)
            clean = re.sub(r"<https?://[^>]+>", "", clean)
            clean = re.sub(r"<@\w+\|([^>]+)>", r"@\1", clean)
            clean = re.sub(r":\w+:", "", clean)
            clean = re.sub(r"\s+", " ", clean).strip()
            first = re.split(r"(?<=[.!?])\s", clean, maxsplit=1)[0].strip("*_ ")
            if len(first) > 110:
                first = first[:107] + "..."
            if not first:
                first = f"Slack in #{ch}" if ch else "Slack message"
            buckets = bucket_by_keywords(text)
            records.append({
                "source": "slack",
                "date": date,
                "title": first,
                "text": text[:500],
                "url": url,
                "people": [m.get("username") or m.get("user_name") or RICHARD_NAME],
                "channel": ch,
                "confidence": "medium",  # keyword-matched, not causal
                "goals": buckets,
                "hash": text_hash(text),
            })
    return records


def normalize_sharepoint(raw):
    """raw = {artifacts: [{title, path, author, author_email, last_modified, file_type, co_authors?, summary}]}

    Applies the 5-tier credit matrix:
      Tier 1 (native Richard-authored)   → confidence=high, people=[Richard]
      Tier 2 (script-generated docx)     → confidence=low, note="script-generated, verify source"
                                            — only kept if author includes Richard AND no obvious team-doc title
      Tier 3 (co-authored native)        → confidence=high with co_authors list
      Tier 4 (shared team docs)          → skipped (title matches SHARED_TEAM_DOC_HINTS) — should be
                                            harvested at paragraph level via a separate content-extract
                                            pipeline, not via doc-level attribution.
    """
    records = []
    if not raw:
        return records
    items = raw.get("artifacts") or raw.get("results") or []
    for a in items:
        title = a.get("title") or ""
        author = a.get("author") or ""
        path = a.get("path") or ""
        last_mod = a.get("last_modified") or ""
        last_mod_by = a.get("last_modified_by") or ""
        file_type = (a.get("file_type") or "").lower()
        summary = a.get("summary") or ""
        co_authors = a.get("co_authors") or []

        # Tier 4: shared team docs → skip at doc level.
        if any(hint.lower() in title.lower() for hint in SHARED_TEAM_DOC_HINTS):
            continue

        # Richard must appear in the Author field to be credited at all.
        if RICHARD_NAME.lower() not in author.lower() and RICHARD_LOGIN not in (a.get("author_email") or "").lower():
            continue

        # Tier 2: script-generated. Our current input set is hand-curated and
        # doesn't include script-generated files, but this future-proofs the
        # normalizer: if a generator marker appears in author, mark low-confidence.
        is_script_generated = any(m in author.lower() for m in SCRIPT_GENERATED_MARKERS)
        confidence = "low" if is_script_generated else "high"

        # Tier 3 detection: if there are other named authors alongside Richard,
        # flag co-authorship.
        if co_authors:
            people = [RICHARD_NAME] + [c for c in co_authors if c]
        else:
            # Parse author string — "Richard Williams;Williams, Richard;Other Name"
            parts = [p.strip() for p in author.split(";") if p.strip()]
            extras = [p for p in parts if RICHARD_NAME.lower() not in p.lower() and "williams, richard" not in p.lower()]
            if extras:
                co_authors = extras
                people = [RICHARD_NAME] + extras
            else:
                people = [RICHARD_NAME]

        # Bucket by title + summary so keyword taxonomy catches the right goal.
        buckets = bucket_by_keywords(title + " " + summary)

        rec = {
            "source": "sharepoint",
            "date": last_mod[:10] if last_mod else "",
            "title": title,
            "text": summary[:500],
            "url": path,
            "people": people,
            "file_type": file_type,
            "confidence": confidence,
            "goals": buckets,
            "hash": text_hash(title),
        }
        if co_authors:
            rec["co_authors"] = co_authors
        if is_script_generated:
            rec["note"] = "script-generated export; verify originating wiki/Quip source for attribution"
        records.append(rec)
    return records


def normalize_quip_created(raw):
    """raw = {richard_quip_author_id, created: [...], commented: [...]}

    Applies tier 5: Quip docs where creator matches Richard's author_id get
    credit. `commented` docs are credited only when NOT flagged as shared_team_doc.
    """
    records = []
    if not raw:
        return records
    created = raw.get("created") or []
    commented = raw.get("commented") or []

    for d in created:
        title = d.get("title") or ""
        link = d.get("link") or ""
        created_date = (d.get("created_date") or "")[:10]
        updated_date = (d.get("updated_date") or "")[:10]
        # Use updated_date for ranking (reflects active work), but retain created_date in text.
        date = updated_date or created_date
        buckets = bucket_by_keywords(title)
        text = f"Quip doc created {created_date}; last touched {updated_date}."
        records.append({
            "source": "quip",
            "date": date,
            "title": f"Quip: {title}",
            "text": text,
            "url": link,
            "people": [RICHARD_NAME],
            "confidence": "high",
            "goals": buckets,
            "hash": text_hash("quip-created|" + title + "|" + link),
        })

    for d in commented:
        if d.get("shared_team_doc"):
            # Tier 4 equivalent — skip at doc level; would need paragraph extraction.
            continue
        title = d.get("title") or ""
        link = d.get("link") or ""
        updated_date = (d.get("updated_date") or "")[:10]
        buckets = bucket_by_keywords(title)
        records.append({
            "source": "quip",
            "date": updated_date,
            "title": f"Quip comment: {title}",
            "text": f"Richard commented; last touched {updated_date}.",
            "url": link,
            "people": [RICHARD_NAME],
            "confidence": "medium",
            "goals": buckets,
            "hash": text_hash("quip-commented|" + title + "|" + link),
        })
    return records


def normalize_quip(raw):
    """raw = {'content': '...', 'comments':[{author, text, timestamp}]} or similar."""
    records = []
    if not raw:
        return records
    # Approach: pull comments authored by Richard + section headings he edited
    items = raw.get("items") or raw.get("comments") or []
    if isinstance(raw, dict) and "content" in raw:
        # If the whole doc text is present, scan for paragraphs with Richard's name
        content = raw.get("content") or ""
        # Richard-tagged paragraphs (e.g., "- [Richard] note here" or "**Richard**: ...")
        for m in re.finditer(r"(?:\[Richard\]|\bRichard Williams\b|\*\*RW\*\*|\*\*Richard\*\*)[^\n]{0,400}", content):
            snippet = m.group(0)
            buckets = bucket_by_keywords(snippet)
            records.append({
                "source": "quip",
                "date": raw.get("updated", "")[:10],
                "title": "Quip: Outbound Marketing Internal",
                "text": snippet,
                "url": QUIP_URL,
                "people": [RICHARD_NAME],
                "confidence": "medium",
                "goals": buckets,
                "hash": text_hash(snippet),
            })
    for c in items:
        author = c.get("author") or c.get("author_name") or ""
        text = c.get("text") or c.get("content") or ""
        if RICHARD_NAME.lower() not in author.lower() and "richard" not in author.lower():
            continue
        if not text:
            continue
        buckets = bucket_by_keywords(text)
        records.append({
            "source": "quip",
            "date": (c.get("timestamp") or c.get("updated") or "")[:10],
            "title": "Quip comment on Outbound Marketing Internal",
            "text": text[:500],
            "url": c.get("url") or QUIP_URL,
            "people": [author],
            "confidence": "high",  # explicitly authored
            "goals": buckets,
            "hash": text_hash(text),
        })
    return records


def normalize_email(raw):
    """raw = {goal_title: {query: results: [{subject, receivedDateTime, bodyPreview, webLink, from, to}]}}
       OR a flat list of messages.
    """
    records = []
    if not raw:
        return records
    # Support both shapes
    if isinstance(raw, dict):
        # goal_title → query list → messages
        for goal_title, payload in raw.items():
            msgs = []
            if isinstance(payload, list):
                msgs = payload
            elif isinstance(payload, dict):
                # payload could be {query_kw: [msgs...]}
                for v in payload.values():
                    if isinstance(v, list):
                        msgs.extend(v)
            for m in msgs:
                subj = m.get("subject") or ""
                body = m.get("bodyPreview") or m.get("body") or ""
                date = (m.get("receivedDateTime") or m.get("sentDateTime") or "")[:10]
                url = m.get("webLink") or ""
                to = m.get("to") or m.get("to_recipients") or []
                if isinstance(to, list):
                    to_names = [t.get("name") if isinstance(t, dict) else str(t) for t in to]
                else:
                    to_names = [str(to)]
                text_for_bucket = subj + " " + body
                buckets = bucket_by_keywords(text_for_bucket)
                if goal_title and goal_title in [g["title"] for g in GOALS]:
                    buckets = list({goal_title, *buckets})
                records.append({
                    "source": "email",
                    "date": date,
                    "title": subj or "(no subject)",
                    "text": body[:500],
                    "url": url,
                    "people": to_names[:6],
                    "confidence": "high",  # explicitly sent by Richard
                    "goals": buckets,
                    "hash": text_hash(subj + "|" + body[:200]),
                })
    return records


# ---------------------------------------------------------------------------
# Consolidation — dedupe across sources + rank per goal.
# ---------------------------------------------------------------------------

def consolidate(records):
    """Return per-goal ranked contribution lists + counts_by_source.

    Dedupe is SOURCE-SCOPED: same-source records with the same text hash
    collapse; cross-source matches keep both but flag the overlap via
    `also_seen_in`. This preserves the signal that one topic showed up in
    Asana AND Slack AND email.
    """
    by_goal = {g["title"]: [] for g in GOALS}
    by_source_hash = {}     # (source, hash) -> record (intra-source dedupe)
    by_hash = {}            # hash -> list of sources (cross-source overlap)
    keep = []
    for r in records:
        key = (r["source"], r["hash"])
        if key in by_source_hash:
            continue  # exact within-source duplicate, skip
        by_source_hash[key] = r
        by_hash.setdefault(r["hash"], []).append(r["source"])
        keep.append(r)
    # Pass 2: annotate cross-source overlap
    for r in keep:
        srcs = by_hash.get(r["hash"], [])
        other = [s for s in srcs if s != r["source"]]
        if other:
            r["also_seen_in"] = sorted(set(other))

    for r in keep:
        for goal in r.get("goals") or []:
            if goal in by_goal:
                by_goal[goal].append(r)

    # Sort each goal by date desc, then confidence (high first)
    rank_order = {"high": 0, "medium": 1, "low": 2}
    for goal, items in by_goal.items():
        items.sort(key=lambda x: (-(1 if x.get("date") else 0), x.get("date") or "", rank_order.get(x.get("confidence"), 2)), reverse=True)

    # Per-goal source counts
    out_goals = []
    for g in GOALS:
        items = by_goal[g["title"]]
        counts = {"asana": 0, "slack": 0, "quip": 0, "sharepoint": 0, "email": 0}
        for r in items:
            src = r.get("source")
            if src in counts:
                counts[src] += 1
        out_goals.append({
            "title": g["title"],
            "markets": g["markets"],
            "keywords": g["keywords"],
            "contribution_count": len(items),
            "counts_by_source": counts,
            "contributions": items,
        })
    return out_goals


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Always refresh the manifest so the agent knows what to collect.
    write_manifest()

    # Load whatever inputs are fresh on disk.
    asana = load_json_if_fresh(INPUT_DIR / "asana_completed.json")
    slack = load_json_if_fresh(INPUT_DIR / "slack_messages.json")
    quip = load_json_if_fresh(INPUT_DIR / "quip_outbound_marketing_internal.json")
    quip_created = load_json_if_fresh(INPUT_DIR / "quip_docs.json")
    sharepoint = load_json_if_fresh(INPUT_DIR / "sharepoint_artifacts.json")
    email = load_json_if_fresh(INPUT_DIR / "email_sent.json")

    sources_available = {
        "asana": asana is not None,
        "slack": slack is not None,
        "quip": (quip is not None) or (quip_created is not None),
        "sharepoint": sharepoint is not None,
        "email": email is not None,
    }
    if not any(sources_available.values()):
        print(
            "No contribution inputs available yet. Agent should collect per the "
            f"manifest: {MANIFEST_OUT}. Writing empty payload.",
            file=sys.stderr,
        )

    records = []
    records.extend(normalize_asana(asana))
    records.extend(normalize_slack(slack))
    records.extend(normalize_quip(quip))
    records.extend(normalize_quip_created(quip_created))
    records.extend(normalize_sharepoint(sharepoint))
    records.extend(normalize_email(email))

    goals_out = consolidate(records)

    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "sources_available": sources_available,
        "total_records": len(records),
        "goals": goals_out,
        "manifest_path": str(MANIFEST_OUT),
    }
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"wrote {OUT}")
    print(f"  sources: {sources_available}")
    print(f"  total records: {len(records)}")
    for g in goals_out:
        print(f"  {g['title']}: {g['contribution_count']} contributions {g['counts_by_source']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
