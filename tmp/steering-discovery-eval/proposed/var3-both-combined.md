# Var3 — Both Layers (Soul Routing Extension + Steering Index)

**Mechanism:** Combine Var1 and Var2. soul.md gets the extended routing table (Canonical Resources by Task Type), AND a new always-on `steering-index.md` file is added.

**Rationale:** Redundancy by design. soul.md's table is where agents orienting on bootstrap will look first. steering-index.md is the dedicated, maintainable artifact. Both files agree on the mappings — soul.md is the summary, steering-index.md is the authority. If an agent misses one, the other catches it.

**Implementation:**
1. Add the "Canonical Resources by Task Type" table to `soul.md` (per Var1 spec)
2. Create `.kiro/steering/steering-index.md` with full directory (per Var2 spec)
3. soul.md's table links to steering-index.md for the full list, references the most common triggers inline

**Expected impact:**
- Maximum discoverability: two different paths to the same information
- Safety net: if one mechanism fails, the other covers

**Tradeoffs:**
- Most context cost of the three variations
- Two maintenance points (soul.md + steering-index.md must stay in sync)
- Adding redundancy violates principle #3 (subtraction before addition) — worth testing whether redundancy's value beats cost
