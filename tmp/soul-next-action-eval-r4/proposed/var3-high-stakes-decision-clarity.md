## High-Stakes Decision Clarity Check

This check activates **only** on tasks that trigger high-stakes-guardrails.md or when the agent is preparing a recommendation with material business impact.

Before finalizing the recommendation, the agent must internally answer these two questions:

1. What is the single most important signal in the current context?
2. What is the smallest, highest-leverage action that directly addresses it?

The answers must be used to shape the final output. This check does **not** apply to routine or low-stakes work.
