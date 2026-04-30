---
inclusion: always
---

# Unasked-Question Log

*Always-on steering rule. On every turn where Richard asks a question, spend 2 seconds on the meta-question: "is there an adjacent question he didn't ask that he probably should have?" 9/10 times the answer is no — noise. The 10th time — the question you almost surfaced and chose not to — gets logged to `context/active/unasked-declined.jsonl`. This is a cheap write, zero author cost beyond the judgment already happening.*

## The rule

After answering Richard's question, before closing the turn, ask:

> "Is there an adjacent question Richard didn't ask that I noticed and chose not to surface?"

If yes: append one line to `context/active/unasked-declined.jsonl`:

```json
{"ts": "2026-04-30T00:00:00Z", "original_q": "what's MX WBR look like", "adjacent_q": "should we change how we forecast MX going forward given Sparkle", "reason_declined": "outside session scope; he asked for WBR data not forecast model review", "session_id": "<current session>"}
```

If no: skip silently. Do not log noise.

## What qualifies as a declined question

**Qualifies:**
- A real question Richard would benefit from considering, that he probably hadn't thought to ask in this moment
- A question where answering it would have pulled the turn away from the original intent
- A question the answer agent actively noticed and actively chose not to raise

**Does not qualify:**
- Every possible adjacent question in the topic space (that's noise)
- Questions Richard has already addressed in prior sessions
- Questions that are too broad to be actionable ("have you thought about the strategy")
- Questions the current turn implicitly answers

## What happens with the log

- The file is read-only from Richard's perspective. He doesn't look at it.
- The weekly 1:1-prep step (before meetings with Brandon or skip-level with Kate) reads the last 7 days of entries, clusters by theme, and surfaces the 1-2 patterns that repeat. Pattern = 3+ entries with the same or closely-related `adjacent_q`.
- Entries older than 60 days rotate to `context/active/archive/unasked-declined-YYYY-MM.jsonl` to keep the live file small.

## Output format for 1:1 prep

When the 1:1-prep agent surfaces a pattern, the framing is:

> "Heads up: you've been asked about [topic] N times this week and there's a pattern. The adjacent question [X] came up 3+ times and you passed on it each time. Worth considering whether to raise it in [next 1:1 with person]."

Do not frame as "you should have asked X." Frame as "here's a pattern worth examining." Richard owns the decision to surface or not — the log's job is to make the pattern visible, not to create should-claims.

## Why this is always-on, not manual

Manual-inclusion would mean agents load this rule only when they're explicitly prepping 1:1s. But the LOGGING happens in every turn — which means the rule needs to be in-context whenever an agent is answering Richard. Always-on is correct.

Cost: 2 seconds of judgment per turn (which agents are already doing) + one file append on the 10% of turns that qualify. Negligible.

## Calibration signal

If the 1:1-prep agent is never finding patterns worth surfacing, the log is either (a) being written to too often with low-signal entries, or (b) not being written to enough because the judgment bar is too high. Check quarterly. Adjust the qualifying criteria above based on whether patterns are surfacing usefully.

If Richard reads this and thinks the log should operate differently (for example: surface high-signal declined questions same-session rather than waiting for weekly 1:1 prep), that's a karpathy-routed decision since it changes the intervention timing and touches the coaching flow.
