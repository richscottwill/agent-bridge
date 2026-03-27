"""Data models and custom exceptions for Wiki-SharePoint Sync."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------

class ConfigError(Exception):
    """Missing or invalid configuration file or fields."""


class AuthError(Exception):
    """OAuth authentication failure (bad credentials, expired, network)."""


class FrontMatterError(Exception):
    """Malformed or missing YAML front-matter in an article file."""


class GraphAPIError(Exception):
    """SharePoint Graph API failure (HTTP errors, network issues)."""


class ConversionError(Exception):
    """Markdown-to-HTML or markdown-to-docx conversion failure."""


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class ArticleMetadata:
    """Parsed front-matter metadata from a wiki article."""

    title: str
    status: str           # DRAFT, REVIEW, FINAL
    audience: str         # amazon-internal, personal, agent-only
    level: str | int      # 1-5 or N/A
    owner: str
    created: str          # YYYY-MM-DD
    updated: str          # YYYY-MM-DD
    update_trigger: str
    slug: str | None = None
    tags: list[str] | None = None


@dataclass
class ArticleAction:
    """Result of processing a single article during sync."""

    file_path: str
    action: str   # created, updated, skipped, conflicted, removed, failed
    mode: str     # site, directory
    sp_url: str | None = None
    error: str | None = None
    duration: float | None = None


@dataclass
class ConflictResult:
    """Result of conflict detection between local and SharePoint versions."""

    is_conflict: bool
    local_modified: str | None = None   # ISO timestamp or description
    sp_modified: str | None = None      # ISO timestamp from SharePoint
    details: str | None = None


@dataclass
class SyncReport:
    """Aggregated results from a sync run."""

    created: list[ArticleAction] = field(default_factory=list)
    updated: list[ArticleAction] = field(default_factory=list)
    skipped_unchanged: list[ArticleAction] = field(default_factory=list)
    skipped_filtered: list[ArticleAction] = field(default_factory=list)
    conflicted: list[ArticleAction] = field(default_factory=list)
    removed: list[ArticleAction] = field(default_factory=list)
    failed: list[ArticleAction] = field(default_factory=list)

    @property
    def has_failures(self) -> bool:
        """True when any article failed during sync."""
        return len(self.failed) > 0

    def summary(self) -> str:
        """Human-readable summary with counts and per-article details."""
        categories = [
            ("Created", self.created),
            ("Updated", self.updated),
            ("Skipped (unchanged)", self.skipped_unchanged),
            ("Skipped (filtered)", self.skipped_filtered),
            ("Conflicted", self.conflicted),
            ("Removed", self.removed),
            ("Failed", self.failed),
        ]

        lines: list[str] = ["Sync Report", "=" * 40]

        for label, actions in categories:
            lines.append(f"  {label}: {len(actions)}")

        total = sum(len(actions) for _, actions in categories)
        lines.append(f"  Total: {total}")
        lines.append("")

        for label, actions in categories:
            if actions:
                lines.append(f"{label}:")
                for a in actions:
                    detail = f"  - {a.file_path} [{a.mode}]"
                    if a.sp_url:
                        detail += f" → {a.sp_url}"
                    if a.error:
                        detail += f" ERROR: {a.error}"
                    if a.duration is not None:
                        detail += f" ({a.duration:.2f}s)"
                    lines.append(detail)
                lines.append("")

        return "\n".join(lines)

    def to_json(self) -> str:
        """Return a JSON-formatted string of the sync report."""
        categories = {
            "created": self.created,
            "updated": self.updated,
            "skipped_unchanged": self.skipped_unchanged,
            "skipped_filtered": self.skipped_filtered,
            "conflicted": self.conflicted,
            "removed": self.removed,
            "failed": self.failed,
        }
        data: dict = {
            "counts": {k: len(v) for k, v in categories.items()},
            "total": sum(len(v) for v in categories.values()),
            "has_failures": self.has_failures,
            "actions": {
                k: [asdict(a) for a in v]
                for k, v in categories.items()
                if v
            },
        }
        return json.dumps(data, indent=2)


@dataclass
class SyncMetrics:
    """Per-sync metrics for structured reporting."""

    total_articles: int = 0
    created_count: int = 0
    updated_count: int = 0
    skipped_unchanged_count: int = 0
    skipped_filtered_count: int = 0
    conflicted_count: int = 0
    removed_count: int = 0
    failed_count: int = 0
    total_duration: float = 0.0
    avg_article_time: float = 0.0

    @classmethod
    def from_report(cls, report: SyncReport, total_duration: float) -> SyncMetrics:
        """Build metrics from a completed SyncReport."""
        total = (
            len(report.created) + len(report.updated)
            + len(report.skipped_unchanged) + len(report.skipped_filtered)
            + len(report.conflicted) + len(report.removed)
            + len(report.failed)
        )
        avg = total_duration / total if total > 0 else 0.0
        return cls(
            total_articles=total,
            created_count=len(report.created),
            updated_count=len(report.updated),
            skipped_unchanged_count=len(report.skipped_unchanged),
            skipped_filtered_count=len(report.skipped_filtered),
            conflicted_count=len(report.conflicted),
            removed_count=len(report.removed),
            failed_count=len(report.failed),
            total_duration=round(total_duration, 3),
            avg_article_time=round(avg, 3),
        )
