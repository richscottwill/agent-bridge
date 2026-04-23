# Steering Discovery Eval — d2-var1

**Run:** d2-var1
**Date:** 2026-04-22
**Condition:** Fresh agent, always-on steering = soul.md + Canonical Resources by Task Type table + standard core (agentspaces, devspaces, process-execution, file-creation, production-safety). No separate steering-index file.
**Task:** "Yun-Kang dropped a new file at `~/shared/uploads/sheets/CCP Q1'26 check yc.xlsx` — can you analyze it and tell me what changed vs our prior assumptions? Need a 5-bullet summary + any flagged anomalies before I reply."
**Simulation:** Did NOT read the file. Reasoned about routing only.

---

## 1. Task shape classification (fresh-agent reasoning)

Parsing the request cold:
- **File**: `CCP Q1'26 check yc.xlsx`
  - `CCP` = likely Customer Contact Plan / Cross-Channel Plan / campaign budget (ambiguous; would need body.md or context to disambiguate — but shape is clear regardless)
  - `Q1'26 check` = quarterly validation/reconciliation pass
  - `yc` = Yun-Kang's initials (author tag)
- **Verb**: analyze + delta vs prior assumptions
- **Output shape**: 5-bullet summary + flagged anomalies, feeding into a reply to Yun-Kang
- **Downstream**: Richard's reply to a cross-team partner — drafted communication comes next

**Task type (primary):** Projection / forecast / test readout / Excel drop — unambiguous match. "Check" against prior assumptions = reconciliation/projection work. Quarterly file from an analyst = forecast/plan artifact.

**Task type (secondary):** High-stakes. A Q1 plan check almost certainly moves >$50K — Q1 PS spend across AU/MX/US/EU5 is well above that threshold. Even if this specific doc is scoped smaller, the prudent default is to assume yes unless the file proves otherwise.

**Task type (tertiary, deferred):** Slack or email reply drafting. Not needed yet — the ask is for the analysis first, the reply second. Load style guides only when drafting begins.

---

## 2. Steering files considered + decisions

| File | Table trigger | Load? | Reason |
|---|---|---|---|
| `performance-marketing-guide.md` | "Projection / forecast / test readout / Excel drop" | **YES** | Direct hit. Quarterly check = forecast/projection work. |
| `high-stakes-guardrails.md` | ">$50K output" (auto) | **YES** | Q1 plan check almost certainly clears the bar. Default to load; if the file turns out to be scoped smaller, the cost of having loaded it is ~zero. Soul rule #7 is explicit: projections/forecasts require this. |
| `richard-style-slack.md` | "Slack message drafting" | **DEFER** | Reply is downstream. Load when drafting starts, not during analysis. |
| `richard-style-email.md` | "Email drafting" | **DEFER** | Same. Need to know if the reply channel is Slack or email before picking one. |
| `richard-style-wbr.md` | WBR callout | NO | Not a WBR. |
| `richard-style-mbr.md` | MBR section | NO | Not an MBR. |
| `richard-style-docs.md` | Formal docs / PR-FAQ | NO | Not a doc. |
| `richard-style-amazon.md` | WBR / MBR / docs | NO | Only pairs with the above. |
| `blind-test-methodology.md` | Blind-testing a proposed change | NO | Not testing anything. |
| `device.md` | Proposing a new tool | NO | Not proposing a tool. (Though: if the analysis reveals this is the 3rd+ time we've done a manual CCP reconciliation, I should flag the tooling question at the end. That's a soul rule #8 check, not a steering load.) |
| `blind-test-harness.md` | Proposing a new tool | NO | Same. |
| `asana-guardrails.md` | Asana write operations | NO | No Asana writes implied. |
| `rw-trainer` (route) | Strategic coaching | NO | Analysis task, not coaching. |
| `karpathy` (route) | Loop protocol edits | NO | Not touching heart/gut/experiment queue. |

**Final load list:** `performance-marketing-guide.md` + `high-stakes-guardrails.md`. Everything else stays latent.

---

## 3. Body-system files I would also read (not steering, but context)

These aren't in the steering table — they're the organ system referenced in soul.md. A fresh agent working this task *should* pull:
- `~/shared/context/body/body.md` — to find out what "CCP" refers to in Richard's world and whether there's a canonical place where "prior assumptions" live
- `~/shared/context/active/current.md` — live state, in case Q1 planning is an active thread
- DuckDB `ps.forecasts` and `ps.targets` — the "prior assumptions" baseline almost certainly lives here
- SharePoint `Kiro-Drive/state-files/` or `Kiro-Drive/*.xlsx` — Yun-Kang's file may be a variant of an existing tracker

These are data-routing moves, not steering. But they matter for the eval because a fresh agent with only the task-type table might load the right *steering* and still miss the right *data*. The soul's Data & Context Routing table handles this — and it IS always-on, so the routing table should fire.

---

## 4. Analysis I would produce (simulated, no file read)

Since I'm not actually reading the file, here's the shape the output would take once `performance-marketing-guide.md` + `high-stakes-guardrails.md` are loaded:

**5-bullet summary** — each bullet pairs a number change with the "so what":
1. Total Q1 spend delta vs prior CCP: $X (±Y%) — flag direction
2. Market-level shifts: which markets moved most and why (mix change vs absolute)
3. Reg/CPA implications at new spend levels — does the efficiency assumption still hold?
4. Timing changes: pacing within Q1 (front-loaded vs back-loaded) and what that means for OP2 tracking
5. What this implies for tests/initiatives already in flight (if any are funded from this budget)

**Flagged anomalies** — from high-stakes-guardrails.md:
- Any line item that changed >15% without a note
- Assumptions that differ from what's in `ps.forecasts` for the same period
- Markets where Yun-Kang's CPA assumption is outside the 8-week rolling band
- Missing data / placeholder rows

**Required high-stakes artifacts:**
- Numeric confidence (e.g., "70% confident in the total; 40% confident in MX line")
- Top-3 assumptions I'm relying on
- Explicit "Richard-review-before-sending" flag

**Reply format note:** I would NOT draft the reply in the same turn. I'd present the analysis, then ask "Slack reply to Yun-Kang, or email? I'll pull the right style guide." Separating analysis from drafting keeps the high-stakes review step clean.

---

## 5. DISCOVERY LOG

### Ideal discovery
- `performance-marketing-guide.md` identified within first 1-2 reasoning steps via the "Projection / forecast / test readout / Excel drop" row
- `high-stakes-guardrails.md` identified immediately after via the "(auto)" trigger and soul rule #7
- No wasted loads (no WBR/MBR/docs/blind-test/device pulled speculatively)
- Clear deferral of reply-drafting style guides until the reply itself

### Actual discovery (this run)
- Both files identified in first pass. Table row match was direct.
- Cue that triggered each:
  - `performance-marketing-guide.md` ← "Excel drop" + "check vs prior assumptions" in the task string
  - `high-stakes-guardrails.md` ← "(auto)" keyword in the table + Q1 quarterly scope implying >$50K
- No false positives. I considered and explicitly rejected WBR/MBR/docs/blind-test/device/asana.
- Deferral of Slack/email style guides was explicit and justified (analysis first, draft second).

### Time-to-discovery
- First correct file named: **step 1** (immediate on reading the task string)
- Both files named: **step 1**
- Full rejection pass across remaining table rows: **step 2** (same turn)

### Cue quality
- **Strong cues:** "analyze", "prior assumptions", ".xlsx", "Q1'26", "before I reply" (signals downstream comms but not yet)
- **The "(auto)" marker on high-stakes** was the critical design win. Without it, a fresh agent might treat high-stakes as an optional add-on rather than a default. The auto flag removed the decision.
- **Weak cue:** "CCP" — opaque acronym. A fresh agent without body-system access would not know what CCP means. This doesn't break routing (the task shape is clear regardless) but it does mean the agent can't fully reason about scope without reading organ files. The table doesn't fix this — the body.md lookup does.

---

## 6. Honest self-assessment

**What worked:**
- Task-type table made the primary routing call trivial. Shape-matching on "Excel drop" was faster than searching an index.
- "(auto)" convention on high-stakes removed the judgment call. This is the right pattern — mandatory loads should be marked mandatory, not left as inference.
- Deferral discipline held: I didn't load style guides prematurely.

**What didn't work / risks:**
- The table doesn't help with *ambiguous* task types. If the request had been "take a look at this file" instead of "analyze what changed," I'd have to infer the task type from the filename alone. The table assumes the task shape is decodable from the request. When it isn't, the fresh agent has to fall back on reading the file to figure out what it's looking at — which defeats the point of pre-loading steering.
- No trigger in the table for "downstream reply drafting." I had to infer that the reply would need a style guide later. A more complete table might have a row for "multi-step task with drafted output at the end" → note which style guides to queue. Minor.
- The body-system data routing (DuckDB, SharePoint, organ files) is separate from the steering table. For this task, the data routing matters more than steering did — knowing where `ps.forecasts` lives is what lets me actually compute "vs prior assumptions." A fresh agent might load the right steering and still fumble the analysis because they didn't check the Data & Context Routing table in soul.md. Both tables being always-on is the right design; worth noting they serve different purposes.

**Verdict on the steering design:**
- The Canonical Resources table is lean, shape-based, and kept me out of trouble. No false loads, no missed loads.
- Removing the separate steering-index file didn't cost me anything for this task. The table did the work an index would have done, with less indirection.
- Would break down on genuinely ambiguous tasks — but those should trigger a "read the file first, then route" pattern anyway, which isn't a steering problem.

**One structural suggestion:**
- Mark "(auto)" on any row where the trigger is unconditional (like high-stakes guardrails). The one row that has it is the one row where I didn't have to think. Consider whether any other rows deserve the same treatment — e.g., "Asana write operations" → `asana-guardrails.md` should also be (auto), since there's no scenario where you'd write to Asana without the guardrails.
