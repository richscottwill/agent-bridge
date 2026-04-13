---
title: "Polaris Brand LP Rollout Timeline"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0106 | duck_id: comms-polaris-rollout-timeline -->

> **⚠️ ARCHIVED — 2026-04-04. Replaced by polaris-rollout-status. Do not update this file.**

---
title: Polaris Brand LP Rollout Timeline
status: archived
audience: amazon-internal
level: 1
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: AEM translations delivered, weblab results, market go-live dates
---

# Polaris Brand LP Rollout Timeline

---

## Overview

Worldwide rollout of Polaris Brand landing pages for Paid Search. US switched 3/24. Weblab dial-up targeting April 6-7. AEM translations in progress.

## Timeline

| Market | Priority | AEM Status | Page Status | Weblab | Target Live | Owner |
|--------|----------|------------|-------------|--------|-------------|-------|
| US | — | N/A | ✅ Switched 3/24 (Stacey) | Dial-up Apr 6-7 | Live | Stacey |
| AU | 1 | Submitted 3/19, due 3/26 | Pending translation | Pending | Apr 2026 | Richard/Alexis |
| MX | 2 | Submitted 3/19, due 3/26 | Pending translation | Pending | Apr 2026 | Richard/Lorena |
| DE | 3 | Andrew recommended | Pending | Pending | Apr-May 2026 | Andrew |
| UK | 4 | English (no translation) | Pending | Pending | Apr-May 2026 | Andrew |
| JP | 5 | Submitted 3/19, due 3/26 | Pending translation | Pending | May 2026 | York Chen |
| FR | 6 | Andrew recommended | Pending (ops ticket ~3/24) | Pending | May-Jun 2026 | Andrew |
| IT | 7 | Pending EU5 ops ticket | Pending | Pending | Jun 2026 | Andrew |
| ES | 8 | Pending EU5 ops ticket | Pending | Pending | Jun 2026 | Andrew |
| CA | 9 | Submitted 3/19, due 3/26 | Pending translation | Pending | May 2026 | Richard |
| US-ES | 10 | Alex + Yun coordinating | noindex/nofollow | N/A | TBD | Yun |

US is done. AU/MX/JP/CA translations are the immediate blocker (due 3/26). EU5 is blocked by the ops ticket. The critical path is AEM → page build → weblab → go-live.

## Key Dependencies

- Alex AEM translations: AU/MX/JP/CA due 3/26
- EU5 AEM: blocked by ops ticket (est. 3/24)
- Weblab setup: needs Taskei ticket per market
- Do-no-harm approach: minimal localization, follow US template (Brandon confirmed)

## Success Criteria

- Per-market weblab: 45% CP improvement threshold, rollback at 35%
- JP: test without intake form (Richard's proposal)
- Measurement: pre/post analysis per market

## Decisions Made

- Brandon priority order: AU > MX > DE > UK > JP > FR > IT > ES > CA > US-ES
- Do-no-harm: minimal localization, follow US template
- AU: full switch (Lena's call, no 50/50 split)

## Alex's Asana Task

PS Polaris Brand pages update WW — 6-step rollout per geo. Alex tracking in Asana.


## Sources
- US switched 3/24 (Stacey) — source: ~/shared/context/active/current.md → Active Projects → Polaris Brand LP Rollout
- Brandon priority order — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout (3/20 sync)
- Weblab dial-up Apr 6-7 — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout
- Alex AEM translations due 3/26 — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout
- EU5 AEM blocked by ops ticket — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout
- Do-no-harm approach, minimal localization — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout (Brandon confirmed)
- AU full switch (Lena's call) — source: ~/shared/context/body/brain.md → D4: AU Landing Page
- JP test without intake form — source: ~/shared/context/body/memory.md → Dwayne meeting dynamic (3/24)
- Success threshold 45% CP, rollback 35% — source: ~/shared/context/body/eyes.md → Predicted QA → Q4
- Alex Asana task — source: ~/shared/context/body/memory.md → Alex VanDerStuyf relationship entry

<!-- AGENT_CONTEXT
machine_summary: "Worldwide rollout timeline for Polaris Brand landing pages. US live 3/24. AEM translations due 3/26. Weblab Apr 6-7. Brandon priority: AU>MX>DE>UK>JP>FR>IT>ES>CA>US-ES. Critical path: AEM translations → page build → weblab → go-live."
key_entities: ["Polaris", "Brand LP", "AEM", "weblab", "Stacey", "Alex", "Andrew", "York Chen", "Brandon Munday"]
action_verbs: ["translate", "build", "switch", "test", "dial-up"]
update_triggers: ["AEM translations delivered", "weblab results available", "market goes live", "ops ticket resolved"]
-->
