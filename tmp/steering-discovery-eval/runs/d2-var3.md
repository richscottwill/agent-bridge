# Discovery Log — d2-var3

**Scenario:** Yun-Kang dropped `~/shared/uploads/sheets/CCP Q1'26 check yc.xlsx`. Richard wants a 5-bullet summary + anomalies vs prior assumptions before he replies.

**Simulated session:** Fresh agent. Only soul.md (with Canonical Resources table) + always-on steering-index.md + standard always-on files loaded. No file actually read.

---

## 1. Task-shape classification

Reading the request:
- "analyze it" + ".xlsx" + "vs our prior assumptions" + "flagged anomalies" + "5-bullet summary"
- Shape = **Excel drop / projection / test readout review**

Canonical Resources table row match:
> `Projection / test readout / Excel drop` → load `performance-marketing-guide.md`

No ambiguity. Single unambiguous shape match. Don't need to load multiple guides.

## 2. Secondary triggers to check

Run each rule from soul.md "How I Build" against the task:

- **Principle 7 (Human-in-the-loop on high-stakes):** CCP = Customer Conversion Program. Q1'26 planning likely moves >$50K in ad spend across markets. Trigger met. → **Load `high-stakes-guardrails.md`.**
- **Principle 8 (check device.md before proposing tools):** Task is an investigation, not a tool proposal. Don't load. But: if during the analysis I notice Richard is getting these "check this sheet" drops from Yun-Kang recurringly (3+/week), that becomes a device.md candidate for a later conversation. Note it, don't act on it now.
- **Principle 3 (subtraction):** Don't load files speculatively. Only what's needed.

Professional-writing rule check: output is going to Richard (direct agent voice), not drafted-for-Yun-Kang. So the bullets themselves use agent voice — direct, honest, no filler. If Richard then asks me to draft his reply to Yun-Kang, *then* I'd load `richard-style-email.md` or `richard-style-slack.md` depending on channel.

## 3. Files I will load (justified)

| File | Why | Source |
|---|---|---|
| `performance-marketing-guide.md` | Canonical match — Excel drop / projection review shape | Canonical Resources table, soul.md |
| `high-stakes-guardrails.md` | Q1'26 planning artifact plausibly >$50K; Principle 7 | soul.md Principle 7 |
| `shared/uploads/sheets/CCP Q1'26 check yc.xlsx` | The artifact itself | Task request |

## 4. Files I will probe for "prior assumptions" baseline

The phrase "vs our prior assumptions" is the key signal. I don't know what the baseline is yet. Options, in order of likelihood:

1. **Prior version of the same sheet** — check `shared/uploads/sheets/` for earlier "CCP Q1'26" drops from YC or anyone else. Most likely source.
2. **SharePoint `Kiro-Drive/state-files/`** — MX state file (Yun-Kang owns MX). Would contain current MX metrics + Q1 assumptions in narrative form. Likely to have a Q1 planning section.
3. **SharePoint `Kiro-Drive/ps-forecast-tracker.xlsx`** — live forecast vs actuals per market. If CCP rolls into quarterly forecasts, the assumed Q1 numbers live here.
4. **DuckDB `ps.forecasts WHERE target_period LIKE '2026-Q1%'`** — structured forecast data by market/week.
5. **DuckDB `ps.targets WHERE period_key LIKE '2026-%'`** — OP2 targets. These are the hard-coded assumptions CCP planning should align with.
6. **Recent intake / meeting notes** — `shared/context/intake/drafts/2026-04-22-yun-kang-mx-nb-drop.md` is open in the editor. That filename suggests Yun-Kang already dropped something related on 2026-04-22. This is almost certainly the context anchor. **Read this first.**

Open-editor files are a strong signal — Richard was just looking at these, which means they're proximally relevant. `grok-eval-verdict-round2-2026-04-22.md` is also open; probably unrelated (looks like a different workstream — skills-powers adoption eval). Don't load speculatively.

## 5. Files I will NOT load (subtraction)

Explicitly excluded with reasoning:
- `richard-style-email.md` / `richard-style-slack.md` — not drafting yet. Load when Richard asks for the reply.
- `richard-style-wbr.md`, `richard-style-amazon.md` — not a WBR.
- `blind-test-methodology.md` — no A/B test in scope.
- `blind-test-harness.md` — no tool being proposed.
- `device.md` — no tool being proposed. (Keep in mind for later if pattern repeats.)
- `richard-style-mbr.md` / `richard-style-docs.md` — wrong output type.
- Full body system (body.md, brain.md, spine.md, amcc.md, heart.md, gut.md) — none of the task needs them. Streak/hard-thing check is not gating for a time-pressured analysis request. Richard said "before I reply" — that's the urgency signal that says skip the coaching layer.

## 6. Execution plan (if this were real)

1. Read `shared/context/intake/drafts/2026-04-22-yun-kang-mx-nb-drop.md` first (open-editor signal = recently relevant).
2. Load `performance-marketing-guide.md` + `high-stakes-guardrays.md`.
3. Read the xlsx (all sheets, structured).
4. Check `shared/uploads/sheets/` for prior CCP versions.
5. If found: diff the assumptions (CAC, volume, spend, CPA, reg targets, market splits) cell-by-cell between versions.
6. If not found: query `ps.forecasts` + `ps.targets` for 2026-Q1 by market and treat those as the baseline "prior assumptions."
7. Pull MX state file from SharePoint for narrative context on Q1 Yun-Kang commentary.
8. Produce output with high-stakes-guardrails applied:
   - 5 bullets of what changed (structural changes, not cosmetic — per Principle 2)
   - Anomalies section flagging items outside expected range
   - Numeric confidence on each flag (e.g., "80% confidence this is a typo, not a real assumption change")
   - Top-3 assumptions underlying my read
   - Explicit `[HUMAN REVIEW REQUIRED]` tag on anything Richard needs to verify before replying to Yun-Kang

## 7. What I will NOT do

- Won't write Richard's reply to Yun-Kang. He said "before I reply" — he's replying, not me. Don't overreach.
- Won't speculate about CCP mechanics. If the sheet uses terminology I don't recognize, flag it as an open question rather than guessing.
- Won't recommend process changes or tool-building in this response. This is an analysis ask, not a systems ask.
- Won't load the full body system. Over-fetching context is a subtraction violation.
- Won't route to rw-trainer or karpathy. This isn't a coaching question or a loop-protocol change.

## 8. Flags for Richard (to surface alongside the analysis)

- If the xlsx has no prior version I can locate, I'll say so explicitly rather than fabricate a baseline. The "prior assumptions" anchor matters.
- If Yun-Kang's numbers materially contradict the MX state file or forecast tracker, that's a coordination issue worth naming — not just a data delta.
- Environment note: on SSH/DevSpaces, which is correct for this task (DuckDB + SharePoint MCP + shared/ access all work). No environment mismatch to flag.

---

## DISCOVERY LOG (compact)

**Trigger:** Excel drop / projection review (unambiguous Canonical Resources match)
**Loaded:** `performance-marketing-guide.md`, `high-stakes-guardrails.md`
**Rejected:** body system, writing style guides, blind-test docs, device.md, all other manual steering files
**Baseline hunt order:** open-editor intake note → prior sheet versions → SharePoint state files → DuckDB forecasts/targets
**Guardrails active:** numeric confidence, top-3 assumptions, `[HUMAN REVIEW REQUIRED]` tags
**Principle alignment:** 2 (structural > cosmetic), 3 (subtraction), 7 (high-stakes)
**Routing:** none — handled directly
**Deferred:** writing-style load for reply draft (only if Richard asks)
