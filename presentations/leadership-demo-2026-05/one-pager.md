# Kiro Orchestration Pattern — One-Pager

> **The claim:** A marketing manager built an agentic operating system for paid search, using only tools already available to every Amazon builder. Three weeks. Zero budget. This is what that looks like and what it could mean at team scale.

---

## The System in One Diagram

```
   SOURCES              ORCHESTRATION               SURFACES
   (live daily)         (agents do the work)       (humans consume)

   Slack ────────┐                                ┌──── Dashboard (live)
   Asana ────────┤    ┌─ AM Backend ─┐            ├──── Slack (brief)
   Email ────────┼───►│                ├──────────┼──── Asana (enrich)
   Hedy meetings─┤    ├─ EOD Backend ─┤            ├──── SharePoint (pub)
   Loop docs ────┤    ├─ WBR Pipeline ┤            └──── Quip (callouts)
   Calendar ─────┤    └─ Wiki Team ───┘
   MotherDuck ───┘           ▲
                             │
                             │ policy + specs + approval
                             │
                       ┌─────┴─────┐
                       │  Richard  │  (orchestrator + policy layer)
                       └───────────┘
```

---

## What's Live Today

| Capability | Built | Producer |
|---|---|---|
| Autonomous morning + EOD routine | ✓ | 6-subagent parallel backend |
| Weekly WBR callouts for 10 markets | ✓ | 3-agent pipeline with quality gate |
| Bayesian forecast pipeline | ✓ | Regime-aware, seasonally-primed |
| 6-agent wiki publishing team | ✓ | 15+ published articles, 8/10 quality bar |
| Asana portfolio auto-enrichment | ✓ | 96+ tasks across 5 projects |
| Live dashboard w/ provenance | ✓ | Every card shows its producer |
| Self-experimentation (Karpathy agent) | ✓ | Bayesian calibration of organ health |

---

## By the Numbers

- **55 tables, 8 schemas** — the MotherDuck analytics database that every agent reads from
- **47+ agent actions/day** — measurable throughput, auditable trail
- **17 Slack channels / 11 meeting series** — ingested continuously
- **10 markets** — WBR callouts produced every week
- **~1 hour/week** — ongoing calibration cost after initial build

---

## Before / After

| Workflow | Before (manual) | After (orchestrated) |
|---|---|---|
| Morning signal triage | 45 min/day | 5 min review of agent output |
| WBR callout production | 3-4 hrs/week | 20 min review; agents draft |
| Portfolio status updates | Ad hoc, inconsistent | Autonomous daily |
| Meeting prep | 30-60 min each | Pre-built brief from transcript history |
| Wiki article production | Weeks per article | 1-2 days through 6-agent pipeline |
| Cross-channel signal routing | Missed often | Autonomous, audited |

---

## The Orchestrator Pattern

Richard's job shifted from **executor** to **orchestrator + policy layer**:

1. **Write specs** — define what agents should do
2. **Set policy** — define quality gates, routing rules, safety constraints
3. **Approve output** — spot-check the 8.0+ quality work; intervene on blocked items
4. **Expand surfaces** — decide what new streams/outputs to add

Everything below that layer is agentic. Humans who aren't Richard (Lena, Alexis, Brandon) can contribute via the same surface — signals they drop get routed by the Signal Router agent.

---

## What If Resourced

Three scalable moves:

### 1. Replicate the Pattern (0-3 months)
One IC per team builds their own orchestration layer following the Kiro pattern. Marginal cost: ~1 afternoon of setup per person. Output: every marketing manager has the same productivity delta.

### 2. Productize the Orchestration Layer (3-9 months)
Turn the agent specs, hook definitions, and context schema into a reusable template. Onboarding becomes 30 minutes instead of 3 weeks. Every new team starts with the base pattern and extends.

### 3. Standardize Human↔Agent Collaboration Surfaces (9+ months)
The "Contribute" affordance + provenance bars + Agent Activity Feed become organizational defaults. Teammates contribute to each other's agents. The dashboard becomes a collaboration surface, not a report.

---

## Security & Trust Model

- **preToolUse hooks** block unsafe writes (external email, calendar invites to non-Richards, unauthorized Asana changes)
- **Read-only Slack ingestion** — agents never post without explicit human approval
- **Audit log** on every Asana write
- **Quality gates** block low-quality agent output from shipping (< 8.0 score → revision)
- **Three-layer durability** — filesystem + SharePoint + git. Any two can fail and the system recovers.

---

## What This Is Not

- **Not a replacement for engineering.** Real scale-up needs code review, hardening, and productization.
- **Not a one-click install.** Building this required ~3 weeks of focused iteration.
- **Not a "prompt engineering" toy.** The leverage comes from the architecture — specs, hooks, provenance, quality gates — not from clever prompts.

---

## Ask

Two things:

1. **Feedback on the pattern.** What would make this replicable across the org?
2. **A conversation about resourcing.** If we put 1-2 engineers behind this for a quarter, what becomes possible?

---

*Contact: Richard Williams · prichwil@amazon.com*
*Source system: `~/shared/` on DevSpaces · dashboard: local served · artifacts: SharePoint `Documents/Kiro-Drive/Artifacts/`*
