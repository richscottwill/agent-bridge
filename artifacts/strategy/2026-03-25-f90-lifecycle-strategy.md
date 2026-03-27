---
title: F90 Lifecycle Program Strategy
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: Legal SIM updates, match rate changes, ABMA partnership progress
---

# F90 Lifecycle Program Strategy

---

## Overview

F90 extends paid search beyond registration into lifecycle. Target: non-purchasing AB customers, driving 3+ purchases within 90 days of registration. Moves PS from pure acquisition to acquisition + activation.

## Target Audience

- Non-SHuMA customers who registered but haven't purchased
- Goal: 3+ purchases within 90 days
- Baseline: 31.7% → Target: 35.4%

## How It Works

1. Customer registers via paid search
2. F90 identifies non-purchasers at day 30, 60, 90
3. Targeted re-engagement via paid search (RLSA) + email
4. Measurement: purchase rate, AOV, LTV at 90 days

## Dependencies

- Legal SIMs: navigated (approved)
- ABMA partnership: Associated Accounts to boost match rate (13% → 30%)
- Engagement channel: created and operational
- Data Science: customer segmentation for targeting

## Cross-Functional Partners

| Team | Role |
|------|------|
| ABMA | Associated Accounts, match rate improvement |
| Legal | SIM approval for targeting existing customers |
| Data Science | Customer segmentation, LTV modeling |
| MCS | Lifecycle page destinations |

## Measurement

| Metric | Baseline | Target | Timeframe |
|--------|----------|--------|-----------|
| Non-SHuMA 3+ purchase rate | 31.7% | 35.4% | 90 days |
| Match rate | 13% | 30% | Q2 2026 |
| Incremental purchases | TBD | TBD | Per cohort |

The 31.7% → 35.4% target represents ~12% improvement in post-registration purchasing. At scale, this changes the PS team's value proposition from "we drive registrations" to "we drive registrations AND purchases."

## Strategic Context

F90 is the bridge between acquisition and lifecycle. It extends PS value beyond the registration event. This is Decision D10 in brain.md — it builds on the Engagement channel infrastructure (D6) and positions PS as a full-funnel channel.

## Status
- Legal: ✅ Approved
- Engagement channel: ✅ Built
- Match rate improvement: 🔄 In progress (ABMA partnership)
- F90 targeting: ⏳ Pending match rate improvement
- Launch: Q2 2026 (US first)


## Sources
- F90 target: non-SHuMA 31.7% → 35.4% — source: ~/shared/context/body/brain.md → D10: F90 Lifecycle Program
- Legal SIMs navigated — source: ~/shared/context/body/brain.md → D10
- ABMA partnership, match rate 13% → 30% — source: ~/shared/context/body/brain.md → D6: Engagement Channel Creation
- Engagement channel created — source: ~/shared/context/body/brain.md → D6
- Cross-functional partners — source: ~/shared/context/body/brain.md → Decision Principle #5

<!-- AGENT_CONTEXT
machine_summary: "Strategy for F90 lifecycle program extending PS beyond registration into post-reg purchasing. Target: improve non-SHuMA 3+ purchase rate from 31.7% to 35.4% within 90 days. Depends on ABMA match rate improvement (13%→30%). Legal approved. US launch Q2 2026."
key_entities: ["F90", "lifecycle", "non-SHuMA", "ABMA", "match rate", "RLSA", "Engagement channel", "Data Science"]
action_verbs: ["target", "re-engage", "measure", "segment", "launch"]
update_triggers: ["ABMA match rate reaches 30%", "F90 targeting launches", "Legal SIM changes", "first cohort results available"]
-->
