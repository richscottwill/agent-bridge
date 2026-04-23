## Conditional Next Best Action Mandate

This rule activates **only** when one or more of the following conditions are true:

- The task is high-stakes (>$50k impact, leadership-facing, or flagged by high-stakes-guardrails.md)
- There are 3 or more viable options being considered
- The agent detects internal uncertainty after loading context

When active, the agent must:

1. Explicitly identify and state **exactly one Next Best Action**.
2. End the relevant section with:
   **"Next Best Action: [single clear action]"**

This rule does **not** apply to routine daily operations or low-ambiguity tasks.
