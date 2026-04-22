"""
Pre-draft keyword matcher — Task 3.4 of the skills-powers-adoption spec.

An AGENT BEHAVIOR codified as a documented procedure. NOT a scheduled process,
NOT an auto-running service. The agent reads this module's docstring and calls
its functions in-turn when reading a user request.

ACTIVATION FLOW (the ONLY machine-enforced activation path)

    The agent, on reading a user request, SHOULD:
      1. Call match_request_to_assets(request_text, triggers_from_inventory).
      2. If any match has score >=0.5 or exact phrase: invoke the strongest-match
         asset via discloseContext(name=...) or kiroPowers(action="activate",
         powerName=...).
      3. The activation tool's success automatically triggers append_activated(...)
         in activation_log.py.
      4. Proceed to draft the response with the activated skill's guidance in
         context.
      5. NO post-draft scan. NO pre-send re-check. Missed skills are surfaced only
         when Richard flags them (append_missed_by_feedback).

    This is the ONLY machine-enforced activation path. Explicitly NOT an
    auto-running service — the matcher runs in-turn inside the agent session,
    called by the agent as part of its normal request-reading flow.
    Per design §Anti-Goals #1 ("not an ongoing audit service") and §Anti-Goals
    #10 ("no post-draft / pre-send self-scan").

SEPARATION OF CONCERNS

    matcher.py returns CANDIDATES and SCORES. It does NOT:
      - call discloseContext or kiroPowers (no tool coupling)
      - append to activation-log.jsonl (no log coupling)
      - maintain state across calls (pure function)

    The agent is responsible for:
      - choosing to invoke the activation tool based on the candidates returned
      - invoking the right activation tool for the kind (skill vs power)
      - the success of that invocation then triggers append_activated(...)
        via the activation-tool-success wrapper

    Three separate concerns, three separate modules. Per design §Architecture
    Phase D ("Activation Logging is continuous — one line per invocation") and
    §Design Decisions → "Why missed-skill detection was cut".

MATCH POLICY (per design §Adoption Habit Integration)

    A candidate asset matches a request when EITHER:
      a) >=50% of its trigger tokens appear somewhere in the request text
         (overlap = |request_tokens intersect trigger_tokens| / |trigger_tokens|), OR
      b) At least one exact trigger-phrase appears verbatim in the request
         text (case-insensitive). An "exact trigger-phrase" is one of the
         comma-separated entries from the Triggers column (skills) or one
         of the strings in the `keywords` array (powers).

    Match score for ranking:
      - Exact phrase match contributes score = 1.0 (highest priority).
      - Otherwise, score = token-overlap ratio (0.0 to 1.0).
      - Multiple matches are sorted descending by score; ties broken by
        most-recently-activated (caller supplies this ordering hint — matcher
        itself returns ties in alphabetical order, deterministic for tests).

CLI

    python3 matcher.py match "I need to write a WBR callout for AU"
    -> prints matching assets with kind, name, score, and match-reason.
"""

from __future__ import annotations

import re
import string
import sys
from pathlib import Path
from typing import Any


# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------

_HOME = Path.home()
DEFAULT_INVENTORY_PATH = _HOME / "shared" / "context" / "skills-powers" / "inventory.md"
DEFAULT_POWERS_ROOT = _HOME / ".kiro" / "powers" / "installed"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

MATCH_THRESHOLD = 0.5  # per design §Adoption Habit Integration
_PUNCT_STRIP = str.maketrans("", "", string.punctuation.replace("-", "").replace("_", ""))
# We preserve hyphens/underscores because asset names are hyphenated
# (e.g., "wbr-callouts", "bridge-sync"). All other punctuation is stripped.


# ----------------------------------------------------------------------------
# Tokenization
# ----------------------------------------------------------------------------


def _normalize(s: str) -> str:
    """Lowercase, strip punctuation (except -, _), collapse whitespace."""
    s = s.lower().translate(_PUNCT_STRIP)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _tokenize(s: str) -> list[str]:
    """Split on whitespace after normalization."""
    s = _normalize(s)
    if not s:
        return []
    return s.split(" ")


# ----------------------------------------------------------------------------
# Inventory parsing — extract per-asset trigger phrases
# ----------------------------------------------------------------------------


def _parse_skill_triggers_from_inventory(inventory_text: str) -> dict[str, list[str]]:
    """
    Parse the Skills table from inventory.md and return {name: [trigger_phrases]}.

    Rows look like:
      | K-S6 | wbr-callouts | legacy | WBR, callout, weekly callout, market callout | ... |

    Trigger phrases are the comma-separated list in column 4.
    Skips rows whose Triggers cell is "(no trigger clause)" or "(invoke-on-...)".
    """
    skills: dict[str, list[str]] = {}
    in_skills_section = False
    for line in inventory_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Skills"):
            in_skills_section = True
            continue
        if stripped.startswith("## ") and in_skills_section:
            # End of skills section (next H2)
            break
        if not in_skills_section:
            continue
        if not stripped.startswith("| K-S"):
            continue
        # Parse table row. Split by pipe and drop leading/trailing empties.
        cells = [c.strip() for c in stripped.split("|")]
        # cells = ['', 'K-S6', 'wbr-callouts', 'legacy', 'WBR, callout, ...', ...]
        if len(cells) < 5:
            continue
        name = cells[2]
        triggers_cell = cells[4]
        if triggers_cell.startswith("(") and triggers_cell.endswith(")"):
            # Placeholder like "(no trigger clause)" — no triggers to extract.
            skills[name] = []
            continue
        phrases = [p.strip() for p in triggers_cell.split(",") if p.strip()]
        skills[name] = phrases
    return skills


def _parse_power_keywords_from_frontmatter(power_md_text: str) -> list[str]:
    """
    Extract the `keywords` list from a POWER.md file's YAML frontmatter.

    The expected shape is a single line:
      keywords: ["a", "b", "c"]
    We parse this with a regex to avoid a YAML dependency here (the matcher
    is a light-touch agent behavior; inventory.py already has PyYAML).
    """
    # Isolate frontmatter between the first two --- fences.
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", power_md_text, flags=re.DOTALL)
    if not m:
        return []
    fm = m.group(1)
    kw_line = None
    for line in fm.splitlines():
        if line.lstrip().startswith("keywords:"):
            kw_line = line
            break
    if kw_line is None:
        return []
    # Extract the list body between the first [ and last ].
    lb = kw_line.find("[")
    rb = kw_line.rfind("]")
    if lb == -1 or rb == -1 or rb < lb:
        return []
    list_body = kw_line[lb + 1 : rb]
    # Split on commas, strip whitespace and quotes.
    items: list[str] = []
    for raw in list_body.split(","):
        val = raw.strip().strip('"').strip("'").strip()
        if val:
            items.append(val)
    return items


def _parse_power_triggers_from_disk(
    inventory_text: str,
    powers_root: Path,
) -> dict[str, list[str]]:
    """
    For each power in the inventory's Powers table, load POWER.md and read its
    `keywords` array. Returns {name: [keyword_phrases]}.

    Powers that exist in inventory but whose POWER.md is missing on disk are
    returned with [] (defensive).
    """
    power_names: list[str] = []
    in_powers_section = False
    for line in inventory_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Powers"):
            in_powers_section = True
            continue
        if stripped.startswith("## ") and in_powers_section:
            break
        if not in_powers_section:
            continue
        if not stripped.startswith("| K-P"):
            continue
        cells = [c.strip() for c in stripped.split("|")]
        if len(cells) < 3:
            continue
        power_names.append(cells[2])

    out: dict[str, list[str]] = {}
    for name in power_names:
        power_md = powers_root / name / "POWER.md"
        if not power_md.is_file():
            out[name] = []
            continue
        try:
            text = power_md.read_text(encoding="utf-8")
        except OSError:
            out[name] = []
            continue
        out[name] = _parse_power_keywords_from_frontmatter(text)
    return out


# ----------------------------------------------------------------------------
# Public API — trigger extraction
# ----------------------------------------------------------------------------


def extract_triggers_from_inventory(
    inventory_md_path: Path | str = DEFAULT_INVENTORY_PATH,
    powers_root: Path | str = DEFAULT_POWERS_ROOT,
) -> dict[str, dict[str, list[str]]]:
    """
    Parse the rendered inventory.md to pull per-asset trigger lists.

    Returns a nested dict:
        {
          "skill": {name: [trigger_phrases], ...},
          "power": {name: [keyword_phrases], ...},
        }

    Skills: triggers come from inventory.md's Triggers column (comma-separated
    phrases from the skill's description "Triggers on ..." clause).
    Powers: keywords come from each POWER.md's frontmatter `keywords` array,
    loaded from disk (inventory.md does not list keywords per power).
    """
    inventory_md_path = Path(inventory_md_path)
    powers_root = Path(powers_root)
    if not inventory_md_path.is_file():
        return {"skill": {}, "power": {}}
    text = inventory_md_path.read_text(encoding="utf-8")
    return {
        "skill": _parse_skill_triggers_from_inventory(text),
        "power": _parse_power_triggers_from_disk(text, powers_root),
    }


# ----------------------------------------------------------------------------
# Public API — matching
# ----------------------------------------------------------------------------


def _phrase_tokens(phrase: str) -> list[str]:
    """Tokens from one trigger phrase."""
    return _tokenize(phrase)


def _all_trigger_tokens(phrases: list[str]) -> set[str]:
    """Union of tokens across all trigger phrases for one asset."""
    toks: set[str] = set()
    for p in phrases:
        toks.update(_phrase_tokens(p))
    return toks


def _request_contains_phrase(request_norm: str, phrase: str) -> bool:
    """Exact phrase match (case-insensitive) as a substring with word boundaries."""
    phrase_norm = _normalize(phrase)
    if not phrase_norm:
        return False
    # Require the phrase to appear as a contiguous substring — this covers
    # both single-word and multi-word trigger phrases. We do a word-boundary
    # check so "wbr" does not match "wbrx".
    pattern = r"\b" + re.escape(phrase_norm) + r"\b"
    return re.search(pattern, request_norm) is not None


def match_request_to_assets(
    request_text: str,
    triggers: dict[str, dict[str, list[str]]],
) -> list[tuple[str, str, float, str]]:
    """
    Score every asset against the request.

    Returns a list of (kind, name, score, reason) tuples, sorted by:
      1. score DESC
      2. name ASC (deterministic tiebreak for tests; caller may re-break on
         most-recently-activated using activation-log data)

    `reason` is a short human-readable explanation:
      - "exact phrase: '<phrase>'"     (exact match — score = 1.0)
      - "token overlap <N>/<M>"        (token overlap — score = N/M ratio)
      - "no match"                      (below threshold; excluded from return)

    Only assets meeting the match policy are returned (score >= 0.5 OR exact
    phrase match).
    """
    results: list[tuple[str, str, float, str]] = []
    request_norm = _normalize(request_text)
    request_tokens = set(_tokenize(request_text))

    for kind, by_name in triggers.items():
        for name, phrases in sorted(by_name.items()):
            if not phrases:
                # Assets with no trigger phrases can never match via this path.
                continue
            # 1. Check for exact phrase match.
            exact_hit: str | None = None
            for p in phrases:
                if _request_contains_phrase(request_norm, p):
                    exact_hit = p
                    break
            if exact_hit is not None:
                results.append((kind, name, 1.0, f"exact phrase: '{exact_hit}'"))
                continue
            # 2. Fall back to token-overlap ratio.
            trigger_tokens = _all_trigger_tokens(phrases)
            if not trigger_tokens:
                continue
            overlap = request_tokens & trigger_tokens
            ratio = len(overlap) / len(trigger_tokens)
            if ratio >= MATCH_THRESHOLD:
                results.append(
                    (
                        kind,
                        name,
                        ratio,
                        f"token overlap {len(overlap)}/{len(trigger_tokens)}",
                    )
                )

    # Sort: score DESC, then name ASC for deterministic tests.
    results.sort(key=lambda r: (-r[2], r[1]))
    return results


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def _cli(argv: list[str]) -> int:
    if len(argv) < 3 or argv[1] != "match":
        print(
            'usage: python3 matcher.py match "<request text>"',
            file=sys.stderr,
        )
        return 2
    request_text = argv[2]
    triggers = extract_triggers_from_inventory()
    matches = match_request_to_assets(request_text, triggers)
    if not matches:
        print("(no matches)")
        return 0
    print(f"request: {request_text!r}")
    print(f"matches ({len(matches)}):")
    for kind, name, score, reason in matches:
        print(f"  [{kind}] {name:<18} score={score:.2f}  ({reason})")
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
