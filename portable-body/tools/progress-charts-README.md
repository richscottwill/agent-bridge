# Progress Charts — Agent Reference

Dense context for any agent executing the `update-dashboard` hook. Read this before running anything.

## What This Is

A stdlib-only Python script that reads 11 body organ files + tracker + changelog, parses structured data from markdown tables and patterns, and outputs a 5-page standalone HTML mini-site with Chart.js visualizations. Zero dependencies beyond Python 3 stdlib.

## How to Run

```bash
python3 ~/shared/tools/progress-charts/generate.py
```

Optional: `--output-dir path/` (default: `~/shared/tools/progress-charts/site/`)

Output: 5 HTML files in the site directory. Open `index.html` to start.

## Output Pages

| Page | File | What it shows |
|------|------|---------------|
| Overview | index.html | Summary cards linking to other pages, Five Levels progress bars, 30-Day Challenge checklist |
| Growth | growth.html | Autonomy spectrum (doughnut + inventory table), competence stage bars (6 principles × 4 stages) |
| Willpower | willpower.html | aMCC streak/resets/resistance, 30-Day Challenge, growth model table, pattern trajectory bars |
| Output | output.html | Weekly scorecard (artifacts/tools/low-leverage grouped bar), Five Levels, low-leverage breakdown |
| Autoresearch | autoresearch.html | Organ word budgets (horizontal bar), experiment savings (before/after bar), experiment log, queue, organ freshness |

## Data Sources (all paths relative to ~/)

| Parser | Source File | What it extracts |
|--------|------------|-----------------|
| `parse_gut_budgets()` | shared/context/body/gut.md | Organ word budget table: organ, budget, actual, utilization% |
| `parse_changelog()` | shared/context/changelog.md | Word savings (before→after), loop run dates, body totals, experiment statuses (CE-N → ADOPTED/REVERTED/QUEUED) |
| `parse_tracker_scorecard()` | shared/context/active/rw-tracker.md | Weekly scorecard: artifacts shipped, tools built, low-leverage hours. Parsed from `### Week of YYYY-MM-DD (WN)` sections |
| `parse_patterns()` | shared/context/body/nervous-system.md | Pattern table: name, status (VALIDATED/ACTIVE/NEW/RESOLVED/STUCK), weeks, trajectory (IMPROVING/STUCK/WORSENING), assessment |
| `parse_amcc()` | shared/context/body/amcc.md | Streak (current/longest), resets, hard thing, resistance types with counters, growth model table |
| `parse_five_levels()` | shared/context/body/brain.md | Levels 1-5: name, description, status (ACTIVE/NEXT/QUEUED/FUTURE). Parsed from `### Level N:` headers |
| `parse_organ_staleness()` | shared/context/body/*.md | Last-updated date from each organ's header, days since update |
| `parse_experiment_queue()` | shared/context/body/heart.md | Queued experiments: `### CE-N: Name — STATUS` |
| `parse_thirty_day_challenge()` | shared/context/active/rw-tracker.md | Checklist items from `## 30-Day Challenge` section, completion count, deadline |
| `parse_competence_stages()` | Computed from patterns + changelog | 6 principles scored 1-4 on competence model, with evidence strings |
| `parse_autonomy_spectrum()` | Hardcoded + shared/context/body/device.md | ~40 work functions classified as fully_agentic/agent_human/delegated/human. Device.md delegation statuses are dynamic. |

## Regex Patterns the Parsers Expect

The script is brittle to format changes in the source markdown. Here's what each parser matches:

- Gut budgets: `| organ | Nw | Nw | N% |`
- Changelog savings: `N,NNNw → N,NNNw` (both >500w and >200w)
- Changelog runs: `## 2026-MM-DD — Autoresearch Loop Run N`
- Changelog experiments: `CE-N ... ADOPTED|REVERTED|QUEUED|IN PROGRESS`
- Tracker weeks: `### Week of YYYY-MM-DD (WN)` then looks for `Strategic artifacts shipped | target | actual`, `Tools/automations built | target | actual`, `Hours on low-leverage work | <target | ~actual`
- Patterns: `| name | STATUS | weeks | TRAJECTORY | assessment |`
- aMCC streak: `Current streak | N day`, `Longest streak | N day`, `Streak resets (total) | N`
- aMCC hard thing: `**Ship something**`
- aMCC resistance: `| **type** | description | ... | "counter"`
- aMCC growth model: `metric | current | target_30d | target_90d |`
- Five Levels: `### Level N: Name` then block until next `### Level`
- Organ staleness: `Last updated: 2026-MM-DD` in first 500 chars
- Experiment queue: `### CE-N: Name — STATUS`
- 30-Day Challenge: `## 30-Day Challenge` section, `- [x] text` or `- [ ] text`

## What Can Break

1. If an organ file doesn't exist → that parser returns empty, chart is skipped with "No data" message
2. If markdown table format changes (extra columns, different separators) → parser silently returns empty
3. If `Last updated:` line is missing from an organ → staleness shows "unknown" / -1 days
4. Autonomy spectrum is mostly hardcoded — only delegation statuses from device.md are dynamic
5. Competence stages are computed with hardcoded logic — scores don't auto-update from organ data (except pattern count and changelog savings count)

## Modifying the Script

The script is ~1010 lines, structured as:
1. Lines 1-28: Imports, paths, constants
2. Lines 30-225: Parsers (all `parse_*` functions)
3. Lines 228-310: Shared HTML head/nav/footer
4. Lines 313-420: `build_overview()` — index.html
5. Lines 424-580: `build_growth()` — growth.html
6. Lines 584-720: `build_willpower()` — willpower.html
7. Lines 720-820: `build_output()` — output.html
8. Lines 822-960: `build_autoresearch()` — autoresearch.html
9. Lines 963-1010: `main()` — arg parsing, data collection, file output

Each `build_*` function returns a complete HTML string. They all call `shared_head(title, active_page)` and `shared_footer(now)`. Chart.js rendering is inline `<script>` at the bottom of each page.

## Design System

- Dark theme: `--bg:#0b0e11`, `--surface:#131820`, `--accent:#4da8da`
- Font: DM Sans via Google Fonts CDN
- Charts: Chart.js 4.4.1 via CDN
- Badge classes: `.b-improving` (green), `.b-stuck` (amber), `.b-worsening` (red), `.b-adopted` (green), `.b-reverted` (red), `.b-queued` (gray)
- Stat cards: `.stat` with `.v` (value) and `.l` (label)
- Navigation: sticky top bar with 5 page links, active state via `.nav-link.active`

## Rules for the Executing Agent

1. Read-only on all organ files. Never modify gut.md, heart.md, brain.md, or any source.
2. Run the script, report what was generated and any errors.
3. If a parser fails, diagnose which source file has a format mismatch — don't modify the source, flag it.
4. The `update-dashboard` hook is the ONLY entry point for regeneration. No other hook, loop step, or agent should call generate.py directly.
5. Output goes to `~/shared/tools/progress-charts/site/` (5 HTML files). The old `dashboard.html` in the parent directory is legacy.

## Portability

Standalone HTML, stdlib-only Python, Chart.js via CDN. No hooks, no MCP, no platform dependencies. Works in any browser on any platform. A new AI on a different platform can run `python3 generate.py` and get the same output with zero setup.
