# ps.market_constraints — Schema Reference

**Purpose:** Single source of truth for market constraints. Consumed by agents (via auto-inclusion `.md` projection), hooks, dashboards, and scripts.

**Source:** `ps.market_constraints` view in MotherDuck `ps_analytics` database.

**Refreshed by:** WBR pipeline step 8 (`shared/tools/prediction/regenerate_market_constraints.py`), which emits `~/.kiro/steering/market-constraints.md` for agent auto-inclusion. For scripts and dashboards, query the view directly — do not parse the .md file.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  ps.market_constraints (VIEW — single source of truth)      │
└─────────────────────────────────────────────────────────────┘
         ▲
         │  (joins)
         │
  ┌──────┼──────────────────────────────────────────┐
  │      │                                           │
  ▼      ▼                                           ▼
[Manual] [Auto-refreshing, weekly via WBR pipeline]  [Historical]
  ├─ ps.market_constraints_manual                    ├─ ps.regime_changes
  │   (governing_constraint, handoff, OCI, CCP,      │   (baseline + impact)
  │    next_milestone, notes — agent-editable)       │
  └─ ps.market_status (actuals)                      
     ps.forecast_tracker (projections)
     ps.targets (monthly OP2)
     ps.forecast_accuracy (hit rate)

         ▲
         │
  ┌──────┴──────────────────────────────────┐
  │  Consumers                              │
  ├─────────────────────────────────────────┤
  │ Agents → market-constraints.md (proj)   │
  │ Hooks → SELECT FROM ps.market_constraints│
  │ Dashboards → SELECT FROM view           │
  │ Scripts → SELECT FROM view              │
  └─────────────────────────────────────────┘
```

[38;5;10m> [0m## Columns[0m[0m
[0m[0m
| Column(s) | Type | Source | Refresh |[0m[0m
|---|---|---|---|[0m[0m
| `market` | VARCHAR | manual | Never |[0m[0m
| `governing_constraint`, `handoff_status`, `oci_status`, `ccp_availability`, `next_milestone`, `manual_notes` | VARCHAR | manual | Agent-edit |[0m[0m
| `manual_updated_at` | TIMESTAMP | manual | Auto on UPDATE |[0m[0m
| `manual_updated_by` | VARCHAR | manual | Agent sets on UPDATE |[0m[0m
| `latest_week` | VARCHAR | market_status | WBR pipeline weekly |[0m[0m
| `last_week_regs` | INTEGER | market_status | WBR pipeline weekly |[0m[0m
| `last_week_cost`, `last_week_cpa` | DOUBLE | market_status | WBR pipeline weekly |[0m[0m
| `next_week_predicted_regs`, `next_week_ci_low_regs`, `next_week_ci_high_regs` | DOUBLE | forecast_tracker | WBR pipeline weekly |[0m[0m
| `next_week_predicted_cost`, `next_week_ci_low_cost`, `next_week_ci_high_cost` | DOUBLE | forecast_tracker | WBR pipeline weekly |[0m[0m
| `month_op2_regs`, `month_op2_cost`, `month_op2_cpa` | DOUBLE | targets | Per OP cycle (rarely) |[0m[0m
| `hit_rate_regs`, `avg_error_regs` | DOUBLE | forecast_accuracy | WBR pipeline weekly |[0m[0m
| `structural_baseline_count` (BIGINT), `structural_baselines` (VARCHAR) | — | regime_changes | Active rows where `is_structural_baseline=true`; pipe-delimited list |[0m[0m
| `active_impact_count` (BIGINT), `active_impact_regimes` (VARCHAR) | — | regime_changes | Non-baseline active with future/null end_date; pipe-delimited with decay info |[0m[0m
| `recent_past_count` (BIGINT), `recent_past_regimes` (VARCHAR) | — | regime_changes | Non-baseline, end_date 0–90 days ago; pipe-delimited |
## How to update manual fields (agents)

Agents MAY update `ps.market_constraints_manual` when they learn of a shift. Always set `updated_at` and `updated_by`:

```sql
UPDATE ps.market_constraints_manual 
SET governing_constraint = 'New target',
    oci_status = 'Live 100% since 2026-04-21',
    updated_at = CURRENT_TIMESTAMP,
    updated_by = 'agent-name (session context)'
WHERE market = 'MX';
```

After an update, run the regenerator if the change needs to propagate to the steering file immediately (otherwise it propagates on next WBR pipeline run):

```bash
python3 ~/shared/tools/prediction/regenerate_market_constraints.py
```

## How to add a regime change

See `regime-change-taxonomy.md` in this directory for the classification. In brief:

- **Structural baseline** (LP, OCI, attribution, campaign restructure): `is_structural_baseline=true`, `half_life_weeks=NULL`, `precedent_source='structural_persistent'`. No `end_date` unless replaced.
- **Active impact** (promo, seasonal, one-off disruption): `is_structural_baseline=false`, set `half_life_weeks` (1-2 for novel, 8-12 for persistent), `precedent_source` (`'yoy_same_event'` for recurring, `'none_novel'` otherwise), set `end_date` when known.

## Consumer examples

**Hook** (daily brief — pacing check):
```python
rows = con.execute("SELECT market, last_week_regs, next_week_predicted_regs, month_op2_regs FROM ps.market_constraints").fetchall()
```

**Dashboard** (callout-writer context panel):
```sql
SELECT * FROM ps.market_constraints WHERE market = ?;
```

**Callout writer** (narrative context):
```sql
SELECT governing_constraint, structural_baselines, active_impact_regimes, recent_past_regimes,
       last_week_regs, next_week_predicted_regs, next_week_ci_low_regs, next_week_ci_high_regs
FROM ps.market_constraints WHERE market = ?;
```

## Do NOT

- Do not parse `market-constraints.md` in scripts — query the view.
- Do not write directly to `ps.market_constraints` (it's a view).
- Do not set `active=false` on baselines to "clean up" — they're the current state. Set a new baseline row and add `end_date` to the old one if the infrastructure actually changed.
