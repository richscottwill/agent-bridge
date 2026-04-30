# WW Testing State File — Agent Protocol

## Purpose
Program-specific parameters for the WW Paid Search Testing daily state file. Loaded by the State File Engine (`state-file-engine.md`) during AM-Backend Step 2E and EOD Step 9. This file defines WHAT to analyze; the engine defines HOW to generate and deliver.

## Activation
This protocol is loaded by the state file engine when processing market='WW Testing'. It is NOT invoked directly by hooks.

## WW Testing-Specific Analytical Parameters

### Five Workstreams
1. OCI Bidding — phased rollout across 10 markets. Measurement: seasonality-adjusted CPA baselines.
2. Modern Search (Ad Copy) — evidence-based messaging from SP study. Measurement: test/control splits.
3. Audiences & Lifecycle — Engagement channel + F90 Lifecycle. Measurement: iOPS, ROAS.
4. User Experience — Polaris Brand LP, Baloo, in-context registration. Measurement: Weblab APT, pre/post.
5. Algorithmic Ads — DG CPC, AI Max. Measurement: CPC benchmarks, incrementality.

### Key Thresholds
- OCI uplift expectation: 18–24% reg uplift (validated in US/UK/DE)
- Ad Copy confidence: HIGH requires 30+ days and meaningful volume (>500 conversions)
- Test status coverage target: 100% of active tests with written status
- Methodology: hypothesis → phased rollout → measurement → scale or stop

### OCI Status Tracking
| Market | Status | Notes |
|---|---|---|
| US | 100% | Baseline. +24% uplift, $16.7MM OPS |
| UK | 100% | +23% uplift |
| DE | 100% | +18% uplift |
| FR | 100% | Live, measuring |
| IT | 100% | Live, measuring |
| ES | 100% | Live, measuring |
| JP | 100% | Live, measuring |
| CA | On track | Apr 7 launch |
| AU | TBD | No MCC |
| MX | TBD | No MCC |

### Data Sources
- Test status: `~/shared/wiki/agent-created/testing/` (all workstream docs)
- Methodology: `~/shared/wiki/agent-created/testing/testing-methodology.md`

- Primary: DuckDB `weekly_metrics` (all markets) for WW aggregate
- OCI status: `~/shared/context/body/eyes.md` → OCI Performance section
- Testing Approach: `~/shared/wiki/agent-created/testing/testing-approach-kate-v5.md`
- WW callouts: `~/shared/wiki/callouts/ww/`
- Quip OCI Planning: https://quip-amazon.com/dSZ9AAZBXQy
- Quip Ad Copy: https://quip-amazon.com/KCY9AAYqWd2
- Quip Baloo: https://quip-amazon.com/TVY9AAomVYU
- Quip LP Testing: https://quip-amazon.com/BLP9AAhFfua

### Stakeholder Context
- Primary audience: Kate Rundell (L8 Director) — Testing Approach doc is for her
- Manager: Brandon Munday (L7) — must review Testing Approach before Kate sees it
- Team: 7-person team managing 10 markets and 12+ cross-functional partnerships
- Key partners: Google, Adobe, MCS, MarTech, Legal, Data Science, ABMA

---

## Test Inventory & Linkage

Canonical table of all active tests with their linked sources. One row per test. The daily engine iterates this table to hydrate Appendix I (Active Test Dossier) and the Loop Reporting Queue.

**Update rule:** This table is the source of truth for what counts as "active." Richard maintains it manually. The engine does not add or remove rows. When a test is killed or scaled to steady state, Richard moves the row to the Inventory Archive section at the bottom of this protocol.

**Column contract:**
- **Test name** — stable identifier. Used as the dossier block header in Appendix I.
- **Workstream** — one of: OCI Bidding, Modern Search, Audiences & Lifecycle, User Experience, Algorithmic Ads, Cross-workstream.
- **Canonical Asana GID** — primary owner task. Subtasks are pulled transitively. `[GID needed — @Richard]` is a valid placeholder; engine skips Asana hydration for that test and emits a NEEDS-ID flag to Appendix J.
- **Standing Loop?** — Y or N. Y = guaranteed bullet in the Loop Reporting Queue at the top of the state file. N = appears in Appendix I only.
- **Keywords** — pipe-separated list the engine uses for Slack/email/Hedy keyword match. Deterministic. No inference. If a test needs broader matching, add keywords here.
- **Technical refs** — weblab ID, MCM number, refmarker pattern, landing page URL, SIM ID, other identifiers. Free text. Used in the Technical block of the dossier.

| Test name | Workstream | Canonical Asana GID | Standing Loop? | Keywords | Technical refs |
|---|---|---|---|---|---|
| Polaris Brand LP weblab (WW) | User Experience | [GID needed — @Richard] | Y | Polaris \| brand LP \| ps-brand \| brand page weblab | Weblab: TBD · URL: `/cp/ps-brand` per market |
| Italy Polaris ref tag P0 | User Experience | 1214128635826241 | Y | Italy Polaris \| ref tag \| it/cp/ps-brand \| ps-brand-new | URL: business.amazon.it/it/cp/ps-brand · ref tag override · parked as `it/cp/ps-brand-new` in AEM |
| OCI CA | OCI Bidding | [GID needed — @Richard] | Y | OCI CA \| Canada OCI \| CA dial-up \| OCI Canada | MCM: TBD · Launch 4/7 · Validated by Artha 4/20 |
| Sitelink Audit/Update | Cross-workstream | 1214074477110993 | Y | Sitelink \| sitelinks \| sitelink audit | Brandon ask 4/15 · Weekly updates cadence |
| Cross-MCC learning investigation | OCI Bidding | [GID needed — @Richard] | N | cross-MCC \| MCC learning \| Sam Tangri \| Mike Babich \| data exclusion | Google MCC structure (NA vs EU) · US 4/7 + 4/13 data exclusions |
| AI Max US design | Algorithmic Ads | [GID needed — @Richard] | Y | AI Max \| AIMax \| AI-Max | Due 4/14 · Q2 2026 US pilot |
| Email overlay (WW rollout) | User Experience | [GID needed — @Richard] | Y | email overlay \| email rollout overlay | SIM/ticket: [needs Richard input] · per-market launch windows |
| In-context registration | User Experience | [GID needed — @Richard] | Y | in-context registration \| in-context reg \| ICR | Owner: Vijay/Criscut · Status: PARKED pending stakeholder cycle |
| F90 Lifecycle | Audiences & Lifecycle | [GID needed — @Richard] | Y | F90 \| F90 Lifecycle \| lifecycle program | Legal SIM: [needs ID] · Status: BLOCKED on Legal |
| UK Ad Copy Phase 2 | Modern Search | [GID needed — @Richard] | N | UK ad copy \| UK Phase 2 \| ad copy UK | Owner: Andrew · Launched 3/6 |
| IT Ad Copy | Modern Search | [GID needed — @Richard] | N | IT ad copy \| Italy ad copy \| ad copy IT | Owner: Andrew · Inconclusive (sample) |
| DG CPC testing (US) | Algorithmic Ads | [GID needed — @Richard] | N | DG CPC \| DG bid \| dynamic grouping CPC | Early · US only |
| Baloo early access | User Experience | [GID needed — @Richard] | N | Baloo \| Project Baloo \| Baloo early access | US only · Aug timeline · Launched 3/30 |

### Inventory Archive
(Tests that have been killed or scaled to steady state move here. The engine does not hydrate dossiers for archived tests.)

*(empty — no tests archived yet)*

---

## Ingestion Rules

Explicit rules the daily engine (AM-Backend Step 2E) follows when refreshing per-test state. These rules govern WHAT the engine pulls and HOW it writes.

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
### Rule 1: Link resolution per test

For each test in the Inventory (not the Archive), the engine pulls, per cycle:

1. **Asana task details**: canonical GID: name, kiro_rw, next_action_rw, due_on, modified_at, permalink. If the GID is a `[GID needed]` placeholder, skip this step and emit NEEDS-ID to Appendix J.
2. **Asana subtasks**: transitive from the canonical GID: same fields as above.
3. **SIM/ticket mentions**: last 14 days, where `author IN {Richard, Brandon, Stacey, Adi, Andrew, Dwayne, Yun-Kang, Peter, Alex VanDerStuyf, Vijay}` AND any keyword from the test's Keywords column is present in title or body.
4. **Slack messages**: last 14 days, from `signals.signal_tracker` (preferred: already ingested) or direct Slack MCP search as fallback. Match against test Keywords.
5. **Email threads**: last 14 days, from Outlook search. Match against test Keywords. Capture subject line and permalink.
6. **Hedy sessions**: last 14 days. Match by session title against test Keywords, OR by topic membership (`LP Testing`, `OCI`, `Polaris`, `Ad Copy`, `Baloo`). Prefer topic membership when available.
7. **Quip doc last-modified timestamps**: LP Testing, OCI Planning, Ad Copy, Baloo. Surface modification date only (not full content diff).

**Source selection for the dossier:** For each test's `Last 3 events` block, pick the 3 most-recent items across all sources above, ordered newest first. For each test's `Sources` block, keep the top 3 most-relevant per source category (Slack, email, Hedy).

### Rule 2 — Last action vs next milestone gate

For each test, after Rule 1 hydration:

- If the most recent event timestamp is `> 7 days ago`, flag the test **STALLED**. The dossier status verb becomes `STALLED`. Row appears in Appendix J (Staleness Report) table 1.
- If `next milestone` (from the Asana `next_action_rw` or equivalent field) is missing or has a past due date, flag the test **NEEDS-SCOPING**. Row appears in Appendix J table 2.
- A test may carry both flags simultaneously.

### Rule 3 — Standing Loop items auto-surface

Any test with `Standing Loop? = Y` in the Inventory gets a guaranteed bullet in the state file's **Loop Reporting Queue** section at the top of the doc.

Bullet format (engine-generated, rebuilt daily):

```
- [Test name] — [status verb] — Next: [next step, owner, by-when] — Sources: [inline permalink(s) to most-recent evidence]
```

If a Standing Loop test has no hydratable sources (e.g., all GIDs are placeholders and no Slack/email/Hedy matches), the bullet still appears but reads: `— Sources: per prior state file, not reverified this cycle`. This forces visibility on broken inventory rows rather than hiding them.

### Rule 4 — Freshness verification (the Polaris guardrail)

Before the engine writes a status claim about a test — "launched X," "dialed up Y," "delivered +6% CVR" — it must have at least one source citation from the last 14 days (Slack, email, Hedy, Quip, or Asana comment permalink).

- **If citation exists:** write the claim with the inline permalink in the `Last 3 events` block and the `Sources` block.
- **If no citation exists:** write the status as literal text: `"per prior state file, not reverified this cycle"`. Do not retain stale claims silently. Do not paraphrase or soften — use the exact phrase so the reader can grep for it.

This is the rule that would have caught the 2026-04-21 Polaris weblab error and the email overlay status hallucination. It is non-negotiable.

### Rule 5 — Daily rebuild, independent of metrics freshness

Per-test ingestion (Rules 1–4) runs every weekday regardless of whether `ps.metrics` has new data. Inventory inputs (Asana, Slack, email, Hedy, Quip mod-timestamps) change daily even when metrics do not. The engine's existing "skip market if ps.metrics stale" rule applies only to the State of Business narrative and metric tables — NOT to the Loop Reporting Queue, Appendix I (Dossier), or Appendix J (Staleness Report). Those three sections rebuild every AM-Backend run.

### Rule 6 — Marker discipline

The Loop Reporting Queue, Appendix I, and Appendix J are each wrapped in `<!-- AM-OWNED:* -->` marker pairs. The daily engine rewrites content inside the markers verbatim each run. No other hook writes to these sections. See `state-file-engine.md` → Field Ownership Contract.

---

## Output Schema
The agent must produce a JSON object matching the placeholder taxonomy defined in the state file. Workstream-level metrics replace market-level metrics. The per-test dossier (Appendix I) and the Loop Reporting Queue are generated from the Inventory + hydrated sources — not from a separate placeholder schema.

## Quality Gates
Before uploading to SharePoint:
1. Schema validation — all required JSON keys present
2. Test status accuracy — every test in the Inventory has a dossier block in Appendix I (or a NEEDS-ID flag in Appendix J); zero silent drops
3. Freshness verification — every status claim either carries a permalink from the last 14 days or reads "per prior state file, not reverified this cycle"
4. Standing Loop completeness — every `Standing Loop? = Y` test has a bullet in the Loop Reporting Queue
5. Weasel word scan — zero violations
6. Style replication — static sections unchanged
7. OCI status matches eyes.md source of truth

## SharePoint Upload Protocol
Handled by the State File Engine (Layer 3). See `state-file-engine.md` → Layer 3: SharePoint Durability Sync.
