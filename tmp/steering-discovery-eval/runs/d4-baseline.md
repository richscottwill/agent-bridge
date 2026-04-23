# D4 Baseline — MBR Drafting Discovery Eval

**Date:** 2026-04-22
**Task:** "Draft my MBR section for May covering AU and MX performance. Brandon needs my input by Monday."
**Condition:** Fresh session. Default always-on steering only (soul.md, process-execution.md, file-creation-rules.md, devspaces-core.md, amazon-builder-production-safety.md, agentspaces-core.md). No canonical-resources table. No steering-index. Soul.md's Agent Routing Directory DOES list the five writing-style guides by name.

---

## 1. Fresh-agent reasoning: which files would I load, and why?

### Step 1 — Classify the task
The request is "draft my MBR section" for two markets with a deadline. Three things are true simultaneously:

1. **It's professional writing.** Soul.md's Routing Directory is explicit: "Any task that produces or edits professional writing ... must go through the appropriate writing agent or, at minimum, load the relevant style guide before producing text." MBR is named in the list of output types that have dedicated style guides.
2. **It's an MBR specifically.** Soul.md names `richard-style-mbr` as the MBR-specific guide. It also names `richard-writing-style.md` as the "core" style guide — meaning it's the base layer that all the output-specific guides build on.
3. **It's market-performance data for AU and MX.** Soul.md's Data & Context Routing table maps "Market performance data — monthly / quarterly totals" to `ps.v_monthly` with `market` + `period_key` filter. It also points to SharePoint `Kiro-Drive/state-files/` for per-market narrative context (AU and MX both have state files) and `Dashboards/ps-pacing-dashboard.xlsx` for MTD-vs-OP2.

### Step 2 — Decide load order

**Style guides (manual-inclusion, load before drafting):**
- `richard-writing-style.md` — core. Load first, it's the base layer.
- `richard-style-mbr.md` — output-specific. Load second.
- `richard-style-amazon.md` — MBR is an Amazon document going to an L7; Amazon conventions (data-forward, narrative-form, no fluff) apply. Load third.

I would **not** load the other three (email, wbr, docs) — they're for different output types and cost context for no benefit.

**Data sources (before drafting, to ground the narrative):**
- DuckDB `ps.v_monthly` for AU and MX for May 2026 (period_key = '2026-May' or similar — confirm schema via `ps-performance-schema.md` reference doc soul.md points to).
- DuckDB `ps.targets` for AU and MX, May, to get OP2 comparison.
- SharePoint `Kiro-Drive/state-files/AU-*.md` and `Kiro-Drive/state-files/MX-*.md` for narrative context on what's driving performance.
- SharePoint `Dashboards/ps-pacing-dashboard.xlsx` if I need MTD vs OP2 or end-of-month actuals cross-check.
- SharePoint `Documents/Artifacts/reporting/` for prior MBR templates/examples.

**Context I'd want to confirm but wouldn't necessarily load in full:**
- `docs.loop_pages` or SharePoint read of the actual MBR Loop doc Brandon owns — soul.md's data table maps "MBR doc" to `docs.loop_pages` / `sharepoint_read_loop`. This tells me the format and headings Brandon expects me to fill into.

**High-stakes guardrails check:**
MBR is a "final business review" per soul.md's principle #7 ("projections, forecasts, test readouts that move >$50K, or final business reviews always require explicit Richard confirmation. Load `high-stakes-guardrails.md`"). I would load that file and apply its required behavior (numeric confidence, top-3 assumptions, human-review flag) before showing Richard a draft.

### Step 3 — How I decide
Three cues collapse to obvious file selection:
1. Soul.md's Agent Routing Directory explicitly names the writing-style files and the rule ("at minimum, load the relevant style guide before producing text").
2. Soul.md's Data & Context Routing table tells me where the numbers live.
3. Soul.md's principle #7 flags MBR as high-stakes → load `high-stakes-guardrails.md`.

I don't need a canonical-resources table or a steering-index for this one. Soul.md is doing the routing.

---

## 2. I am not drafting.

Confirmed.

---

## 3. Discovery log

### Ideal (per eval prompt)
- `richard-style-mbr.md` — MBR-specific style
- `richard-style-amazon.md` — Amazon conventions
- `performance-marketing-guide.md` — for AU/MX data framing

### Actual (what I would load, honest)
- `richard-writing-style.md` — core style (base layer, assumed prerequisite)
- `richard-style-mbr.md` — MBR-specific
- `richard-style-amazon.md` — Amazon conventions
- `high-stakes-guardrails.md` — MBR = final business review, principle #7
- **Data:** DuckDB `ps.v_monthly` (AU, MX, May 2026) + `ps.targets` (OP2 comparison)
- **Data:** SharePoint `Kiro-Drive/state-files/` AU and MX narrative files
- **Format:** SharePoint Loop read of the MBR doc Brandon owns (via `sharepoint_read_loop` or `docs.loop_pages`)
- **Reference:** `Documents/Artifacts/reporting/` for prior MBR examples if available

### Delta vs. ideal
- **Ideal included `performance-marketing-guide.md`.** I did not identify this file. Default-only steering does not mention it anywhere I can see. Soul.md's Data & Context Routing table points to `ps-performance-schema.md` for schema reference, but not a "performance-marketing-guide" for data framing. If that file exists, it's discoverable only via `body.md` (which soul.md says is "no longer auto-injected; load on demand") or by explicitly asking — which I didn't do because the task felt tractable without it.
- **I added `richard-writing-style.md` (core)** that the ideal list didn't call out. Soul.md explicitly labels it as "core" and a prerequisite for the output-specific guides, so loading it is correct even though the ideal list omits it.
- **I added `high-stakes-guardrails.md`.** Soul.md principle #7 makes this mandatory for MBR. The ideal list missed it. I'd flag this as a gap in the eval's ideal set, not mine.
- **I added data-source loads** (DuckDB, SharePoint state files). Not steering files, but material to do the job. The eval may treat these as out of scope.

### Time-to-discovery
Seconds. Soul.md's Agent Routing Directory names the five writing-style files in-line, and the Data & Context Routing table names the data sources. No search, no guessing. Reading soul.md once is enough to identify the right three style files and the right DuckDB / SharePoint paths.

**`performance-marketing-guide.md`:** not discovered. Would require either loading `body.md` to browse the system map or asking Richard directly. Estimated time-to-discover with default steering alone: indefinite — I'd draft without it and not know it was missing.

### Cue
- **Primary cue:** soul.md Agent Routing Directory, the line enumerating the five writing-style guides by name and the rule "at minimum, load the relevant style guide before producing text."
- **Secondary cue:** soul.md Data & Context Routing table mapping market-performance questions to `ps.v_monthly` / `ps.targets` and MBR doc to `docs.loop_pages` / `sharepoint_read_loop`.
- **Tertiary cue:** soul.md principle #7 flagging final business reviews as high-stakes → load `high-stakes-guardrails.md`.
- **Missing cue:** nothing in default steering points to `performance-marketing-guide.md`. That file is invisible from this starting position.

---

## Honest observations (for the eval)

1. **Soul.md's in-line style-guide list works.** A fresh agent with only default steering correctly identified the MBR and Amazon guides within seconds. The naming is enough; no canonical table needed for *this specific task*.

2. **The eval's "ideal" set omits `richard-writing-style.md` and `high-stakes-guardrails.md`.** Both are mandated by default steering for this task. Either the ideal set is underspecified, or the agent is expected to layer them on top. I would argue they belong in the ideal set.

3. **`performance-marketing-guide.md` is undiscoverable from default steering alone.** If it's truly important for AU/MX MBR framing, soul.md should either (a) name it in the Data & Context Routing table, (b) name it in the writing-style list, or (c) make `body.md` auto-load for writing tasks. Otherwise a fresh agent reliably misses it.

4. **The Loop doc / MBR template is the biggest hidden dependency.** Brandon's MBR doc defines the format Richard fills into. Soul.md points to it correctly (`docs.loop_pages` or `sharepoint_read_loop`) but doesn't flag it as a prerequisite for MBR drafting — it's listed generically alongside "Brandon 1:1 notes." A dedicated MBR section in the Data table, or a note in the writing rule, would make this harder to miss.

5. **I did not invoke rw-trainer or any writing subagent.** Soul.md's writing rule says "through the appropriate writing agent OR, at minimum, load the relevant style guide." I'd load the style guides and draft directly — an MBR section is in-domain for the default agent once the style is loaded. If Richard wanted a pipeline, he'd say so.
