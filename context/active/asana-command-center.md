# Asana Command Center Protocol

Last updated: 2026-04-15

## Purpose
Asana My Tasks is now the command center — replacing Microsoft To-Do as the canonical task list. The agent reads and writes Richard's tasks directly via the Enterprise Asana MCP.

## My Tasks Project
- Project type: User Task List
- GID: `1212732838073807`
- Name: "My Tasks in amazon.com"

## Custom Field Schema (My Tasks)

| Field | GID | Type | Options (GID → Name) |
|-------|-----|------|----------------------|
| Routine_RW | `1213608836755502` | enum | `1213608836755503` → Sweep (Low-friction), `1213608836755504` → Core Two (Deep Work), `1213608836755505` → Engine Room (Excel and Google ads), `1213608836755506` → Admin (Wind-down), `1213924412583429` → Wiki |
| Priority_RW | `1212905889837829` | enum | `1212905889837830` → Today, `1212905889837831` → Urgent, `1212905889837833` → Not urgent |
| Importance_RW | `1212905889837865` | enum | `1212905889837866` → Important |
| Begin-Date_RW | `1213440376528542` | date | — |
| Notes - Task | `1209637014993158` | text | — |

### Mapping to Microsoft To-Do Lists

| To-Do List | Asana Routine Value | When |
|------------|-------------------|------|
| 🧹 Sweep | Sweep (Low-friction) | Quick unblocking: send, confirm, triage. Cap: 5 |
| 🎯 Core | Core Two (Deep Work) | Strategic: test designs, frameworks, stakeholder docs. Cap: 4 |
| ⚙️ Engine Room | Engine Room (Excel and Google ads) | Hands-on: campaign builds, keyword changes, bids. Cap: 6 |
| 📋 Admin | Admin (Wind-down) | Budget, POs, invoices, compliance, goal updates. Cap: 3 |
| 📦 Backlog | (no Routine set) | Deferred/blocked/future — tasks without a Routine value |

### Priority Mapping

| To-Do Priority | Asana Priority_RW | Meaning |
|---------------|-------------------|---------|
| My Day | Today | Do today — surfaces in morning brief |
| High | Urgent | Do this week |
| Normal | Not urgent | Scheduled but not pressing |
| Low | (none) | Backlog/unset |

## ABPS AI Project

The ABPS AI Portfolio contains two projects — Content (autonomous document factory) and Build (system development). The Content project is the primary workspace for agent-created and agent-maintained work products.

### ABPS AI - Content (Document Factory)
- Project GID: `1213917352480610`
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1213917352480610
- Sections:
  - Intake: `1213917352480612`
  - In Progress: `1213917923741223`
  - Review: `1213917923779848`
  - Active: `1213917968512184`
  - Archive: `1213917833240629`
- Frequency Field GID: `1213921303350613`
  - One-time: `1213921303350614`
  - Weekly: `1213921303350615`
  - Monthly: `1213921303350616`
  - Quarterly: `1213921303350617`

### ABPS AI - Build (System Development)
- Project GID: `1213379551525587`
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1213379551525587
- Sections:
  - Untitled section: `1213379551525588`
  - Intake: `1213921303350623`
  - Active Development: `1213917923816097`
  - Shipped: `1213917833362766`
  - Ideas / Backlog: `1213917853421462`

### Shared Custom Fields (ABPS AI Content Project)

These fields are available on ABPS AI Content project tasks. All field names end with `_RW` (Richard Williams namespace).

| Field | GID | Type | Options (GID → Name) |
|-------|-----|------|----------------------|
| Pipeline_RW | `1213925755205188` | enum | `1213925755205189` → Idea, `1213925368050658` → Drafting, `1213925368050659` → Review, `1213925368050660` → Rewrite, `1213925368050661` → Published, `1213925368050662` → Archived |
| Audience_RW | `1213917488341145` | enum | `1213917488341146` → Leadership, `1213925368050663` → Team, `1213917488341147` → Personal, `1213917488341148` → Agent |
| Category_RW | `1213917488341137` | multi_enum | `1213917488341138` → Testing, `1213917488341139` → Strategy, `1213917488341140` → Program Details, `1213917488341141` → Tools, `1213917488341142` → Communication, `1213917488341143` → Best Practices |
| Levels_RW | `1213917488341130` | multi_enum | `1213917488341131` → L1: Sharpen Yourself, `1213917488341132` → L2: Drive WW Testing, `1213917488341133` → L3: Team Automation, `1213917488341134` → L4: Zero-Click Future, `1213917488341135` → L5: Agentic Orchestration |
| Frequency_RW | `1213921303350613` | enum | `1213921303350614` → One-time, `1213921303350615` → Weekly, `1213921303350616` → Monthly, `1213921303350617` → Quarterly |
| Series_RW | `1213917488341099` | text | Groups related articles (e.g., "Kate Doc", "OCI") |
| Path_RW | `1213917488341150` | text | Local file path (e.g., ~/shared/artifacts/strategy/2026-04-04-oci-business-case.md) |
| Routine_RW | `1213608836755502` | enum | (inherited from My Tasks — all wiki tasks use Wiki option `1213924412583429`) |
| Priority_RW | `1212905889837829` | enum | (inherited from My Tasks) |
| Kiro_RW | `1213915851848087` | text | Agent scratchpad — pipeline state, sync timestamps, critic scores |
| Next-action_RW | `1213921400039514` | text | Next concrete step for the task |
| Begin-Date_RW | `1213440376528542` | date | Execution window start |

### Pipeline Stage Workflow (replaces section-based tracking)

Pipeline_RW is the canonical pipeline stage. Sections are now used for topic grouping, not pipeline tracking.

| Pipeline_RW Value | Meaning | Who Moves It Here | Next Step |
|-------------------|---------|-------------------|-----------|
| Idea | Raw topic — not yet assigned to researcher | Editor or Richard | Editor triages → Drafting |
| Drafting | Researcher gathering sources, writer drafting | Editor assigns | Writer completes → Review |
| Review | Critic scoring (5 dimensions, 8/10 bar) | Writer moves after draft | Critic scores → Published or Rewrite |
| Rewrite | Critic scored <8, revision notes provided | Critic moves back | Writer revises → Review (max 2 cycles) |
| Published | Scored >=8, approved, content synced to Asana | Critic/Librarian | Librarian maintains |
| Archived | Superseded, merged, or killed | Editor decides | No further action |

### Audience_RW Mapping

| Audience | Writing Standard | Review Rubric | Who Reads It |
|----------|-----------------|---------------|-------------|
| Leadership | Amazon narrative standard (prose-driven, 18-20 word sentences, purpose first, data embedded) | Strict — Kate wouldn't change a word | Kate, Todd, cross-org |
| Team | Actionable execution standard (how-to, checklists OK, step-by-step) | Practical — teammate can follow without asking | Brandon, peers, market owners |
| Personal | Lighter review — Richard's working docs | Functional — serves Richard's needs | Richard only |
| Agent | Machine-readable, structured for extraction | Structural — frontmatter, AGENT_CONTEXT, cross-refs | Agent swarm |
| Kiro_RW | `1213915851848087` | text | Agent scratchpad |
| Begin-Date_RW | `1213440376528542` | date | Execution window start (`start_on`) |
| Next-action_RW | `1213921400039514` | text | Next concrete step for the task |
| Levels_RW | `1213917488341130` | multi_enum | L1–L5 classification. Options: L1 Sharpen (`1213917488341131`), L2 Testing (`1213917488341132`), L3 Automation (`1213917488341133`), L4 Zero-Click (`1213917488341134`), L5 Agentic (`1213917488341135`) |
| Category_RW | `1213917488341137` | multi_enum | Content category. Options: Testing (`1213917488341138`), Strategy (`1213917488341139`), Program Details (`1213917488341140`), Tools (`1213917488341141`), Communication (`1213917488341142`), Best Practices (`1213917488341143`) |
| Audience_RW | `1213917488341145` | enum | Target audience. Options: Leadership (`1213917488341146`), Team (`1213925368050663`), Personal (`1213917488341147`), Agent (`1213917488341148`) |
| Path_RW | `1213917488341150` | text | Local file path for the work product artifact |
| Series_RW | `1213917488341099` | text | Series grouping for related articles |
| Pipeline_RW | `1213925755205188` | enum | Pipeline stage. Options: Idea (`1213925755205189`), Drafting (`1213925368050658`), Review (`1213925368050659`), Rewrite (`1213925368050660`), Published (`1213925368050661`), Archived (`1213925368050662`) |
| Frequency_RW | `1213921303350613` | enum | Update cadence |

### GID Discovery Protocol

When setting up a new ABPS AI project or verifying configuration:

1. `AsanaSearch(query="ABPS AI", resource_type="project")` → find project GIDs
2. `GetProjectSections(project_gid)` → record all section GIDs
3. `GetTaskDetails` on any project task → inspect `custom_fields` array for field GIDs (Frequency, Routine, etc.)
4. If a custom field doesn't exist: create it via Asana UI (no CreateCustomField tool in MCP), then re-read
5. Record all discovered GIDs in this section of `asana-command-center.md`

### Section Workflow (Content Project)

| Section | Purpose | Tasks Move Here When |
|---------|---------|---------------------|
| Intake | Raw ideas from Richard | Richard creates task or agent proposes |
| In Progress | Pipeline active (research/draft) | Begin Date <= today, triage approved |
| Review | Draft complete, awaiting critic + approval | wiki-writer finishes ~500w draft |
| Active | Approved, expanded, living documents | Richard approves + wiki-writer expands |
| Archive | One-time docs, completed | One-time frequency, post-expansion |

## Portfolio Projects

Two portfolios contain Richard's active market and program projects. The agent discovers children dynamically via `GetPortfolioItems` and records profiles here.

### ABIX PS Portfolio (`1212775592612914`)

Children discovered via `GetPortfolioItems(portfolio_gid="1212775592612914")`: AU, MX.

#### AU (`1212762061512767`)
- Portfolio: ABIX PS (`1212775592612914`)
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1212762061512767
- Sections:
  - Planning: `1212762061512769`
  - Milestones: `1212762061512776`
  - Next steps: `1212762061512777`
  - Comms Plan: `1212762061512778`
  - Complete: `1213924252564467`
- Terminal Sections: Complete (`1213924252564467`)
- Custom Fields (project-specific):
  - Priority: `1212762061512785` (enum)
  - Task Progress: `1212762061512790` (enum)
- Custom Fields (inherited from My Tasks):
  - Priority_RW: `1212905889837829`, Importance_RW: `1212905889837865`, Notes - Task: `1209637014993158`, Begin-Date_RW: `1213440376528542`, Routine_RW: `1213608836755502`, Kiro_RW: `1213915851848087`, Next-action_RW: `1213921400039514`
- Some tasks also carry: Date diff (`1213440376802787`), MX Priority (`1212775592612935`), MX Task Progress (`1212762061512741`), Important/Urgent (`1200200115836714`), Time Left (`1207564683818996`) — these appear on multi-homed tasks shared with MX or Paid App
- Pinned Context Task: `1213917747438931` (📌 AU — Market Context (Kiro))
- Active: yes

##### Recurring Task Patterns (AU)

The agent detects completed tasks matching these patterns during AM-2 Phase 1C and auto-creates the next instance with computed dates (Requirement 13.1).
| AU meetings Agenda | Weekly | Next steps (`1212762061512777`) | due_on = prev_due_on + 7d; start_on = due_on - 2d |
| MBR callout | Monthly | Milestones (`1212762061512776`) | due_on = same day next month; start_on = due_on - 5d |
| Bi-monthly Flash | Bi-monthly | Milestones (`1212762061512776`) | due_on = prev_due_on + 14d; start_on = due_on - 3d |

**Detection keywords:** Weekly, Reporting, Agenda, MBR, Bi-monthly, Flash
**Project-specific fields to copy:** AU Priority (`1212762061512785`), Task Progress (`1212762061512790`)

#### MX (`1212775592612917`)
- Portfolio: ABIX PS (`1212775592612914`)
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1212775592612917
- Sections:
  - Planning: `1212775592612919`
  - Milestones: `1212775592612926`
  - Next steps: `1212775592612927`
  - Comms Plan: `1212775592612928`
  - Complete: `1213924047255341`
- Terminal Sections: Complete (`1213924047255341`)
- Custom Fields (project-specific):
  - Priority: `1212775592612935` (enum)
  - Task Progress: `1212762061512741` (enum)
- Custom Fields (inherited from My Tasks):
  - Priority_RW: `1212905889837829`, Importance_RW: `1212905889837865`, Notes - Task: `1209637014993158`, Begin-Date_RW: `1213440376528542`, Routine_RW: `1213608836755502`, Kiro_RW: `1213915851848087`, Next-action_RW: `1213921400039514`
- Some tasks also carry: AU Priority (`1212762061512785`), AU Task Progress (`1212762061512790`), Important/Urgent (`1200200115836714`), Time Left (`1207564683818996`), Date diff (`1213440376802787`) — multi-homed tasks
- Cross-team fields (on Vijeth/MCS tasks): MCSOpsSprint # (`1210696086448065`), MCS Status (`1210695351001980`), MCSOpsPlanned (`1211096369985794`), MCS-authoring-task-type (`1210831625635211`), MCS Initiative (`1210688295507229`), ReleaseTech (`1210696085033654`), MCS Sub-Initiative (`1210688295507253`)
- Pinned Context Task: `1213917639688517` (📌 MX — Market Context (Kiro))
- Active: yes

##### Recurring Task Patterns (MX)

The agent detects completed tasks matching these patterns during AM-2 Phase 1C and auto-creates the next instance with computed dates (Requirement 13.1).

| Task Name Pattern | Cadence | Section | Date Computation |
|-------------------|---------|---------|-----------------|
| Weekly Reporting / WBR | Weekly | Next steps (`1212775592612927`) | due_on = prev_due_on + 7d; start_on = due_on - 2d |
| MBR callout | Monthly | Milestones (`1212775592612926`) | due_on = same day next month; start_on = due_on - 5d |
| Bi-monthly Flash | Bi-monthly | Milestones (`1212775592612926`) | due_on = prev_due_on + 14d; start_on = due_on - 3d |
| Kingpin | Monthly | Milestones (`1212775592612926`) | due_on = same day next month; start_on = due_on - 5d |

**Detection keywords:** Weekly, Reporting, WBR, MBR, Bi-monthly, Flash, Kingpin
**Project-specific fields to copy:** MX Priority (`1212775592612935`), MX Task Progress (`1212762061512741`)

### ABPS Portfolio (`1212762061512816`)

Children discovered via `GetPortfolioItems(portfolio_gid="1212762061512816")`: ABPS - NA, ABPS - JP, ABPS - EU5.

**Note:** WW Testing (`1205997667578893`), WW Acquisition (`1206011235630048`), and Paid App (`1205997667578886`) are NOT children of the ABPS portfolio — they are standalone projects in Richard's workspace. They are documented below as managed projects outside the portfolio hierarchy.

#### ABPS - NA (`1205997667578854`)
- Portfolio: ABPS (`1212762061512816`)
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1205997667578854
- Sections:
  - Backlog: `1206020650712113`
  - Prioritized: `1205997667578855`
  - In progress: `1205997667578862`
  - Blocked: `1205997667578864`
  - Complete: `1205997667578863`
- Terminal Sections: Complete (`1205997667578863`)
- Active: no (Richard owns but is not hands-on)

#### ABPS - JP (`1205997667578874`)
- Portfolio: ABPS (`1212762061512816`)
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1205997667578874
- Sections:
  - Backlog: `1206020650712112`
  - Prioritized: `1205997667578875`
  - In progress: `1205997667578876`
  - Blocked: `1205997667578878`
  - Complete: `1205997667578877`
- Terminal Sections: Complete (`1205997667578877`)
- Active: no (Richard owns but is not hands-on)

#### ABPS - EU5 (`1205997667578868`)
- Portfolio: ABPS (`1212762061512816`)
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1205997667578868
- Sections:
  - Backlog: `1206020650712111`
  - Prioritized: `1205997667578869`
  - In progress: `1205997667578870`
  - Blocked: `1205997667578872`
  - Complete: `1205997667578871`
- Terminal Sections: Complete (`1205997667578871`)
- Active: no (Richard owns but is not hands-on)

### Managed Projects (Outside Portfolio Hierarchy)

These projects are in Richard's workspace and actively managed, but are not children of ABIX PS or ABPS portfolios.

#### WW Testing & Projects (`1205997667578893`)
- Owner: Richard Williams (`1212732742544167`)
- URL: https://app.asana.com/1/8442528107068/project/1205997667578893
- Sections:
  - WW Doc Inputs: `1206497184489067`
  - Prioritized: `1205997667578894`
  - In progress: `1205997667578901`
  - Blocked: `1205997667578903`
  - Backlog: `1206020650712107`
  - Complete: `1205997667578902`
- Terminal Sections: Complete (`1205997667578902`)
- Custom Fields (project-specific):
  - Status C-week: `1211898465243458` (enum)
  - Help Needed flag: `1211898253103683` (multi_enum)
  - Status L-week: `1211898253103687` (enum)
  - Impact (EU Reg): `1211898253103663` (number)
  - Marketplace/Region: `1212629048694011` (multi_enum)
  - ATL/BTL?: `1212663856382198` (enum)
  - Tech PM: `1203721406585927` (people)
  - OPS Impact: `1211349736814429` (number)
- Custom Fields (inherited from My Tasks): Priority_RW, Importance_RW, Notes - Task, Begin-Date_RW, Routine_RW, Kiro_RW, Next-action_RW
- Some tasks also carry: Time Left (`1207564683818996`), Important/Urgent (`1200200115836714`), Date diff (`1213440376802787`)
- Pinned Context Task: `1213917851621567` (📌 WW Testing — Project Context (Kiro))
- Active: yes

#### WW Acquisition (`1206011235630048`)
- Owner: Richard Williams (member, not project owner)
- URL: https://app.asana.com/1/8442528107068/project/1206011235630048
- Sections:
  - Backlog: `1206020650712109`
  - Prioritized: `1206011235630049`
  - In progress: `1206011240457088`
  - Blocked: `1206011240457092`
  - Complete: `1206011240457091`
- Terminal Sections: Complete (`1206011240457091`)
- Custom Fields (inherited from My Tasks): Priority_RW, Importance_RW, Notes - Task, Begin-Date_RW, Routine_RW, Kiro_RW, Next-action_RW
- Some tasks also carry: Time Left (`1207564683818996`), Status C-week (`1211898465243458`), Help Needed flag (`1211898253103683`)
- Pinned Context Task: `1213917771203342` (📌 WW Acquisition — Team Context (Kiro))
- Active: yes

#### Paid App (`1205997667578886`)
- Owner: Richard Williams (member, not project owner)
- URL: https://app.asana.com/1/8442528107068/project/1205997667578886
- Sections:
  - Backlog: `1206020650712110`
  - Prioritized: `1205997667578887`
  - In progress: `1205997667578888`
  - Blocked: `1205997667578890`
  - Complete: `1205997667578889`
- Terminal Sections: Complete (`1205997667578889`)
- Custom Fields (project-specific):
  - Important/Urgent: `1200200115836714` (enum)
  - Time Left: `1207564683818996` (number)
- Custom Fields (inherited from My Tasks): Priority_RW, Importance_RW, Notes - Task, Begin-Date_RW, Routine_RW, Kiro_RW, Next-action_RW
- Some tasks also carry: Date diff (`1213440376802787`), AU/MX Priority and Task Progress fields (multi-homed tasks)
- Pinned Context Task: `1213917771155873` (📌 Paid App — Project Context (Kiro))
- Active: yes

##### Event Calendar (Paid App)

The agent uses this calendar to drive event countdown automation (Requirement 15.1). During AM-2 Phase 1C, tasks whose names match event keywords are scanned for escalation when the event enters its prep or escalation window.

| Event | Approximate Date | Prep Window | Escalation Trigger | Keywords |
|-------|-----------------|-------------|-------------------|----------|
| Prime Day | Mid-June | 30 days before | 14 days before | prime day, prime, PD |
| Back to School | Late July | 21 days before | 10 days before | back to school, BTS, school |
| PBBD (Prime Big Deals Day) | Mid-October | 30 days before | 14 days before | PBBD, prime big deal, big deals day |
| BFCM (Black Friday/Cyber Monday) | Late November | 45 days before | 21 days before | BFCM, black friday, cyber monday, BF, CM |
| Gift Guide | Early December | 30 days before | 14 days before | gift guide, gift, holiday guide |

**Event keyword matching rules:**
- Match is case-insensitive against task name
- Any keyword from the Keywords column triggers a match
- A task can match multiple events (rare but possible for cross-event tasks)
- Matching drives three behaviors: prep window escalation (Backlog → Prioritized), escalation trigger (Prioritized → In progress + Today), and critical blocker flagging (Blocked + escalation trigger)

### GID Discovery Protocol (Portfolio Projects)

When setting up a new portfolio project or verifying configuration:

1. `GetPortfolioItems(portfolio_gid)` → enumerate child projects (GID + name + owner)
2. `GetProjectSections(project_gid)` → record all section GIDs, identify terminal sections (Complete/Done)
3. `GetTasksFromProject(project_gid)` → get first task assigned to Richard
4. `GetTaskDetails(task_gid, opt_fields="custom_fields.name,custom_fields.gid,custom_fields.type")` → discover available custom fields
5. If a new project appears not recorded here → flag for Richard: "New project detected in [portfolio]: [name]. GIDs recorded."
6. Record all discovered GIDs in this section of `asana-command-center.md`
7. Check for pinned context task (name pattern: "📌 [Project] — ... Context (Kiro)"). If none exists, create one.

### Cross-Project Field Availability Summary

| Field | GID | AU | MX | WW Testing | WW Acq | Paid App |
|-------|-----|----|----|------------|--------|----------|
| Priority_RW | `1212905889837829` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Importance_RW | `1212905889837865` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Routine_RW | `1213608836755502` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kiro_RW | `1213915851848087` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Next-action_RW | `1213921400039514` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Begin-Date_RW | `1213440376528542` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Notes - Task | `1209637014993158` | ✅ | ✅ | ✅ | ✅ | ✅ |
| AU Priority | `1212762061512785` | ✅ | — | — | — | — |
| AU Task Progress | `1212762061512790` | ✅ | — | — | — | — |
| MX Priority | `1212775592612935` | — | ✅ | — | — | — |
| MX Task Progress | `1212762061512741` | — | ✅ | — | — | — |
| Important/Urgent | `1200200115836714` | ⚡ | ⚡ | ⚡ | — | ✅ |
| Time Left | `1207564683818996` | ⚡ | ⚡ | ⚡ | ⚡ | ✅ |
| Status C-week | `1211898465243458` | — | — | ✅ | ⚡ | — |
| Help Needed flag | `1211898253103683` | — | — | ✅ | ⚡ | — |

✅ = native to project, ⚡ = appears on multi-homed tasks only, — = not present

## View Structure
Richard's My Tasks view:
- Grouped by: Routine_RW (first), then Priority_RW
- Sorted by: Due date
- Filtered: Incomplete tasks only

## Agent Read Protocol (Morning Routine — AM-1/AM-2)

### AM-1: Ingest
1. Pull all incomplete tasks assigned to Richard: `SearchTasksInWorkspace(assignee_any=1212732742544167, completed=false)`
2. For tasks due today or overdue, get full details including custom fields
3. Categorize by Routine_RW field into Sweep/Core/Engine Room/Admin/Backlog
4. Flag: tasks with Priority_RW = "Today" that have no Routine_RW (needs triage)
5. Flag: tasks overdue by 7+ days (stale — decision needed: do, delegate, kill)

### AM-2: Triage + Draft
1. Read the categorized task list from AM-1
2. For each Routine bucket, check against caps (Sweep: 5, Core: 4, Engine Room: 6, Admin: 3)
3. If over cap, flag lowest-priority tasks for demotion to Backlog
4. Surface "Today" tasks in the daily brief
5. Draft any reply/send tasks that are in Sweep

### AM-3: Brief
1. Include in daily brief:
   - 🧹 Sweep (today): [list]
   - 🎯 Core (today): [list]
   - ⚙️ Engine Room (today): [list]
   - 📋 Admin (today): [list]
   - ⚠️ Overdue: [count] tasks, oldest: [name, days overdue]
   - 📦 Backlog needing triage: [count]

## Agent Write Protocol

### Interactive Command Center (AM-2 Phase 2)
During AM-2, the agent presents the task board and executes Richard's directions in real-time. This is the primary task management interface — not just ingestion, but active curation.

**Supported operations:**
- Move tasks between Routine_RW buckets
- Change due dates
- Change Priority_RW (Today/Urgent/Not urgent)
- Create new tasks with Routine_RW + Priority pre-set
- Write/update task descriptions (notes or html_notes)
- Add comments (CreateTaskStory)
- Complete tasks
- Create subtasks
- Set Importance_RW

**Agent-initiated proposals:** The agent doesn't just wait — it proposes changes based on overdue tasks, bucket overflows, untriaged items, stale tasks, and due date conflicts. Richard approves, modifies, or gives new directions.

### Setting Priority_RW
```
UpdateTask(task_gid, custom_fields={"1212905889837829": "1212905889837830"})  // Today
UpdateTask(task_gid, custom_fields={"1212905889837829": "1212905889837831"})  // Urgent
UpdateTask(task_gid, custom_fields={"1212905889837829": "1212905889837833"})  // Not urgent
```

### Setting Routine_RW
```
UpdateTask(task_gid, custom_fields={"1213608836755502": "1213608836755503"})  // Sweep
UpdateTask(task_gid, custom_fields={"1213608836755502": "1213608836755504"})  // Core Two
UpdateTask(task_gid, custom_fields={"1213608836755502": "1213608836755505"})  // Engine Room
UpdateTask(task_gid, custom_fields={"1213608836755502": "1213608836755506"})  // Admin
```

### Setting Importance_RW
```
UpdateTask(task_gid, custom_fields={"1212905889837865": "1212905889837866"})  // Important
```

## EOD-2: System Refresh
1. Pull task completion count for the day
2. Update rw-tracker.md with daily task stats
3. Flag tasks that were "Today" but not completed — carry forward or demote?
4. Check for new tasks assigned to Richard since morning (from team activity)

## Guardrail Protocol

Every Asana write operation — whether from AM-2, a pipeline agent (wiki-editor, wiki-researcher, wiki-writer, wiki-critic), or an on-demand command — MUST follow this protocol. No exceptions.

### 1. Pre-Write Verification (Assignee Check)

Before ANY write operation (`UpdateTask`, `CreateTask`, `CreateTaskStory`) on an ABPS_AI_Project task:

```
1. GetTaskDetails(task_gid) → read assignee
2. VERIFY: task.assignee.gid === "1212732742544167" (Richard Williams)
3. IF assignee matches → proceed to step 2 (Audit Log) then execute write
4. IF assignee does NOT match → BLOCK the write, do NOT execute it
   a. Log to audit log with result="blocked" (see format below)
   b. Write Kiro_RW entry: "[date] BLOCKED: Write attempted on task not assigned to Richard (assignee: [gid])"
   c. Flag in daily brief: "⛔ Blocked write on [task_name] — not assigned to Richard"
```

For My Tasks writes: the existing guard-asana hook enforces ownership. For ABPS_AI_Project writes: this protocol is the enforcement layer. Both use the same principle — only modify tasks assigned to Richard.

### 2. Audit Log (Every Write Operation)

Every write operation appends one JSON line to `~/shared/context/active/asana-audit-log.jsonl`. This is append-only — never overwrite, never truncate.

**Format for ABPS AI Project writes (extended fields):**

```json
{"timestamp":"2026-04-15T08:30:00Z","tool":"UpdateTask","task_gid":"1234567890123","task_name":"AEO Strategy Guide","project":"ABPS_AI_Project","pipeline_agent":"wiki-writer","pipeline_stage":"draft","fields_modified":["html_notes"],"result":"success","notes":"500w draft written"}
```

**Field definitions:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timestamp` | ISO 8601 | yes | UTC timestamp of the operation |
| `tool` | string | yes | Asana MCP tool name: `UpdateTask`, `CreateTask`, `CreateTaskStory` |
| `task_gid` | string | yes | Asana task GID |
| `task_name` | string | yes (ABPS) | Human-readable task name for audit readability |
| `project` | string | yes (ABPS) | `"ABPS_AI_Project"` for Content project tasks, `"ABPS_AI_Build"` for Build project tasks, `"My_Tasks"` for My Tasks writes |
| `pipeline_agent` | string | ABPS only | Which wiki agent acted: `wiki-editor`, `wiki-researcher`, `wiki-writer`, `wiki-critic`, or `null` for non-pipeline writes |
| `pipeline_stage` | string | ABPS only | Current stage: `triage`, `research`, `draft`, `review`, `expansion`, `refresh`, or `null` |
| `fields_modified` | array | yes | List of fields changed: `["html_notes"]`, `["custom_fields.Kiro_RW"]`, `["completed"]`, etc. |
| `result` | string | yes | `"success"`, `"failure"`, `"blocked"`, `"retry_success"`, `"retry_failure"` |
| `notes` | string | optional | Human-readable context: what was done and why |

**Format for My Tasks writes (existing format, backward-compatible):**

```json
{"timestamp":"2026-04-03T04:29:37Z","tool":"UpdateTask","task_gid":"1213531814325315","fields_modified":["completed"],"result":"auto-write","rule":"whitelist","note":"AU invoice confirmed submitted"}
```

My Tasks writes continue using the existing format with `rule` and `note` fields. ABPS writes use the extended format with `project`, `pipeline_agent`, `pipeline_stage`, `task_name`, and `notes`. Both formats coexist in the same JSONL file.

**When to log:**
- BEFORE executing the write: prepare the log entry
- AFTER the write completes: append with `result="success"` or `result="failure"`
- ON BLOCK: append immediately with `result="blocked"` (the write was never executed)
- ON RETRY: append the retry result as `result="retry_success"` or `result="retry_failure"`

### 3. Read-Before-Write Pattern (html_notes Protection)

Before ANY `UpdateTask(html_notes=...)` call on an ABPS_AI_Project task:

```
1. GetTaskDetails(task_gid) → read current html_notes content
2. Parse Kiro_RW for the most recent agent write timestamp
   (look for patterns like "pipeline: draft completed [date]" or "pipeline: expanded [date]")
3. Compare: has Richard added content since the last agent write?
   - Check GetTaskStories(task_gid) for comments or edits by Richard
     (created_by.gid === "1212732742544167") after the Kiro_RW timestamp
   - If the html_notes content differs from what the agent last wrote
     AND Richard has activity after the agent's last write → Richard added content

4. IF Richard added content since last agent write:
   a. PRESERVE Richard's additions — do NOT overwrite them
   b. Integrate agent content AROUND Richard's additions:
      - If Richard added a section: keep it in place, add agent content before/after
      - If Richard edited existing text: keep Richard's version of that text
      - If Richard added notes at the top/bottom: preserve them, add agent content in the appropriate location
   c. Log in Kiro_RW: "[date] Read-before-write: Richard additions detected and preserved"

5. IF no Richard additions detected:
   a. Safe to write new content (overwrite is acceptable)
   b. Proceed with the UpdateTask(html_notes=...) call

6. ALWAYS update Kiro_RW with a timestamp after writing html_notes:
   "[date] html_notes updated by [agent_name] — [brief description]"
   This timestamp becomes the baseline for the next read-before-write check.
```

This pattern applies to ALL html_notes writes: drafts (Stage 2), expansions (Stage 5), and refreshes. The wiki-writer agent must implement this check before every html_notes update.

### 4. API Failure Retry Logic

When any Asana API call fails during an ABPS_AI_Project operation:

```
1. ON FIRST FAILURE:
   a. Log to audit log with result="failure" and notes describing the error
   b. Write Kiro_RW entry: "[date] API FAILURE: [tool] failed on [task_name] — [error summary]. Retrying once."
   c. Wait 2 seconds (brief pause before retry)
   d. RETRY the exact same API call — one retry, no more

2. IF RETRY SUCCEEDS:
   a. Log to audit log with result="retry_success"
   b. Update Kiro_RW: append "Retry succeeded."
   c. Continue pipeline execution normally

3. IF RETRY FAILS:
   a. Log to audit log with result="retry_failure"
   b. Update Kiro_RW: "[date] API FAILURE (permanent): [tool] failed on [task_name] after retry. FLAGGED FOR MANUAL ATTENTION."
   c. FLAG for daily brief: "🔴 API failure on [task_name] — [tool] failed after retry. Manual attention needed."
   d. SKIP this task in the current pipeline run — do NOT attempt further operations on it
   e. The task will be retried on the next AM-2 cycle (next morning)

4. CONSTRAINTS:
   - Maximum ONE retry per failure per API call
   - No exponential backoff — single 2-second pause then retry
   - No retry loops — if the retry fails, stop and flag
   - Read failures (GetTaskDetails, GetSubtasksForTask, etc.): log and skip the task for this cycle
   - Write failures (UpdateTask, CreateTask, CreateTaskStory): log, retry once, flag if still failing
   - Audit log write failures: write to stderr, continue operation (never block pipeline on audit failure)
```

### Guardrail Summary (Quick Reference)

| Check | When | Action on Violation |
|-------|------|-------------------|
| Assignee = Richard | Before every ABPS write | Block write, log `result="blocked"`, alert in brief |
| Audit log append | After every write (success or failure) | Append JSON line to `asana-audit-log.jsonl` |
| Read-before-write | Before every `html_notes` update | Read current content, preserve Richard's additions |
| Kiro_RW brevity | After every task modification | `M/D: <concise status>`. Use M/D date format. No YYYY-MM-DD. 500-char field limit is the only constraint. |
| Next-action_RW update | After every task modification | Set Next-action_RW field to the single most specific next step |
| API retry | On any API failure | Log, retry once, flag for manual attention if retry fails |
| Triage approval | Before executing triage field writes | Present to Richard, wait for approval |
| Expansion approval | Before expanding draft to full doc | Require completed Approval subtask |
| Critic escalation | After 2 consecutive sub-8 scores | Stop iterating, flag for Richard |

### 5. Kiro_RW Brevity Rule

Kiro_RW is a glanceable scratchpad, not a journal. Every entry MUST be:
- **Format:** `M/D: <status in under 10 words>`
- **Date format:** Always `M/D` (e.g., `4/3`, `12/15`). Never `YYYY-MM-DD`, never `[M/D]`, never `MM/DD`.
- **Length:** No hard word limit. Be concise but include what's useful — blockers, context, status, cross-references. The 500-char field limit is the only constraint.
- **Examples:**
  - `4/3: Triaged. Core, quarterly, guide.`
  - `4/3: Research posted. Draft next.`
  - `4/3: Draft done. Moved to Review.`
  - `4/3: Critic 8.2/10. Approval created.`
  - `4/3: Approved. Expanding to 2000w.`
  - `4/3: Expanded. Active. Monthly refresh.`
  - `4/3: OVERDUE 3d. Extend or kill.`
  - `4/3: API fail. Retry succeeded.`
- **Anti-patterns (do NOT write):**
  - ❌ `[4/3] TRIAGE: Routine=Core, Priority=Not urgent, Freq=quarterly, Type=guide. Scope: Comprehensive AU keyword strategy...`
  - ❌ `2026-04-03: Pipeline research stage completed for wiki-researcher agent`
  - ❌ `pipeline: draft completed [2026-04-03]`
- **Append rule:** New entries go on a new line below existing content. Oldest entries get dropped if approaching the 500-char limit.

### 6. Next-action_RW Field Protocol

The Next-action_RW field (GID: `1213921400039514`) must be updated on EVERY task modification — ABPS AI and My Tasks alike. It answers: "What is the single most specific thing to do next?"

- **Format:** One sentence, imperative verb, specific. Must add information beyond the task title — don't repeat what the name already says. Focus on the specific next step, blocker, person to contact, or decision to make.
- **Examples:**
  - `Draft 500w keyword strategy guide from research brief`
  - `Review critic feedback and approve or request revision`
  - `Extend due date to 4/17 — blocked on MX data`
  - `Complete approval subtask to trigger expansion`
  - `Run quarterly refresh — pull Q2 AU metrics`
- **When to update:**
  - After triage: next action = what the pipeline will do first
  - After each pipeline stage: next action = what happens next
  - After approval: next action = expansion instruction
  - After expansion: next action = refresh cadence note or "Complete — living doc"
  - On overdue/escalation: next action = Richard's decision needed
- **API call:** `UpdateTask(task_gid, custom_fields={"1213921400039514": "next action text"})`
- **Applies to:** ALL tasks the agent touches — ABPS AI Content, ABPS AI Build, My Tasks, any project.

### Legacy Guardrails (My Tasks — unchanged)

These rules continue to apply for My Tasks operations outside the ABPS AI pipeline:
- Only modify tasks assigned to Richard
- Never touch teammate tasks
- Draft-first for comments on others' tasks
- No project-level changes without approval

## Signal-to-Routine Mapping (Slack/Email → Asana)

When the agent creates Asana tasks from Slack [ACTION-RW] signals or email action items, use this mapping to set Routine + Priority_RW:

| Signal Type | Examples | Routine_RW | Priority_RW |
|-------------|----------|---------|-------------|
| Quick reply/send/confirm | "Reply to Vijeth", "Confirm budget with Kate", "Send AU update" | Sweep (Low-friction) | Today |
| Strategic discussion/artifact | "Draft testing framework", "Write AEO POV", "Prepare OP1 section" | Core Two (Deep Work) | Urgent |
| Campaign/keyword/bid work | "Update MX bids", "Add negative keywords", "Pull WBR data", "Build campaign" | Engine Room (Excel and Google ads) | Today |
| Admin/budget/invoice | "Submit PO", "Review invoice", "Update compliance tracker", "Budget reconciliation" | Admin (Wind-down) | Today |
| Unclear/ambiguous | Signal doesn't clearly map to a bucket | (none — Backlog) | (none — flag for triage) |

**Decision detection keywords:** When a Slack thread contains any of these keywords, the agent queues the decision for Project Notes "Recent Decisions & Changes" update:
- "decided", "agreed", "confirmed", "approved", "going with", "final call", "locked in"

## Five Levels — Project-to-Level Mapping

Each Asana task maps to a Five Levels alignment based on its project membership and content. Used by AM-3 (daily brief annotations) and EOD-2 (level breakdown in EOD summary).

| Level | Label | Projects / Signals | GIDs |
|-------|-------|-------------------|------|
| L1 | Sharpen Yourself | Goal tracking tasks, streak data, artifact tasks, individual goals update | (goal tasks, no single project) |
| L2 | Drive WW Testing | WW Testing & Projects | `1205997667578893` |
| L2 | Drive WW Testing | PS-Owned Global Testing | `1213279426031997` |
| L2 | Drive WW Testing | Paid App | `1205997667578886` |
| L2 | Drive WW Testing | PS ENG | `1213235338214787` |
| L2 | Drive WW Testing | AU | `1212762061512767` |
| L2 | Drive WW Testing | MX | `1212775592612917` |
| L3 | Team Automation | Team visibility tasks, meeting prep, cross-team collaboration tasks | (detected by content/context) |
| L4 | Zero-Click Future | AI/AEO research tasks, "Using AI for paid search", AEO POV work | (detected by task name/content) |
| L5 | Agentic Orchestration | Agentic loop tasks, Kiro_RW as persistent memory, full AM→EOD loop | (detected by task name/content) |
| L5 | Agentic Orchestration | ABPS AI - Content (document factory) | `1213917352480610` |
| L5 | Agentic Orchestration | ABPS AI - Build (system development) | `1213379551525587` |

**Mapping rules (priority order):**
1. If task name contains "goal", "goals update", "Kingpin", or task is in goal-tracking context → L1
2. If task belongs to any L2 project (by GID match) → L2
3. If task involves team meeting prep, cross-team docs, or team tool adoption → L3
4. If task name contains "AI", "AEO", "AI Overviews", "zero-click", or "POV" → L4
5. If task involves agent workflows, automation loops, or Kiro system work → L5
6. Default: L2 (most of Richard's work is testing-related)

## Deprecation: Microsoft To-Do Sync

### On-Demand Command Center
Richard can invoke Asana command center operations at any time during a chat session — not just during AM-2. When Richard says things like "move X to Sweep", "push Y to Friday", "add a task for Z", "mark that done", or "what's overdue?", the agent should:
1. Pull current task state from Asana if not already in context
2. Execute the requested operation immediately
3. Confirm the change

This makes Asana a live command center through the agent, not just a morning routine data source.

## Deprecation: Microsoft To-Do Sync
The Asana ↔ To-Do sync protocol (`asana-sync-protocol.md`) is now deprecated. Asana is the source of truth. Microsoft To-Do may still be used for personal reminders but is no longer the canonical task list.

## Deprecation: Slack as Command Center
Slack was a temporary command center while waiting for Asana MCP access. Slack remains the communication layer (ingestion, drafts, DMs) but task management moves to Asana.

---

## State Files

These files persist across sessions in `~/shared/context/active/` and are read/written by the morning routine, EOD reconciliation, and guardrail layer.

| File | Purpose | Written By | Read By | Update Cadence |
|------|---------|------------|---------|----------------|
| `asana-scan-state.json` | Last-scanned timestamp per task for Activity_Monitor. Prevents re-processing old stories. | AM-1 (Activity_Monitor) | AM-1 (next scan) | Every morning scan |
| `asana-audit-log.jsonl` | Append-only audit trail of every Asana write operation (tool name, task GID, fields modified, timestamp). | Every Asana write (guardrail layer) | On-demand review | Every write operation |
| `asana-morning-snapshot.json` | Frozen AM-1 task state: bucket counts, today tasks, overdue tasks. Baseline for EOD diff. | AM-1 (Ingest) | EOD-2 (Reconciliation) | Every morning |
| `asana-command-center.md` | Field GIDs, capability map, protocol, surface capabilities. | Manual + design phase | All hooks | As needed |

### File Schemas

**asana-scan-state.json:**
```json
{
  "last_scan_timestamp": null,       // ISO 8601 — most recent scan time
  "per_task_timestamps": {},         // task_gid → ISO 8601 last-scanned time
  "last_updated": null               // ISO 8601 — when this file was last written
}
```

**asana-audit-log.jsonl:** One JSON object per line:
```json
{"timestamp": "2026-04-03T08:15:00Z", "tool": "UpdateTask", "task_gid": "1234567890", "fields_modified": ["custom_fields.Kiro_RW"], "result": "success"}
```

**asana-morning-snapshot.json:**
```json
{
  "snapshot_date": null,             // YYYY-MM-DD
  "tasks": [],                       // Array of task objects with gid, name, routine, priority, due_on, completed
  "bucket_counts": {"sweep": 0, "core": 0, "engine_room": 0, "admin": 0, "backlog": 0},
  "today_tasks": [],                 // GIDs of Priority_RW = Today tasks
  "overdue_tasks": []                // GIDs of overdue tasks
}
```

---

## Surface Capabilities

_This section documents which Asana objects support writable Notes surfaces. Updated 2026-04-03 during Tasks 7/8._

| Object | Type | GID | Notes Writable? | Expected Surface | Probed? | Protocol Doc |
|--------|------|-----|-----------------|------------------|---------|--------------|
| AU | Project | `1212762061512767` | No (API limitation) | Pinned context task | ✅ Live | GID: `1213917747438931` |
| MX | Project | `1212775592612917` | No (API limitation) | Pinned context task | ✅ Live | GID: `1213917639688517` |
| Paid App | Project | `1205997667578886` | No (API limitation) | Pinned context task | ✅ Live | GID: `1213917771155873` |
| WW Testing | Project | `1205997667578893` | No (API limitation) | Pinned context task | ✅ Live | GID: `1213917851621567` |
| WW Acquisition | Project | `1206011235630048` | No (API limitation) | Pinned context task | ✅ Live | GID: `1213917771203342` |
| ABIX PS | Portfolio | `1212775592612914` | No (no UpdateProject in MCP) | AU + MX context tasks | ✅ Live | — |
| ABPS | Portfolio | `1212762061512816` | No (no UpdateProject in MCP) | WW Testing + WW Acq + Paid App tasks | ✅ Live | — |

**Not maintained (Richard no longer active):** ABPS-NA, ABPS-JP, ABPS-EU5. Richard still owns these projects in Asana but is not hands-on.

**Fallback chain (confirmed):** Project Notes tab → NOT accessible via API. Project description (html_notes) → no UpdateProject tool in MCP. **Actual surface: pinned context tasks** within each project, updated via UpdateTask(html_notes). This is the working pattern.

**Discovery status:** Live probing complete (2026-04-03). Project Notes tabs and project descriptions are not writable via the Enterprise Asana MCP. Pinned context tasks are the confirmed writable surface. AU and MX context tasks created and pinned. ABPS projects (NA, JP, EU5) pending.

**Draft status:** All four onboarding docs (AU, MX, ABIX PS, ABPS) are drafted and awaiting Richard's review. See asana-notes-protocol.md §5 for review checklist.

---

## Full Task Audit (2026-04-02)

### Additional Custom Fields Discovered

| Field | GID | Type | Notes |
|-------|-----|------|-------|
| Kiro_RW | `1213915851848087` | text | Agent notes field — empty on all tasks. Available for agent to write context, status updates, next actions. |
| Status C-week | `1211898465243458` | enum | Not Started, Green - On track, Yellow - At risk, Completed, Red-blocked, Green - Under Experiment |
| Help Needed flag | `1211898253103683` | multi_enum | Yes, No |
| Important/Urgent | `1200200115836714` | enum | Important/Urgent, Important/Non Urgent (Eisenhower matrix — older field, may overlap with Priority_RW + Importance_RW) |
| Date diff | `1213440376802787` | number | Auto-calculated days between Begin Date and Due Date |
| Marketplace/Region | `1212629048694011` | multi_enum | Market tags (FR, DE, ES, IT, etc.) |
| Impact (EU Reg) | `1211898253103663` | number | Registration impact estimate |
| Status L-week | `1211898253103687` | enum | Last week status |
| ATL/BTL? | `1212663856382198` | enum | Above/Below the line |
| Tech PM | `1203721406585927` | people | Tech PM assignment |
| OPS Impact | `1211349736814429` | number | Ops impact estimate |
| Time Left | `1207564683818996` | number | Hours remaining |
| Task Progress | various | enum | Done, In Progress, etc. (project-specific) |

### Kiro_RW Field — Agent Opportunity
The `Kiro_RW` text field (GID: `1213915851848087`) is empty on every task. This is the agent's scratchpad. Use it for:
- Morning brief context ("Overdue 8d — needs decision: do, delegate, or kill")
- Blockers detected from Slack/email ("Blocked by Vijeth footer — last mentioned 3/15")
- Next action reminders ("Draft outline before DDD on Thursday")
- Cross-reference notes ("Related to Slack thread in #ab-paid-search from 3/28")

### Task State Summary

**TODAY (Priority_RW = Today): 11 tasks**

| Task | Routine_RW | Due | Overdue? | Subtasks | Key Detail |
|------|---------|-----|----------|----------|------------|
| Mondays - Write into EU SSR Acq Asana | Sweep | Mar 30 | 3d | 0 | Recurring weekly |
| ie%CCP calc - insert MX spend/regs before 9th | Sweep | Apr 3 | — | 0 | Quip link in notes |
| AU meetings - Agenda | Sweep | Mar 31 | 2d | 0 | Task Progress = Done but not completed |
| Come prepared: Bi-weekly with Adi | Sweep | Apr 1 | 1d | 0 | AI brainstorm prep |
| It's time to update your goal(s) | Sweep | Apr 3 | — | 0 | 12 goals need updates |
| Testing Document for Kate | Core | Apr 1 | 1d | 6 | THE HARD THING. Doc captain. OP1 foundation. |
| Update and close your goal(s) | Core | Apr 3 | — | 0 | 2 goals due soon |
| Email overlay WW rollout/testing | Core | Mar 27 | 6d | 7 | 7 subtasks, overdue |
| Weekly Reporting - Global WBR sheet | Engine Room | Mar 30 | 3d | 4 | Recurring, has Quip links |
| Look over AU landing page switch | Engine Room | Mar 25 | 8d | 0 | 8 days overdue |
| MBR callout | Admin | Apr 2 | DUE TODAY | 0 | AU + MX projects |
| Send AU team invoice for prev month | Admin | Apr 2 | DUE TODAY | 0 | Monthly recurring |
| Monthly - Confirm actual budgets | Admin | Apr 1 | 1d | 0 | Paid App project |

**URGENT (Priority_RW = Urgent): 1 task**
- WW keyword gap fill based on market-level ASINs | Core | no due date | 6 subtasks | Important

**NOT URGENT (Priority_RW = Not urgent): 5 tasks**
- Update Kingpin for MX | Sweep | Apr 7 | Important
- Bi-monthly Flash | Sweep | May 21 | 3 projects
- Monthly: Individual Goals update | Engine Room | Apr 10 | Important
- AppsFlyer setup | Core | Jul 1 | Important, Paid App
- F90 | Core | Apr 30 | 9 subtasks, Important. Legal + Tech + Creative. Red to 3/30 ETA.

**NO PRIORITY SET: ~48 tasks** — These need triage. Many are subtasks of F90 or older backlog items.

### Parent-Child Relationships
- **F90** (9 subtasks): Get Legal Approval, Paid Media Legal Approval, Audience Request, Finish Audience Request, Add Audiences to Google, Enable Enhanced Match, Get Enhanced Match Legal Approval, Creative, Enable F90 Ads
- **Testing Document for Kate** (6 subtasks): Create structure, DDD to identify owners, Contact Megan, Create Timeline, 1st Review, 2nd Review
- **Email overlay WW rollout/testing** (7 subtasks): Quip detail, LP list, Gather markets, Rollout, DDD 2/12, Comment to Frank/Vijay, Tech scoping
- **WW keyword gap fill** (6 subtasks): not yet pulled
- **Get Enhanced Match Legal Approval** (2 subtasks): child of F90

### Tasks with No Routine (Backlog/Untriaged)
These tasks have no Routine field set — they won't appear in any block:
- Get Enhanced Match Legal Approval (child of F90)
- Get Enhanced Match details (child of above)
- Paid App (has Status C-week = Green, but no Routine)
- Promo Test (Core Two set, but no due date)
- Many F90 subtasks appearing as standalone
- Empty-name task (GID: 1213828814349972) — garbage, should be deleted
- Several audience/media pipeline tasks (sequential chain)

### Recurring Tasks Pattern
These recur but aren't using Asana's recurring task feature — they're manually duplicated:
- Weekly Reporting - Global WBR sheet (weekly)
- Mondays - Write into EU SSR Acq Asana (weekly)
- AU meetings - Agenda (weekly)
- MBR callout (monthly)
- ie%CCP calc (monthly)
- Send AU team invoice (monthly)
- Monthly - Confirm actual budgets (monthly)
- Bi-monthly Flash (bi-monthly)
- Individual Goals update (monthly)
- Come prepared: Bi-weekly with Adi (bi-weekly)

### Agent Actions Available

**Read (unrestricted):**
- GetTaskDetails — full task with all custom fields
- GetSubtasksForTask — child tasks
- GetTaskStories — full activity/comment history
- SearchTasksInWorkspace — filtered search
- GetProjectSections — project structure
- GetStatusUpdatesFromObject — project status updates
- GetGoal — goal progress and metrics

**Write (Richard's tasks only):**
- UpdateTask — change name, due_on, start_on, completed, notes, custom_fields, assignee_section
- CreateTask — new tasks (assign to Richard, set project, custom fields)
- CreateTaskStory — add comments to tasks
- SetParentForTask — restructure parent/child relationships
- AddTagForTask / RemoveTagForTask — tagging

**Key write patterns for the agent:**
1. Set Kiro_RW field with context notes: `custom_fields={"1213915851848087": "text"}`
2. Triage untriaged tasks by setting Routine_RW + Priority_RW
3. Mark recurring tasks complete and note in Kiro_RW when the next instance exists
4. Add comments with status updates or blockers detected from other sources
5. Create subtasks for decomposed work
6. Update due dates when signals indicate timeline changes

---

## Full Capability Map (Enterprise Asana MCP)

### Tools Available

**Tasks (core):**
- `GetTaskDetails` — full task record with custom fields, notes, projects, subtask count
- `GetSubtasksForTask` — child tasks
- `GetTaskStories` — full activity log (comments, field changes, assignments, section moves)
- `SearchTasksInWorkspace` — filtered search (assignee, completed, due dates, projects, sections, tags, text)
- `CreateTask` — new task with name, notes, assignee, project, custom_fields, due_on, parent
- `UpdateTask` — modify any field: name, notes, due_on, completed, custom_fields, assignee
- `CreateTaskStory` — add comment (plain text or rich HTML)
- `SetParentForTask` — restructure parent/child
- `AddTagForTask` / `RemoveTagForTask` — tagging
- `GetProjectsForTask` — which projects a task belongs to

**Projects:**
- `GetProject` — full project details (owner, members, status, dates, notes)
- `GetProjectSections` — sections/columns within a project
- `CreateProjectSection` — add new section
- `GetTasksFromProject` — all tasks in a project (up to 100)
- `GetProjectTaskCount` — quick stats (total, completed, incomplete, milestones)
- `GetStatusUpdatesFromObject` — project status updates

**Goals:**
- `GetGoal` — full goal details (status, owner, metric with current/target values, time period)
- `GetStatusUpdate` — individual status update detail

**Portfolios:**
- `GetAllPortfolios` — portfolios owned by a user
- `GetPortfolioItems` — projects within a portfolio with custom fields and status

**Users & Teams:**
- `GetCurrentUser` — authenticated user info
- `AsanaSearch` — fuzzy search for projects, users, teams, tasks, tags, goals, portfolios, custom fields, templates

**Stories/Activity:**
- `GetTaskStories` / `GetStoriesForTask` — activity feed
- `UpdateStory` — edit/pin comments

### Richard's Goals (14 total)

| Goal | GID | Status | Period | Metric | Current |
|------|-----|--------|--------|--------|---------|
| MX/AU paid search registrations | 1213245014119128 | 🟢 green | FY26 | 100% | 18% |
| MX registrations | 1213204514049680 | 🟢 green | FY26 | 11,100 | 2,167 (20%) |
| AU registrations | 1213204514049684 | 🟢 green | FY26 | 12,906 | 2,231 (17%) |
| MX + AU market testing | 1213245014119125 | — | FY26 | 4 experiments | 0% |
| MX tests | 1213204514049688 | 🟡 yellow | FY26 | 100% | 0% |
| AU tests | 1213204514049691 | 🟡 yellow | FY26 | 100% | 0% |
| AU test 1: Brand LP | 1213204514049694 | 🟡 yellow | Q1 FY26 | 100% | 0% (Q1 ended) |
| MX test 1: Brand LP | 1213204514049706 | 🟡 yellow | Q1 FY26 | 100% | 0% (Q1 ended) |
| Globalized cross-market testing | 1213245014119131 | 🟢 green | FY26 | 3 tests | 0% |
| WW in-context email overlay | 1213204514049667 | 🟢 green | H1 FY26 | 100% | 0% |
| PS redirect mapping | 1213204514049671 | 🟢 green | H1 FY26 | 100% | 0% |
| Paid App | 1213204514049810 | 🟢 green | FY26 | 100% | 14% |
| Paid App Installs | 1213204514049812 | 🟢 green | FY26 | 435,000 | 120,621 (28%) |
| Paid App Tests | 1213204514049830 | — | FY26 | 3 tests | 0 |

**Goal status updates last refreshed: Mar 6.** All need April updates (task: "It's time to update your goal(s)").

### Richard's Portfolios

| Portfolio | GID | Projects |
|-----------|-----|----------|
| ABIX PS | 1212775592612914 | AU (Richard owns), MX (Richard owns) |
| ABPS | 1212762061512816 | ABPS - NA (Richard owns), ABPS - JP (Richard owns), ABPS - EU5 (Richard owns) |

### Richard's Projects (confirmed membership)

| Project | GID | Role |
|---------|-----|------|
| ABPS - WW Testing & Projects | 1205997667578893 | Owner |
| PS-Owned Global Testing | 1213279426031997 | Member |
| ABPS - WW Acquisition | 1206011235630048 | Member |
| AU | 1212762061512767 | Owner |
| MX | 1212775592612917 | Owner |
| Paid App | 1205997667578886 | Member |
| PS ENG | 1213235338214787 | Member |
| EU SSR Acquisition Roadmap | 1211638878682721 | Member |
| Paid Search Promo Experiments | 1212707241411307 | Member |
| ABPS AI - Content | 1213917352480610 | Owner |
| ABPS AI - Build | 1213379551525587 | Owner |

### Agentic Opportunities by Capability

**Goals (Level 1 — Sharpen Yourself):**
- Morning brief: Pull all goals, show current vs target, flag yellow/red
- Monthly: Auto-draft goal status updates from task completion data + WBR metrics
- Q1 Brand LP goals (AU + MX) ended at 0% — flag for retrospective or rollover to Q2

**Goals (Level 2 — Drive WW Testing):**
- Cross-reference test goals (MX tests, AU tests, Globalized testing) with test tasks
- Surface: "You have 3 test goals at 0% with 9 months left — which tasks advance them?"
- Auto-link test tasks to goals when creating them

**Portfolios (Level 3 — Team Automation):**
- Read portfolio status across all 5 market projects for team standup prep
- Surface projects with no status update in 14+ days

**Status Updates (Level 2):**
- Read project status updates to detect stale projects
- Draft status updates from task completion data

**Activity/Stories (Level 1):**
- Read task activity to detect: who commented, what changed, when
- Surface tasks where teammates commented but Richard hasn't responded
- Detect tasks that were reassigned or had due dates changed by others

**Search (Level 3):**
- Search across all workspace tasks for cross-team context
- Find tasks in other teams' projects that mention Richard's markets

**Kiro_RW Field (Level 5 — Agentic Orchestration):**
- Agent writes context into every task during morning routine
- EOD reconciliation updates Kiro_RW with completion status
- Creates a persistent, task-level agent memory that survives session restarts
- Other agents (market-analyst, callout-writer) can read Kiro_RW for context
