# amcc.md patch — replace "The Hard Thing Queue" section

**Scope:** Replace the entire section starting at `## The Hard Thing Queue` through (and including) `### Hard Thing History` in `~/shared/context/body/amcc.md`. Everything else in the file stays.

**Rationale:** The old model picked the hard thing from the Asana task queue. That manufactures targets. Testing Approach and AEO POV are both artifacts of that top-down logic — neither survives contact with the current-state question "what are signals converging on that Richard has produced no referenceable artifact for?" The new selection is signal-driven and bottom-up.

---

## Replacement text

```markdown
## The Hard Thing

At any given time, there is ONE hard thing. Not three. Not a prioritized list. One. The top-3 candidate list exists to make the choice legible — it's not a queue to work through.

### How the hard thing is found

The hard thing is not chosen from the task queue. It's discovered from cross-channel signal convergence. Specifically: the gap between "signals converging on a topic" and "Richard has produced a referenceable artifact on that topic."

**Definitions:**

- **Signal** — any mention of a topic in Slack, email, Hedy meetings, or Asana comments. Already tracked in `signals.signal_tracker`.
- **Referenceable artifact** — output another person or agent can point to. Sent email, published wiki article, merged code, Asana task consumed by someone else, decision logged in a Loop page. NOT "worked on it." NOT "have a draft in the wiki staging folder." NOT "thought about it in a meeting." Referenceable output only.
- **Window** — 7 days rolling. Older signals decay exponentially but aren't cut off.
- **Top 3** — the three highest-scoring topics at any moment. Surfaced continuously, not batched.

### Two modes a topic can qualify under

Both produce a valid hard thing. The system doesn't prefer one over the other.

| Mode | Signal pattern | Why it's hard |
|------|---------------|--------------|
| **Valuable-and-avoided** | High signal density across 2+ channels, low-or-zero Richard artifact production. Brandon or Kate keeps raising it, meetings keep hitting it, and nothing referenceable has left Richard's desk. | The avoidance IS the signal. If it were easy Richard would have shipped already. |
| **Valuable-and-latent** | Signal density building but no one — including Richard — has named it as a priority yet. Cross-channel spread is widening, authors are multiplying, no Asana task exists. | Seeing it first is the value. Naming an emerging topic before anyone asks is what L4/L5 work looks like. |

### Scoring math

```
signal_weight(t)  = base_weight × 0.5 ^ (age_days / half_life)
topic_score       = Σ signal_weight across channels
                    × impact_multiplier (L1=1.0 … L5=2.0)
                    ÷ (1 + action_recency_penalty)

incumbent_advantage: a challenger at rank 4 must score > incumbent_at_rank_3 × 1.15
                     to displace it. Prevents noise-driven churn.
```

**Defaults (tunable, see experiment queue):**
- `half_life_days = 3.5` — half of the 7-day window. At day 7, a signal is worth ~25% of its original weight. At day 14, ~6%.
- `incumbent_margin = 1.15` — challenger needs a 15% margin to displace.
- `impact_multiplier` — Level 1 = 1.0, Level 2 = 1.25, Level 3 = 1.5, Level 4 = 1.75, Level 5 = 2.0. Mapping based on topic classification against brain.md Strategic Priorities.
- `action_recency_penalty` — `max(0, 14 - days_since_last_richard_artifact)`. Suppresses a topic Richard just shipped on. Shipped today → penalty 14 → score ÷ 15. Shipped 14+ days ago or never → penalty 0 → full weight. Keeps the system from re-surfacing yesterday's work.

Full SQL and join logic live in `~/shared/context/protocols/hard-thing-selection.md`. The protocol is the executable spec; this section is the why.

### Completion threshold

A candidate is retired from the top-3 when a referenceable artifact is produced. The agent detects this via:

- Asana: a task tagged to the topic completes AND at least one non-Richard actor interacts with it (comment, assignment, story).
- Wiki: a matching article lands in `wiki.publication_registry` with status `published`.
- Email: a Richard-authored email containing the topic gets sent to a non-Richard recipient.
- Code: a commit referencing the topic merges to mainline.
- Loop/doc: a document is updated with Richard as last_editor and shared with at least one other person.

"Worked on it" does not count. "Have a draft" does not count. "Mentioned it in a meeting" does not count.

### Stickiness (incumbent advantage)

Once a topic holds the #1 slot, it needs momentum, not noise, to be displaced. A challenger at rank 4 must beat the current rank-3 holder by `incumbent_margin × score` (default 1.15×). This prevents the hard thing from flipping daily on churn.

`hard_thing_candidates.incumbent_since` records how long the current #1 has held. If it's been #1 for 7+ days with no artifact produced, escalate to rw-trainer — that's a stuck pattern, not a scoring problem.

### Null state

If no topic clears `score > 2.0` AND `channel_spread >= 2` AND `unique_authors >= 2`, the system returns:

> **No hard thing currently — signals flat.**

Do NOT manufacture one from the task queue. A flat-signal day is a legitimate state. Use it for Level 3 tooling work, delegation cleanup, or rest. Log it in the streak as a neutral day (neither hard-choice nor avoidance).

### Current top 3

Populated by `ps_analytics.main.hard_thing_candidates`. Refresh trigger: AM-Backend + after every signal-write to `signal_tracker`. View contract:

| rank | topic | score | mode | channels | authors | last_richard_artifact | incumbent_since |
|------|-------|-------|------|----------|---------|----------------------|-----------------|
| 1 | — | — | — | — | — | — | — |
| 2 | — | — | — | — | — | — | — |
| 3 | — | — | — | — | — | — | — |

The #1 row IS the hard thing. Rows 2 and 3 are context — they show what's pressing up against it, and they're what the system watches for incumbent displacement.

### Implementation intention

IF Richard opens a session, THEN the first aMCC read is:
1. Query `main.hard_thing_candidates WHERE rank = 1`.
2. Name the topic, the score, the mode, and the last referenceable artifact date.
3. If `incumbent_since > 7 days`, flag for rw-trainer escalation.
4. If null state, say so. Don't fabricate.
```

---

## What stays (do not touch)

Everything else in amcc.md is preserved:

- Preamble, operating principle, last-updated line
- `## Purpose`
- `## The Streak` (table, history note, what counts, what resets, common failures)
- `## Real-Time Intervention Protocol` (trigger detection, escalation ladder, after-intervention handling)
- `## Resistance Taxonomy`
- `## Political Awareness Layer` (all of it)
- `## Integration with Other Organs`
- `## Avoidance Ratio`
- `## Growth Model`
- `## Common Failures in Using This Organ`
- `## When to Read This File` — minor edit: add "Before naming today's hard thing, query `main.hard_thing_candidates`."

## Rationale against soul.md principles

- **Structural over cosmetic (#2):** The selection logic is structural. No emojis, no formats, no reordering. The change is about *how the hard thing is chosen*.
- **Subtraction before addition (#3):** Removes the "Current Hard Thing" table and "Hard Thing History" subsection. Replaces with a view reference. Net reduction in amcc.md length.
- **Reduce decisions, not options (#6):** Richard doesn't choose from a list of 3. The system names #1. The list exists only for legibility.
- **Invisible over visible (#5):** Once the view is populated, the aMCC read happens on every session without Richard noticing. No new ritual.
- **Protect the habit loop (#4):** The cue (session start) and reward (streak increment) are unchanged. Only the "what is the hard thing" step inside the routine changes.
