#!/usr/bin/env python3
"""
build-wiki-index.py — Crawl all wiki content and build a search index JSON.

Sources indexed:
  1. agent-created articles (~/shared/wiki/agent-created/**)
  2. quip-mirror documents (~/shared/wiki/quip-mirror/**)
  3. meeting series files (~/shared/wiki/meetings/*.md)
  4. state files (~/shared/wiki/state-files/*.md)
  5. callout files (~/shared/wiki/callouts/**/*.md)

Output: data/wiki-search-index.json
        data/wiki-docs/<id>.txt  (full body text per doc for viewer)
"""
import json, re, os, sys, hashlib, subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter

# Bucket C #028 — agent attribution via git log parsing.
# Commit subject prefixes reliably identify the authoring agent:
#   "agent-bus: kiro-server NNN ..." → kiro-server post
#   "agent-bus: kiro-local NNN ..."  → kiro-local post
#   "feat(wiki-search): ..."         → kiro-local (owns wiki-search.html)
#   "feat(projection): ..."          → kiro-server (owns projection engine)
#   "feat(weekly-review): ..."       → either agent depending on commit; parsed via co-signature if present
# Everything else falls back to "unknown".
AGENT_PATTERNS = [
    (re.compile(r"(?i)kiro-server", re.I), "kiro-server"),
    (re.compile(r"(?i)kiro-local", re.I), "kiro-local"),
    (re.compile(r"(?i)karpathy", re.I), "karpathy"),
    (re.compile(r"(?i)rw-trainer", re.I), "rw-trainer"),
    (re.compile(r"(?i)wiki-writer", re.I), "wiki-writer"),
    (re.compile(r"(?i)wiki-researcher", re.I), "wiki-researcher"),
    (re.compile(r"(?i)wiki-editor", re.I), "wiki-editor"),
    (re.compile(r"(?i)wiki-critic", re.I), "wiki-critic"),
]

_git_root_cache = None
def _git_root():
    global _git_root_cache
    if _git_root_cache is not None:
        return _git_root_cache
    try:
        r = subprocess.run(
            ["git", "-C", str(WIKI_ROOT.parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0:
            _git_root_cache = r.stdout.strip()
        else:
            _git_root_cache = ""
    except Exception:
        _git_root_cache = ""
    return _git_root_cache


def infer_agent_attribution(rel_path):
    """Parse git log for a file and derive agent attribution.

    Returns dict with:
      - last_agent: the agent tied to the most recent commit that touched this file
      - commit_count: total commits touching this file
      - authoring_agents: sorted list of agents ever touching the file, most-frequent-first
    Returns {} if git is unavailable or the file has no history yet.
    """
    root = _git_root()
    if not root:
        return {}
    try:
        r = subprocess.run(
            ["git", "-C", root, "log", "--format=%s", "--", str(Path("wiki") / rel_path)],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode != 0 or not r.stdout.strip():
            return {}
        subjects = [s for s in r.stdout.splitlines() if s.strip()]
    except Exception:
        return {}

    def classify(subj):
        for pat, name in AGENT_PATTERNS:
            if pat.search(subj):
                return name
        # Path-based fallback — commits touching wiki-search.html are kiro-local by convention,
        # projection.html / mpe_engine.py are kiro-server. For wiki content files themselves
        # we have no strong signal from these patterns, so return "unknown" rather than guess.
        return "unknown"

    agents = [classify(s) for s in subjects]
    counter = Counter(agents)
    # last_agent = agent of most recent commit (first in git log output)
    last_agent = agents[0] if agents else "unknown"
    ranked = [a for a, _ in counter.most_common() if a != "unknown"]
    if not ranked and "unknown" in counter:
        ranked = ["unknown"]
    return {
        "last_agent": last_agent,
        "commit_count": len(agents),
        "authoring_agents": ranked,
    }

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
OUTPUT = Path(__file__).parent / "data" / "wiki-search-index.json"
DOCS_DIR = Path(__file__).parent / "data" / "wiki-docs"
SHAREPOINT_CACHE = Path(__file__).parent / "data" / "sharepoint-artifacts.json"
WIKI_INDEX_MD = WIKI_ROOT / "agent-created" / "_meta" / "wiki-index.md"


def load_sharepoint_cache():
    """Load SharePoint artifacts cache if present. Returns dict keyed by slug stem.

    Each value has: {category, path, modified, size}.
    Returns empty dict if cache missing — builder still works, just no published status.
    """
    if not SHAREPOINT_CACHE.exists():
        return {}, None
    try:
        data = json.loads(SHAREPOINT_CACHE.read_text())
    except Exception as e:
        print(f"Warning: SharePoint cache malformed: {e}")
        return {}, None
    lookup = {}
    for art in data.get("artifacts", []):
        stem = art.get("stem", "").lower()
        if stem:
            # If the same stem appears in multiple categories, prefer the first match.
            # (This is rare; stems should be globally unique.)
            lookup.setdefault(stem, art)
    generated = data.get("generated")
    return lookup, generated


SP_LOOKUP, SP_GENERATED = load_sharepoint_cache()

# ── Market detection ──
MARKET_PATTERNS = {
    "AU": [r'\bau\b', r'\baustralia\b', r'\bau[\-_]'],
    "MX": [r'\bmx\b', r'\bmexico\b', r'\bmx[\-_]'],
    "US": [r'\bus\b', r'\bunited states\b', r'\bus[\-_]', r'\bna\b'],
    "JP": [r'\bjp\b', r'\bjapan\b', r'\bjp[\-_]'],
    "UK": [r'\buk\b', r'\bunited kingdom\b'],
    "DE": [r'\bde\b', r'\bgermany\b'],
    "FR": [r'\bfr\b', r'\bfrance\b'],
    "IT": [r'\bitaly\b', r'\bitalian\b', r'\bit[\-_]market\b', r'\bit[\-_]ps\b'],
    "ES": [r'\bspain\b', r'\bspanish\b', r'\bes[\-_]market\b', r'\bes[\-_]ps\b'],
    "CA": [r'\bca\b', r'\bcanada\b'],
    "EU5": [r'\beu5\b', r'\beu\b'],
    "WW": [r'\bww\b', r'\bworldwide\b', r'\bglobal\b'],
}

TOPIC_PATTERNS = {
    "OCI": [r'\boci\b'],
    "Polaris": [r'\bpolaris\b'],
    "AI Max": [r'\bai[\s\-]?max\b'],
    "Baloo": [r'\bbaloo\b'],
    "Testing": [r'\btest(?:ing|s|ed)?\b', r'\bexperiment\b'],
    "Budget": [r'\bbudget\b', r'\bforecast\b', r'\bspend\b'],
    "Landing Pages": [r'\blanding[\s\-]?page\b', r'\blp\b'],
    "Ad Copy": [r'\bad[\s\-]?copy\b', r'\bcreative\b'],
    "Bidding": [r'\bbid(?:ding|s)?\b', r'\bcpc\b', r'\bcpa\b'],
    "Onboarding": [r'\bonboard(?:ing)?\b'],
    "Reporting": [r'\bwbr\b', r'\bmbr\b', r'\bqbr\b', r'\bcallout\b'],
    "AEO": [r'\baeo\b', r'\bai[\s\-]?overview\b'],
    "F90": [r'\bf90\b', r'\blifecycle\b'],
}


def detect_markets(text, path_str):
    """Detect which markets a document relates to."""
    markets = []
    combined = (text[:3000] + " " + path_str).lower()
    for market, patterns in MARKET_PATTERNS.items():
        for p in patterns:
            if re.search(p, combined):
                markets.append(market)
                break
    # Path-based detection
    if "/abix/au/" in path_str or "/au/" in path_str: markets.append("AU")
    if "/abix/mx/" in path_str or "/mx/" in path_str: markets.append("MX")
    if "/eu/" in path_str: markets.append("EU5")
    if "/jp/" in path_str: markets.append("JP")
    if "/na/" in path_str: markets.append("US")
    markets = sorted(set(markets))

    # EU5 consolidation: any doc with a EU5 member also gets EU5 tag
    # Individual market tags are removed (use EU5 filter to find them)
    eu5_members = {"DE", "FR", "IT", "ES", "UK"}
    eu5_in_doc = eu5_members & set(markets)
    if eu5_in_doc:
        markets = [m for m in markets if m not in eu5_members]
        if "EU5" not in markets:
            markets.append("EU5")
        markets = sorted(set(markets))

    return markets


def detect_topics(text):
    """Detect which topics a document substantively covers.
    
    Returns (primary_topic, all_topics):
    - primary_topic: the single highest-density topic (for filtering)
    - all_topics: all topics meeting threshold (for badges/search/backlinks)
    
    A topic is only assigned if the document would be useful to someone
    researching that topic from scratch. Requires multiple keyword hits
    AND sufficient density.
    """
    all_topics = []
    scores = {}
    lower = text.lower()
    word_count = len(lower.split())
    min_hits = max(5, word_count // 200)
    
    for topic, patterns in TOPIC_PATTERNS.items():
        hits = 0
        for p in patterns:
            hits += len(re.findall(p, lower))
        if hits >= min_hits:
            density = hits / max(word_count, 1)
            if density >= 0.005:
                all_topics.append(topic)
                scores[topic] = density
    
    # Primary topic = highest density, or None
    primary = max(scores, key=scores.get) if scores else ""
    return primary, all_topics


# ── Frontmatter parser ──
def parse_frontmatter(text):
    """Extract YAML-like frontmatter from markdown.

    Handles docs with multiple leading --- blocks (e.g. a wrapper added on top
    of an original frontmatter). The first block's keys take precedence, but
    all blocks are stripped from the body.
    """
    fm = {}
    body = text
    # Strip any number of leading frontmatter blocks, merging keys first-wins.
    while True:
        if not body.startswith("---"):
            break
        end = body.find("---", 3)
        if end == -1:
            break
        block = body[3:end].strip()
        body = body[end + 3:].lstrip("\n")
        # Strip any inline HTML comment between FM blocks (doc-id markers)
        body = re.sub(r'^\s*<!--[^>]*-->\s*\n*', '', body, count=1)
        for line in block.split("\n"):
            m = re.match(r'^(\w[\w\-]*)\s*:\s*(.+)', line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip().strip('"').strip("'")
                # First occurrence wins (outer wrapper is freshest)
                if key not in fm:
                    fm[key] = val
    return fm, body


def extract_headings(text, max_depth=3):
    headings = []
    for line in text.split("\n"):
        m = re.match(r'^(#{1,' + str(max_depth) + r'})\s+(.+)', line)
        if m:
            headings.append(m.group(2).strip())
    return headings


def make_snippet(text, max_len=400):
    clean = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    clean = re.sub(r'```.*?```', '', clean, flags=re.DOTALL)
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
    clean = re.sub(r'[#*_`~>|]', '', clean)
    clean = re.sub(r'\n{2,}', '\n', clean)
    clean = re.sub(r'^\s*[-+]\s+', '', clean, flags=re.MULTILINE)
    lines = [l.strip() for l in clean.split("\n") if l.strip() and len(l.strip()) > 10]
    snippet = " ".join(lines[:8])
    if len(snippet) > max_len:
        snippet = snippet[:max_len].rsplit(" ", 1)[0] + "…"
    return snippet


def extract_keywords(text, top_n=20):
    stops = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'shall', 'can', 'this', 'that',
        'these', 'those', 'it', 'its', 'not', 'no', 'nor', 'so', 'if', 'as',
        'we', 'our', 'us', 'they', 'them', 'their', 'he', 'she', 'his', 'her',
        'i', 'me', 'my', 'you', 'your', 'what', 'which', 'who', 'whom', 'how',
        'when', 'where', 'why', 'all', 'each', 'every', 'both', 'few', 'more',
        'most', 'other', 'some', 'such', 'than', 'too', 'very', 'just', 'also',
        'about', 'up', 'out', 'into', 'over', 'after', 'before', 'between',
        'under', 'again', 'then', 'once', 'here', 'there', 'any', 'only',
        'same', 'own', 'still', 'new', 'now', 'one', 'two', 'first', 'last',
        'per', 'via', 'etc', 'e.g', 'i.e', 'vs', 'see', 'use', 'using',
        'based', 'need', 'needs', 'make', 'made', 'get', 'got', 'set',
    }
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    words = [w for w in words if w not in stops]
    counts = Counter(words)
    return [w for w, _ in counts.most_common(top_n)]


def classify_source(path_str):
    if "agent-created" in path_str:
        if "/testing/" in path_str: return "wiki-testing"
        if "/strategy/" in path_str: return "wiki-strategy"
        if "/markets/" in path_str: return "wiki-markets"
        if "/operations/" in path_str: return "wiki-operations"
        if "/reporting/" in path_str: return "wiki-reporting"
        if "/research/" in path_str: return "wiki-research"
        if "/reviews/" in path_str: return "wiki-reviews"
        if "/_meta/" in path_str: return "wiki-meta"
        return "wiki-article"
    if "quip-mirror" in path_str:
        if "/testing/" in path_str: return "quip-testing"
        if "/partnerships/" in path_str: return "quip-partnerships"
        if "/onboarding/" in path_str: return "quip-onboarding"
        if "/review/" in path_str: return "quip-review"
        if "/planning/" in path_str: return "quip-planning"
        if "/mobile-app/" in path_str: return "quip-app"
        return "quip-other"
    if "meetings" in path_str: return "meeting-series"
    if "state-files" in path_str: return "state-file"
    if "callouts" in path_str: return "callout"
    return "other"


def category_label(source):
    """Map source to a content-based category for the TYPE filter.
    
    Categories should be mutually exclusive and describe what the doc IS,
    not where it came from. Aim for 6-8 categories max.
    """
    labels = {
        # Agent-created wiki articles
        "wiki-testing": "Testing & Experimentation",
        "wiki-strategy": "Strategy & Frameworks",
        "wiki-markets": "Markets & Programs",
        "wiki-operations": "Operations & Best Practices",
        "wiki-reporting": "Reporting & Dashboards",
        "wiki-research": "Research & Analysis",
        "wiki-reviews": "Reviews & Evaluations",
        "wiki-meta": "Wiki System",
        "wiki-article": "Strategy & Frameworks",
        # Quip mirrors — reclassify by content
        "quip-testing": "Testing & Experimentation",
        "quip-partnerships": "Partnerships & CPS",
        "quip-onboarding": "Operations & Best Practices",
        "quip-review": "Reviews & Evaluations",
        "quip-planning": "Strategy & Frameworks",
        "quip-app": "Operations & Best Practices",
        "quip-other": "Working Document",
        # Other sources
        "meeting-series": "Meeting Series",
        "state-file": "Market State File",
        "callout": "WBR Callout",
    }
    return labels.get(source, "Other")


def index_file(filepath):
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    if len(text.strip()) < 50:
        return None

    fm, body = parse_frontmatter(text)
    title = fm.get("title", "")
    if not title:
        m = re.search(r'^#\s+(.+)', body, re.MULTILINE)
        if m:
            title = m.group(1).strip()
        else:
            title = filepath.stem.replace("-", " ").title()

    rel_path = str(filepath.relative_to(WIKI_ROOT))
    source = classify_source(rel_path)

    # Archive detection — index but flag as archived
    # Check path AND body text for archive markers
    is_archived = "/archive/" in rel_path
    if not is_archived:
        # Check first 500 chars of body for explicit ARCHIVED banner
        body_start = body[:500].upper()
        if "⚠️ ARCHIVED" in body[:500] or "ARCHIVED —" in body_start or "ARCHIVED—" in body_start:
            is_archived = True
        # Check frontmatter status
        if fm.get("status", "").lower() == "archived":
            is_archived = True

    headings = extract_headings(body)
    snippet = make_snippet(body)
    keywords = extract_keywords(body)
    markets = detect_markets(body, rel_path)
    primary_topic, topics = detect_topics(body)

    # Build searchable text blob
    search_text = f"{title} {' '.join(headings)} {body}"
    search_text = re.sub(r'[^\w\s]', ' ', search_text.lower())
    search_text = re.sub(r'\s+', ' ', search_text).strip()

    tags_raw = fm.get("tags", "")
    if tags_raw.startswith("["):
        tags = [t.strip().strip('"').strip("'") for t in tags_raw.strip("[]").split(",")]
    else:
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    doc_id = hashlib.md5(rel_path.encode()).hexdigest()[:10]

    # Write full body to separate file for viewer
    doc_file = DOCS_DIR / f"{doc_id}.txt"
    doc_file.write_text(body, encoding="utf-8")

    # SharePoint publication status (from cache)
    sp_info = SP_LOOKUP.get(filepath.stem.lower())
    published = bool(sp_info)
    sharepoint_path = sp_info["path"] if sp_info else ""
    sharepoint_modified = sp_info["modified"] if sp_info else ""
    # Stale detection: SP copy is older than local 'updated' field
    sharepoint_stale = False
    if published and sharepoint_modified and fm.get("updated"):
        # Compare date portions only (ISO format). local 'updated' may be date-only.
        try:
            sp_date = sharepoint_modified[:10]
            local_date = fm.get("updated", "")[:10]
            if local_date > sp_date:
                sharepoint_stale = True
        except Exception:
            pass

    # Bucket C #026 — published_lag_days: how many days the SharePoint copy trails the local update.
    # Positive = SP is behind local (needs re-push). Negative = SP is ahead (unusual). Null = not published or missing dates.
    published_lag_days = None
    if published and sharepoint_modified and fm.get("updated"):
        try:
            sp_date = datetime.fromisoformat(sharepoint_modified[:10])
            local_date = datetime.fromisoformat(fm.get("updated", "")[:10])
            published_lag_days = (local_date - sp_date).days
        except Exception:
            published_lag_days = None

    # Bucket C #028 — agent attribution via git log.
    attribution = infer_agent_attribution(rel_path)

    return {
        "id": doc_id,
        "title": title,
        "path": rel_path,
        "source": source,
        "category": category_label(source),
        "status": fm.get("status", "").upper(),
        "audience": fm.get("audience", ""),
        "doc_type": fm.get("doc-type", ""),
        "level": fm.get("level", ""),
        "tags": tags,
        "markets": markets,
        "topics": topics,
        "primary_topic": primary_topic,
        "headings": headings[:15],
        "snippet": snippet,
        "keywords": keywords,
        "updated": fm.get("updated", fm.get("created", "")),
        "created": fm.get("created", ""),
        "word_count": len(body.split()),
        "search_text": search_text[:2000],
        "archived": is_archived,
        "published": published,
        "sharepoint_path": sharepoint_path,
        "sharepoint_modified": sharepoint_modified,
        "sharepoint_stale": sharepoint_stale,
        "published_lag_days": published_lag_days,
        "last_agent": attribution.get("last_agent", "unknown"),
        "commit_count": attribution.get("commit_count", 0),
        "authoring_agents": attribution.get("authoring_agents", []),
    }


def build_backlinks(docs, min_shared=3):
    """Build related-docs graph based on shared keyword overlap.

    For each doc, find other docs that share >= min_shared non-trivial
    keywords. Returns dict of doc_id -> [(related_id, shared_count), ...].
    """
    # Build inverted index: keyword -> set of doc_ids
    kw_to_docs = {}
    doc_kw = {}
    for doc in docs:
        kws = set(doc["keywords"][:15])  # top 15 keywords per doc
        # Also include topics and markets as linkable terms
        kws.update(t.lower() for t in doc.get("topics", []))
        doc_kw[doc["id"]] = kws
        for kw in kws:
            kw_to_docs.setdefault(kw, set()).add(doc["id"])

    # For each doc, count shared keywords with every other doc
    related = {}
    for doc in docs:
        scores = Counter()
        for kw in doc_kw.get(doc["id"], set()):
            for other_id in kw_to_docs.get(kw, set()):
                if other_id != doc["id"]:
                    scores[other_id] += 1
        # Dynamic threshold: require overlap > median of all scores for this doc
        # This means only docs with above-average relatedness qualify
        all_scores = [cnt for _, cnt in scores.most_common(30) if cnt >= min_shared]
        if not all_scores:
            continue
        median_score = sorted(all_scores)[len(all_scores)//2]
        threshold = max(min_shared, median_score)
        candidates = [(did, cnt) for did, cnt in scores.most_common(30) if cnt > threshold]
        # Natural gap detection: cut where score drops >40%
        if len(candidates) > 4:
            for i in range(3, len(candidates)):
                prev = candidates[i-1][1]
                curr = candidates[i][1]
                if curr < prev * 0.6:
                    candidates = candidates[:i]
                    break
            else:
                candidates = candidates[:10]
        if candidates:
            related[doc["id"]] = candidates
    return related


def build_tag_index(docs):
    """Build aggregated tag counts across all docs."""
    tag_counts = Counter()
    for doc in docs:
        for tag in doc.get("tags", []):
            if tag.strip():
                tag_counts[tag.strip()] += 1
    return dict(tag_counts)


def compute_groups(docs):
    """Assign group_key and group_role to documents.

    Grouping rules:
    0. Topic families: cross-directory doc families sharing a path keyword
       (e.g., kate-doc, testing-approach-kate → "family-kate-doc").
    1. Callouts: group by market folder (e.g., callouts/au/* → "callout-au").
       The latest week file is "latest", others are "member".
    2. Iterations: docs with version suffixes (-v1, -v2, -v5) or
       eval/review variants (eval-a, eval-b) share a base name group.
       The highest version or most recent is "latest".
    3. Everything else: group_key=None (standalone).
    """
    # ── Topic-family grouping: cross-directory doc families ──
    # Map of family_key -> list of path substrings that belong to it
    TOPIC_FAMILIES = {
        "kate-doc": ["kate-doc", "testing-approach-kate", "ps-testing-approach-kate", "testing-approach-outline"],
        "five-year-outlook": ["five-year-outlook", "ps-five-year"],
        "oci-playbook": ["oci-playbook", "oci-rollout-playbook", "oci-execution-guide"],
        "agent-architecture": ["agent-architecture", "agent-system-architecture"],
        "workstream-algorithmic": ["workstream-algorithmic-ads"],
        "workstream-ux": ["workstream-user-experience"],
    }
    for family_key, path_patterns in TOPIC_FAMILIES.items():
        family_docs = []
        for doc in docs:
            if doc.get("archived"):
                continue
            stem = Path(doc["path"]).stem.lower()
            if any(pat in stem for pat in path_patterns):
                family_docs.append(doc)
        if len(family_docs) < 2:
            continue
        gk = f"family-{family_key}"
        # Sort: prefer the main article (testing/ or strategy/) over reviews
        def family_sort(d):
            # Main articles first, then by updated date descending
            is_review = 1 if d["source"] in ("wiki-reviews",) else 0
            updated = d.get("updated") or ""
            return (is_review, updated)
        family_docs.sort(key=family_sort)
        # Sort: main articles first (non-reviews), then by updated desc
        non_reviews = [d for d in family_docs if d["source"] != "wiki-reviews"]
        reviews = [d for d in family_docs if d["source"] == "wiki-reviews"]
        non_reviews.sort(key=lambda d: d.get("updated", ""), reverse=True)
        reviews.sort(key=lambda d: d.get("updated", ""), reverse=True)
        family_docs = non_reviews + reviews
        for i, doc in enumerate(family_docs):
            doc["group_key"] = gk
            doc["group_role"] = "latest" if i == 0 else "member"
    # ── Callout grouping ──
    callout_groups = {}  # market -> list of docs
    for doc in docs:
        if doc["source"] == "callout" and not doc.get("archived"):
            # Extract market from path: callouts/<market>/...
            m = re.match(r'callouts/(\w+)/', doc["path"])
            if m:
                market = m.group(1).upper()
                callout_groups.setdefault(market, []).append(doc)

    for market, group_docs in callout_groups.items():
        gk = f"callout-{market.lower()}"
        # Sort by week number descending (extract from filename like au-2026-w15)
        def week_sort(d):
            wm = re.search(r'-w(\d+)', d["path"])
            return int(wm.group(1)) if wm else 0
        group_docs.sort(key=week_sort, reverse=True)
        for i, doc in enumerate(group_docs):
            doc["group_key"] = gk
            doc["group_role"] = "latest" if i == 0 else "member"

    # ── Iteration grouping (versioned docs) ──
    # Match patterns: -v1, -v2, -v5, -eval-a, -eval-b, -r2, etc.
    version_re = re.compile(r'(.+?)[-_](v\d+|eval[-_][ab]|r\d+|rescore)$')
    base_groups = {}  # base_stem -> list of docs
    for doc in docs:
        if doc.get("group_key"):
            continue  # already grouped as callout
        if doc.get("archived"):
            continue
        stem = Path(doc["path"]).stem
        vm = version_re.match(stem)
        if vm:
            base = vm.group(1)
            # Normalize: also check the directory for context
            dir_path = str(Path(doc["path"]).parent)
            full_base = f"{dir_path}/{base}"
            base_groups.setdefault(full_base, []).append(doc)

    for base, group_docs in base_groups.items():
        if len(group_docs) < 2:
            continue  # no group needed for singletons
        gk = f"iter-{hashlib.md5(base.encode()).hexdigest()[:8]}"
        # Sort by version number or updated date
        def version_sort(d):
            stem = Path(d["path"]).stem
            vm = re.search(r'v(\d+)', stem)
            if vm:
                return int(vm.group(1))
            return 0
        group_docs.sort(key=lambda d: (version_sort(d), d.get("updated", "")), reverse=True)
        for i, doc in enumerate(group_docs):
            doc["group_key"] = gk
            doc["group_role"] = "latest" if i == 0 else "member"

    # ── Review docs that share a base article name ──
    # e.g., kate-doc-v2-eval-a, kate-doc-v3-eval-b → group under "kate-doc"
    review_re = re.compile(r'(.+?)[-_](v\d+[-_])?eval[-_][ab]')
    review_groups = {}
    for doc in docs:
        if doc.get("group_key"):
            continue
        if doc["source"] != "wiki-reviews":
            continue
        stem = Path(doc["path"]).stem
        rm = review_re.match(stem)
        if rm:
            base = rm.group(1)
            dir_path = str(Path(doc["path"]).parent)
            full_base = f"{dir_path}/{base}"
            review_groups.setdefault(full_base, []).append(doc)

    for base, group_docs in review_groups.items():
        if len(group_docs) < 2:
            continue
        gk = f"review-{hashlib.md5(base.encode()).hexdigest()[:8]}"
        group_docs.sort(key=lambda d: d.get("updated", ""), reverse=True)
        for i, doc in enumerate(group_docs):
            doc["group_key"] = gk
            doc["group_role"] = "latest" if i == 0 else "member"

    # ── Series grouping: wiki audits, health reports, daily briefs ──
    # Match dated files like audit-2026-04-04, health-2026-04-05, daily-brief-*
    series_re = re.compile(r'(.+?)[-_](\d{4}[-_]\d{2}[-_]\d{2})')
    series_groups = {}
    for doc in docs:
        if doc.get("group_key") or doc.get("archived"):
            continue
        stem = Path(doc["path"]).stem
        sm = series_re.match(stem)
        if sm:
            base = sm.group(1)
            dir_path = str(Path(doc["path"]).parent)
            full_base = f"{dir_path}/{base}"
            series_groups.setdefault(full_base, []).append(doc)

    for base, group_docs in series_groups.items():
        if len(group_docs) < 2:
            continue
        gk = f"series-{hashlib.md5(base.encode()).hexdigest()[:8]}"
        # Sort by date descending (most recent first)
        group_docs.sort(key=lambda d: d.get("updated", ""), reverse=True)
        for i, doc in enumerate(group_docs):
            doc["group_key"] = gk
            doc["group_role"] = "latest" if i == 0 else "member"

    # ── Duplicate-title grouping: docs with identical titles ──
    title_groups = {}
    for doc in docs:
        if doc.get("group_key") or doc.get("archived"):
            continue
        title_groups.setdefault(doc["title"], []).append(doc)

    for title, group_docs in title_groups.items():
        if len(group_docs) < 2:
            continue
        gk = f"dup-{hashlib.md5(title.encode()).hexdigest()[:8]}"
        # Most recently updated first
        group_docs.sort(key=lambda d: d.get("updated", ""), reverse=True)
        for i, doc in enumerate(group_docs):
            doc["group_key"] = gk
            doc["group_role"] = "latest" if i == 0 else "member"

    # ── Prefix grouping: docs in same directory sharing a filename prefix ──
    # e.g., kate-doc-appendix-revisions, kate-doc-batch-review, kate-doc-oci-revisions
    prefix_groups = {}
    for doc in docs:
        if doc.get("group_key") or doc.get("archived"):
            continue
        stem = Path(doc["path"]).stem
        dir_path = str(Path(doc["path"]).parent)
        # Try progressively shorter prefixes (min 8 chars)
        parts = re.split(r'[-_]', stem)
        if len(parts) >= 3:
            prefix = "-".join(parts[:2])  # first two segments
            if len(prefix) >= 8:
                key = f"{dir_path}/{prefix}"
                prefix_groups.setdefault(key, []).append(doc)

    for key, group_docs in prefix_groups.items():
        if len(group_docs) < 3:  # require 3+ to avoid false grouping
            continue
        gk = f"prefix-{hashlib.md5(key.encode()).hexdigest()[:8]}"
        group_docs.sort(key=lambda d: d.get("updated", ""), reverse=True)
        for i, doc in enumerate(group_docs):
            doc["group_key"] = gk
            doc["group_role"] = "latest" if i == 0 else "member"

    # Count groups
    groups = {}
    for doc in docs:
        gk = doc.get("group_key")
        if gk:
            groups.setdefault(gk, []).append(doc)
    return groups


def write_wiki_index_md(docs, sp_generated=None):
    """Write ~/shared/wiki/agent-created/_meta/wiki-index.md from the scanned docs.

    Only includes agent-created articles (source starts with 'wiki-' and not meta/reviews).
    Grouped into 8 sections matching the dashboard category filter.
    """
    ac_docs = [d for d in docs
               if d["source"].startswith("wiki-")
               and d["source"] not in ("wiki-reviews", "wiki-meta")
               and not d.get("archived")
               and (not d.get("group_key") or d.get("group_role") == "latest")]

    # Bucket into 8 sections
    # Historical tests = dated filenames in testing/
    testing_historical = []
    agent_sys = []
    by_cat = {
        "Testing & Experimentation": [],
        "Strategy & Frameworks": [],
        "Markets / PS Operations": [],
        "Operations & Process": [],
        "Reporting": [],
        "Research Briefs": [],
    }
    AGENT_SLUGS = {"agent-architecture", "body-system-architecture", "grok-swarm",
                   "kiro-cli-pretooluse-hook-bug", "meeting-ingestion-pipeline"}
    SKIP_ORPHAN_SLUGS = {"ai-automation-impact", "testing-appendix"}
    skipped = []

    for doc in ac_docs:
        stem = Path(doc["path"]).stem
        if stem in SKIP_ORPHAN_SLUGS:
            skipped.append(doc); continue
        if stem in AGENT_SLUGS or doc.get("audience") == "agent":
            agent_sys.append(doc); continue
        if doc["source"] == "wiki-testing":
            fn = Path(doc["path"]).name
            if fn[:4].isdigit() and len(fn) > 4 and fn[4] == "-":
                testing_historical.append(doc)
            else:
                by_cat["Testing & Experimentation"].append(doc)
        elif doc["source"] == "wiki-strategy":
            by_cat["Strategy & Frameworks"].append(doc)
        elif doc["source"] == "wiki-markets":
            by_cat["Markets / PS Operations"].append(doc)
        elif doc["source"] == "wiki-operations":
            by_cat["Operations & Process"].append(doc)
        elif doc["source"] == "wiki-reporting":
            by_cat["Reporting"].append(doc)
        elif doc["source"] == "wiki-research":
            by_cat["Research Briefs"].append(doc)
        elif doc["source"] == "wiki-article":
            by_cat["Strategy & Frameworks"].append(doc)

    sections = [
        ("Testing & Experimentation", by_cat["Testing & Experimentation"],
         "Active test designs, methodologies, experiment frameworks, and workstream deep-dives."),
        ("Historical Tests (snapshot)", testing_historical,
         "Dated test artifacts preserved as snapshots — do not decay-audit these."),
        ("Strategy & Frameworks", by_cat["Strategy & Frameworks"],
         "POVs, playbooks, mental models, strategic narratives, leadership-facing docs."),
        ("Markets / PS Operations", by_cat["Markets / PS Operations"],
         "Market wikis (AU/MX/US), team capacity, cross-market programs."),
        ("Operations & Process", by_cat["Operations & Process"],
         "SOPs, playbooks, tool specs, vocabulary guides, process documentation."),
        ("Reporting", by_cat["Reporting"],
         "Dashboards, WBR/MBR templates, analysis docs."),
        ("Research Briefs", by_cat["Research Briefs"],
         "Investigation outputs, vendor/competitor intel, experimental research dossiers."),
        ("Agent / System Documentation", agent_sys,
         "Agent architecture, body system, agent personas, meta-docs about the system itself."),
    ]

    def entry(doc):
        title = doc["title"] or Path(doc["path"]).stem.replace("-", " ").title()
        desc = doc["snippet"] or "(no description)"
        if len(desc) > 180:
            desc = desc[:180].rsplit(" ", 1)[0] + "..."
        stem = Path(doc["path"]).stem
        parts = [f"slug: {stem}", f"status: {doc.get('status') or 'DRAFT'}"]
        if doc.get("doc_type"): parts.append(f"doc-type: {doc['doc_type']}")
        if doc.get("audience"): parts.append(f"audience: {doc['audience']}")
        if doc.get("level"): parts.append(f"level: {doc['level']}")
        if doc.get("published"):
            marker = "published"
            if doc.get("sharepoint_stale"):
                marker = "published (stale — local newer)"
            parts.append(f"sharepoint: {marker}")
        else:
            parts.append("sharepoint: local-only")
        out = f"- [{title}](~/shared/wiki/{doc['path']}): {desc}\n  - {' | '.join(parts)}"
        return out

    lines = [
        "---",
        'title: "Wiki Index"',
        "status: FINAL",
        "audience: amazon-internal",
        "owner: Richard Williams",
        "created: 2026-04-12",
        f"updated: {datetime.now().strftime('%Y-%m-%d')}",
        "doc-type: reference",
        "auto_generated: true",
        "---",
        "<!-- DOC-0449 | duck_id: wiki-meta-wiki-index -->",
        "<!-- AUTO-GENERATED by build-wiki-index.py. Do not edit by hand; changes will be overwritten. -->",
        "",
        "# Wiki Index",
        "",
        "> Knowledge base for Amazon Business Paid Search. Auto-generated from a filesystem scan of `~/shared/wiki/agent-created/` by `build-wiki-index.py`. SharePoint publication status pulled from `data/sharepoint-artifacts.json`.",
        "",
        f"Last generated: {datetime.now().isoformat(timespec='seconds')}",
    ]
    if sp_generated:
        lines.append(f"SharePoint cache as of: {sp_generated}")
    lines += ["", "---", "", "## Articles", ""]

    totals = {}
    for name, bucket, blurb in sections:
        lines.append(f"### {name} ({len(bucket)})")
        lines.append("")
        lines.append(f"_{blurb}_")
        lines.append("")
        totals[name] = len(bucket)
        for doc in sorted(bucket, key=lambda d: Path(d["path"]).stem):
            lines.append(entry(doc))
            lines.append("")
        lines.append("")

    lines += ["---", "", "## Summary", "", "| Category | Count |", "|----------|-------|"]
    total = 0
    for name, _, _ in sections:
        lines.append(f"| {name} | {totals[name]} |")
        total += totals[name]
    lines.append(f"| **Total (indexed)** | **{total}** |")
    lines.append("")

    all_in = [d for _, bkt, _ in sections for d in bkt]
    st = Counter(d["status"] or "UNSET" for d in all_in)
    published = sum(1 for d in all_in if d.get("published"))
    stale = sum(1 for d in all_in if d.get("sharepoint_stale"))
    lines.append(f"**Status:** {st.get('REVIEW',0)} REVIEW | {st.get('DRAFT',0)} DRAFT | {st.get('FINAL',0)} FINAL | {st.get('UNSET',0)} unset")
    lines.append(f"**SharePoint:** {published} published | {total - published} local-only | {stale} published-stale (local newer than SP)")
    lines.append("")

    lines += ["---", "", "## Intentional orphans (not indexed)", ""]
    lines.append("Docs that exist in the corpus but intentionally not tracked as wiki articles:")
    lines.append("")
    for d in skipped:
        lines.append(f"- `{Path(d['path']).stem}` — `{d['path']}`. Rationale: see `_meta/roadmap.md` Orphan Decisions table.")
    lines.append("")
    lines.append("Plus the 13 Kiro steering packages in `kiro-steering/` — these are steering files for the Paid Acq team rollout, not wiki articles.")
    lines.append("")

    lines += ["---", "", "## Distribution model", "",
              "Local wiki (`~/shared/wiki/agent-created/`) is the working branch. SharePoint `Documents/Artifacts/` is production.",
              "",
              "- **DRAFT** — article exists locally, still being written or revised.",
              "- **REVIEW** — article is ready for Richard to review for SharePoint publish.",
              "- **FINAL** — article has been human-approved and published to SharePoint.",
              "- **sharepoint: published** — a matching `<slug>.docx` exists under `Documents/Artifacts/<category>/`.",
              "- **sharepoint: published (stale)** — the SharePoint copy is older than the local `updated` date. Needs a re-push.",
              "- **sharepoint: local-only** — no matching `<slug>.docx` on SharePoint.",
              "",
              "The wiki-search dashboard (`shared/dashboards/wiki-search.html`) is the browsing UI over this index.",
              ""]

    WIKI_INDEX_MD.write_text("\n".join(lines))
    return total, published, stale


# ─────────────────────────────────────────────────────────────────────────────
# WS-M03 / M05 / M11 helpers (added 2026-04-30 by kiro-server)
# ─────────────────────────────────────────────────────────────────────────────

def build_ingest_log(docs, limit=20):
    """Return up to `limit` most-recently-updated active docs for the WS-M03 ingest strip.

    Shape: [{id, title, category, updated, word_count, primary_topic}]
    """
    active = [d for d in docs if not d.get("archived") and d.get("updated")]
    active.sort(key=lambda d: d.get("updated", ""), reverse=True)
    return [
        {
            "id": d["id"],
            "title": d["title"],
            "category": d.get("category", ""),
            "updated": d.get("updated", ""),
            "word_count": d.get("word_count", 0),
            "primary_topic": d.get("primary_topic", ""),
            "path": d.get("path", ""),
        }
        for d in active[:limit]
    ]


DEMAND_LOG = WIKI_ROOT / "agent-created" / "_meta" / "wiki-demand-log.md"


def load_demand_log(limit=30):
    """Parse wiki-demand-log.md if present. Tolerant — matches bullets starting with '- '
    and YAML-ish `query:` / `searched:` lines. Returns newest first.

    Each entry: {query, count, last_seen, status (open|satisfied), note}
    """
    if not DEMAND_LOG.exists():
        return []
    try:
        text = DEMAND_LOG.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    entries = []
    # Match bullet-style entries:  - <query>  [count=N] [last=YYYY-MM-DD] [status=open|satisfied] [note=...]
    bullet_re = re.compile(
        r"^\s*[-*]\s+(?P<q>[^\[]+?)\s*"
        r"(?:\[count=(?P<count>\d+)\])?\s*"
        r"(?:\[last=(?P<last>[0-9]{4}-[0-9]{2}-[0-9]{2})\])?\s*"
        r"(?:\[status=(?P<status>open|satisfied|archived)\])?\s*"
        r"(?:\[note=(?P<note>[^\]]+)\])?\s*$",
        re.MULTILINE,
    )
    for m in bullet_re.finditer(text):
        q = m.group("q").strip()
        if not q or q.startswith("#") or q.startswith("**"):
            # Skip headings, empty bullets, and bold-lead format-doc bullets (which are
            # explanatory text in the file's own docstring, not real demand signals).
            continue
        entries.append({
            "query": q[:200],
            "count": int(m.group("count") or 1),
            "last_seen": m.group("last") or "",
            "status": m.group("status") or "open",
            "note": (m.group("note") or "").strip(),
        })
    # Sort: open first by count desc, then satisfied
    entries.sort(key=lambda e: (0 if e["status"] == "open" else 1, -e["count"], e["last_seen"]), reverse=False)
    return entries[:limit]


INTAKE_DIR = WIKI_ROOT.parent / "context" / "intake"
WIKI_STAGING = WIKI_ROOT / "staging"


def scan_agent_drafts(limit=20):
    """Scan known draft locations for agent-authored markdown awaiting promotion.

    Sources (in priority order):
      1. wiki/staging/*.md — critic-approved drafts staged for librarian
      2. context/intake/*.md files matching patterns suggesting a draft (not digests/logs)

    Returns: [{title, author, path, words, stage}]
    """
    drafts = []
    DIGEST_PATTERNS = ("digest", "triage", "tracker", "log", "brief", "queue", "snapshot", "response")

    # wiki/staging/ — everything here is draft-ready
    if WIKI_STAGING.exists():
        for f in sorted(WIKI_STAGING.glob("*.md")):
            try:
                body = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if not body.strip():
                continue
            # Title = first # heading or filename stem
            title_m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            title = title_m.group(1).strip() if title_m else f.stem.replace("-", " ").title()
            # Author from front-matter `author:` or `owner:` or default
            author_m = re.search(r"^(?:author|owner)\s*:\s*(.+)$", body, re.MULTILINE | re.IGNORECASE)
            author = author_m.group(1).strip() if author_m else "wiki-writer"
            drafts.append({
                "title": title[:140],
                "author": author[:60],
                "path": str(f.relative_to(WIKI_ROOT.parent)),
                "words": len(body.split()),
                "stage": "draft-ready",
            })

    # context/intake/ — skip clearly non-draft files (digests, logs, triage queues, brief dumps)
    if INTAKE_DIR.exists():
        for f in sorted(INTAKE_DIR.glob("*.md")):
            name_l = f.name.lower()
            if any(p in name_l for p in DIGEST_PATTERNS):
                continue
            try:
                body = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            wc = len(body.split())
            if wc < 300:
                continue
            title_m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            title = title_m.group(1).strip() if title_m else f.stem.replace("-", " ").title()
            author_m = re.search(r"^(?:author|owner)\s*:\s*(.+)$", body, re.MULTILINE | re.IGNORECASE)
            author = author_m.group(1).strip() if author_m else "wiki-researcher"
            drafts.append({
                "title": title[:140],
                "author": author[:60],
                "path": str(f.relative_to(WIKI_ROOT.parent)),
                "words": wc,
                "stage": "intake",
            })

    # Dedup by path, cap
    seen = set()
    deduped = []
    for d in drafts:
        if d["path"] in seen:
            continue
        seen.add(d["path"])
        deduped.append(d)
        if len(deduped) >= limit:
            break
    return deduped


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    sources = [
        WIKI_ROOT / "agent-created",
        WIKI_ROOT / "quip-mirror",
        WIKI_ROOT / "meetings",
        WIKI_ROOT / "state-files",
        WIKI_ROOT / "callouts",
    ]

    all_files = []
    for src in sources:
        if src.exists():
            all_files.extend(src.rglob("*.md"))

    print(f"Found {len(all_files)} markdown files to index")

    docs = []
    skipped = 0
    for f in sorted(all_files):
        doc = index_file(f)
        if doc:
            docs.append(doc)
        else:
            skipped += 1

    # Compute document groups (callout series, iterations, review sets)
    print("Computing document groups...")
    groups = compute_groups(docs)
    active_docs = [d for d in docs if not d.get("archived")]
    archived_docs = [d for d in docs if d.get("archived")]
    grouped_count = sum(1 for d in docs if d.get("group_key"))
    print(f"  {len(groups)} groups covering {grouped_count} docs")
    print(f"  {len(archived_docs)} archived docs (hidden by default)")

    # Build backlinks graph (keyword-overlap based, active docs only)
    print("Building backlinks graph...")
    backlinks = build_backlinks(active_docs, min_shared=3)
    link_count = sum(len(v) for v in backlinks.values())
    print(f"  {len(backlinks)} docs have related pages ({link_count} total links)")

    # Attach related_docs to each doc (with snippet + category for tooltips)
    id_to_doc = {d["id"]: d for d in docs}
    for doc in docs:
        rels = backlinks.get(doc["id"], [])
        doc["related_docs"] = [
            {
                "id": rid,
                "title": id_to_doc[rid]["title"] if rid in id_to_doc else "?",
                "snippet": id_to_doc[rid]["snippet"][:150] if rid in id_to_doc else "",
                "category": id_to_doc[rid]["category"] if rid in id_to_doc else "",
                "shared": cnt,
            }
            for rid, cnt in rels
            if rid in id_to_doc
        ]

    # WS-M08: reverse_related_docs — invert related_docs so a doc knows who points AT it.
    # Used by the lineage strip in wiki-search.html to show "X docs reference this page".
    reverse_edges = {}  # target_id -> [(source_id, shared)]
    for doc in docs:
        src_id = doc["id"]
        for rel in doc.get("related_docs", []):
            tgt = rel["id"]
            reverse_edges.setdefault(tgt, []).append((src_id, rel.get("shared", 0)))
    for doc in docs:
        incoming = reverse_edges.get(doc["id"], [])
        incoming.sort(key=lambda t: -t[1])
        doc["reverse_related_docs"] = [
            {
                "id": sid,
                "title": id_to_doc[sid]["title"] if sid in id_to_doc else "?",
                "category": id_to_doc[sid]["category"] if sid in id_to_doc else "",
                "shared": cnt,
            }
            for sid, cnt in incoming[:10]
            if sid in id_to_doc
        ]

    # WS-M09: per-doc lint_status — structural + content checks. Drives contradiction badges
    # in search results. Each check is cheap; results are a compact list of {code, severity, detail}.
    # severity: "error" (blocks publish), "warn" (review), "info" (nice-to-have).
    for doc in docs:
        lint = []
        wc = doc.get("word_count", 0)
        status = (doc.get("status") or "").upper()
        # Too-thin content for FINAL
        if status == "FINAL" and wc < 200:
            lint.append({"code": "thin-final", "severity": "warn",
                         "detail": f"FINAL doc with only {wc} words — expand or downgrade to DRAFT"})
        # Missing primary topic
        if not doc.get("primary_topic") and status in ("FINAL", "ACTIVE", "REVIEW"):
            lint.append({"code": "no-topic", "severity": "info",
                         "detail": "No primary topic detected — consider tagging"})
        # No related docs → orphan signal (keeping it as info; orphan detection below is authoritative)
        if not doc.get("related_docs") and not doc.get("archived") and wc > 300:
            lint.append({"code": "isolated", "severity": "info",
                         "detail": "No related docs found — may be disconnected from the graph"})
        # Missing headings (thin structure)
        if wc > 500 and len(doc.get("headings", [])) < 3:
            lint.append({"code": "flat-structure", "severity": "info",
                         "detail": f"{wc}-word doc with only {len(doc.get('headings', []))} headings"})
        # SharePoint-stale (published but local newer)
        if doc.get("sharepoint_stale"):
            lint.append({"code": "sp-stale", "severity": "warn",
                         "detail": "SharePoint copy is behind local — run sharepoint-sync"})
        doc["lint_status"] = {
            "ok": len([l for l in lint if l["severity"] == "error"]) == 0,
            "error_count": len([l for l in lint if l["severity"] == "error"]),
            "warn_count": len([l for l in lint if l["severity"] == "warn"]),
            "info_count": len([l for l in lint if l["severity"] == "info"]),
            "issues": lint,
        }

    # WS-M02 polish: orphan + contradiction counts at the index top level.
    # Orphan = active non-archived doc with zero related_docs AND zero reverse_related_docs AND word_count>200
    # (we keep short stubs out of the count — they're often callouts or placeholders by design).
    orphan_docs = [
        d for d in docs
        if not d.get("archived")
        and not d.get("related_docs")
        and not d.get("reverse_related_docs")
        and d.get("word_count", 0) > 200
        and d.get("source") not in ("wiki-callouts", "wiki-meetings", "wiki-meta")
    ]
    # Contradiction = any doc with a "warn"-level lint issue (excluding sp-stale since that's sync debt, not content).
    contradiction_docs = [
        d for d in docs
        if any(l["severity"] == "warn" and l["code"] != "sp-stale" for l in d.get("lint_status", {}).get("issues", []))
    ]
    print(f"  {len(orphan_docs)} orphaned docs | {len(contradiction_docs)} docs with content warnings")

    # Build tag index (active docs only)
    tag_counts = build_tag_index(active_docs)
    print(f"  {len(tag_counts)} unique tags across all docs")

    # Counts exclude archived docs AND group members (show unique only)
    unique_docs = [d for d in active_docs if not d.get("group_key") or d.get("group_role") == "latest"]
    cat_counts = Counter(d["category"] for d in unique_docs)
    status_counts = Counter(d["status"] for d in unique_docs if d["status"])
    market_counts = Counter(m for d in unique_docs for m in d["markets"])
    topic_counts = Counter(d["primary_topic"] for d in unique_docs if d["primary_topic"])
    doctype_counts = Counter(d["doc_type"] for d in unique_docs if d["doc_type"])
    # SharePoint publication stats (agent-created articles only — others don't sync to SP)
    ac_for_sp = [d for d in unique_docs if d["source"].startswith("wiki-") and d["source"] not in ("wiki-reviews", "wiki-meta")]
    sp_published = sum(1 for d in ac_for_sp if d.get("published"))
    sp_stale = sum(1 for d in ac_for_sp if d.get("sharepoint_stale"))
    sp_local_only = len(ac_for_sp) - sp_published

    # Build group summary for UI
    group_summary = {}
    for gk, gdocs in groups.items():
        latest = next((d for d in gdocs if d.get("group_role") == "latest"), gdocs[0])
        group_summary[gk] = {
            "count": len(gdocs),
            "latest_id": latest["id"],
            "latest_title": latest["title"],
        }

    # WS-M03: ingest_log — recent additions/updates scraped from git + filesystem mtimes.
    # Gives the "what landed recently" strip at the top of wiki-search.
    ingest_log = build_ingest_log(docs, limit=20)

    # WS-M05: demand_log — parse wiki-demand-log.md if present. File tracks topics/questions that
    # agents or humans searched for but couldn't find an article on. Format: tolerant — bullets
    # starting with "- " or YAML-ish lines get picked up.
    demand_log = load_demand_log()

    # WS-M11: agent_drafts — scan context/intake/ for agent-authored draft markdown that could
    # be promoted to the wiki. Emit shape matching what wiki-search.html expects.
    agent_drafts = scan_agent_drafts()

    # Bucket C #027 — category_mean_word_count: per-category mean + p50/p90 word counts so
    # consumers can render a bullet chart for "this doc's length vs category norm".
    # Skip archived + near-empty stub docs (<50 words) so the mean reflects meaningful articles.
    cat_lengths = {}
    for d in unique_docs:
        if d.get("archived"):
            continue
        wc = d.get("word_count", 0)
        if wc < 50:
            continue
        cat = d.get("category", "Uncategorized")
        cat_lengths.setdefault(cat, []).append(wc)
    category_word_stats = {}
    for cat, lens in cat_lengths.items():
        slens = sorted(lens)
        n = len(slens)
        mean = sum(slens) / n if n else 0
        p50 = slens[n // 2] if n else 0
        p90 = slens[min(n - 1, int(n * 0.9))] if n else 0
        category_word_stats[cat] = {
            "n": n,
            "mean": round(mean),
            "p50": p50,
            "p90": p90,
        }

    # Bucket C #028 — last_agent_counts: dashboard-wide rollup of per-agent authored doc counts.
    last_agent_counts = Counter(d.get("last_agent", "unknown") for d in unique_docs if not d.get("archived"))

    index = {
        "generated": datetime.now().isoformat(),
        "total_docs": len(unique_docs),
        "total_all": len(active_docs),
        "total_archived": len(archived_docs),
        "skipped": skipped,
        "categories": dict(cat_counts),
        "statuses": dict(status_counts),
        "markets": dict(market_counts),
        "topics": dict(topic_counts),
        "doc_types": dict(doctype_counts),
        "sharepoint": {
            "cache_generated": SP_GENERATED,
            "published": sp_published,
            "local_only": sp_local_only,
            "stale": sp_stale,
            "total_agent_created": len(ac_for_sp),
        },
        "tags": tag_counts,
        "groups": group_summary,
        # WS-M02/M09 — content-quality surfaces
        "orphan_count": len(orphan_docs),
        "orphans": [{"id": d["id"], "title": d["title"], "category": d["category"], "word_count": d.get("word_count", 0)} for d in orphan_docs[:50]],
        "contradiction_count": len(contradiction_docs),
        "contradictions": [
            {
                "id": d["id"],
                "title": d["title"],
                "issues": [l["code"] for l in d["lint_status"]["issues"] if l["severity"] == "warn" and l["code"] != "sp-stale"],
            }
            for d in contradiction_docs[:50]
        ],
        # WS-M03 — recent ingest strip
        "ingest_log_entries": ingest_log,
        # WS-M05 — demand-gap panel
        "demand_log_entries": demand_log,
        # WS-M11 — agent-authored drafts awaiting promotion
        "agent_drafts": agent_drafts,
        # Bucket C #027 — per-category word-count stats for canonical-length bullet chart
        "category_word_stats": category_word_stats,
        # Bucket C #028 — per-agent authored doc count rollup
        "last_agent_counts": dict(last_agent_counts),
        "documents": docs,
    }

    OUTPUT.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"Indexed {len(unique_docs)} unique + {len(active_docs)-len(unique_docs)} grouped + {len(archived_docs)} archived documents ({skipped} skipped)")
    print(f"Categories: {dict(cat_counts)}")
    print(f"Markets: {dict(market_counts)}")
    print(f"Topics: {dict(topic_counts)}")
    print(f"Tags: {len(tag_counts)} unique")
    print(f"Groups: {len(group_summary)} ({grouped_count} docs grouped)")
    print(f"SharePoint: {sp_published} published / {sp_local_only} local-only / {sp_stale} published-stale (cache: {SP_GENERATED or 'MISSING'})")
    print(f"Doc body files: {DOCS_DIR}")
    print(f"Output: {OUTPUT}")

    # Write human-readable meta index
    try:
        md_total, md_pub, md_stale = write_wiki_index_md(docs, SP_GENERATED)
        print(f"Wiki index .md: {WIKI_INDEX_MD} ({md_total} articles, {md_pub} published, {md_stale} stale)")
    except Exception as e:
        print(f"Warning: failed to write wiki-index.md: {e}")


if __name__ == "__main__":
    main()
