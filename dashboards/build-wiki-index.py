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
import json, re, os, sys, hashlib
from pathlib import Path
from datetime import datetime
from collections import Counter

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
OUTPUT = Path(__file__).parent / "data" / "wiki-search-index.json"
DOCS_DIR = Path(__file__).parent / "data" / "wiki-docs"

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
    """Extract YAML-like frontmatter from markdown."""
    fm = {}
    if not text.startswith("---"):
        return fm, text
    end = text.find("---", 3)
    if end == -1:
        return fm, text
    block = text[3:end].strip()
    body = text[end + 3:].strip()
    if body.startswith("---"):
        end2 = body.find("---", 3)
        if end2 != -1:
            block2 = body[3:end2].strip()
            body = body[end2 + 3:].strip()
            for line in block2.split("\n"):
                m = re.match(r'^(\w[\w\-]*)\s*:\s*(.+)', line)
                if m:
                    fm[m.group(1).strip()] = m.group(2).strip().strip('"').strip("'")
    for line in block.split("\n"):
        m = re.match(r'^(\w[\w\-]*)\s*:\s*(.+)', line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip().strip('"').strip("'")
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

    # Build group summary for UI
    group_summary = {}
    for gk, gdocs in groups.items():
        latest = next((d for d in gdocs if d.get("group_role") == "latest"), gdocs[0])
        group_summary[gk] = {
            "count": len(gdocs),
            "latest_id": latest["id"],
            "latest_title": latest["title"],
        }

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
        "tags": tag_counts,
        "groups": group_summary,
        "documents": docs,
    }

    OUTPUT.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"Indexed {len(unique_docs)} unique + {len(active_docs)-len(unique_docs)} grouped + {len(archived_docs)} archived documents ({skipped} skipped)")
    print(f"Categories: {dict(cat_counts)}")
    print(f"Markets: {dict(market_counts)}")
    print(f"Topics: {dict(topic_counts)}")
    print(f"Tags: {len(tag_counts)} unique")
    print(f"Groups: {len(group_summary)} ({grouped_count} docs grouped)")
    print(f"Doc body files: {DOCS_DIR}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
