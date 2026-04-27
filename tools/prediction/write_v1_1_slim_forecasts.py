"""
write_v1_1_slim_forecasts.py — Phase 6.5.5 — write v1.1 Slim Brand-Anchor +
NB-Residual + Locked-YTD forecasts to ps.forecasts tagged method='v1_1_slim'.

Runs as a standalone subprocess invoked from wbr_pipeline.py Stage 4b so the
mpe_fitting read-only connection and the writable one don't collide.

Writes 4 rows per market per remaining week of the year:
    registrations, cost, brand_registrations, nb_registrations

Usage:
    python3 -m prediction.write_v1_1_slim_forecasts --week 2026-W17
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta


MARKETS = ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"]


def _writable_con():
    """Open a writable MotherDuck connection. Separate from mpe_fitting's
    read-only connection; caller responsibility to close when done.
    """
    import duckdb
    import os
    token = os.environ.get("MOTHERDUCK_TOKEN",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig")
    return duckdb.connect(f"md:ps_analytics?motherduck_token={token}")


def _fetch_params(con, market):
    rows = con.execute("""
        SELECT parameter_name, value_scalar, value_json
        FROM ps.market_projection_params_current
        WHERE market = ?
    """, [market]).fetchall()
    out = {}
    for name, scalar, js in rows:
        rec = {"value_scalar": scalar, "value_json": None}
        if js is not None:
            if isinstance(js, (dict, list)):
                rec["value_json"] = js
            else:
                try:
                    rec["value_json"] = json.loads(js)
                except Exception:
                    rec["value_json"] = None
        out[name] = rec
    return out


def run(week_key: str) -> int:
    try:
        yr_str, wk_str = week_key.split("-W")
        year = int(yr_str)
        current_wk = int(wk_str)
    except Exception:
        print(f"  invalid week key {week_key}", file=sys.stderr)
        return 0

    # Pre-open a single writable connection and inject it into mpe_fitting
    # BEFORE importing brand_trajectory / locked_ytd. This prevents the
    # "same database different configuration" duckdb error.
    from prediction import mpe_fitting
    shared_con = _writable_con()
    mpe_fitting._con = shared_con   # inject; mpe_fitting._db() will return this

    from prediction.brand_trajectory import project_brand_trajectory
    from prediction.locked_ytd import project_with_locked_ytd

    jan4 = date(year, 1, 4)
    start_of_w1 = jan4 - timedelta(days=jan4.weekday())
    all_weeks = [start_of_w1 + timedelta(weeks=i) for i in range(52)]
    forward_week_schedule = [(i + 1, f"{year}-W{i+1}") for i in range(current_wk, 52)]

    # Compute all projections, then insert
    projected_rows = []
    for market in MARKETS:
        try:
            params = _fetch_params(shared_con, market)

            nb_elast_json = (params.get("nb_cpa_elasticity") or {}).get("value_json") or {}
            nb_cpa_elast = {"a": float(nb_elast_json.get("a", 0)), "b": float(nb_elast_json.get("b", 0))}
            brand_ccp = None
            if params.get("brand_ccp") and params["brand_ccp"]["value_scalar"] is not None:
                brand_ccp = float(params["brand_ccp"]["value_scalar"])
            nb_ccp = None
            if params.get("nb_ccp") and params["nb_ccp"]["value_scalar"] is not None:
                nb_ccp = float(params["nb_ccp"]["value_scalar"])

            supp = (params.get("supported_target_modes") or {}).get("value_json") or ["spend"]
            target_mode = "spend"
            target_value = 0.0
            if "ieccp" in supp:
                ie_row = params.get("ieccp_target")
                if ie_row and ie_row["value_scalar"]:
                    target_mode = "ieccp"
                    target_value = float(ie_row["value_scalar"])
            if target_mode == "spend" and target_value == 0:
                op2 = shared_con.execute("""
                    SELECT SUM(target_value) FROM ps.targets
                    WHERE market = ? AND fiscal_year = ? AND metric_name = 'cost'
                      AND period_type = 'monthly'
                """, [market, year]).fetchone()
                if op2 and op2[0]:
                    target_value = float(op2[0])

            bt = project_brand_trajectory(market=market, target_weeks=all_weeks)
            if not bt or not bt.regs_per_week:
                print(f"  {market}: no Brand trajectory — skipping")
                continue

            result = project_with_locked_ytd(
                market=market, year=year,
                target_mode=target_mode, target_value=target_value,
                nb_cpa_elast=nb_cpa_elast,
                brand_ccp=brand_ccp, nb_ccp=nb_ccp,
            )
            if not result:
                continue

            nb_spend_annual = float(result.total_nb_spend or 0)
            nb_regs_annual = float(result.total_nb_regs or 0)
            nb_week_spend = nb_spend_annual / 52.0 if nb_spend_annual else 0
            nb_week_regs = nb_regs_annual / 52.0 if nb_regs_annual else 0

            for wk_num, wk_key in forward_week_schedule:
                idx = wk_num - 1
                if idx >= len(bt.regs_per_week):
                    break
                brand_r = float(bt.regs_per_week[idx])
                brand_s = float(bt.spend_per_week[idx]) if idx < len(bt.spend_per_week) else 0
                total_r = brand_r + nb_week_regs
                total_s = brand_s + nb_week_spend
                if total_r <= 0:
                    continue
                for metric, value in [
                    ("registrations", total_r),
                    ("cost", total_s),
                    ("brand_registrations", brand_r),
                    ("nb_registrations", nb_week_regs),
                ]:
                    if value is None or value <= 0:
                        continue
                    projected_rows.append((market, wk_key, wk_num - current_wk, metric,
                                           float(value), float(value) * 0.85, float(value) * 1.15))
        except Exception as e:
            print(f"  {market}: {type(e).__name__}: {e}", file=sys.stderr)
            import traceback; traceback.print_exc()
            continue

    # Write via same shared writable conn
    forecast_date = datetime.now().strftime("%Y-%m-%d")
    written = 0
    for (market, wk_key, lead, metric, value, ci_lo, ci_hi) in projected_rows:
        shared_con.execute("""
            DELETE FROM ps.forecasts
            WHERE market = ? AND metric_name = ? AND target_period = ?
              AND method = 'v1_1_slim'
              AND (scored IS NULL OR scored = false)
        """, [market, metric, wk_key])
        shared_con.execute("""
            INSERT INTO ps.forecasts
                (market, channel, metric_name, target_period, period_type,
                 predicted_value, confidence_low, confidence_high,
                 method, forecast_date, scored, lead_weeks)
            VALUES (?, 'ps', ?, ?, 'weekly', ?, ?, ?, 'v1_1_slim', ?, false, ?)
        """, [market, metric, wk_key, value, ci_lo, ci_hi, forecast_date, lead])
        written += 1
    shared_con.close()

    print(f"  v1.1 Slim: {written} forecast rows written (method='v1_1_slim')")
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True, help="ISO week key, e.g. 2026-W17")
    args = ap.parse_args()
    n = run(args.week)
    sys.exit(0 if n > 0 else 1)


if __name__ == "__main__":
    main()
