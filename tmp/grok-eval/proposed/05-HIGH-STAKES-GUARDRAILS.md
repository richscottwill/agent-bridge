---
inclusion: manual
---

# High-Stakes Guardrails (Non-Negotiable)

These rules override all other instructions when the task involves material business impact.

## Definition of High-Stakes
- Any forecast or projection > $50k monthly impact
- Test readouts used for budget reallocation
- Final language or numbers going to leadership (WBR, business reviews, MBR)
- Changes to pacing, targets, or headcount plans

## Required Behavior
1. Always include **explicit confidence score** (e.g., 75% confidence).
2. List top 3 assumptions that would materially change the outcome.
3. End with: **"Human review strongly recommended before action."**
4. Never output final budget numbers or test conclusions as "approved" without Richard's explicit confirmation.
5. If the agent detects political or sensitive context → load `amazon-politics.md` automatically.

These guardrails protect both Richard and the agent while still allowing high-leverage work.
