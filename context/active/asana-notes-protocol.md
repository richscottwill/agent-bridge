# Asana Notes Protocol — Surface Discovery & Onboarding Docs

Last updated: 2026-04-03

## Purpose

This document serves as the complete protocol for writing market onboarding docs (project-level) and program onboarding docs (portfolio-level) into Asana. It covers surface discovery, draft templates, and exact API calls for writing once Richard approves.

---

## 1. Surface Discovery Protocol

### Why Discovery Is Needed

The Enterprise Asana MCP exposes different write surfaces depending on object type (project vs portfolio). Not all objects support a "Notes tab" — some only expose `html_notes` on the description field, others may only support status updates. The agent must probe each object to determine the best writable surface before attempting writes.

### Fallback Chain (ordered by preference)

1. **Notes tab** — Rich text, navigable with H1/H2/H3 outline. Ideal for onboarding docs. Check if `GetProject` or portfolio equivalent returns a `notes` or `html_notes` field that is writable.
2. **Project/Portfolio description (`html_notes`)** — The description field on projects. Writable via `UpdateProject(project_gid, html_notes="<body>...")`. This is the most likely writable surface for projects.
3. **Pinned status update** — Create a status update via the status update API and pin it. Less ideal because status updates are temporal, not persistent docs.
4. **Pinned task with comments** — Create a task named "📋 [Market] Onboarding Doc" within the project, pin it, and use the task description + comments as the doc surface. Last resort.

### Discovery Instructions — Projects (AU, MX)

**Step 1: Probe project for writable fields**
```
GetProject(project_gid="1212762061512767")  // AU
GetProject(project_gid="1212775592612917")  // MX
```

**What to check in the response:**
- Does the response include `notes` (plain text) and/or `html_notes` (rich text)? → If yes, the project description is writable via `UpdateProject`.
- Does the response include a `project_brief` object? → If yes, there may be a separate brief/overview surface.
- Check `is_template`, `archived`, `public` for any access restrictions.

**Step 2: Test write capability**
```
// Test with a minimal write to AU project description
UpdateProject(project_gid="1212762061512767", html_notes="<body><h1>AU — Paid Search</h1><p>Test write — delete after confirming.</p></body>")
```
If this succeeds → `html_notes` on project description is the writable surface.
If this fails → fall back to status update or pinned task.

**Step 3: Check for status update support**
```
GetStatusUpdatesFromObject(object_gid="1212762061512767", object_type="project")
```
If status updates are supported → this is the fallback surface.

### Discovery Instructions — Portfolios (ABIX PS, ABPS)

**Step 1: Probe portfolio**
```
GetAllPortfolios(owner_gid="1212732742544167", workspace_gid="8442528107068")
```
This returns portfolio objects. Check if the portfolio object includes `notes` or `html_notes` fields.

**Step 2: Check portfolio items**
```
GetPortfolioItems(portfolio_gid="1212775592612914")  // ABIX PS
GetPortfolioItems(portfolio_gid="1212762061512816")  // ABPS
```

**Step 3: Determine write surface**
- If portfolios support `html_notes` → write directly via portfolio update API.
- If portfolios only support status updates → use `CreateStatusUpdateForObject` with the portfolio GID.
- If neither → create a pinned project or task within the portfolio's first project as the doc surface.

**Note:** The Enterprise Asana MCP may not expose a direct "update portfolio description" tool. If `UpdateProject` exists but `UpdatePortfolio` does not, the fallback is status updates on the portfolio object, or writing the portfolio-level doc into each constituent project's description as a cross-reference.

### Expected Findings (Pre-Discovery Assessment)

Based on the Asana API and Enterprise MCP tool list in asana-command-center.md:

| Object | GID | Expected Surface | Confidence |
|--------|-----|-----------------|------------|
| AU (project) | `1212762061512767` | `html_notes` via `UpdateProject` | High — projects reliably support description writes |
| MX (project) | `1212775592612917` | `html_notes` via `UpdateProject` | High |
| ABIX PS (portfolio) | `1212775592612914` | Status update or constituent project descriptions | Medium — portfolio write support varies |
| ABPS (portfolio) | `1212762061512816` | Status update or constituent project descriptions | Medium |


---

## 2. Project Notes Templates — Market Onboarding Docs

These are the draft onboarding documents for AU and MX projects. They follow the header hierarchy from Requirement 7 and are populated with known data from the command center audit (2026-04-02).

### 2a. AU — Paid Search (Project GID: 1212762061512767)

**HTML version for `UpdateProject(html_notes=...)`:**

```html
<body>
<h1>AU — Paid Search</h1>

<h2>Market Overview</h2>
<p>Australia is one of two hands-on markets managed directly by Richard Williams (Paid Search, WW Outbound Marketing). AU Paid Search drives seller registrations through Google Ads campaigns targeting Australian small-to-medium businesses.</p>
<ul>
<li><strong>FY26 Registration Target:</strong> 12,906</li>
<li><strong>Current Registrations (as of Apr 2026):</strong> 2,231 (17% of target)</li>
<li><strong>CPA Target:</strong> ~$140 AUD</li>
<li><strong>Efficiency Guardrail:</strong> CPA must stay at or below target; no scaling at the expense of efficiency</li>
<li><strong>Key Stakeholder:</strong> Lena (AU market lead / local ops contact)</li>
<li><strong>Program Owner:</strong> Richard Williams</li>
<li><strong>Portfolio:</strong> ABIX PS (Amazon Business International Expansion — Paid Search)</li>
</ul>

<h2>Active Campaigns &amp; Accounts</h2>
<ul>
<li><strong>Google Ads Account:</strong> [AU Google Ads account — link TBD]</li>
<li><strong>Campaign Structure:</strong> Brand, Non-Brand, Competitor segments</li>
<li><strong>Bid Strategy:</strong> [Current bid strategy — populate from Google Ads data]</li>
<li><strong>Monthly Budget:</strong> [Current budget — populate from budget confirmation task]</li>
<li><strong>Invoice Cadence:</strong> Monthly — "Send AU team invoice for prev month" task (recurring, Admin bucket)</li>
</ul>

<h2>Active Tests &amp; Experiments</h2>
<ul>
<li><strong>AU Test 1: Brand LP</strong> — Goal GID: <code>1213204514049694</code>. Status: 🟡 Yellow. Q1 FY26 target: 100%. Current: 0%. Q1 has ended with no progress. Needs retrospective or rollover to Q2.</li>
<li><strong>AU LP Switch:</strong> Task "Look over AU landing page switch" — 9 days overdue as of Apr 2. Engine Room bucket. Needs decision: proceed, defer, or kill.</li>
</ul>

<h2>Planned Work</h2>
<ul>
<li>Brand LP test execution (rolled from Q1 → Q2)</li>
<li>Landing page switch evaluation (blocked on LP review)</li>
<li>Monthly budget confirmation cycle</li>
<li>Weekly AU meetings agenda prep</li>
<li>Keyword gap fill (WW initiative, AU component) — subtask of WW keyword gap fill</li>
</ul>

<h2>Blockers &amp; Risks</h2>
<ul>
<li><strong>Brand LP test at 0%:</strong> Q1 ended with no test launched. Risk: FY26 testing goals (4 experiments across AU+MX) will miss if Q2 doesn't start immediately.</li>
<li><strong>AU LP switch overdue (9d):</strong> Needs Richard's review. No blocker owner identified — this is on Richard.</li>
<li><strong>Registration pacing:</strong> 17% of FY26 target through ~Q1. On pace if linear, but back-half loaded targets may require acceleration.</li>
</ul>

<h2>Key Metrics &amp; Targets</h2>
<table>
<tr><th>Metric</th><th>Target</th><th>Current</th><th>Pacing</th></tr>
<tr><td>FY26 Registrations</td><td>12,906</td><td>2,231</td><td>17% — needs monitoring</td></tr>
<tr><td>CPA</td><td>~$140 AUD</td><td>[Pull from DuckDB/WBR]</td><td>—</td></tr>
<tr><td>Brand LP Test</td><td>100% (Q1)</td><td>0%</td><td>🔴 Missed Q1</td></tr>
<tr><td>AU Tests (FY26)</td><td>100%</td><td>0%</td><td>🟡 At risk</td></tr>
</table>

<h2>Recent Decisions &amp; Changes</h2>
<ul>
<li><strong>2026-04-02:</strong> Asana integration activated. AU project now managed via Asana command center. Microsoft To-Do deprecated.</li>
<li><strong>2026-04-02:</strong> Full task audit completed. 11 Today tasks identified, AU LP switch flagged as 8d overdue.</li>
<li><strong>2026-Q1:</strong> Brand LP test did not launch in Q1. Decision needed on Q2 rollover vs. alternative test design.</li>
</ul>

<h2>Key Links</h2>
<ul>
<li><strong>Asana Project:</strong> AU (GID: <code>1212762061512767</code>)</li>
<li><strong>Portfolio:</strong> ABIX PS (GID: <code>1212775592612914</code>)</li>
<li><strong>AU Registration Goal:</strong> GID <code>1213204514049684</code></li>
<li><strong>AU Tests Goal:</strong> GID <code>1213204514049691</code></li>
<li><strong>AU Brand LP Goal:</strong> GID <code>1213204514049694</code></li>
<li><strong>Google Ads Account:</strong> [Link TBD]</li>
<li><strong>WBR Dashboard:</strong> [Link TBD]</li>
<li><strong>Slack Channel:</strong> #ab-paid-search</li>
</ul>
</body>
```


### 2b. MX — Paid Search (Project GID: 1212775592612917)

**HTML version for `UpdateProject(html_notes=...)`:**

```html
<body>
<h1>MX — Paid Search</h1>

<h2>Market Overview</h2>
<p>Mexico is one of two hands-on markets managed directly by Richard Williams (Paid Search, WW Outbound Marketing). MX Paid Search drives seller registrations through Google Ads campaigns targeting Mexican small-to-medium businesses.</p>
<ul>
<li><strong>FY26 Registration Target:</strong> 11,100</li>
<li><strong>Current Registrations (as of Apr 2026):</strong> 2,167 (20% of target)</li>
<li><strong>CPA Target:</strong> [Pull from WBR/budget data — MXN]</li>
<li><strong>Efficiency Guardrail:</strong> CPA must stay at or below target</li>
<li><strong>Key Contact:</strong> Carlos (MX invoicing and local ops)</li>
<li><strong>Program Owner:</strong> Richard Williams</li>
<li><strong>Portfolio:</strong> ABIX PS (Amazon Business International Expansion — Paid Search)</li>
</ul>

<h2>Active Campaigns &amp; Accounts</h2>
<ul>
<li><strong>Google Ads Account:</strong> [MX Google Ads account — link TBD]</li>
<li><strong>Campaign Structure:</strong> Brand, Non-Brand, Competitor segments</li>
<li><strong>Bid Strategy:</strong> [Current bid strategy — populate from Google Ads data]</li>
<li><strong>Monthly Budget:</strong> [Current budget — populate from budget confirmation task]</li>
<li><strong>Invoice Cadence:</strong> Monthly — coordinated through Carlos</li>
</ul>

<h2>Active Tests &amp; Experiments</h2>
<ul>
<li><strong>MX Test 1: Brand LP</strong> — Goal GID: <code>1213204514049706</code>. Status: 🟡 Yellow. Q1 FY26 target: 100%. Current: 0%. Q1 has ended with no progress. Needs retrospective or rollover to Q2.</li>
<li><strong>MX Auto Page:</strong> Blocked on Vijeth (footer issue). Last mentioned ~Mar 15 in Slack. 14+ days stale.</li>
</ul>

<h2>Planned Work</h2>
<ul>
<li>Brand LP test execution (rolled from Q1 → Q2)</li>
<li>ie%CCP calc — insert MX spend/regs before 9th of each month (recurring, Sweep bucket)</li>
<li>Monthly budget confirmation cycle</li>
<li>Keyword gap fill (WW initiative, MX component)</li>
<li>Kingpin update for MX (due Apr 7, Sweep, Important)</li>
<li>MX Auto page unblock (depends on Vijeth)</li>
</ul>

<h2>Blockers &amp; Risks</h2>
<ul>
<li><strong>Brand LP test at 0%:</strong> Q1 ended with no test launched. Same risk as AU — FY26 testing goals at risk.</li>
<li><strong>MX Auto page blocked on Vijeth:</strong> Footer dependency. 14+ days with no movement. Escalation path: follow up directly or escalate through team lead.</li>
<li><strong>Registration pacing:</strong> 20% of FY26 target through ~Q1. Slightly ahead of AU but still needs monitoring.</li>
<li><strong>Invoice coordination:</strong> Depends on Carlos for timely processing. No current blocker but historically a friction point.</li>
</ul>

<h2>Key Metrics &amp; Targets</h2>
<table>
<tr><th>Metric</th><th>Target</th><th>Current</th><th>Pacing</th></tr>
<tr><td>FY26 Registrations</td><td>11,100</td><td>2,167</td><td>20% — slightly ahead of linear</td></tr>
<tr><td>CPA</td><td>[TBD — MXN]</td><td>[Pull from DuckDB/WBR]</td><td>—</td></tr>
<tr><td>Brand LP Test</td><td>100% (Q1)</td><td>0%</td><td>🔴 Missed Q1</td></tr>
<tr><td>MX Tests (FY26)</td><td>100%</td><td>0%</td><td>🟡 At risk</td></tr>
</table>

<h2>Recent Decisions &amp; Changes</h2>
<ul>
<li><strong>2026-04-02:</strong> Asana integration activated. MX project now managed via Asana command center.</li>
<li><strong>2026-04-02:</strong> Full task audit completed. MX Auto page flagged as blocked on Vijeth (14d+).</li>
<li><strong>2026-Q1:</strong> Brand LP test did not launch in Q1. Decision needed on Q2 rollover.</li>
</ul>

<h2>Key Links</h2>
<ul>
<li><strong>Asana Project:</strong> MX (GID: <code>1212775592612917</code>)</li>
<li><strong>Portfolio:</strong> ABIX PS (GID: <code>1212775592612914</code>)</li>
<li><strong>MX Registration Goal:</strong> GID <code>1213204514049680</code></li>
<li><strong>MX Tests Goal:</strong> GID <code>1213204514049688</code></li>
<li><strong>MX Brand LP Goal:</strong> GID <code>1213204514049706</code></li>
<li><strong>Google Ads Account:</strong> [Link TBD]</li>
<li><strong>WBR Dashboard:</strong> [Link TBD]</li>
<li><strong>Slack Channel:</strong> #ab-paid-search</li>
</ul>
</body>
```


---

## 3. Portfolio Notes Templates — Program Onboarding Docs

### 3a. ABIX PS — Amazon Business International Expansion, Paid Search (Portfolio GID: 1212775592612914)

**HTML version:**

```html
<body>
<h1>ABIX PS — Amazon Business International Expansion, Paid Search</h1>

<h2>Program Overview</h2>
<p>ABIX PS is the portfolio covering Paid Search expansion into international markets outside the established NA/EU/JP footprint. Currently contains Australia (AU) and Mexico (MX) — two markets where Richard Williams directly manages campaign operations, testing, and registration growth.</p>
<ul>
<li><strong>Program Owner:</strong> Richard Williams</li>
<li><strong>Markets:</strong> AU, MX</li>
<li><strong>FY26 Combined Registration Target:</strong> 24,006 (AU: 12,906 + MX: 11,100)</li>
<li><strong>Current Combined Registrations:</strong> 4,398 (18% of target)</li>
<li><strong>Parent Goal:</strong> MX/AU paid search registrations (GID: <code>1213245014119128</code>) — 🟢 Green, 18% of 100% target</li>
</ul>

<h2>AU — Market Summary</h2>
<ul>
<li><strong>Registration Target:</strong> 12,906 | Current: 2,231 (17%)</li>
<li><strong>CPA Target:</strong> ~$140 AUD</li>
<li><strong>Key Stakeholder:</strong> Lena</li>
<li><strong>Active Tests:</strong> Brand LP (0% — missed Q1), AU LP switch (overdue 9d)</li>
<li><strong>Top Blocker:</strong> Brand LP test not launched; LP switch needs review</li>
<li><strong>Status:</strong> Registration pacing on track if linear; testing goals at risk</li>
<li><strong>Full Details:</strong> See AU project Notes (GID: <code>1212762061512767</code>)</li>
</ul>

<h2>MX — Market Summary</h2>
<ul>
<li><strong>Registration Target:</strong> 11,100 | Current: 2,167 (20%)</li>
<li><strong>CPA Target:</strong> [TBD — MXN]</li>
<li><strong>Key Contact:</strong> Carlos (invoicing/local ops)</li>
<li><strong>Active Tests:</strong> Brand LP (0% — missed Q1), MX Auto page (blocked on Vijeth 14d+)</li>
<li><strong>Top Blocker:</strong> MX Auto page blocked on Vijeth footer; Brand LP test not launched</li>
<li><strong>Status:</strong> Registration pacing slightly ahead; testing goals at risk</li>
<li><strong>Full Details:</strong> See MX project Notes (GID: <code>1212775592612917</code>)</li>
</ul>

<h2>Cross-Market Initiatives</h2>
<ul>
<li><strong>MX + AU Market Testing (Goal GID: <code>1213245014119125</code>):</strong> Target 4 experiments across both markets in FY26. Current: 0%. Both Brand LP tests missed Q1. Q2 is critical for recovery.</li>
<li><strong>Globalized Cross-Market Testing (Goal GID: <code>1213245014119131</code>):</strong> Target 3 tests that apply across markets. Current: 0%. 🟢 Green status but no progress yet.</li>
<li><strong>WW Keyword Gap Fill:</strong> Cross-market initiative to identify keyword coverage gaps by market-level ASINs. AU and MX are components. Task is Urgent/Important with 6 subtasks.</li>
<li><strong>WW In-Context Email Overlay (Goal GID: <code>1213204514049667</code>):</strong> H1 FY26 target. 0% progress. Email overlay rollout/testing task has 7 subtasks, 6d overdue.</li>
</ul>

<h2>Program Metrics &amp; Goals</h2>
<table>
<tr><th>Goal</th><th>Target</th><th>Current</th><th>Status</th></tr>
<tr><td>MX/AU Combined Registrations</td><td>100%</td><td>18%</td><td>🟢 Green</td></tr>
<tr><td>AU Registrations</td><td>12,906</td><td>2,231 (17%)</td><td>🟢 Green</td></tr>
<tr><td>MX Registrations</td><td>11,100</td><td>2,167 (20%)</td><td>🟢 Green</td></tr>
<tr><td>MX + AU Testing</td><td>4 experiments</td><td>0%</td><td>⚠️ No status set</td></tr>
<tr><td>AU Tests</td><td>100%</td><td>0%</td><td>🟡 Yellow</td></tr>
<tr><td>MX Tests</td><td>100%</td><td>0%</td><td>🟡 Yellow</td></tr>
<tr><td>AU Brand LP (Q1)</td><td>100%</td><td>0%</td><td>🔴 Missed Q1</td></tr>
<tr><td>MX Brand LP (Q1)</td><td>100%</td><td>0%</td><td>🔴 Missed Q1</td></tr>
<tr><td>Globalized Testing</td><td>3 tests</td><td>0%</td><td>🟢 Green</td></tr>
</table>
</body>
```


### 3b. ABPS — Amazon Business Paid Search (Portfolio GID: 1212762061512816)

**HTML version:**

```html
<body>
<h1>ABPS — Amazon Business Paid Search</h1>

<h2>Program Overview</h2>
<p>ABPS is the portfolio covering Paid Search operations across established Amazon Business markets. Contains NA (North America), JP (Japan), and EU5 (UK, DE, FR, IT, ES). Richard Williams owns these projects within the portfolio; day-to-day campaign execution is shared with market-specific team members.</p>
<ul>
<li><strong>Program Owner:</strong> Richard Williams</li>
<li><strong>Markets:</strong> NA, JP, EU5</li>
<li><strong>Related Projects:</strong> ABPS - NA, ABPS - JP, ABPS - EU5</li>
<li><strong>Team:</strong> WW Outbound Marketing (Brandon Munday, L7)</li>
</ul>

<h2>NA — Market Summary</h2>
<ul>
<li><strong>Project:</strong> ABPS - NA (Richard owns)</li>
<li><strong>Scale:</strong> Largest AB Paid Search market by spend and registration volume</li>
<li><strong>Key Focus Areas:</strong> Paid App installs (Goal GID: <code>1213204514049812</code> — target 435,000, current 120,621 at 28%), PS redirect mapping, email overlay rollout</li>
<li><strong>Active Goals:</strong> Paid App (14% of 100%), Paid App Installs (28% of 435K), Paid App Tests (0 of 3)</li>
<li><strong>Status:</strong> Paid App installs pacing reasonably (28% through ~Q1). Redirect mapping and email overlay at 0%.</li>
</ul>

<h2>JP — Market Summary</h2>
<ul>
<li><strong>Project:</strong> ABPS - JP (Richard owns)</li>
<li><strong>Scale:</strong> Second-largest international market</li>
<li><strong>Key Focus Areas:</strong> [Populate from JP project tasks and goals when probed]</li>
<li><strong>Status:</strong> [Populate after probing JP project]</li>
</ul>

<h2>EU5 — Market Summary</h2>
<ul>
<li><strong>Project:</strong> ABPS - EU5 (Richard owns)</li>
<li><strong>Markets Covered:</strong> UK, DE, FR, IT, ES</li>
<li><strong>Key Focus Areas:</strong> EU SSR Acquisition Roadmap (project GID: <code>1211638878682721</code>), cross-market testing, Paid Search Promo Experiments (project GID: <code>1212707241411307</code>)</li>
<li><strong>Related Tasks:</strong> "Mondays - Write into EU SSR Acq Asana" (recurring weekly, Sweep), Bi-monthly Flash</li>
<li><strong>Status:</strong> [Populate after probing EU5 project]</li>
</ul>

<h2>Cross-Market Initiatives</h2>
<ul>
<li><strong>WW In-Context Email Overlay (Goal GID: <code>1213204514049667</code>):</strong> H1 FY26 target 100%. Current: 0%. Task "Email overlay WW rollout/testing" has 7 subtasks, 6d overdue. Spans all ABPS markets.</li>
<li><strong>PS Redirect Mapping (Goal GID: <code>1213204514049671</code>):</strong> H1 FY26 target 100%. Current: 0%. Cross-market redirect strategy.</li>
<li><strong>Globalized Cross-Market Testing (Goal GID: <code>1213245014119131</code>):</strong> Target 3 tests. Current: 0%. Tests designed to apply across NA/JP/EU5 and potentially ABIX markets.</li>
<li><strong>WW Keyword Gap Fill:</strong> Market-level ASIN-based keyword expansion. Urgent/Important. 6 subtasks across markets.</li>
<li><strong>Testing Document for Kate:</strong> THE HARD THING. Doc captain responsibility. OP1 foundation. 6 subtasks, Core bucket. Due Apr 1 (1d overdue). Cross-market testing methodology that applies to all ABPS markets.</li>
</ul>

<h2>Program Metrics &amp; Goals</h2>
<table>
<tr><th>Goal</th><th>Target</th><th>Current</th><th>Status</th></tr>
<tr><td>Paid App</td><td>100%</td><td>14%</td><td>🟢 Green</td></tr>
<tr><td>Paid App Installs</td><td>435,000</td><td>120,621 (28%)</td><td>🟢 Green</td></tr>
<tr><td>Paid App Tests</td><td>3 tests</td><td>0</td><td>⚠️ No status</td></tr>
<tr><td>WW Email Overlay</td><td>100% (H1)</td><td>0%</td><td>🟢 Green (but 0%)</td></tr>
<tr><td>PS Redirect Mapping</td><td>100% (H1)</td><td>0%</td><td>🟢 Green (but 0%)</td></tr>
<tr><td>Globalized Testing</td><td>3 tests</td><td>0%</td><td>🟢 Green</td></tr>
</table>

<p><em>Note: Several goals show 🟢 Green status despite 0% progress. These were last updated Mar 6 and need April refreshes. The Goal Updater (Task 6) will draft honest assessments.</em></p>
</body>
```


---

## 4. Write Instructions — Exact API Calls

Once Richard reviews and approves the drafts above, use these exact calls to write the docs to Asana.

### 4a. Project Notes (AU and MX)

**Primary surface: Project description via `html_notes`**

Projects in Asana support a description field that accepts rich HTML. This is the most reliable writable surface for project-level onboarding docs.

```
// Write AU onboarding doc to AU project description
UpdateProject(
  project_gid = "1212762061512767",
  html_notes = "<body>...[AU HTML from Section 2a above]...</body>"
)

// Write MX onboarding doc to MX project description
UpdateProject(
  project_gid = "1212775592612917",
  html_notes = "<body>...[MX HTML from Section 2b above]...</body>"
)
```

**Pre-write checklist:**
1. ✅ Richard has reviewed and approved the draft content
2. ✅ Verify project ownership: `GetProject(project_gid)` → confirm `owner.gid === 1212732742544167`
3. ✅ Read existing content first: check if `html_notes` already has content that should be preserved
4. ✅ Log the write to `asana-audit-log.jsonl`:
   ```json
   {"timestamp": "2026-04-03T...", "tool": "UpdateProject", "object_gid": "1212762061512767", "fields_modified": ["html_notes"], "result": "success", "note": "AU market onboarding doc written"}
   ```

**If `UpdateProject` is not available in the MCP:**
Fall back to creating a status update:
```
CreateStatusUpdateForObject(
  object_gid = "1212762061512767",
  object_type = "project",
  title = "AU — Paid Search: Market Onboarding Doc",
  html_text = "<body>...[AU HTML]...</body>",
  status_type = "on_track"
)
```

**If status updates are not available:**
Create a pinned task:
```
CreateTask(
  name = "📋 AU — Market Onboarding Doc (Pinned)",
  assignee = "1212732742544167",
  projects = ["1212762061512767"],
  html_notes = "<body>...[AU HTML]...</body>"
)
// Then pin the task to the top of the project
```

### 4b. Portfolio Notes (ABIX PS and ABPS)

**Primary surface: Portfolio description (if supported)**

```
// If UpdatePortfolio or equivalent exists:
UpdatePortfolio(
  portfolio_gid = "1212775592612914",
  html_notes = "<body>...[ABIX PS HTML from Section 3a]...</body>"
)

UpdatePortfolio(
  portfolio_gid = "1212762061512816",
  html_notes = "<body>...[ABPS HTML from Section 3b]...</body>"
)
```

**If portfolio description is not writable (likely scenario):**

Option A — Status update on portfolio:
```
CreateStatusUpdateForObject(
  object_gid = "1212775592612914",
  object_type = "portfolio",
  title = "ABIX PS — Program Onboarding Doc",
  html_text = "<body>...[ABIX PS HTML]...</body>",
  status_type = "on_track"
)
```

Option B — Write to each constituent project's description as a cross-reference:
```
// Add a "Portfolio Context" section to AU project description
// Add a "Portfolio Context" section to MX project description
// This ensures the portfolio-level context is accessible from within each project
```

Option C — Create a dedicated "Program Overview" project within the portfolio:
```
// Create a project named "ABIX PS — Program Overview"
// Write the portfolio doc as the project description
// Add to the ABIX PS portfolio
```

**Pre-write checklist (same as projects):**
1. ✅ Richard has reviewed and approved
2. ✅ Verify ownership
3. ✅ Read existing content first
4. ✅ Log to audit trail

### 4c. Ongoing Updates

**Monthly refresh cadence:**
- Project Notes (AU, MX): Update Key Metrics, Active Tests, Blockers sections in-place. Append to Recent Decisions log.
- Portfolio Notes (ABIX PS, ABPS): Update market summaries and program metrics after Goal Updater runs.

**Update pattern:**
1. Read current `html_notes` from the object
2. Parse the HTML to identify sections by H2 headers
3. Replace section content while preserving structure
4. Append new entries to "Recent Decisions & Changes" (dated log — never overwrite)
5. Write back the full updated HTML
6. Log the update to audit trail

**Section-specific update rules:**
| Section | Update Type | Frequency |
|---------|------------|-----------|
| Market Overview | In-place refresh | Monthly or on change |
| Active Campaigns | In-place refresh | Monthly |
| Active Tests | In-place refresh | Weekly or on status change |
| Planned Work | In-place refresh | Weekly |
| Blockers & Risks | In-place refresh | Daily (during AM-2) |
| Key Metrics | In-place refresh | Monthly (after Goal Updater) |
| Recent Decisions | Append-only dated log | On each decision |
| Key Links | In-place refresh | As needed |

---

## 5. Review Status

### Drafts Pending Richard's Review

| Doc | Object | GID | Status | Action Needed |
|-----|--------|-----|--------|---------------|
| AU Market Onboarding | Project | `1212762061512767` | ✅ DRAFTED | Richard: review Section 2a above, approve or request changes |
| MX Market Onboarding | Project | `1212775592612917` | ✅ DRAFTED | Richard: review Section 2b above, approve or request changes |
| ABIX PS Program Overview | Portfolio | `1212775592612914` | ✅ DRAFTED | Richard: review Section 3a above, approve or request changes |
| ABPS Program Overview | Portfolio | `1212762061512816` | ✅ DRAFTED | Richard: review Section 3b above, approve or request changes |

### Known Gaps (to populate after probing or from Richard)

- [ ] AU Google Ads account link
- [ ] MX Google Ads account link
- [ ] MX CPA target (MXN)
- [ ] AU/MX current bid strategies
- [ ] AU/MX monthly budgets
- [ ] WBR dashboard links
- [ ] JP market details (tasks, goals, status)
- [ ] EU5 market details beyond EU SSR Acq
- [ ] NA market details beyond Paid App goals

### Next Steps

1. **Richard reviews** all four drafts in this document
2. **Agent probes** AU, MX, ABIX PS, ABPS via Asana MCP to confirm writable surfaces (Task 7.1, 8.1)
3. **Agent writes** approved docs to confirmed surfaces (Task 7.5, 8.5)
4. **Agent updates** asana-command-center.md Surface Capabilities table with probe results
5. **Monthly refresh** cycle begins — Context_Writer updates sections per the cadence table above
