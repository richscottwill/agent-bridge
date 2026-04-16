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
    "IT": [r'\bit\b', r'\bitaly\b'],
    "ES": [r'\bes\b', r'\bspain\b'],
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
    return sorted(set(markets))


def detect_topics(text):
    """Detect which topics a document covers."""
    topics = []
    lower = text[:5000].lower()
    for topic, patterns in TOPIC_PATTERNS.items():
        for p in patterns:
            if re.search(p, lower):
                topics.append(topic)
                break
    return topics


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
    if "quip-mirror" in path_str: return "quip-mirror"
    if "meetings" in path_str: return "meeting-series"
    if "state-files" in path_str: return "state-file"
    if "callouts" in path_str: return "callout"
    return "other"


def category_label(source):
    labels = {
        "wiki-testing": "Testing & Experimentation",
        "wiki-strategy": "Strategy & Frameworks",
        "wiki-markets": "Markets & Programs",
        "wiki-operations": "Operations & Best Practices",
        "wiki-reporting": "Reporting & Dashboards",
        "wiki-research": "Research & Analysis",
        "wiki-reviews": "Reviews & Evaluations",
        "wiki-meta": "Wiki System",
        "wiki-article": "Wiki Article",
        "quip-mirror": "Quip Document",
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

    if "/archive/" in rel_path:
        return None

    headings = extract_headings(body)
    snippet = make_snippet(body)
    keywords = extract_keywords(body)
    markets = detect_markets(body, rel_path)
    topics = detect_topics(body)

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
        "headings": headings[:15],
        "snippet": snippet,
        "keywords": keywords,
        "updated": fm.get("updated", fm.get("created", "")),
        "created": fm.get("created", ""),
        "word_count": len(body.split()),
        "search_text": search_text[:2000],
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

    # Build backlinks graph (keyword-overlap based)
    print("Building backlinks graph...")
    backlinks = build_backlinks(docs, min_shared=3)
    link_count = sum(len(v) for v in backlinks.values())
    print(f"  {len(backlinks)} docs have related pages ({link_count} total links)")

    # Attach related_docs to each doc
    id_to_title = {d["id"]: d["title"] for d in docs}
    for doc in docs:
        rels = backlinks.get(doc["id"], [])
        doc["related_docs"] = [
            {"id": rid, "title": id_to_title.get(rid, "?"), "shared": cnt}
            for rid, cnt in rels
        ]

    # Build tag index
    tag_counts = build_tag_index(docs)
    print(f"  {len(tag_counts)} unique tags across all docs")

    cat_counts = Counter(d["category"] for d in docs)
    status_counts = Counter(d["status"] for d in docs if d["status"])
    market_counts = Counter(m for d in docs for m in d["markets"])
    topic_counts = Counter(t for d in docs for t in d["topics"])
    doctype_counts = Counter(d["doc_type"] for d in docs if d["doc_type"])

    index = {
        "generated": datetime.now().isoformat(),
        "total_docs": len(docs),
        "skipped": skipped,
        "categories": dict(cat_counts),
        "statuses": dict(status_counts),
        "markets": dict(market_counts),
        "topics": dict(topic_counts),
        "doc_types": dict(doctype_counts),
        "tags": tag_counts,
        "documents": docs,
    }

    OUTPUT.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"Indexed {len(docs)} documents ({skipped} skipped)")
    print(f"Categories: {dict(cat_counts)}")
    print(f"Markets: {dict(market_counts)}")
    print(f"Topics: {dict(topic_counts)}")
    print(f"Tags: {len(tag_counts)} unique")
    print(f"Doc body files: {DOCS_DIR}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
