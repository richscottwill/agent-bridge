#!/usr/bin/env python3
"""Generate the remaining docs-to-fetch list, excluding the 3 we already have."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE.parent / "manifest.json"
ALREADY = {"IAJ9AAZJsDL", "FZQ9AARARAN", "PcT9AAjVFnR"}

m = json.load(open(MANIFEST))
docs = [
    e
    for e in m
    if e.get("doc_type") == "document"
    and e.get("source_url")
    and e.get("quip_id") not in ALREADY
]
print(f"Remaining docs to fetch: {len(docs)}")
for e in docs[:3]:
    print(e["rel_path"], e["source_url"])
