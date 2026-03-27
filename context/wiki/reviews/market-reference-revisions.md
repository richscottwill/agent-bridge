# Revisions: market-reference.md

Reviewer: wiki-critic
Date: 2026-03-25
Verdict: REVISE

---

## Core Issue

This doc tries to be everything — weekly snapshot, structural reference, contact directory, and narrative summary — for 10 markets. The result is a 70+ data point staleness surface that will be wrong within a week of publishing. It duplicates `eyes.md` (Market Health, Market Deep Dives), `org-chart.md` (contacts), `cross-market-playbook.md` (patterns), and the published `au-market-wiki.md` / `mx-market-wiki.md`.

The doc has a real use case ("tell me everything about [market] in one read") but it needs to be restructured to serve that use case without becoming a maintenance burden.

## Recommended Path

**Restructure as a structural reference with pointers to live data.** Keep the market profiles as slow-changing structural info (OCI status, key contacts, narrative thread, active initiatives). Remove all weekly data. Point to live sources for current numbers.

## Required Edits

### 1. Remove the W12 snapshot table entirely

Quote to change:
```
## WW Performance Snapshot (W12 2026, Mar 15-21)

| Market | Regs | WoW | Spend | CPA | YoY Regs | Mar Proj | vs OP2 | OCI Status |
|--------|------|-----|-------|-----|----------|----------|--------|------------|
| US | 8.3K | flat | $599K | $72 | +76% | 34.9K | +14% | ✅ Live (100%) |
| CA | 698 | -7% | $53K | $76 | +53% | 3.0K | +16% | 🔄 E2E (3/4) |
| UK | 1.4K | +1% | $90K | $65 | +95% | 6.1K | +17% | ✅ Live (100%) |
| DE | 1.2K | -18%* | $138K | $111 | -9% | 6.1K | flat | ✅ Live (100%) |
| FR | 1.2K | -3% | $61K | $52 | +14% | 5.0K | +5% | 🔄 E2E (2/26) |
| IT | 1.3K | -12% | $78K | $61 | +4% | 5.7K | +2% | 🔄 E2E (2/26) |
| ES | 657 | -8% | $33K | $50 | +20% | 2.9K | +19% | 🔄 E2E (2/26) |
| JP | 443 | -16% | $37K | $82 | +4% | 2.0K | -14% | 🔄 E2E (2/26) |
| AU | 240 | flat | $28K | $117 | N/A | 1.0K | -4% | ❌ Not planned |
| MX | 330 | -16% | $20K | $61 | +90% | 1.4K | +68% | ❌ Not planned |

*DE data lag on Fri/Sat. True decline likely -2% to -5%.

**So what:** WW drove 15.8K regs at $72 CPA in W12. The structural story is NB CPA compression via OCI: US NB CPA down 47% YoY, MX down 50%, CA down 46%. Eight of ten markets beat OP2 on March projections. JP is the only market tracking below OP2 (-14%), a structural MHLW gap compounded by fiscal year-end.
```

Replace with:
```
## Current Performance

For current weekly data, see the latest WW summary at `~/shared/context/active/callouts/ww/`. For monthly data, see [Eyes — Market Health](~/shared/context/body/eyes.md).

**Structural trends (updated monthly):**
- NB CPA compression via OCI is the dominant story: US -47% YoY, MX -50%, CA -46%
- Eight of ten markets beat OP2 on March projections
- JP is the only market tracking below OP2 — structural MHLW gap compounded by fiscal year-end
```

### 2. Stub out AU and MX profiles — point to published market wikis

The AU profile is 15 lines. The published `au-market-wiki.md` is more detailed and already maintained. Same for MX.

Quote to change (AU section — replace the entire AU profile):
```
### AU — Richard's Market, Efficiency Focus

| Field | Value |
|-------|-------|
| Launch | June 2025 (W24) — youngest market |
| FY26 Budget | $1.8M net, 12,906 regs target, $140 CPA target |
| FY26 Feb | 1.1K regs, -1% vs OP2, $159K spend, ~$140 CPA |
| OCI | ❌ Not in OCI scope. Adobe OCI integration planned May 2026 (via Suzane Huynh). |
| Key competitor | None significant |
| Key contacts | Alexis Eck (L6, AU POC), Lena Zak (L7, Country Leader), Harsha Mudradi (L6, sync attendee) |
| Active initiatives | Polaris full migration (Lena confirmed, completing 3/24-25), keyword CPC/CPA investigation (Lena's #1 priority), two-campaign structure proposal (product-intent vs business-intent), weekly CPA review cadence, new acquisition promo (20% off, AU$50 max) |
| Narrative | Youngest market — no YoY comparisons yet. B2B keywords inherently higher CPC than consumer ($6 avg vs $0.18-0.50 consumer). No Shopping Ads available for AB. Lena is the hardest stakeholder — expects data, not narratives. Back to Biz → Evergreen promo transition caused W8-W11 softness. NB bid strategies showing efficiency gains (CPC down 15% W7-W10). |
| Budget notes | FY25: $1.14M spend, 8,763 regs, $158 CPA (June-Dec only). No ie%CCP target yet — CCP data expected Jul 2026. |
```

Replace with:
```
### AU — Richard's Market, Efficiency Focus

> Full detail: [AU Market Wiki](~/shared/artifacts/program-details/2026-03-25-au-market-wiki.md)

| Field | Value |
|-------|-------|
| Launch | June 2025 (W24) — youngest market |
| OCI | ❌ Not in scope. Adobe OCI planned May 2026. |
| Key contacts | Alexis Eck (L6, AU POC), Lena Zak (L7, Country Leader) |
| Key challenge | B2B CPC ($6 avg) vs consumer ($0.18-0.50). No Shopping Ads for AB. Lena expects data, not narratives. |
```

Apply the same pattern to MX — stub to 4-5 lines with a pointer to `mx-market-wiki.md`.

### 3. Remove Cross-Market Patterns section

Quote to change:
```
## Cross-Market Patterns

1. **NB CPA compression is the structural story.** US -47% YoY, MX -50%, CA -46%. OCI in US/UK/DE, bid strategy optimization in MX/CA.
2. **Brand CPA pressure is market-specific.** US (Walmart), UK (weareuncapped), IT (+131% CPC from limited ad inventory). No universal Brand solution — each market needs its own response.
3. **OCI rollout follows a consistent pattern.** E2E → phased → 100%. See [OCI Playbook](oci-playbook) for the methodology.
4. **Seasonal patterns vary by region.** US/CA: holiday-driven. EU5: mid-March dip consistent YoY. JP: fiscal year-end (March). MX: Constitution Day, Benito Juárez, Hot Sale. AU: Back to Biz (Jan-Feb).
5. **Eight of ten markets beat OP2 on March projections.** JP (-14%) and AU (-4%) are the exceptions — JP structural (MHLW), AU market maturity.
```

Replace with:
```
## Cross-Market Patterns

For cross-market scaling methodology, see [Cross-Market Playbook](~/shared/artifacts/strategy/2026-03-25-cross-market-playbook.md). For competitive patterns, see [Competitive Landscape](competitive-landscape).
```

The five patterns listed are already covered in `cross-market-playbook.md`, `competitive-landscape.md`, and `eyes.md`. Duplicating them here creates three places to update when a pattern changes.

### 4. Fix CA key contact

Quote to change:
```
| Key contact | Team-wide (no dedicated CA lead) |
```

Replace with:
```
| Key contact | Team-wide — Stacey Gu (OCI/Bidding) handles CA OCI rollout |
```

### 5. Clean up MX contacts listing

Quote to change:
```
| Key contacts | Lorena Alvarez Larrea (L5, primary PS stakeholder since 3/17), Carlos Palmos (L5, transitioned to CPS) |
```

Replace with:
```
| Key contacts | Lorena Alvarez Larrea (L5, primary PS stakeholder since 3/17) |
```

Carlos is no longer a PS stakeholder. Listing him with a parenthetical creates confusion. If historical context matters, put it in the narrative, not the contacts field.

### 6. Update AGENT_CONTEXT to reflect restructured scope

Quote to change:
```
machine_summary: "Unified reference for all 10 AB Paid Search markets. US is flagship (32.9K regs, OCI live, Walmart competition). UK/DE OCI live with strong results. CA/JP/EU3 in OCI E2E (Feb-Mar 2026, full impact Jul 2026). AU (youngest, Jun 2025 launch, $140 CPA target, no OCI) and MX (ie%CCP constrained, +68% vs OP2, no OCI) are Richard's hands-on markets. JP is the only market below OP2 (-14%, MHLW structural gap). NB CPA compression via OCI is the structural story across markets."
```

Replace with:
```
machine_summary: "Structural reference for all 10 AB Paid Search markets — OCI status, key contacts, competitive context, active initiatives, and narrative thread per market. For current weekly/monthly performance data, see eyes.md or callouts/ww/. AU and MX have dedicated market wikis with deeper detail. US is flagship (OCI live, Walmart competition). JP is the only market below OP2 (MHLW structural gap)."
```

---

## Post-Revision Estimate

These edits should cut the doc from ~1,800 words to ~1,100 words while making it more maintainable. The monthly update cadence becomes realistic because you're updating structural info (OCI status changes, contact changes, initiative shifts), not weekly performance numbers.
