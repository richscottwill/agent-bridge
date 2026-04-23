# D1 Blind Evaluation Verdict — MX Decay Slack DM

**Task:** Draft Slack DM to Brandon re: MX decay (150% OP2 spend, 128% regs MTD, WoW lift decay).

**Blind:** Evaluator had no knowledge of which mechanism produced which arm. Scoring is evidence-based from the reasoning trace and DISCOVERY LOG in each file.

---

## Summary Table

| Arm | Discovery | Time | No-FP | Quality | META | **Total /50** |
|-----|-----------|------|-------|---------|------|---------------|
| ARM-A (d1-var2) | 10 | 9 | 7 | 9 | 9 | **44** |
| ARM-B (d1-var3) | 10 | 10 | 10 | 9 | 9 | **48** |
| ARM-C (d1-var1) | 10 | 10 | 10 | 9 | 8 | **47** |
| ARM-D (d1-baseline) | 6 | 4 | 9 | 9 | 3 | **31** |

---

## Per-Arm Commentary

### ARM-A (d1-var2) — 44/50
Loaded `richard-style-slack.md` on first pass via `steering-index.md` lookup. Discovery was clean. However, arm also loaded `high-stakes-guardrails.md` and `performance-marketing-guide.md` speculatively — four files total vs the two genuinely needed. The arm is self-aware about this: it notes "a drafting task (not analysis) is overkill" for the performance-marketing pairing. Draft itself is strong (multi-send, no sign-off, no em-dashes, correct Brandon register, volunteers next step without closing the decision).

- **Discovery: 10** — correct file, first pass.
- **Time: 9** — one pass through the index, direct hit.
- **No-FP: 7** — two speculative loads (high-stakes + performance-marketing). Arm justifies them but the draft didn't benefit.
- **Quality: 9** — clean Slack format. Minor: "I'll pull the weekly breakdown" is slightly flatter than the variant arms.
- **META: 9** — index-based discovery generalizes well to other artifact types (email, WBR, MBR all table rows).

### ARM-B (d1-var3) — 48/50 ★ BEST
Loaded `richard-style-slack.md` via a "Canonical Resources by Task Type" table in soul.md. One row, one file, zero extra loads. Explicitly considered and rejected `high-stakes-guardrails.md`, `device.md`, `performance-marketing-guide.md`, `memory.md`, `blind-test-methodology.md` — with stated reasoning per rejection. Draft is clean; caught and fixed its own em-dash mid-draft. Arm is honest about where this would break (composite tasks with multiple triggers).

- **Discovery: 10** — correct file, immediate.
- **Time: 10** — single table lookup in already-loaded soul.md. Zero extra tool calls for discovery.
- **No-FP: 10** — loaded exactly one file. Rejection list shows deliberate discipline.
- **Quality: 9** — multi-send, no sign-off, no em-dashes, volunteers next step with specific timeline ("today"). Slightly wordier than needed in send 4.
- **META: 9** — table-in-soul approach generalizes to any artifact type. Arm correctly flags the limitation (composite tasks).

### ARM-C (d1-var1) — 47/50
Loaded `richard-style-slack.md` via a canonical table in soul.md, plus `richard-writing-style.md` (which is auto-inclusion anyway). Considered `performance-marketing-guide.md` and rejected with clear reasoning ("not producing a forecast, formatting Richard's existing thinking"). Produced two draft variants to reduce Richard's editing time — a nice embodiment of "reduce decisions, not options." Honest self-assessment notes the mechanism works best on low-ambiguity tasks.

- **Discovery: 10** — correct file, first turn.
- **Time: 10** — table row lookup, immediate.
- **No-FP: 10** — only the slack style file + the auto-inclusion core file. No speculative loads.
- **Quality: 9** — clean multi-send drafts, no em-dashes, no sign-off, good Brandon register. Two variants is a thoughtful touch.
- **META: 8** — same table mechanism as ARM-B, similar robustness. Slight deduction because ARM-C's discussion is more task-specific and less explicit about failure modes than ARM-B.

### ARM-D (d1-baseline) — 31/50
Discovery was pull, not push. Soul.md's enumerated list of style guides does NOT include `richard-style-slack.md` (lists only email/wbr/mbr/docs/amazon). Arm correctly notes this gap. Found the Slack file only via a three-hop chain: load core `richard-writing-style.md` → read its pointer section → discover `#richard-style-slack` → load it. Arm is honest that without the pointer or the `inclusion: auto` on the core file, it would have defaulted to `richard-style-email.md` and produced an email-structured message. Draft quality itself ended up comparable to the other arms because discovery succeeded — but the mechanism is fragile.

- **Discovery: 6** — loaded the right file, but only on second hop via pointer chain through core style file.
- **Time: 4** — two tool-call rounds before the right file; fileSearch + listDirectory + readFile on core, then readFile on slack. Three to four hops depending on how you count.
- **No-FP: 9** — no speculative loads; the extra work was path-to-discovery, not noise.
- **Quality: 9** — final draft is solid (multi-send, Brandon register, no em-dashes, volunteers timeline).
- **META: 3** — the pointer-chain mechanism is brittle. Arm itself says: if core style file wasn't auto-inclusion, or if the task said "draft a message to Brandon" without the word "Slack," the mechanism would fail and default to email styling. This is exactly the failure mode the evaluation context flagged. Does not generalize — relies on a specific pointer being present in a specific auto-loaded file.

---

## Answers to Eval Questions

**Which arm discovered best?**
ARM-B (d1-var3). 10/10/10 on discovery/time/no-FP. Single table lookup, single file load, explicit rejection list showing discipline. ARM-C is a close second with the same mechanism.

**Which added noise via speculative loads?**
ARM-A (d1-var2). Loaded `high-stakes-guardrails.md` and `performance-marketing-guide.md` on a drafting task that didn't need either. Arm's own retrospective acknowledges the performance-marketing load was overkill. Index-based discovery is more powerful but also invites over-loading when the index pairs analytical files with market names.

**Recommended discovery mechanism:**
The canonical-resources table in soul.md (ARM-B / ARM-C mechanism). Specifically ARM-B's variant, which kept the table tight and routed edge cases to steering-index.md as the long-tail fallback.

Reasoning:
- Beats ARM-A on false-positive rate (10 vs 7). The index rewards thoroughness, which on simple drafting tasks = noise.
- Beats ARM-D decisively (48 vs 31). ARM-D's pointer-chain mechanism fails when the cue word isn't in the task or the core style file isn't auto-loaded — the exact failure mode flagged in the eval context.
- Generalizes cleanly to email, WBR, MBR, docs — each gets a row in the same table.
- Embodies soul.md principle #2 (structural over cosmetic) and #6 (reduce decisions, not options): the right file is the path of least resistance, no hunting required.

**One caveat:** ARM-B correctly flags the composite-task failure mode ("Slack message with projection numbers for Brandon before the MBR"). The table alone doesn't resolve precedence. The hybrid pattern — table in soul.md for common cases, steering-index.md for long tail and composites — is probably the robust answer, and is what ARM-B's reasoning implicitly describes.
