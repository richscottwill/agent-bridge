<!-- DOC-0179 | duck_id: intake-motherduck-dive-lessons -->
# MotherDuck Dive Development Lessons

Captured from PS Forecast Tracker build (v1-v37, 2026-04-06).

## Critical Technical Patterns

### Pushing Large Content
- **Empty-param MCP failure**: When composing large JSX (>15KB) inline in the `sql` parameter, the tool call frequently emits with an empty parameter. This is a systemic issue, not a one-off.
- **Solution: SET VARIABLE + getvariable()**: Store content in a DuckDB variable, then pass it to the table function. This bypasses the "table function cannot contain subqueries" limitation.
  ```sql
  SET VARIABLE dive_content = (SELECT new_content FROM dive_edit);
  SELECT * FROM MD_UPDATE_DIVE_CONTENT(id='...', content=getvariable('dive_content'));
  ```
- **SQL Surgery pattern**: For small edits to existing Dives, use `MD_GET_DIVE` → temp table → REPLACE chains → SET VARIABLE → `MD_UPDATE_DIVE_CONTENT`. Avoids re-emitting the full component.
- **Full rebuild**: When changes touch multiple sections or risk JSX syntax issues, do a clean rebuild rather than surgical REPLACE. Minify aggressively.

### React/JSX Gotchas in Dives
- **Arrow functions break under minification**: `() => {}` can get mangled into `returnReact is not defined`. Use `function(){}` declarations instead.
- **DATE columns from DuckDB**: Return as `{days: N}` objects, not strings. React error #31 ("objects not valid as React child"). Fix: `CAST(column AS VARCHAR)` in views.
- **Style object surgery is fragile**: REPLACE on `{{padding:"5px 8px"}}` can create `}},fontWeight:` (double-brace) if not careful. Always verify brace matching after edits.
- **Row-level opacity interferes with background tint**: `opacity:0.5` on a `<tr>` halves the background color too. Use text color changes instead of opacity for dimming rows.
- **SVG fixed height causes zoom whitespace**: `height:700` stays fixed while width scales with container. Remove fixed height, let viewBox control aspect ratio: `style={{width:"100%"}}`.
- **Empty divs don't render as dividers**: A `<div>` with `width:1` and no content won't show. Use `borderLeft` on the adjacent element instead.

### Dive Architecture
- **useSQLQuery hook**: Each query is a separate hook call. Keep queries focused — one per data concern.
- **Dollar-quoting for content**: Use `$dive$...$dive$` to avoid quote escaping hell.
- **Template literals in SQL**: `'${market}'` inside useSQLQuery strings works for state-driven filtering.
- **String concatenation for dynamic columns**: `"SELECT " + cumCol + " as cum_value"` works for column selection based on state.

## Design Lessons

### Data Model
- **Cumulative > standalone**: For forecast tracking, cumulative actuals on a shared timeline is the right model. Standalone period predictions (780 regs in April) are less useful than cumulative endpoints (2,974 YTD by end of April).
- **Period-specific in tables, cumulative in charts**: Chart shows the running total growing. Tables show what happened in each period (computed as delta between consecutive cumulative values).
- **Predictions need revision tracking**: Store every revision with date, prior value, drift %, and reason. The `forecast_revisions` table enables drift analysis.
- **Narratives in DB, not hardcoded**: `forecast_narratives` table lets justifications update independently of the Dive code.

### Visual Design
- **Color = meaning, not decoration**: Use color only where it conveys information (green/yellow/red for accuracy, blue for actuals). Everything else should be neutral (dark navy #1a2744, near-black #2c3e50).
- **Quarter banding**: Alternating subtle tint (`rgba(26,39,68,0.05)`) on Q1/Q3 across chart and all tables creates visual rhythm without noise.
- **Three-layer x-axis**: Week numbers (darkest), month names (medium), quarter labels (lightest) — each at different font sizes and opacities.
- **KPI boxes inside the chart card**: Keeps the page top clean (just title + filters). KPI boxes sit between SVG and tables.
- **Hover tooltips in SVG**: Invisible larger circles as hover targets, tooltip rect flips left/right based on chart position.

## Dive ID Reference
- PS Forecast Tracker: `f39a3470-d7cf-45f4-b1d0-2bde437e948c` (v37 as of 2026-04-06)
- PS Team Testing Dashboard: `df173821-0ba2-47bc-86d7-8018517e92d5`
- Karpathy Autoresearch Lab: `d46b341a-21c4-4d82-b379-a95f0647d789`
- Monday Command Center: `e5328c74-1d35-4d5c-ad1e-3ad4a0b25007`
