<!-- DOC-0336 | duck_id: protocol-asana-guardrails -->
# Asana Guardrails

## Write Rules

1. **Only modify tasks assigned to Richard** (GID: `1212732742544167`). Before any CreateTask, UpdateTask, or CreateTaskStory call, verify the task is assigned to Richard or is being created by Richard.
2. **Never reassign, close, or modify tasks belonging to teammates** — read-only for team context.
3. **Draft-first for comments** — When Richard asks to comment on a teammate's task, draft the comment text for review before posting.
4. **No project-level changes** — Do not create projects, sections, or modify project settings without explicit approval.

## Read Rules (unrestricted)

- Search tasks across any project
- Read task details, comments, subtasks for any task
- Read project membership, sections, status updates
- Read goals, portfolios, user info

## Richard's Asana Identity

- User GID: `1212732742544167`
- Email: prichwil@amazon.com
- Workspace: amazon.com (GID: `8442528107068`)

## Key Projects

| Project | GID | Role | Members |
|---------|-----|------|---------|
| ABPS - WW Testing & Projects | 1205997667578893 | Owner | Richard, Brandon, Yun, Peter, Stacey, Alex |
| PS-Owned Global Testing | 1213279426031997 | Member | Brandon (owner), Richard |
| ABPS - WW Acquisition | 1206011235630048 | Member | TBD |

## Team Members (for read-only context)

- Brandon (GID: 1208504441751632) — Manager, L7
- Yun Chu (GID: 1206266932859021)
- Peter Ocampo (GID: 1204614660619574)
- Stacey Gu (GID: 1211117984143122)
- Alex VanDerStuyf (GID: 1209982366897765)

## Open Tasks Summary (64 tasks as of 2026-04-02)

### High-signal tasks for Five Levels alignment:

**Level 1 — Sharpen Yourself:**
- Testing Document for Kate (due 2026-04-01, overdue) — doc captain, foundation for OP1
- Monthly: Individual Goals update
- It's time to update your goal(s)

**Level 2 — Drive WW Testing:**
- WW weblab dial-up
- Email overlay WW rollout/testing
- OCI TT/suffix - FR to 25%
- AU NB testing focus: MRO/Trades
- Promo Test
- WW keyword gap fill based on market-level ASINs

**Level 4 — Zero-Click Future:**
- Using AI for paid search (detailed notes on inference-based optimization)

**Recurring/Operational:**
- Bi-monthly Flash
- MBR callout
- Weekly Reporting - Global WBR sheet
- Mondays - Write into EU SSR Acq Asana
- Make changes to AU/MX/PAM for the week
- Flash topics due today
- PAM R&O
- MX/AU confirm budgets

## Agentic Integration Ideas (Levels 1-5)

### Level 1 — Sharpen Yourself
- Morning routine: Pull overdue/due-today tasks into AM brief
- Weekly artifact check: Query "did Richard complete and close any tasks this week?" for streak tracking
- Surface tasks with no due date that have been open 30+ days — force a decision: do it, delegate it, or kill it

### Level 2 — Drive WW Testing
- Auto-surface test tasks with no status update in 7+ days
- Cross-reference Asana test tasks with WBR callout schedule
- Before each WBR, pull all tasks in "ABPS - WW Testing & Projects" and flag any without a written status — key metric is "every test has written status"

### Level 3 — Team Automation
- Read team tasks to pre-populate meeting agendas (AU meetings, bi-weekly with Adi)
- Surface blocked tasks across team for standup prep
- Build a "team pulse" read: how many tasks were completed this week
### Level 4 — Zero-Click Future
- The "Using AI for paid search" task is a goldmine — connect its notes to the AEO POV work
- Track AEO/AI Overviews research tasks in Asana as a dedicated section
- Use Asana task notes as a living research log that feeds the published POV

### Level 5 — Agentic Orchestration
- Asana → Slack draft: When a task is due tomorrow, draft a Slack reminder to rsw-channel
- Auto-close completed recurring tasks and create next occurrence
- Full loop: morning hook reads Asana → EOD hook checks completion → updates Asana status
