> **SUPERSEDED — 2026-05-03 end-of-day.** This handoff is kept for provenance only. Do not execute its build spec. Two of its load-bearing assumptions turned out wrong once kiro-local tested them:
> 1. **DuckDB postgres extension was the wrong client.** Plain PG wire-protocol auth fails Shepherd audit even when network works. Canonical path is Redshift Data API (port 443) or the JDBC driver with `groupFederation=true`.
> 2. **Network wasn't DevSpaces-specific.** kiro-local hit the same TCP timeout on :8192 from Windows on corp VPN. rs-01 is `PubliclyAccessible:True` but SGs restrict source CIDRs that don't include either environment.
>
> **What actually shipped (2026-05-03):** Path 1 — Hubble + QuickSuite for teammates, MotherDuck unchanged for agent-side. Teammate-facing artifact is `paid-search-hubble-query-library.docx` (v3.1) in SharePoint `AB-Paid-Acq-Team/methodology/`. Path 2 (Data API + IAM ticket on `Redshift_Person_SDO_Identity_Access_Role`) is drafted but dormant — triggers only on a concrete programmatic need.
>
> **Full thread:** `/shared/user/agent-bus/threads/redshift-programmatic-access/` and `hubble-query-library-audit/`. Session-log entries 2026-05-03 from "kiro-local returned test results" onward.

---

# Handoff to kiro-local — PS Analytics Redshift Path Build (ORIGINAL — SUPERSEDED)

**From:** kiro-server (DevSpaces)
**To:** kiro-local (Mac on VPN)
**Date:** 2026-05-03
**Why this exists:** kiro-server proved the auth path works end-to-end but hit a network wall — DevSpaces can't reach the ABDAI Redshift VPC. The build has to happen on your Mac where VPN is available. Everything in this doc is verified and deterministic; no discovery work is needed from you, just execution.

---

## TL;DR

Connect Richard's local Kiro to the ABDAI Redshift sandbox so he can query `abbd_sandbox_mktg` (and other marketing-relevant schemas) programmatically from agent hooks and ad-hoc Python scripts, same ergonomics as the current MotherDuck MCP. Access is already granted via LDAP — this is purely setup.

**Success criteria:**
1. `SELECT current_user;` runs from local Python via `ada` + DuckDB postgres extension
2. One real query against `abbd_sandbox_mktg` returns rows
3. A hook or CLI wrapper that teammates (or future kiro-server sessions) could use exists at a documented path
4. Parity check: one metric query gives consistent results between MotherDuck `ps_analytics` and Redshift (where that metric exists in both)

**Non-goals for this session:**
- Do not migrate DuckDB hooks to Redshift. Agent-side DevSpaces hooks stay on MotherDuck (they can't reach Redshift). This build is for *Richard's local* and *teammate-facing* surfaces only.
- Do not file any tickets. Access is already confirmed.
- Do not write to Redshift. RO only.

---

## Background — how we got here

Three sessions with kiro-server evolved the recommendation:

1. **2026-05-02 session 1:** Recommended "file SIM to `ABBD-SANDBOX-MGRS-DDL` for shared write access." Wrong starting point.
2. **2026-05-03 morning:** Discovered Richard already has RO LDAPs (`ABDAI-ATLAS-RO`, `RS-ABBD-SANDBOX-MARKETING`, `ABDAI-SANDBOX-RO`). No tickets needed for read path.
3. **2026-05-03 afternoon:** Tested `ada + DuckDB` from DevSpaces. Auth works, network doesn't — VPC egress blocked from container. Concluded: programmatic Redshift access has to be on Mac over VPN; DevSpaces hooks stay on MotherDuck.

The decision boundary that emerged:
- **DevSpaces (agent-side compute):** MotherDuck. Unchanged.
- **Local Mac (Richard's programmatic access):** Redshift via ada + DuckDB postgres extension. **This is what you're building.**
- **Teammates (human self-serve):** Hubble browser + QuickSuite. Separate track, not blocked on you.

Full history in `~/shared/context/intake/session-log.md` entries dated 2026-05-02 through 2026-05-03.

---

## Verified facts — do not re-derive

These were confirmed with tool calls during kiro-server sessions. Trust them.

### Access
- Richard's LDAP memberships (verified via permissions.amazon.com/a/user/prichwil):
  - `ABDAI-ATLAS-RO` — Redshift cluster read access
  - `ABDAI-SANDBOX-RO` — sandbox schemas read access
  - `RS-ABBD-SANDBOX-MARKETING` — marketing sandbox logical DB
  - `AB_DATA_EXPLORER_USERS` — Shelley-org data access
  - Plus QuickSuite groups (`ab-cbd-quicksight-access`, `QSConsumerL5`, etc.)
- Boto3 `redshift.get_cluster_credentials_with_iam` returned temp user `CDO:amzn:cdo:person:prichwil` — AWS authorizes him. **No access SIM needed.**

### Connection parameters (from ABDAI Andes3.0 FAQ wiki)
```
AWS Account:  148928884632
Role:         Redshift_Person_SDO_Identity_Access_Role
Provider:     conduit
Profile:      ABDAI_Redshift

Cluster ID:   abdw-dev-rs-01
Database:     abatlasdtl
Host:         abdw-dev-rs-01.ccfkbzcxqcix.us-east-1.redshift.amazonaws.com
Port:         8192
Region:       us-east-1
```

There's a second cluster `abdw-dev-rs-02` behind a VPCE endpoint. Stick with `abdw-dev-rs-01` for this build. ABDAI load-balances between them via the logical DB `l_abatlas` but you don't need that complexity yet.

### Relevant schemas on the cluster
| Schema | What's in it | Owner (FYI) |
|---|---|---|
| `abbd_sandbox_mktg` | AB Marketing sandbox — primary target | Naresh Chevula (chevulan@) |
| `abbd_sandbox_mgrs` | ABMA Marketing Managers sandbox | Nitisha Gupta (gupnitis@) |
| `abbd_sandbox_eu_bi` | EU BI (Europe marketing data) | — |
| `abbd_dtl`, `abbd_agg` | ABDAI detail/aggregate layers | ABDAI team |
| `andes.*` | Andes 3.0 datashares (different auth path — datanet user, skip this session) | — |

Start with `abbd_sandbox_mktg`. Schema owner has granted the relevant SELECT grants to `abbd_sandbox_ro` and `ABDAI-ATLAS-RO` already.

### What's installed where
- On Richard's Mac, expected present: `toolbox`, `ada`, Midway setup. Confirm with `which ada && which mwinit`.
- If missing: install toolbox per https://builderhub.corp.amazon.com/docs/builder-toolbox/user-guide/getting-started.html#install-toolbox-macos, then `toolbox install ada`.
- Python: needs `duckdb >= 0.9` (postgres extension) and `boto3`. pip-install if absent.

### Known auth gotcha
`ada credentials print` creds last ~1 hour. Redshift `get_cluster_credentials_with_iam` hands out a 15-min DB password. The DuckDB ATTACH has to happen within that window. For a long-running script, re-fetch creds on expiry — don't cache across boundaries.

---

## Build spec

### Phase 1: Prove the connection works (~15 min)

Goal: `SELECT current_user;` returns `CDO:amzn:cdo:person:prichwil` from local Python.

**Setup commands (run on Mac):**
```bash
# 1. Midway (once per day)
mwinit -o

# 2. Create ada profile (once, idempotent)
~/.toolbox/bin/ada profile add \
  --account 148928884632 \
  --profile ABDAI_Redshift \
  --provider conduit \
  --role Redshift_Person_SDO_Identity_Access_Role

# 3. Wire profile into ~/.aws/credentials for any SDK that reads it directly
tail -3 ~/.aws/config >> ~/.aws/credentials
# Then edit ~/.aws/credentials to make sure credential_process uses full path:
# credential_process = /Users/prichwil/.toolbox/bin/ada credentials print --profile ABDAI_Redshift
# (On some Mac setups the path is $HOME/.toolbox/bin/ada — use whichever exists)

# 4. Verify
~/.toolbox/bin/ada credentials print --profile ABDAI_Redshift | head -c 80
# Should print '{"Version":1,"AccessKeyId":"ASIA...'
```

**Python smoke test** — save as `~/code/redshift-tools/smoke.py` or wherever your local project lives:
```python
#!/usr/bin/env python3
"""Smoke test: Redshift over ada + DuckDB postgres extension."""
import json
import subprocess
import sys

CLUSTER_ID = "abdw-dev-rs-01"
DB_NAME = "abatlasdtl"
HOST = "abdw-dev-rs-01.ccfkbzcxqcix.us-east-1.redshift.amazonaws.com"
PORT = 8192
REGION = "us-east-1"
PROFILE = "ABDAI_Redshift"
ADA_PATH = "/Users/prichwil/.toolbox/bin/ada"  # adjust if ada lives elsewhere


def get_redshift_temp_creds():
    ada_out = subprocess.check_output(
        [ADA_PATH, "credentials", "print", "--profile", PROFILE],
        text=True,
    )
    creds = json.loads(ada_out)

    import boto3
    rs = boto3.client(
        "redshift",
        region_name=REGION,
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )
    cluster_creds = rs.get_cluster_credentials_with_iam(
        ClusterIdentifier=CLUSTER_ID,
        DbName=DB_NAME,
        DurationSeconds=900,  # 15 min max for IAM-issued creds
    )
    return cluster_creds["DbUser"], cluster_creds["DbPassword"]


def connect():
    """Returns a duckdb connection with Redshift attached as 'rs'."""
    import duckdb
    db_user, db_pass = get_redshift_temp_creds()

    con = duckdb.connect(":memory:")
    con.execute("INSTALL postgres; LOAD postgres;")

    # Escape single-quotes in password (they appear in IAM-issued passwords)
    escaped_pass = db_pass.replace("'", "''")
    attach_sql = (
        f"ATTACH 'host={HOST} port={PORT} dbname={DB_NAME} "
        f"user={db_user} password={escaped_pass} sslmode=require' "
        f"AS rs (TYPE postgres, READ_ONLY)"
    )
    con.execute(attach_sql)
    return con


def main():
    con = connect()

    # 1. Identity check
    r = con.execute("SELECT current_user FROM rs.pg_catalog.pg_tables LIMIT 1").fetchone()
    print(f"[OK] current_user = {r[0]}")

    # 2. List mktg schema tables
    print("\n=== abbd_sandbox_mktg (first 20 tables) ===")
    rows = con.execute("""
        SELECT tablename
        FROM rs.pg_catalog.pg_tables
        WHERE schemaname = 'abbd_sandbox_mktg'
        ORDER BY tablename
        LIMIT 20
    """).fetchall()
    for (t,) in rows:
        print(f"  {t}")

    # 3. Count rows on first table (sanity)
    if rows:
        t = rows[0][0]
        n = con.execute(f"SELECT COUNT(*) FROM rs.abbd_sandbox_mktg.{t}").fetchone()[0]
        print(f"\n[OK] rs.abbd_sandbox_mktg.{t} has {n:,} rows")


if __name__ == "__main__":
    main()
```

**Expected output (if VPN is up and LDAP access is valid):**
```
[OK] current_user = CDO:amzn:cdo:person:prichwil
=== abbd_sandbox_mktg (first 20 tables) ===
  <some table names>
[OK] rs.abbd_sandbox_mktg.<table> has N rows
```

**Failure modes and remediations:**
| Symptom | Cause | Fix |
|---|---|---|
| `Failed to refresh process-based credentials` | Midway expired | `mwinit -o` |
| `Connection timed out` to port 8192 | VPN down, or routing weird | Reconnect to corp VPN, retry |
| `Unauthorized` from Redshift | LDAP membership not propagated | Wait 10min, retry. Shouldn't happen — verified yesterday. |
| `get_cluster_credentials_with_iam` denied | IAM role not assuming correctly | Re-run `ada profile add`, verify profile in `~/.aws/config` |
| `permission denied for schema abbd_sandbox_mktg` | Schema owner hasn't granted SELECT to your SDO | Shouldn't happen — mktg schema grants to ABDAI-ATLAS-RO. If it does, query a different sandbox or grant-check. |

### Phase 2: Wrap as reusable module (~30 min)

Don't leave this as a one-off script. Make it a module Richard's other tools can import.

Suggested location: `~/code/redshift-tools/ps_redshift/__init__.py`

API shape to aim for (mirror the DuckDB MCP pattern so consumers barely notice):
```python
from ps_redshift import query, query_df

# Simple query → list of rows
rows = query("SELECT current_user")

# Pandas DataFrame
df = query_df("""
    SELECT region_id, SUM(spend_usd) AS spend
    FROM rs.abbd_sandbox_mktg.<some_daily_table>
    WHERE date_key >= CURRENT_DATE - 7
    GROUP BY region_id
""")
```

Connection caching: keep the DuckDB con alive across calls, but detect cred expiry (catch the Redshift-side auth error, re-fetch creds, re-attach, retry once). Don't build a fancy connection pool — this is single-user on Richard's laptop.

### Phase 3: One real parity check (~20 min)

Pick one metric that exists in both MotherDuck `ps_analytics.ps.v_weekly` and somewhere in `abbd_sandbox_mktg`. Run it both places. Report delta.

**Suggested target:** weekly US paid search registrations for the last 4 weeks. MotherDuck's `ps.v_weekly` has this. Find the equivalent in `abbd_sandbox_mktg` (query schema first — don't guess table names).

If numbers match within 1-2% → parity confirmed, MotherDuck scrape is faithful.
If they diverge materially → flag to Richard. That's a signal about which source is actually ground truth. Don't try to reconcile; just surface.

**What "parity" proves:** that when you migrate teammate-facing views from MotherDuck-derived dashboards to Redshift-backed ones, users won't see the numbers jump.

### Phase 4: Document what you built (~10 min)

Write back to `~/shared/context/handoffs/2026-05-03-kiro-local-redshift-build-COMPLETE.md` with:
- Path to the module
- Example queries that work
- Any gotchas you hit that aren't in this doc
- Parity result (delta %, which table matched which)
- What you'd do next if we extend this

---

## What's intentionally out of scope

**Do not do these — they're separate tracks:**
- QuickSuite Q Topic setup (browser, not code — Richard can click through himself)
- Hubble query examples (browser)
- Writing data back to a `abbd_sandbox_ps` schema (needs DDL ticket, separate conversation)
- Porting the MotherDuck hook system to Redshift (DevSpaces can't reach Redshift — architectural boundary, not a build task)
- Anything that requires filing a SIM

**Do not touch:**
- `~/.aws/credentials` beyond adding the one ABDAI_Redshift profile — don't rewrite existing profiles
- DuckDB MCP configuration (`~/.kiro/settings/mcp.json`) — leave as-is this session, we'll decide whether to add a Redshift MCP separately once Phase 1-3 prove out

---

## Decision log (so you don't have to rediscover)

| Question | Answer | Source |
|---|---|---|
| Why DuckDB postgres extension, not psycopg2 or redshift_connector? | DuckDB already in the MotherDuck stack, same query dialect (mostly), no extra install. Redshift speaks postgres wire, so DuckDB's postgres extension works. | kiro-server test 2026-05-03 |
| Why not SQL Workbench / DataGrip? | Those are human interfaces. This is for programmatic use. If Richard wants a GUI too, tell him to install DBeaver — docs in ABDAI Andes3.0 FAQ §2.8. | scope |
| Why 15-min IAM-issued DB passwords, not a longer-lived credential? | AWS `get_cluster_credentials_with_iam` hard-caps at 900 seconds. Not negotiable. Cache the ada creds (~1h) and re-fetch DB creds on expiry. | AWS API |
| Why `abdw-dev-rs-01` not `abdw-dev-rs-02`? | Both work, rs-01 has a public-ish endpoint that's simpler. rs-02 requires VPCE interface endpoint routing. Can switch later if load balancing matters. | ABDAI FAQ 2.6 |
| Can I just use Hubble? | Yes, and Richard should for ad-hoc. But Hubble isn't programmatic — no Python API, no hook integration. This build exists to unblock the agent/scripting path. | kiro-server judgment |

---

## Interface with kiro-server (future)

Once Phase 1-3 are done, if we ever want kiro-server (DevSpaces) to read Redshift, the only viable path is:
1. A proxy Richard runs on his Mac that exposes Redshift-backed data over HTTPS, callable from DevSpaces
2. Or an export pipeline that ships Redshift extracts to MotherDuck on a schedule

Both are v2 work, not this session. Flag to Richard if you see a strong use case emerge while building.

---

## Sign-off

kiro-server has done the auth verification, endpoint discovery, and architecture mapping. You have everything needed to execute. The only thing that could go wrong during your session is VPN or Midway state — both solvable in under 2 minutes by Richard.

If you hit a genuine unknown (schema-owner grant missing, unexpected error shape, etc.), log it in `~/shared/context/intake/session-log.md` and flag to Richard before improvising. Do not file tickets on his behalf. Do not email ABMA oncall. Surface the blocker and let him decide.

Good hunting.
