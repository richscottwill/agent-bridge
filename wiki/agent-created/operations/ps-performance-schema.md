---
title: "PS Performance Data — Source of Truth"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-20
updated: 2026-04-20
tags: [foundational, reference]
---

# PS Performance Data — Source of Truth

**One table. Four grains. Ten markets + WW aggregate. Query via pre-filtered views so you can't accidentally overcount.**

## ⚠️ Grain safety (read this first)

`ps.performance` holds daily **and** weekly **and** monthly **and** quarterly rows in the same table, keyed by `(market, period_type, period_key)`. A query without a `period_type` filter will sum rows from **every grain** and produce a 3-4x overcount.

**Rule:** always use one of the pre-filtered views:

- `ps.v_daily` — daily only (`period_type='daily'`)
- `ps.v_weekly` — weekly only (`period_type='weekly'`)
- `ps.v_monthly` — monthly only (`period_type='monthly'`)
- `ps.v_quarterly` — quarterly only (`period_type='quarterly'`)

If you must query the base table directly, always include `WHERE period_type = 'x'`.

## Shape

Every row has these key columns:

| Column | Type | Format / Example |
|---|---|---|
| `market` | VARCHAR | `'AU'`, `'MX'`, `'US'`, `'CA'`, `'JP'`, `'UK'`, `'DE'`, `'FR'`, `'IT'`, `'ES'`, `'WW'` |
| `period_type` | VARCHAR | `'daily'`, `'weekly'`, `'monthly'`, `'quarterly'` |
| `period_key` | VARCHAR | `'2026-04-14'` (daily), `'2026-W16'` (weekly), `'2026-M04'` (monthly), `'2026-Q2'` (quarterly) |
| `period_start` | DATE | First day of the period |
| `registrations` | INTEGER | Blended reg count |
| `cost` | DOUBLE | Blended spend |
| `cpa`, `cpc`, `cvr`, `ctr` | DOUBLE | Derived ratios |
| `brand_*`, `nb_*` | INTEGER/DOUBLE | Segment splits (regs, cost, cpa, clicks, cpc, cvr) |
| `ieccp` | DOUBLE | Only on weekly rows; null elsewhere |
| `source` | VARCHAR | `'AB SEM WW Dashboard_Y26 W16.xlsx'` or `'ww_rollup'` |

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
## Market codes

Ten individual markets plus one aggregate:

- **Individual**: AU, MX, US, CA, JP, UK, DE, FR, IT, ES
- **WW**: `market='WW'` = sum of the 10 markets at the matching grain and period_key. Computed by rollup after every ingest. Use this for WW-level numbers; do **not** sum the 10 markets manually (you'll drift if an analyst re-ingests a single market).

## Period keys

- **Daily**: ISO date string — `'2026-04-14'`
- **Weekly**: dashboard week label — `'2026-W16'`. The AB WW Dashboard uses **Sun–Sat** weeks, which differs from ISO calendar. Weekly rows align with the xlsx Weekly tab exactly.
- **Monthly**: `'2026-M04'` for April 2026
- **Quarterly**: `'2026-Q2'` for Q2 2026

**Internal consistency**: weekly/monthly/quarterly rows are computed by summing daily rows in the same period. Daily is the single authoritative source; all higher grains derive from it.

## Five worked examples

### 1. Current week's registrations for every market

```sql
SELECT market, registrations, cost, cpa
FROM ps.v_weekly
WHERE period_key = '2026-W16'
ORDER BY market;
```

### 2. MTD April for AU (from daily rows)

```sql
SELECT
  SUM(registrations) AS mtd_regs,
  SUM(cost) AS mtd_cost,
  ROUND(SUM(cost) / NULLIF(SUM(registrations), 0), 2) AS mtd_cpa
FROM ps.v_daily
WHERE market = 'AU'
  AND period_start BETWEEN '2026-04-01' AND '2026-04-18';
```

Or equivalently, read the month row directly:

```sql
SELECT registrations, cost, cpa FROM ps.v_monthly
WHERE market = 'AU' AND period_key = '2026-M04';
```

The monthly row reflects daily-sum math across whatever dates the xlsx currently has — so for an in-progress month it's MTD through the latest ingested day.

### 3. WoW comparison — last two weeks for WW

```sql
SELECT period_key, registrations, cost, cpa
FROM ps.v_weekly
WHERE market = 'WW' AND period_key IN ('2026-W15', '2026-W16')
ORDER BY period_key;
```

### 4. YoY — W16 this year vs last year, for US


```sql
SELECT period_key, registrations, cost, cpa
FROM ps.v_weekly
WHERE market = 'US' AND period_key IN ('2025-W16', '2026-W16')
ORDER BY period_key;
```


```sql
SELECT market, registrations, cost, cpa
FROM ps.v_quarterly
WHERE period_key = '2026-Q2'
ORDER BY market;
```

## Coverage check

If you're unsure what data is available:

```sql
SELECT market, period_type, rows, first_key, last_key
FROM ps.v_grain_coverage
WHERE market IN ('AU', 'MX', 'WW')
ORDER BY market, period_type;
```

## Refresh cadence

- Richard drops a new `AB SEM WW Dashboard_Y26 WNN.xlsx` weekly (Sunday or Monday)
- Pipeline: `python3 ~/shared/tools/prediction/wbr_pipeline.py <xlsx>` runs the full ingest + load + score + project flow and writes to `ps.performance` + views
- Standalone rebuild (full history from one xlsx): `python3 ~/shared/tools/prediction/full_rebuild_performance.py <xlsx>`
- Every ingest refreshes daily + rolls up weekly, monthly, quarterly, WW at every grain in one transaction

## Related tables

- `ps.targets` — OP2 targets by market / metric / period. Not part of this schema; referenced for "vs OP2" math.
- `ps.forecasts` — forward projections (next week, month-end, quarter-end) with credible intervals. Generated after ingest.
- `ps.callout_scores` — quality scores for weekly callouts.

## Anti-patterns

- ❌ `SELECT SUM(registrations) FROM ps.performance WHERE market='AU'` — sums daily + weekly + monthly + quarterly, overcounts ~4x. Always filter `period_type`.
- ❌ Summing 10 market monthly rows to get WW monthly — use `market='WW'` row instead, which is kept consistent.
- ❌ Using ISO week math (`date.isocalendar()`) to map a date to a weekly `period_key` — the dashboard uses Sun-Sat, ISO uses Mon-Sun, they disagree ~1 day per week. If you need week-for-a-date, read it from the xlsx daily row's `week` column during ingest, or SUM daily rows by `period_start BETWEEN` date ranges.
- ❌ Writing to `ps.performance` from a custom script without going through `wbr_pipeline.py` or `full_rebuild_performance.py` — risks grain drift. All writes should flow through one of those two entry points.
