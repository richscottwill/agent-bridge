"""
Activation log writer — Phase D of the skills-powers-adoption spec.

Append-only JSONL writer for ~/shared/context/skills-powers/activation-log.jsonl.
Implements three event types from design §Data Model → Activation log:

  1. `activated`        — emitted AUTOMATICALLY on every successful
                          discloseContext(...) / kiroPowers activate(...).
                          Written by `append_activated(...)`.

  2. `missed-by-feedback` — emitted ONLY when Richard explicitly flags a missed
                          activation. No auto-detection, no pre-send scanner,
                          no post-draft loop. Written by
                          `append_missed_by_feedback(...)`.
                          Per design §Anti-Goals #10 and §Design Decisions →
                          "Why missed-skill detection was cut".

  3. `correction`       — erratum for a prior row. Appended (never mutates the
                          erroneous row). Written by `append_correction(...)`.

WRITE DISCIPLINE (all three functions)

    Open file with mode="a" (append-only). Write one JSON line + "\\n".
    flush() then os.fsync(fileno()) so the row survives an interrupt or SIGKILL
    mid-session. No truncation, no rewriting, no mutation of prior rows. The
    file can only grow. Parent directory auto-created if missing.

TIMESTAMP FORMAT

    datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    Example: "2026-04-22T16:30:45-0700". Offset without colon, matching the
    baseline rows written by Group 1.

SESSION ID

    If caller omits session_id, auto-generate:
      datetime.now().strftime("sess-%Y-%m-%d-%H%M%S")
    The log is portable — session_id is a label for humans reading the log
    later, not a DB key.

SCOPE

    Write-only against ~/shared/context/skills-powers/activation-log.jsonl.
    Does NOT read the log. Does NOT know about inventory.md. Does NOT call
    any activation tool. The matcher (matcher.py) surfaces candidates; the
    agent invokes the activation tool; the activation tool's success triggers
    append_activated(...). These are three separate concerns.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------

HOME = Path(os.path.expanduser("~"))
LOG_DIR = HOME / "shared" / "context" / "skills-powers"
LOG_PATH = LOG_DIR / "activation-log.jsonl"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

Kind = Literal["skill", "power"]

_REQUEST_SUMMARY_MAX = 120
_FEEDBACK_TEXT_MAX = 200
_CORRECTION_REASON_MAX = 200
_TRUNCATE_SUFFIX = "\u2026"  # horizontal ellipsis — one visible char

# Valid subtypes for `created` event per design §Data Model → Activation log.
# "created" — new asset written via Phase C safe-creation (new-asset path)
# "classified" — legacy asset reclassified to `current` via touch-it-classify-it
_CREATED_SUBTYPES = ("created", "classified")


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _now_ts() -> str:
    """ISO 8601 with tz offset, no colon in offset. Matches Group 1 baseline."""
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")


def _auto_session_id() -> str:
    """Generate a human-readable session id from the current local clock."""
    return datetime.now().strftime("sess-%Y-%m-%d-%H%M%S")


def _truncate(s: str, max_chars: int) -> str:
    """Truncate to max_chars and append U+2026 (…) if truncation occurred."""
    if len(s) <= max_chars:
        return s
    # We replace the final char with the ellipsis so total length == max_chars.
    return s[: max_chars - 1] + _TRUNCATE_SUFFIX


def _ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _append_row(row: dict) -> None:
    """
    Append one JSON line to activation-log.jsonl with fsync.

    JSON is dumped with ensure_ascii=False so Unicode (e.g., the U+2026
    ellipsis added by _truncate) round-trips cleanly. separators default
    (", ", ": ") is kept for parity with the baseline rows.
    """
    _ensure_log_dir()
    line = json.dumps(row, ensure_ascii=False) + "\n"
    with open(LOG_PATH, mode="a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def _validate_kind(kind: str) -> Kind:
    if kind not in ("skill", "power"):
        raise ValueError(f"kind must be 'skill' or 'power', got {kind!r}")
    return kind  # type: ignore[return-value]


# ----------------------------------------------------------------------------
# Task 3.1 — `activated` event
# ----------------------------------------------------------------------------


def append_activated(
    kind: Kind,
    name: str,
    request_summary: str,
    session_id: str | None = None,
) -> dict:
    """
    Append one `activated` row to the activation log.

    Shape per design §Data Model → Activation log:
        {"event":"activated","kind":"skill"|"power","name":"{n}",
         "request_summary":"{≤120 chars}","session_id":"{sess}",
         "ts":"{ISO8601 with tz}"}

    Caller contract:
      - Called by the activation-tool-success wrapper — i.e., after a
        discloseContext or kiroPowers activate call that succeeded.
      - `request_summary` is a short free-text description of what the user
        asked for (truncated to 120 chars if longer).
      - `session_id` defaults to sess-YYYY-MM-DD-HHMMSS if omitted.

    Returns the row as a dict (for inspection / testing); the row is
    already persisted to disk before returning.
    """
    _validate_kind(kind)
    row = {
        "event": "activated",
        "kind": kind,
        "name": name,
        "request_summary": _truncate(request_summary, _REQUEST_SUMMARY_MAX),
        "session_id": session_id or _auto_session_id(),
        "ts": _now_ts(),
    }
    _append_row(row)
    return row


# ----------------------------------------------------------------------------
# Task 3.2 — `missed-by-feedback` event
# ----------------------------------------------------------------------------


def append_missed_by_feedback(
    kind: Kind,
    name: str,
    feedback_text: str,
    session_id: str | None = None,
) -> dict:
    """
    Append one `missed-by-feedback` row.

    CRITICAL INVARIANT (restated here because it is easy to violate):
      This function is NEVER called automatically. There is no pre-send
      scanner, no post-draft detector, no "remember to check if I missed a
      skill" pattern. It is called ONLY when Richard explicitly flags a
      missed activation after the fact, e.g.,
          "you should have activated the coach skill for that"
          "you missed wbr-callouts"
      The agent receives Richard's feedback, then calls this function.

      Per design §Anti-Goals #10 ("No post-draft / pre-send self-scan") and
      §Design Decisions → "Why missed-skill detection was cut": the platform
      offers no event between response draft and response send, so any
      convention-based self-check recreates the "remember to remember"
      failure mode skills were designed to eliminate. Richard-flag-only is
      the ONLY source of `missed-by-feedback` rows.

    Shape:
        {"event":"missed-by-feedback","kind":"skill"|"power","name":"{n}",
         "feedback_text":"{≤200 chars}","session_id":"{sess}",
         "ts":"{ISO8601 with tz}"}
    """
    _validate_kind(kind)
    row = {
        "event": "missed-by-feedback",
        "kind": kind,
        "name": name,
        "feedback_text": _truncate(feedback_text, _FEEDBACK_TEXT_MAX),
        "session_id": session_id or _auto_session_id(),
        "ts": _now_ts(),
    }
    _append_row(row)
    return row


# ----------------------------------------------------------------------------
# Task 3.3 — `correction` event
# ----------------------------------------------------------------------------


def append_correction(
    target_ts: str,
    reason: str,
    session_id: str | None = None,
) -> dict:
    """
    Append one `correction` row referencing a prior row's `ts`.

    CRITICAL INVARIANT: this function APPENDS a new row. It does NOT mutate,
    delete, or rewrite the erroneous prior row. The log is append-only per
    design §Data Model → Activation log → "No updates, no deletes". A reader
    of the log sees both rows: the original (wrong) and the correction
    (referencing the wrong row's ts).

    Shape:
        {"event":"correction","target_ts":"{erroneous row ts}",
         "reason":"{≤200 chars}","session_id":"{sess}",
         "ts":"{ISO8601 with tz}"}

    `target_ts` should match the `ts` field of the erroneous row exactly so
    readers can join the correction to the original.
    """
    row = {
        "event": "correction",
        "target_ts": target_ts,
        "reason": _truncate(reason, _CORRECTION_REASON_MAX),
        "session_id": session_id or _auto_session_id(),
        "ts": _now_ts(),
    }
    _append_row(row)
    return row


# ----------------------------------------------------------------------------
# Task 6.4 — `pruned` event (Phase E pruning)
# ----------------------------------------------------------------------------


def append_pruned_event(
    kind: Kind,
    name: str,
    archive_path: str,
    session_id: str | None = None,
) -> dict:
    """
    Append one `pruned` row for a successfully archived + deleted asset.

    Called by Phase E (`pruning.post_prune_update`) after the source dir has
    been archived to the dated archive path and the source has been removed.

    Shape per design §Data Model → Activation log:
        {"event":"pruned","kind":"skill|power","name":"{n}",
         "archive_path":"{path}","session_id":"{sess}","ts":"{ISO8601}"}

    `archive_path` is expected to be HOME-relative (e.g.,
    "~/shared/wiki/agent-created/archive/skills-powers-pruned-YYYY-MM-DD/{n}/")
    so the log survives a $HOME move; callers SHOULD pass in that format.

    Returns the row as a dict; already persisted to disk before return.
    """
    _validate_kind(kind)
    row = {
        "event": "pruned",
        "kind": kind,
        "name": name,
        "archive_path": archive_path,
        "session_id": session_id or _auto_session_id(),
        "ts": _now_ts(),
    }
    _append_row(row)
    return row


# ----------------------------------------------------------------------------
# Task 5.6 — `created` event (new asset or legacy reclassification)
# ----------------------------------------------------------------------------


def append_created_event(
    kind: Kind,
    name: str,
    subtype: str,
    overlap_check_ref: str | None,
    session_id: str | None = None,
) -> dict:
    """
    Append one `created` row for a new asset write or legacy reclassification.

    Called by Phase C.5 (`post_creation_update`). Enforces the design's
    §Data Model → Activation log shape:

        {"event":"created","subtype":"{created|classified}",
         "kind":"skill|power","name":"{n}","session_id":"{sess}",
         "ts":"{ISO8601}","overlap_check_ref":"{path|null}"}

    Rules per design:
      - `subtype` MUST be one of {"created", "classified"}.
      - For subtype "created" (new asset), overlap_check_ref SHOULD point to
        the archived overlap-check.json.
      - For subtype "classified" (legacy migration), overlap_check_ref MUST
        be None — legacy reclassification has no overlap check to reference.

    Returns the row as a dict; already persisted to disk before return.
    """
    _validate_kind(kind)
    if subtype not in _CREATED_SUBTYPES:
        raise ValueError(
            f"subtype must be one of {_CREATED_SUBTYPES}, got {subtype!r}"
        )
    if subtype == "classified" and overlap_check_ref is not None:
        raise ValueError(
            "subtype 'classified' (legacy migration) MUST have "
            "overlap_check_ref=None; no overlap check is run on legacy "
            "reclassification per design §Phase C.1"
        )
    row: dict = {
        "event": "created",
        "subtype": subtype,
        "kind": kind,
        "name": name,
        "session_id": session_id or _auto_session_id(),
        "ts": _now_ts(),
        "overlap_check_ref": overlap_check_ref,
    }
    _append_row(row)
    return row


# ----------------------------------------------------------------------------
# Module-level smoke test entry (optional)
# ----------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    # Print the functions exported. No side effects when imported.
    print("activation_log module — append-only writer for activation-log.jsonl")
    print("  append_activated(kind, name, request_summary, session_id=None)")
    print("  append_missed_by_feedback(kind, name, feedback_text, session_id=None)")
    print("  append_correction(target_ts, reason, session_id=None)")
    print("  append_created_event(kind, name, subtype, overlap_check_ref, session_id=None)")
    print("  append_pruned_event(kind, name, archive_path, session_id=None)")
    print(f"  LOG_PATH = {LOG_PATH}")
