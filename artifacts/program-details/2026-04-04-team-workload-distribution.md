---
title: Team Capacity & Workload Distribution
status: DRAFT
audience: amazon-internal
level: N/A
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-04
update-trigger: team changes, market ownership shifts, new initiatives assigned, quarterly planning
tags: team, capacity, workload, brandon, operations
---

# Team Capacity & Workload Distribution

> Who is doing what across 10 markets. Designed for Brandon's team management — identifying coverage gaps, overload risks, and delegation opportunities.

---

## Team Overview

AB Paid Search operates across 10 markets with a core team of 7 people under Brandon Munday (L7). The team is lean by design — efficiency through OCI, standardized processes, and cross-market playbooks is how 7 people cover 10 markets. But lean also means that single-point-of-failure risks are real, and workload distribution is uneven.

| Team Member | Level | Primary Domain | Markets Covered |
|------------|-------|---------------|-----------------|
| Richard Williams | L5 | Testing methodology, AU/MX hands-on | AU, MX (hands-on), WW (testing) |
| Andrew Wirtz | L5 | DG/Algorithmic Ads, EU lead | UK, DE, FR, IT, ES |
| Stacey Gu | L6 | OCI/Bidding, US lead | US (primary), CA (OCI) |
| Yun-Kang Chu | L6 | Modern Search/Adobe | WW (analytics), MX (support) |
| Dwayne Palmer | L6 | MCS/Website | WW (landing pages, Polaris) |
| Adi Thakur | L5 | Landing Pages/UX | WW (LP testing, UX) |
| Peter Ocampo | L6 | Mobile App | WW (app marketing) |

---

## Market Coverage Map

| Market | Primary Owner | Backup | OCI Status | Key Stakeholder | Risk Level |
|--------|-------------|--------|------------|-----------------|------------|
| US | Stacey | Andrew | 100% | Brandon | LOW |
| UK | Andrew | Richard | 100% | - | LOW |
| DE | Andrew | Richard | 100% | - | LOW |
| FR | Andrew | - | 100% | - | MEDIUM (no backup) |
| IT | Andrew | - | 100% | - | MEDIUM (no backup) |
| ES | Andrew | - | 100% | - | MEDIUM (no backup) |
| CA | Stacey (OCI) / Richard | - | E2E (4/7 target) | - | LOW |
| JP | York Chen* | Richard | 100% | - | MEDIUM (York returning) |
| AU | Richard | - | Not started | Lena Zak, Alexis Eck | HIGH (no backup, demanding stakeholder) |
| MX | Richard | - | Not started | Lorena Alvarez Larrea | MEDIUM (new stakeholder) |

*York Chen is not a Brandon direct but owns JP PS operations.

### Coverage Gaps

**Andrew covers 5 markets with no backup on 3 of them.** If Andrew is OOO, FR/IT/ES have no coverage. UK and DE have Richard as backup, but FR/IT/ES do not. This is the team's biggest single-point-of-failure risk on the market coverage side.

**Richard covers AU and MX hands-on with no backup on either.** AU is particularly high-risk because Lena Zak is the most demanding stakeholder in the portfolio — she expects weekly CPA reviews and data-forward responses. If Richard is OOO, there is no one who can cover AU at the level Lena expects.

**JP has a returning owner.** York Chen returned from paternity leave on 3/22. JP is underperforming (-14% vs OP2) due to the MHLW structural gap. York needs to ramp back up quickly, and the OCI dial-up (3/31) adds complexity.

---

## Workload Distribution by Function

### Campaign Management (Weekly)

| Function | Owner | Time Estimate | Frequency |
|----------|-------|--------------|-----------|
| US campaign monitoring | Stacey | 3-4 hrs/wk | Weekly |
| EU5 campaign monitoring | Andrew | 5-6 hrs/wk | Weekly |
| AU campaign management | Richard | 4-5 hrs/wk | Weekly |
| MX campaign management | Richard | 2-3 hrs/wk | Weekly |
| CA/JP campaign monitoring | Stacey/York | 2-3 hrs/wk each | Weekly |

### Reporting (Weekly/Monthly)

| Report | Owner | Backup | Time | Frequency |
|--------|-------|--------|------|-----------|
| WBR Callouts (all markets) | Dwayne | Richard | 3-4 hrs | Weekly |
| MBR Summary | Richard | - | 4-6 hrs | Monthly |
| Kingpin Goals | Richard | - | 1-2 hrs | Monthly |
| R&O Budget Input | Richard | - | 30-60 min | Per cycle |
| AU Weekly CPA Review | Richard | - | 1-2 hrs | Weekly |

### Initiative Ownership

| Initiative | Primary | Support | Status |
|-----------|---------|---------|--------|
| OCI Rollout (WW) | Richard | Stacey (US), Andrew (EU) | 7/10 at 100% |
| Polaris LP Rollout | Dwayne/Stacey | Richard (AU/MX), Andrew (EU) | US live, WW in progress |
| Ad Copy Testing | Andrew (EU) | Richard (methodology) | UK complete, scaling |
| AI Max Test | Richard | Stacey (US execution) | Overdue (test design) |
| Email Overlay WW | Richard | - | Blocked (Vijay) |
| F90 Lifecycle | Richard | - | Pending (match rate) |
| Project Baloo | TBD | Richard (cost analysis) | Early access |
| Testing Approach Doc | Richard | - | Not started |

---

## Overload Assessment

### Richard Williams — HIGH Overload Risk

Richard's portfolio is the broadest on the team: 2 hands-on markets (AU, MX), WW testing methodology ownership, 4 initiative leads (AI Max, email overlay, F90, Testing Approach doc), monthly reporting (MBR, Kingpin, R&O), and the AU weekly CPA review that Lena demands.

Estimated weekly time allocation:
- AU hands-on: 4-5 hrs
- MX hands-on: 2-3 hrs
- Reporting (WBR backup, MBR, Kingpin, R&O): 3-5 hrs
- Initiative work (OCI, AI Max, email overlay, F90): 5-8 hrs
- Admin (invoices, POs, email triage): 2-3 hrs
- Strategic artifacts (Testing Approach, wiki): 0 hrs (this is the problem)

Total: ~16-24 hrs of committed work before any strategic output. The Testing Approach doc — the single most important deliverable — has zero allocated time because everything else fills the week first. This is the structural problem behind the Level 1 gate failure.

### Andrew Wirtz — MEDIUM Overload Risk

Andrew covers 5 EU markets plus ad copy testing leadership. His workload is high but more execution-focused (campaign monitoring, ad copy rollout) than strategic. The risk is coverage breadth — if any EU market has an issue while Andrew is focused on ad copy testing, response time suffers.

### Stacey Gu — LOW Overload Risk

Stacey owns the largest market (US) but has the most mature infrastructure (OCI at 100%, Polaris live). Her workload is steady-state monitoring plus CA OCI rollout support. She has capacity for AI Max test execution when the design is ready.

---

## Delegation Opportunities

| Task | Current Owner | Potential Delegate | Effort Saved | Blocker |
|------|-------------|-------------------|-------------|---------|
| Invoice/PO processing | Richard | Lorena (MX) or finance | 2-3 hrs/wk | Need to decide MX invoice owner |
| WBR callout drafting | Dwayne/Richard | Dashboard ingester (automated) | 2-3 hrs/wk | Ingester built, adoption in progress |
| R&O budget input | Richard | Budget forecast helper (tool) | 30-60 min/cycle | Blocked on OP2 plan numbers |
| AU weekly CPA report | Richard | Automated dashboard | 1-2 hrs/wk | Dashboard not yet built |
| Campaign link generation | Richard | Campaign link generator (tool) | 30-60 min/promo | Tool not yet built |

The delegation opportunities total 6-9 hours per week if all tools and handoffs are completed. That is the difference between zero strategic output and 1-2 days per week for the Testing Approach doc and other Level 1 artifacts.

---

## Recommendations for Brandon

1. **Assign FR/IT/ES backup coverage.** Andrew covering 5 markets with no backup on 3 is a risk. Richard or Adi could serve as emergency backup for EU3 with minimal ramp-up (the markets are small and follow the same playbook as UK/DE).

2. **Protect Richard's strategic time.** The Testing Approach doc will not ship unless Richard has dedicated blocks. The morning routine and calendar blocking hooks exist for this purpose, but they need to be enforced. Brandon's explicit support ("Richard is heads-down on the Kate doc this week") would help.

3. **Decide MX invoice ownership.** Carlos transitioned to CPS on 3/17. MX invoices have no owner. This is a small task but it is blocking — invoices cannot be submitted without a designated owner. Lorena or Richard needs to own it.

4. **Monitor JP recovery.** York is back but JP is -14% vs OP2 with OCI just going live. The first 4-6 weeks of JP OCI data will determine whether the MHLW gap is recoverable. Brandon should check in with York at the next team sync.

---

## Sources
- Team structure (Brandon's directs) — source: ~/shared/context/active/org-chart.md
- Market ownership — source: ~/shared/context/body/hands.md -> Recurring Execution Work
- Initiative ownership — source: ~/shared/context/body/hands.md -> Core tasks + eyes.md -> Active initiatives
- Richard's time allocation — source: ~/shared/context/body/device.md -> Operational Time Estimates
- Invoice/PO blocker — source: ~/shared/context/body/hands.md -> Admin tasks
- Testing Approach doc status — source: ~/shared/context/body/memory.md -> Active Projects
- Andrew EU5 coverage — source: ~/shared/context/body/memory.md -> Andrew Wirtz
- Lena stakeholder demands — source: ~/shared/context/body/memory.md -> Lena Zak

<!-- AGENT_CONTEXT
machine_summary: "Team capacity analysis for AB Paid Search. 7 people covering 10 markets. Key risks: Andrew covers 5 EU markets with no backup on FR/IT/ES. Richard is overloaded (2 hands-on markets + 4 initiative leads + reporting = 16-24 hrs/wk before strategic work). Testing Approach doc has 0 allocated time. Delegation opportunities total 6-9 hrs/wk if tools and handoffs complete. Recommendations: assign EU3 backup, protect Richard's strategic time, decide MX invoice owner, monitor JP recovery."
key_entities: ["Richard Williams", "Andrew Wirtz", "Stacey Gu", "Dwayne Palmer", "Adi Thakur", "Yun-Kang Chu", "Peter Ocampo", "Brandon Munday", "Lena Zak"]
action_verbs: ["delegate", "protect", "assign", "monitor", "decide"]
update_triggers: ["team changes", "market ownership shifts", "new initiatives assigned", "quarterly planning"]
-->
