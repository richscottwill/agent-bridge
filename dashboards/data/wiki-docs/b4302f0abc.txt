# MPE Owner Operations Runbook

**Version**: v1 skeleton | **Last updated**: 2026-04-22 | **Owner**: Richard Williams
**Purpose**: Everything you need to use and maintain the Market Projection Engine (MPE) without reading code. One file to rule them all.

**Status**: This is the Phase 0 skeleton (Task 0.4). It gets filled out as each phase completes. Task 4.4 finalizes it after hooks and refit are wired.

---

## Daily Use (2-5 minutes)

1. **Open the tool**:
   - Kiro dashboard → "Projections" tab, OR
   - SharePoint: `Kiro-Drive/Artifacts/strategy/projection-engine.html` (standalone)

2. **Pick scope**:
   - Single market (any of the 10) for market-specific conversation
   - NA / EU5 / WW for regional rollup

3. **Pick time period**: Week, Month, Quarter, Year, Multi-Year (1 or 2 years)

4. **Pick target mode**:
   - Spend → fix total spend, compute regs and ieCCP
   - ieCCP → fix ie%CCP target, compute spend and regs (hidden for AU)
   - Regs → fix registration target, compute spend and ieCCP

5. **Adjust sliders** or click a preset (Conservative / Moderate / Aggressive / Placement-Persists / Placement-Decays / Base-Case)

6. **Read the output**:
   - Summary card: totals and 70% credible interval
   - ie%CCP gauge: current vs target
   - Charts: regs/spend over time with CI bands, Brand vs NB stacked
   - Warnings: yellow = attention, red = action needed
   - Every number has an "Explain this" tooltip

7. **Copy the narrative** to clipboard for email, Slack, or WBR callout

8. **Save the projection** if it's one you want to recall later

**Pro tip**: On first open, click the "MX 4/22 Demo" preset. It reproduces the exact pressure-test conversation from 2026-04-22 in under 90 seconds.

---

## Weekly Check (30 seconds)

Look at the top banner: "Parameters current as of {date}."

- If the date is within the quarterly cadence: green, nothing to do.
- If stale: yellow banner with "run the refit hook" link. Follow it.
- Any red warnings in the warnings panel? Click "Explain" — it tells you what to do.

---

## Quarterly Refit (15-20 minutes, once per quarter)

This is the only regular maintenance. It keeps numbers current.

**Steps**:

1. In Kiro chat or terminal: `kiro hook run mpe-refit`
2. The hook automatically:
   - Audits data quality for all 10 markets (`data_audit.py`)
   - Refits elasticity, seasonality, YoY trends, CPCs for each market
   - Checks for anomalies (>3 SD from trailing 4 quarters)
   - Produces a 1-page report at `shared/dashboards/data/refit-reports/{today}.md`
   - Prompts you: "Any new regime changes since last quarter?"
3. Answer the regime prompt. If yes, describe the event in plain English; the agent adds it to `ps.regime_changes`.
4. Review the refit report. Look for:
   - Green = all good
   - Yellow = "Review this parameter" (usually small, approve with a click)
   - Red = "ACTION REQUIRED" (anomaly or MAPE regression >5pp — tag it, decide)
5. Approve or reject flagged changes one by one (or tell Kiro "approve all except JP NB").
6. Refit report is automatically pushed to SharePoint under `Kiro-Drive/system-state/mpe-refits/`.

**Rollback if something looks wrong after refit**:
- Tell Kiro: "Roll back the {market} {parameter} to the previous version."
- Kiro flips `is_active = FALSE` on the new row and `is_active = TRUE` on the prior version in `ps.market_projection_params`.
- Tell stakeholders: "We rolled back to the previous quarterly parameters — numbers match what we used before the refit."

---

## "Something Looks Wrong" Diagnostic (no code required)

1. Check the freshness banner. If stale, run the refit hook.
2. Hover the suspicious number — "Explain this" shows formula, data range, fallback status.
3. If it says "Using regional fallback — data limited": normal for any market below 80 clean weeks. Number is trustworthy but CI is wider.
4. If solver says "INFEASIBLE — binding constraint: {parameter}": lower your target or increase the constraint's tolerance.
5. Still stuck? Run `kiro hook run mpe-acceptance-core`. Paste the output into Kiro chat: "Help me understand this acceptance failure."

---

## Regime Event Classification (at every refit)

Every row in `ps.regime_changes` is one of 4 classes. When the refit hook asks "any new regime changes?", use this decision tree:

| Situation | Classification | Flags |
|---|---|---|
| Market moved permanently (OCI launch stuck, CCP renegotiation, PAM pause for tax reason) | **Structural** | `is_structural_baseline=TRUE`, `active=TRUE`, `half_life_weeks` null |
| One-time spike or dip that decays (Semana Santa, outage, one-off promo) | **Transient** | `is_structural_baseline=FALSE`, `half_life_weeks` set (1-4 typically), `active=TRUE` |
| Event happened but was reverted before it stabilized (Polaris LP 2026-03-26 reverted 4/13) | **Short-term-excluded** | `is_structural_baseline=FALSE`, `half_life_weeks=0`, `active=TRUE` — exclude those weeks from fit |
| Partial-phase superseded by later event (UK OCI 25% then 100%), or draft-never-launched, or observation-only | **Excluded** | `active=FALSE` |

When unsure, flag it in the refit report as "NEEDS CLASSIFICATION" and leave it until the next refit or escalate.

---

## Adding a New Market (4-6 hours first time, settling to 2 hours)

Post-v1 activity. Templated once the pattern is established.

1. `python3 -m shared.tools.prediction.data_audit --markets {NEW}` → tells you which parameters need fitting vs fallback
2. Copy the most similar market's parameter template (MX for ieccp-bound, AU for efficiency-strategy, US for balanced, JP for brand-dominant)
3. Update 4-5 values in the registry:
   - CCPs from finance (column U)
   - `supported_target_modes` based on market strategy
   - `ieccp_target` and `ieccp_range` if applicable
   - Narrative tone
4. If the new market is below the equator, add a Southern Hemisphere hybrid handling task — see R14.9-R14.15 in requirements.md. AU is the reference implementation.
5. Run the refit hook on the new market
6. Test one projection and add to UI selector (Task 2.3 scope_selector schema)
7. Done. System treats it like any other market from then on.

---

## Leadership Demo Script (90 seconds — memorize this)

*[Finalized in Task 5.4 with live numbers before each demo]*

Draft form:

"Here's our new Market Projection Engine.

For MX at 75% ie%CCP in Q2: it projects {X} total registrations, ${Y}M spend, with a 70% credible interval of {L} to {H} regs.

The blue band shows uncertainty from the model parameters — honest ranges, not fake precision.

I can change the target live, apply a placement uplift, or switch to 2-year view. All numbers trace back to the actual negotiated CCPs from finance and our historical data.

Quarterly refit keeps it current — I just ran it {last_refit_date}.

Questions?"

---

## When to Ask for Help (Escalation)

- New regime shift that breaks the fit badly across multiple markets (major algo change, platform migration, global event)
- Solver won't converge on a realistic target
- SharePoint version stops rendering
- Adding cross-elasticity, macro scenarios, or Streamlit/Reflex (these are post-v1 features and require a new spec)

In those cases, paste the exact error banner and report into Kiro chat: "Help me fix this for the non-technical owner."

---

## File Locations (bookmark these)

- **Main tool**: Kiro dashboard "Projections" tab, or SharePoint `Kiro-Drive/Artifacts/strategy/projection-engine.html`
- **Refit reports**: `shared/dashboards/data/refit-reports/` (and SharePoint `Kiro-Drive/system-state/mpe-refits/`)
- **Data audit reports**: `shared/dashboards/data/data-audit-reports/`
- **Acceptance test reports**: `shared/dashboards/data/acceptance-test-reports/`
- **Saved projections**: `shared/dashboards/data/projections/`
- **This runbook**: `shared/wiki/agent-created/operations/mpe-owner-operations.md`
- **MX 4/22 simulation checklist**: `shared/wiki/agent-created/operations/mpe-mx-422-simulation.md` (Task 5.2)
- **Demo script**: `shared/wiki/agent-created/operations/mpe-demo-script.md` (Task 5.4)
- **Raw parameters**: DuckDB `ps.market_projection_params` (you never edit directly; refit hook writes here)
- **Regime changes**: DuckDB `ps.regime_changes` (owner confirms classification at each refit)

---

## Kiro Hooks (your maintenance spine)

| Hook | When you run it | What it does |
|---|---|---|
| `mpe-refit` | Quarterly, or ad-hoc after major regime event | Full refit for all 10 markets + anomaly check + owner-friendly report |
| `mpe-acceptance-core` | Before any demo, or after engine changes | Runs acceptance tests for all 10 markets + 3 regions |
| `mpe-parity` | Automatic — fires when you save mpe_engine.py or mpe_engine.js | Catches Python/JS drift before commit |
| `mpe-demo-prep` | 30 min before leadership demo | Full pre-demo checklist: audit, acceptance, SharePoint push, demo-script refresh |

Run any hook: `kiro hook run {name}`, or from Kiro chat: "run the {name} hook".

---

**You are not expected to understand the code.** The tool + this runbook + Kiro hooks are designed so you can operate it confidently. If anything feels confusing, the design failed — tell Kiro to simplify.
