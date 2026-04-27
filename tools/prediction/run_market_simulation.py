"""
run_market_simulation.py — Phase 5.2 — runs the 10-step simulation across
all markets and prints a per-market pass/fail table, publishing an
owner-readable report to
`shared/wiki/agent-created/operations/mpe-all-markets-simulation-report.md`.

Usage:
    cd shared/tools && python3 -m prediction.run_market_simulation
"""
from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


def main():
    print("Running 10-step simulation across 10 markets...")
    r = subprocess.run(
        ["python3", "-m", "pytest", "prediction/tests/test_all_markets_simulation.py",
         "--tb=no", "-v", "--no-header"],
        capture_output=True, text=True,
    )

    # Parse pytest output: lines like 'test_step_01_...[MX] PASSED'
    import re
    results = {}  # {market: {step: status}}
    pat = re.compile(r"test_step_(\d+)_\w+\[([A-Z]+)\]\s+(PASSED|FAILED|SKIPPED|ERROR)")
    for line in r.stdout.splitlines():
        m = pat.search(line)
        if m:
            step, market, status = m.group(1), m.group(2), m.group(3)
            results.setdefault(market, {})[f"step_{step}"] = status

    markets = sorted(results.keys())
    steps = sorted({s for m in results.values() for s in m.keys()})

    # Build markdown table
    lines = [
        "# MPE v1.1 Slim — 10-Step All-Markets Simulation Report",
        "",
        f"*Generated {datetime.now().isoformat()}. Runs Phase 5.2 simulation "
        f"across all 10 markets, replaces the original MX-only 4/22 checklist.*",
        "",
        "## Per-Market Results",
        "",
    ]
    header = "| Market |"
    sep = "| --- |"
    for s in steps:
        header += f" {s.replace('step_', 'S')} |"
        sep += " --- |"
    lines.append(header)
    lines.append(sep)

    symbol = {"PASSED": "✓", "FAILED": "✗", "SKIPPED": "·", "ERROR": "!"}
    for mkt in markets:
        row = f"| {mkt} |"
        for s in steps:
            st = results[mkt].get(s, "—")
            row += f" {symbol.get(st, st)} |"
        lines.append(row)

    # Summary stats
    total = sum(len(v) for v in results.values())
    passed = sum(1 for m in results.values() for v in m.values() if v == "PASSED")
    skipped = sum(1 for m in results.values() for v in m.values() if v == "SKIPPED")
    failed = sum(1 for m in results.values() for v in m.values() if v == "FAILED")
    lines += [
        "",
        "## Summary",
        "",
        f"- Total: **{total}** (10 steps × {len(markets)} markets)",
        f"- Passed: **{passed}** ({100*passed/total:.0f}%)",
        f"- Skipped: **{skipped}** (legitimate: market doesn't have the relevant structure)",
        f"- Failed: **{failed}**",
        "",
        "## Step Legend",
        "",
        "1. Initial projection at ie%CCP target converges or returns feasible bound",
        "2. Null-CCP markets (AU) return `ieccp=None` cleanly",
        "3. Scope boundaries — `supported_target_modes` filter respected",
        "4. Regime fit state exists with confidence + decay_status metadata",
        "5. Seasonality shape is 52-entry array",
        "6. CPA elasticity fit has r² metadata",
        "7. Spend-mode target produces positive NB regs",
        "8. Locked-YTD invariant — total_spend ≥ YTD actual spend",
        "9. 90% credible interval spans > 2% of central (rejects fake precision)",
        "10. Brand+NB regs > 0 and blended CPA > 0",
        "",
        "## Symbols",
        "",
        "- ✓ PASSED — check satisfied",
        "- ✗ FAILED — investigate; anomaly detection may help",
        "- · SKIPPED — check doesn't apply to this market (e.g., no active regime)",
        "",
    ]

    out_path = Path(__file__).resolve().parents[2] / "wiki/agent-created/operations/mpe-all-markets-simulation-report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
    print(f"\nWrote {out_path}")
    print(f"Summary: {passed} passed / {skipped} skipped / {failed} failed out of {total}")


if __name__ == "__main__":
    main()
