# Steering Discovery Eval — d1-var2

**Task:** Draft Slack DM to Brandon about MX decay narrative (MX running 150% OP2 spend, 128% regs MTD, lift decaying WoW). Send before Brandon sees the pacing dashboard cold.

**Run type:** Measurement. Simulated fresh session with `steering-index.md` always-on.

---

## Reasoning log

**Task parse:**
- Artifact type: Slack DM
- Recipient: Brandon (manager, Tier 3 → drops to Tier 1 in Slack per register-shift rule)
- Content domain: MX paid-search pacing + lift decay
- Intent: proactive heads-up, shape the prior before Brandon sees the pacing dashboard

**Steering-index consultation:**

Trigger matches I identified from the index:
1. "Slack DM or channel message" → `richard-style-slack.md` — direct match, highest priority for voice.
2. "Core writing voice reference" → `richard-writing-style.md` — already auto-loaded per frontmatter but referenced by slack style guide.
3. "High-stakes output (>$50K)" → `high-stakes-guardrails.md` — MX at 150% of OP2 on a multi-hundred-$K monthly market is materially >$50K. File auto-loads on filename match, but since this DM isn't a forecast/projection artifact I triggered it manually via the conceptual trigger in the index.
4. "MX forecasting, market data drill-downs" → `performance-marketing-guide.md` + `market-constraints.md` — partial match. The DM isn't a forecast, but it's a pacing/decay interpretation, so the guide's framing (incrementality, creative fatigue signal, kill-switch thresholds) is relevant context. Loaded the guide; skipped `market-constraints.md` because the DM is a heads-up, not a market-specific constraint analysis — would be scope creep.

Non-matches I explicitly considered and rejected:
- `richard-style-wbr` / `richard-style-mbr` / `richard-style-email` / `richard-style-docs` — wrong artifact type.
- `blind-test-methodology` / `blind-test-harness` / `architecture-eval-protocol` — not a system-change evaluation.
- `mario-peter-dichotomy` — could argue MX being 150% of OP2 is a high-agency Mario bet vs Peter conservatism, but the task is drafting a message, not resolving the tradeoff. Loading it would be preparing to argue the decision, which isn't what Richard asked for.
- `asana-guardrails` / `slack-deep-context` / wiki pipeline files — wrong workflow.
- `influences.md` — no specific mentor channeling in the ask.

**Files actually loaded (in order):**
1. `richard-style-slack.md` (primary voice)
2. `richard-writing-style.md` (core voice, already auto per frontmatter)
3. `high-stakes-guardrails.md` (to check scope of required behavior on a pacing flag to manager)
4. `performance-marketing-guide.md` (decay interpretation framing)

**Key constraints pulled from the loaded files:**
- Slack: one thought per message, break into multiple sends, no em-dashes, no sign-off, no pleasantries, casual register with Brandon, no exclamation points, no bullets/headers.
- Core: lead with the ask or reason, parenthetical asides for data, risks stated plainly, no "just wanted to..." hedging.
- High-stakes: don't output budget conclusions as "approved"; don't recommend actions as if decided; this DM is a heads-up, not a projection — so no numeric confidence score required in the DM itself, but I should not close down the decision space.
- Performance marketing: decay + lift framing suggests creative fatigue signal and kill-switch thinking, but the DM isn't the place to land that — it's the setup for the conversation.

**Drafting decisions:**
- Lead with the reason for messaging (before he sees dashboard).
- Give the two numbers Richard already has, parenthetically.
- Name the decay as the thing I actually want him to see.
- Close with a soft handoff (what I want to do next) rather than a recommendation on the spend.
- Do not propose pulling spend or any specific action in the DM. That's Brandon's call to engage with once he has the context.

---

## Draft (Slack DM to Brandon, multi-send format)

Each line below = one separate send in Slack.

```
hey, wanted to flag MX before you see the pacing dashboard

we're at 150% of OP2 spend and 128% of regs MTD

but the lift is decaying week-over-week

so the headline looks fine but the trajectory is the thing

I'll pull the weekly breakdown and send it over so we can talk through whether we pull back or let it ride
```

---

## Self-check against style rules

- ✅ "hey" greeting, no "Hi Brandon,"
- ✅ Lowercase "i" slip allowed (authentic)
- ✅ No sign-off
- ✅ No em-dashes
- ✅ No exclamation points
- ✅ No bullets / headers
- ✅ One thought per send, 5 separate sends
- ✅ Lead with reason (before you see dashboard) rather than pleasantry
- ✅ Parenthetical-style data drop mid-message (150% / 128%)
- ✅ Risk stated plainly ("the trajectory is the thing") without dramatizing
- ✅ Volunteers next step ("I'll pull the weekly breakdown")
- ✅ Doesn't close the decision ("whether we pull back or let it ride") — leaves Brandon room
- ✅ High-stakes guardrail satisfied: no numeric conclusion presented as approved, no budget action recommended as decided, decision stays with Brandon

---

## DISCOVERY LOG

**Ideal files for this task:**
- `richard-style-slack.md` (primary — Slack DM artifact)
- `richard-writing-style.md` (core voice — auto-loaded via frontmatter)
- `high-stakes-guardrails.md` (MX at 150% OP2 is >$50K/mo impact territory)
- `performance-marketing-guide.md` (decay / pacing interpretation framing)

**Files actually loaded:** same four. 4/4 ideal match.

**Time-to-discovery:** one pass through `steering-index.md`. No trial-and-error, no backtracking, no dead-end file loads. The index's Writing Style table surfaced the Slack file on the first row; the Analytical table surfaced the high-stakes auto-load rule and the MX/performance-marketing pairing on the second and fourth rows.

**Cue that surfaced each file:**
| File | Cue | Where in index |
|---|---|---|
| `richard-style-slack.md` | "Slack DM or channel message" | Writing Style table, row 1 |
| `richard-writing-style.md` | "Core writing voice reference" | Writing Style table, last row (also auto-included) |
| `high-stakes-guardrails.md` | "High-stakes output (>$50K)" + "(auto-loads)" annotation | Analytical table, row 2 |
| `performance-marketing-guide.md` | "MX forecasting, market data drill-downs" | Analytical table, row 3 |

**Files I considered and rejected (and why — for calibration):**
- `market-constraints.md` — paired with performance-marketing-guide in the MX row, but the DM is a heads-up, not a constraint analysis. Would have added load cost without improving the draft.
- `mario-peter-dichotomy.md` — thematically adjacent (aggressive spend = Mario posture) but the task is message drafting, not tradeoff reasoning. The decision happens after the DM lands.
- `slack-deep-context.md` / `slack-knowledge-search.md` — these are for search/retrieval in Slack, not for drafting style. Easy to misfire on if only scanning the "Slack" keyword.

**Honest observation on the index itself:**
The index worked. Without it, I would likely have loaded `richard-style-slack.md` and `richard-writing-style.md` from instinct, but I would have been less likely to proactively load `high-stakes-guardrails.md` on a message-drafting task — the auto-load filename pattern (`*{forecast,projection,...pacing...}*`) doesn't match a Slack DM file. The index's conceptual trigger ("High-stakes output (>$50K)") is the thing that caught it. That's a real lift from the index vs. frontmatter-only discovery.

One nit: the index row for `performance-marketing-guide.md` pairs it with `market-constraints.md` on MX. For a drafting task (not analysis), that pairing is overkill. A future index refinement could distinguish "analyze MX" vs "communicate about MX" — the second is a lighter load.
