#!/usr/bin/env python3
"""Parse Google Ads change history report into flat keyword-level rows."""
import csv
import re
import sys

INPUT = sys.argv[1] if len(sys.argv) > 1 else "shared/uploads/sheets/Change history report (1).csv"
OUTPUT = INPUT.rsplit(".", 1)[0] + " - parsed.csv"

# Read raw file
with open(INPUT, "rb") as f:
    raw_bytes = f.read()
# Detect encoding
for enc in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "latin-1"):
    try:
        raw = raw_bytes.decode(enc)
        break
    except (UnicodeDecodeError, UnicodeError):
        continue

# The file is tab-delimited with quoted multi-line cells.
# Header row: Date & time | User | Campaign | Ad group | Changes
# We'll use csv.reader with tab delimiter.
lines = raw.splitlines()

# Skip the first two header lines (report title + date range)
data_start = None
for i, line in enumerate(lines):
    if line.startswith("Date & time"):
        data_start = i
        break

if data_start is None:
    print("Could not find header row")
    sys.exit(1)

# Re-join from header onward and parse as TSV
tsv_text = "\n".join(lines[data_start:])
reader = csv.reader(tsv_text.splitlines(), delimiter="\t")
header = next(reader)

# Regex to extract keyword changes from the Changes cell
# Pattern: [keyword] or "keyword": final URL changed from <url> to <url>
change_re = re.compile(
    r'([\[\"][^\]\"]+[\]\"]):\s*final URL changed from\s+(https?://\S+)\s+to\s+(https?://\S+)'
)

rows = []
for row in reader:
    if len(row) < 5:
        continue
    date, user, campaign, ad_group, changes = row[0], row[1], row[2], row[3], row[4]
    for m in change_re.finditer(changes):
        keyword, before_url, after_url = m.group(1), m.group(2), m.group(3)
        if keyword.startswith("["):
            match_type = "Exact match"
        elif keyword.startswith('"'):
            match_type = "Phrase match"
        else:
            match_type = "Broad match"
        rows.append([date, campaign, ad_group, keyword, match_type, before_url, after_url])

# Write output
with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Campaign", "Ad Group", "Keyword", "Criterion Type", "Before Final URL", "After Final URL"])
    w.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUTPUT}")
