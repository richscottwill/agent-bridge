# Hard-Thing Selection Redesign — Staging Folder

Status: **Awaiting Richard's sign-off.** Do not promote to the live aMCC organ or protocols directory until Richard explicitly approves.

## What's here

| File | Purpose | Promotion target |
|------|---------|------------------|
| `amcc-patch.md` | Replacement text for the "The Hard Thing Queue" section in `~/shared/context/body/amcc.md`. Includes model description, scoring math, stickiness rule, decay, completion threshold, and the two qualification modes. | Splices into `body/amcc.md` (replaces lines under `## The Hard Thing Queue` heading through `### Hard Thing History`). |
| `hard-thing-selection.md` | Executable protocol with SQL for the scoring join, decay function, incumbent-advantage stickiness, and null-state handling. | `~/shared/context/protocols/hard-thing-selection.md` |
| `implementation-plan.md` | Table DDL (`main.hard_thing_candidates`), refresh trigger points, surface locations (AM brief / ambient / null-state), and the first experiment proposal (half-life tuning). | Reference doc; sections land in `brain.md → Strategic Priorities` and the autoresearch queue. |

## Why staged

This changes a core behavioral module. The current hard thing ("Send Testing Approach v5 to Brandon") was manufactured by the old top-down logic Richard rejected. Under the new model, today's top-3 candidates — computed live against `signals.heat_map` with a 3.5-day half-life over a 7-day window — are:

1. **polaris-brand-lp** — score 13.13 (raw 16.0, 4 channels, 8 mentions, Brandon + Alex + Dwayne + brandoxy)
2. **oci-rollout** — score 6.08 (raw 7.4, 2 channels, Brandon + Sam + brandoxy + system)
3. **au-cpa-cvr** — score 5.30 (raw 6.5, 3 channels, Brandon + Richard + brandoxy)

The old hard thing (Testing Approach → Brandon) no longer appears in the top 3 under this model because signals around it have decayed past the window. That's the point: the new system surfaces where the team's attention is converging *right now*, not where a task queue said it should be 3 weeks ago.

Run the rejection test before promoting:
- Does the top slot match what Richard would pick if asked "what does the team keep talking about that you haven't written anything referenceable on?"
- If yes → promote.
- If no → tune `half_life_days` or `impact_multiplier` weights in the protocol and re-query.

## Promotion checklist (when Richard greenlights)

1. Apply `amcc-patch.md` to `body/amcc.md` (section replacement, not append).
2. Copy `hard-thing-selection.md` to `~/shared/context/protocols/`.
3. Create `ps_analytics.main.hard_thing_candidates` per `implementation-plan.md`.
4. Wire the refresh trigger into AM-Backend and after-signal-write hooks.
5. Update `amcc.md → ## When to Read This File` to reference the protocol.
6. File the half-life tuning experiment in `autoresearch_experiments`.
7. Log the change in `changelog.md` with the rationale (Richard's rejection of manufactured hard things).

## What does NOT change

- aMCC streak mechanics — unchanged.
- Resistance taxonomy, escalation ladder, political awareness layer — unchanged.
- "What counts as choosing the hard thing" / "what resets the streak" — unchanged.
- The streak table in amcc.md — unchanged.

Only the selection logic for THE hard thing changes. Everything downstream of selection is preserved.
