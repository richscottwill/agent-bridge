"""
Phase 6.1.7 Python↔JS parity test for v1.1 Slim.

Runs the JS V1_1_Slim.projectWithLockedYtd against all 10 markets via node,
compares to Python output. Tolerance 10% per market for Phase 6.1 (tightening
to 1% is Phase 6.1.8 acceptance work).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SMOKE_SCRIPT = REPO_ROOT / "tools" / "prediction" / "tests" / "js_parity_smoke.js"


def _require_node():
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


@pytest.mark.skipif(not _require_node(), reason="node not available")
def test_js_smoke_runs_all_10_markets_without_error():
    """JS V1_1_Slim.projectWithLockedYtd runs for MX/US/CA/UK/DE/FR/IT/ES/JP/AU."""
    r = subprocess.run(
        ["node", str(SMOKE_SCRIPT)],
        capture_output=True, text=True, timeout=60,
        cwd=str(REPO_ROOT),
    )
    assert r.returncode == 0, f"JS smoke failed: {r.stderr}"
    # Every market line appears in output.
    for m in ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"]:
        assert f"{m}  |" in r.stdout or f"{m} |" in r.stdout, (
            f"Market {m} missing from JS smoke output:\n{r.stdout}"
        )


@pytest.mark.skipif(not _require_node(), reason="node not available")
def test_js_converges_to_75pct_for_ieccp_markets():
    """All 9 ie%CCP markets converge to 75% ± 0.5pp in JS (matches Python)."""
    r = subprocess.run(
        ["node", str(SMOKE_SCRIPT)],
        capture_output=True, text=True, timeout=60,
        cwd=str(REPO_ROOT),
    )
    assert r.returncode == 0
    lines = r.stdout.splitlines()
    for m in ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP"]:
        line = next((l for l in lines if l.startswith(f"{m}  |")), None)
        assert line, f"Missing line for {m}"
        # Extract ie%CCP from "... ie%CCP  75.00%"
        import re
        match = re.search(r"ie%CCP\s+([\d.]+)%", line)
        assert match, f"{m} ie%CCP not parseable from line: {line}"
        ieccp = float(match.group(1))
        assert abs(ieccp - 75.0) < 0.5, (
            f"{m} ie%CCP {ieccp:.2f}% not within 0.5pp of 75%: {line}"
        )


@pytest.mark.skipif(not _require_node(), reason="node not available")
def test_js_python_parity_within_10pct_all_markets():
    """Python-vs-JS total_spend delta should be within 10% per market."""
    # Collect JS outputs
    r = subprocess.run(
        ["node", str(SMOKE_SCRIPT)],
        capture_output=True, text=True, timeout=60,
        cwd=str(REPO_ROOT),
    )
    assert r.returncode == 0

    def _parse_js_line(mkt: str) -> float | None:
        for line in r.stdout.splitlines():
            if line.startswith(f"{mkt}  |"):
                # Format: "MX  | total_spend $      836,708 | total_regs    15,194 | ..."
                parts = line.split("|")
                # parts[1] = " total_spend $      836,708 "
                spend_str = parts[1].split("$")[1].strip().replace(",", "")
                return float(spend_str)
        return None

    # Collect Python outputs (not AU or JP — both are spend-only per v6 refactor)
    markets_ieccp = ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES"]
    from prediction.mpe_engine import ProjectionInputs, project
    for m in markets_ieccp:
        inputs = ProjectionInputs(
            scope=m, time_period="Y2026",
            target_mode="ieccp", target_value=0.75,
        )
        py_out = project(inputs)
        py_spend = py_out.totals["total_spend"]
        js_spend = _parse_js_line(m)
        assert js_spend is not None, f"JS did not return spend for {m}"
        delta = abs(py_spend - js_spend) / py_spend
        assert delta < 0.10, (
            f"{m}: Python ${py_spend:,.0f} vs JS ${js_spend:,.0f} "
            f"delta={delta*100:.1f}% exceeds 10%"
        )
