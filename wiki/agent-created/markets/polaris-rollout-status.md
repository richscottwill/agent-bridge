---
title: "Polaris WW Rollout - Current Status & Decision Log"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0324 | duck_id: program-polaris-rollout-status -->

---
title: Polaris WW Rollout - Current Status & Decision Log
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-04
update-trigger: market go-live dates, weblab results, AEM translations delivered, stakeholder decisions
tags: polaris, landing-pages, rollout, ww, brandon
---

# Polaris WW Rollout - Current Status & Decision Log

> Single source of truth for the Polaris Brand landing page rollout across all 10 markets. Tracks status, decisions, blockers, and measurement for Brandon's cross-market coordination.

---

## Executive Summary

Polaris is the next-generation landing page platform for Amazon Business Paid Search, replacing legacy MCS (Marketing Content Services) pages. The US switched on March 24 with a weblab dial-up targeting April 6-7. AU is executing a full migration (Lena's decision, no phased test). The remaining 8 markets are in various stages of AEM translation and page build.

The rollout follows Brandon's priority order: AU > MX > DE > UK > JP > FR > IT > ES > CA > US-ES. The critical path is AEM translations (5-7 business days) followed by page build followed by weblab setup. EU5 is blocked by an ops ticket for AEM access.

---

## Why Polaris Matters

Legacy MCS pages were built market-by-market with inconsistent templates, limited mobile optimization, and no standardized measurement framework. Polaris provides:

1. **Consistent template across markets.** One design system, localized per market. Reduces page build time from weeks to days.
2. **Mobile-first design.** Legacy pages were desktop-optimized. Polaris is responsive by default. Mobile traffic is growing across all markets.
3. **Weblab-ready measurement.** Polaris pages integrate with Amazon's weblab infrastructure for A/B testing. Legacy pages required manual pre/post analysis.
4. **Faster iteration.** Template changes propagate to all markets. A CTA improvement tested in US can be rolled to EU5 in days, not weeks.

The US MCS brand page template showed a 38bps conversion improvement in early testing. If this holds across markets, the compounding effect across 10 markets is significant.

---

## Current Status by Market

> This table tracks Polaris Brand LP rollout status specifically — not OCI status. For OCI status, see [OCI Execution Guide](~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md).

| Market | Priority | AEM Status | Page Status | Weblab | Target Live | Owner | Notes |
|--------|----------|------------|-------------|--------|-------------|-------|-------|
| US | - | N/A | Switched 3/24 | Dial-up Apr 6-7 | LIVE | Stacey | Reference implementation |
| AU | 1 | Submitted 3/19, delivered | Migrating | N/A (full switch) | Apr 2026 | Richard/Alexis | Lena directed full switch, no 50/50 |
| MX | 2 | Submitted 3/19, delivered | Pending build | Pending | Apr 2026 | Richard/Lorena | Spanish translation |
| DE | 3 | Andrew recommended | Pending | Pending | Apr-May 2026 | Andrew | German translation |
| UK | 4 | English (no translation) | Pending | Pending | Apr-May 2026 | Andrew | No translation needed |
| JP | 5 | Submitted 3/19, delivered | Pending build | Pending | May 2026 | York Chen | Japanese translation |
| FR | 6 | Pending EU5 ops ticket | Pending | Pending | May-Jun 2026 | Andrew | Blocked by ops ticket |
| IT | 7 | Pending EU5 ops ticket | Pending | Pending | Jun 2026 | Andrew | Blocked by ops ticket |
| ES | 8 | Pending EU5 ops ticket | Pending | Pending | Jun 2026 | Andrew | Blocked by ops ticket |
| CA | 9 | Submitted 3/19, delivered | Pending build | Pending | May 2026 | Richard | English (no translation) |
| US-ES | 10 | Alex + Yun coordinating | noindex/nofollow | N/A | TBD | Yun | Spanish US page |

---

## Decision Log

| Date | Decision | Made By | Rationale | Impact |
|------|----------|---------|-----------|--------|
| 3/13 | AU full switch (no 50/50 split) | Lena Zak | Lena overrode phased test recommendation. "Just switch it." | AU migrating without measurement baseline. Risk accepted. |
| 3/20 | Priority order: AU>MX>DE>UK>JP>FR>IT>ES>CA>US-ES | Brandon | Based on market priority and translation readiness. | Defines rollout sequence. |
| 3/20 | Do-no-harm approach: minimal localization, follow US template | Brandon | Speed over customization. Localize only what is necessary. | Reduces AEM scope per market. |
| 3/24 | US switched to Polaris | Stacey | US page ready, weblab infrastructure in place. | Reference implementation live. |
| 3/24 | JP test without intake form (proposed) | Richard | Intake form may not be relevant for JP market. | Pending York's input. |

### Key Decision: AU Full Switch

Lena's decision to skip the 50/50 phased test is a departure from the team's standard methodology (Decision Principle #4: phased rollout over full migration). Brandon is aware and has flagged Lena's pattern of reversing previously agreed decisions. The risk is that if Polaris underperforms in AU, there is no control group to compare against — the team will rely on pre/post analysis with all its confounding factors.

The W13 data shows AU CVR dropped 12% WoW, with the mid-week Polaris migration as a possible contributor. Isolating the Polaris signal from seasonal factors and the Back-to-Biz to Evergreen promo transition will be difficult without a control group.

---

## Blockers

| Blocker | Markets Affected | Owner | Status | Escalation Path |
|---------|-----------------|-------|--------|-----------------|
| EU5 AEM ops ticket | FR, IT, ES | Andrew | Pending (~3/24 estimate) | Andrew -> Brandon if not resolved by mid-April |
| Weblab setup (per market) | All non-US | MCS (Frank) | Pending page builds | Requires Taskei ticket per market |
| US-ES coordination | US-ES | Alex + Yun | In progress | Low priority (noindex/nofollow) |

The EU5 ops ticket is the primary blocker for the second half of the rollout. FR, IT, and ES cannot begin AEM translation until the ops ticket is resolved. This affects 3 of 10 markets.

---

## Measurement Framework

### Per-Market Weblab (Standard Approach)

| Metric | Success Threshold | Rollback Threshold |
|--------|------------------|-------------------|
| Conversion improvement (CP) | 45% | 35% |
| Registration volume | No degradation | >10% drop for 2+ weeks |
| Bounce rate | Improvement or flat | >20% increase |

The 45% CP improvement threshold and 35% rollback threshold were established for the US weblab. The same thresholds apply to all markets unless market-specific factors warrant adjustment.

### AU Exception (Pre/Post Analysis)

Because Lena directed a full switch without a weblab, AU measurement relies on pre/post comparison:

1. Capture 4 weeks of pre-migration performance (completed)
2. Compare post-migration performance at 2, 4, and 8 weeks
3. Adjust for known confounders: seasonality, promo transitions, CPC trends
4. Report with explicit confidence level (likely MEDIUM due to lack of control)

---

## Cross-Initiative Dependencies

| Initiative | Dependency | Impact |
|-----------|-----------|--------|
| Ad Copy Testing | New ad copy must align with Polaris LP messaging | Disconnect between ad and LP hurts CVR |
| OCI | Polaris pages must have correct conversion tracking | OCI depends on accurate conversion signals |
| Email Overlay | Overlay must work on Polaris page templates | Adobe Target implementation needs Polaris compatibility |
| Category Pages | MX Auto/Beauty pages are Polaris-based | Category page template is a Polaris variant |

---

## Alex's Asana Task

Alex VanDerStuyf is tracking the WW rollout in Asana: "PS Polaris Brand pages update WW" with a 6-step rollout per geo. Steps: (1) AEM translation submission, (2) Translation delivery, (3) Page build, (4) QA review, (5) Weblab setup, (6) Go-live.

---

## Sources
- US switched 3/24 (Stacey) — source: ~/shared/context/active/current.md -> Polaris Brand LP Rollout
- Brandon priority order — source: ~/shared/context/active/current.md -> Polaris Brand LP Rollout (3/20 sync)
- Weblab dial-up Apr 6-7 — source: ~/shared/context/active/current.md -> Polaris Brand LP Rollout
- AU full switch (Lena's decision 3/13) — source: ~/shared/context/body/brain.md -> D4: AU Landing Page
- Do-no-harm approach — source: ~/shared/context/active/current.md -> Polaris Brand LP Rollout (Brandon confirmed)
- Success threshold 45% CP, rollback 35% — source: ~/shared/context/body/eyes.md -> Predicted QA
- W13 AU CVR drop — source: ~/shared/context/body/eyes.md -> Market Health -> AU
- Alex Asana task — source: ~/shared/context/body/memory.md -> Alex VanDerStuyf
- Frank/MCS requirements — source: ~/shared/context/body/memory.md -> Frank Volinsky

<!-- AGENT_CONTEXT
machine_summary: "Polaris WW rollout status tracker. US live (3/24), weblab Apr 6-7. AU full migration (Lena's decision, no phased test). Brandon priority: AU>MX>DE>UK>JP>FR>IT>ES>CA>US-ES. EU5 blocked by AEM ops ticket. Measurement: 45% CP improvement threshold, 35% rollback. AU using pre/post analysis (no control group). W13 AU CVR -12% WoW may be partially Polaris-related. Alex tracking in Asana."
key_entities: ["Polaris", "MCS", "AEM", "weblab", "Stacey", "Alex", "Andrew", "Lena Zak", "Brandon", "Frank"]
action_verbs: ["migrate", "translate", "build", "test", "measure", "rollback"]
update_triggers: ["market go-live dates", "weblab results", "AEM translations delivered", "EU5 ops ticket resolved"]
-->
