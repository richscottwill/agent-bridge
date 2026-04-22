#!/usr/bin/env python3
"""
refresh-all.py — Run the full dashboard refresh pipeline in sequence.

Steps:
  1. extract-ly-data.py  → _Daily_Data sheet in ps-forecast-tracker.xlsx
  2. refresh-forecast.py → data/forecast-data.json
  3. refresh-callouts.py → data/callout-data.json

Usage: python3 refresh-all.py
"""
import subprocess, sys, time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
STEPS = [
    ("Extract daily data", "extract-ly-data.py"),
    ("Write ps.forecasts → xlsx", "update-forecast-tracker.py"),
    ("Refresh forecast JSON", "refresh-forecast.py"),
    ("Refresh callout JSON", "refresh-callouts.py"),
    ("Generate command center JSON", "generate-command-center.py"),
    ("Refresh body system JSON", "refresh-body-system.py"),
    ("Refresh state files JSON", "refresh-state-files.py"),
    ("Refresh goals JSON", "refresh-goals.py"),
    ("Refresh contributions JSON", "refresh-contributions.py"),
    ("Build wiki search index", "build-wiki-index.py"),
    ("Generate per-section freshness manifest", "generate-section-freshness.py"),
]

def main():
    print("=" * 50)
    print("Dashboard Refresh Pipeline")
    print("=" * 50)
    start = time.time()

    for i, (label, script) in enumerate(STEPS, 1):
        path = SCRIPT_DIR / script
        if not path.exists():
            print(f"\n[{i}/{len(STEPS)}] SKIP: {script} not found")
            continue
        print(f"\n[{i}/{len(STEPS)}] {label}")
        print("-" * 40)
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(SCRIPT_DIR),
            capture_output=False,
        )
        if result.returncode != 0:
            print(f"\nERROR: {script} failed with exit code {result.returncode}")
            sys.exit(1)

    elapsed = time.time() - start
    print(f"\n{'=' * 50}")
    print(f"Pipeline complete in {elapsed:.1f}s")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    main()
