"""Wiki-SharePoint Sync — config loading and SyncEngine orchestrator.

This module provides config loading utilities and the SyncEngine class
that coordinates the full sync pipeline: discover → filter → hash →
conflict-check → convert → upload → manifest update.
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from conflict import ConflictResolver
from converter import MarkdownConverter
from filters import AudienceFilter, StatusFilter
from frontmatter_io import FrontMatterParser
from manifest import SyncManifest
from models import (
    ArticleAction,
    ConfigError,
    ConversionError,
    FrontMatterError,
    GraphAPIError,
    SyncMetrics,
    SyncReport,
)
from sp_client import SharePointClient

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_PATH = "~/shared/tools/sharepoint-sync/config.yaml"

REQUIRED_FIELDS: dict[str, list[str]] = {
    "sharepoint": ["output_path"],
    "sync": ["mode"],
}

_ENV_VAR_RE = re.compile(r"\$\{([^}]+)\}")


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------


def _resolve_env_vars(value: Any) -> Any:
    """Recursively resolve ``${ENV_VAR}`` references in string values.

    Non-string values (ints, lists, bools, etc.) are returned unchanged.
    Nested dicts and lists are walked recursively.
    """
    if isinstance(value, str):
        def _replacer(match: re.Match) -> str:
            var_name = match.group(1)
            env_val = os.environ.get(var_name)
            if env_val is None:
                return match.group(0)  # leave unresolved if env var missing
            return env_val
        return _ENV_VAR_RE.sub(_replacer, value)
    if isinstance(value, dict):
        return {k: _resolve_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env_vars(item) for item in value]
    return value


def _validate_required_fields(config: dict[str, Any]) -> None:
    """Raise ``ConfigError`` listing every missing required field."""
    missing: list[str] = []
    for section, fields in REQUIRED_FIELDS.items():
        section_data = config.get(section)
        if not isinstance(section_data, dict):
            missing.extend(f"{section}.{f}" for f in fields)
            continue
        for field in fields:
            if field not in section_data or section_data[field] is None:
                missing.append(f"{section}.{field}")
    if missing:
        raise ConfigError(
            f"Missing required config fields: {', '.join(missing)}"
        )


def _apply_overrides(
    config: dict[str, Any], overrides: dict[str, Any]
) -> dict[str, Any]:
    """Merge *overrides* into *config* (shallow per-section merge).

    Override keys use dot notation (``"sync.mode"``) or flat section dicts.
    """
    for key, value in overrides.items():
        if "." in key:
            section, field = key.split(".", 1)
            config.setdefault(section, {})[field] = value
        elif isinstance(value, dict) and isinstance(config.get(key), dict):
            config[key].update(value)
        else:
            config[key] = value
    return config


def load_config(
    config_path: str | None = None,
    config_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Load, resolve, validate, and return the sync configuration.

    Parameters
    ----------
    config_path:
        Path to the YAML config file.  Defaults to
        ``~/shared/tools/sharepoint-sync/config.yaml``.
    config_overrides:
        Optional dict of CLI argument overrides.  Keys may use dot
        notation (e.g. ``"sync.mode": "site"``) or be section dicts.

    Returns
    -------
    dict
        Fully resolved and validated configuration dictionary.

    Raises
    ------
    ConfigError
        If the file is missing, contains invalid YAML, or is missing
        required fields.
    """
    path = Path(os.path.expanduser(config_path or DEFAULT_CONFIG_PATH))

    # --- Read file ---
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"Cannot read config file {path}: {exc}") from exc

    # --- Parse YAML ---
    try:
        config = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(config, dict):
        raise ConfigError(f"Config file {path} must contain a YAML mapping")

    # --- Resolve env vars ---
    config = _resolve_env_vars(config)

    # --- Apply CLI overrides (after env resolution so overrides win) ---
    if config_overrides:
        config = _apply_overrides(config, config_overrides)

    # --- Validate ---
    _validate_required_fields(config)

    return config


# ---------------------------------------------------------------------------
# SyncEngine — orchestrator
# ---------------------------------------------------------------------------


class SyncEngine:
    """Orchestrate the full wiki-to-SharePoint sync pipeline.

    Usage::

        engine = SyncEngine(config_path="path/to/config.yaml")
        report = engine.sync(mode="both", dry_run=True)
        print(report.summary())
    """

    def __init__(
        self,
        config_path: str | None = None,
        config_overrides: dict[str, Any] | None = None,
    ) -> None:
        self.config = load_config(config_path, config_overrides)

        sp_cfg = self.config["sharepoint"]
        sync_cfg = self.config.get("sync", {})

        # Components
        self.audience_filter = AudienceFilter()
        self.status_filter = StatusFilter(
            eligible_statuses=sync_cfg.get("eligible_statuses"),
        )
        self.parser = FrontMatterParser()
        self.manifest = SyncManifest(
            manifest_path=sync_cfg.get(
                "manifest_path",
                "~/shared/tools/sharepoint-sync/.sync-manifest.json",
            ),
        )
        self.converter = MarkdownConverter()
        self.sp_client = SharePointClient(
            output_path=sp_cfg.get("output_path", "~/shared/tools/sharepoint-sync/output"),
        )
        self.conflict_resolver = ConflictResolver()

        # Paths
        self.articles_path = Path(
            os.path.expanduser(sync_cfg.get("articles_path", "~/shared/artifacts/"))
        )

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def sync(
        self,
        mode: str | None = None,
        file_path: str | None = None,
        force: bool = False,
        dry_run: bool = False,
        json_output: bool = False,
    ) -> SyncReport:
        """Run the sync pipeline and return a :class:`SyncReport`.

        Parameters
        ----------
        mode:
            ``"site"``, ``"directory"``, or ``"both"``.  Falls back to
            the value in config.
        file_path:
            Optional single article path.  When provided only that file
            is synced.
        force:
            Overwrite SharePoint content even when a conflict is detected.
        dry_run:
            Execute the full pipeline but skip all SharePoint writes and
            manifest updates.
        json_output:
            When True the caller can use ``report.to_json()`` for
            structured output.
        """
        sync_start = time.monotonic()
        effective_mode = mode or self.config.get("sync", {}).get("mode", "both")
        report = SyncReport()

        modes = (
            ["site", "directory"] if effective_mode == "both" else [effective_mode]
        )

        articles = self._discover_articles(file_path)
        eligible_paths: dict[str, set[str]] = {m: set() for m in modes}

        for m in modes:
            for article_path in articles:
                action = self._process_article(article_path, m, force, dry_run)
                self._categorise(report, action)
                if action.action not in ("skipped_filtered", "failed"):
                    eligible_paths[m].add(str(article_path))

            orphan_actions = self._handle_orphans(m, eligible_paths[m], dry_run)
            for oa in orphan_actions:
                self._categorise(report, oa)

        if not dry_run:
            self.manifest.save()

        sync_duration = time.monotonic() - sync_start
        self._metrics = SyncMetrics.from_report(report, sync_duration)

        if json_output:
            logger.info(report.to_json())

        return report

    # ------------------------------------------------------------------ #
    # Article discovery
    # ------------------------------------------------------------------ #

    def _discover_articles(self, file_path: str | None = None) -> list[Path]:
        """Return article paths to process.

        If *file_path* is given, return ``[Path(file_path)]``.
        Otherwise walk all top-level subdirectories under
        ``articles_path``, ignoring hidden dirs and non-directory
        entries at the top level.
        """
        if file_path:
            return [Path(os.path.expanduser(file_path))]

        articles: list[Path] = []
        if not self.articles_path.is_dir():
            logger.warning("Articles path does not exist: %s", self.articles_path)
            return articles

        for entry in sorted(self.articles_path.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name.startswith("."):
                continue
            for md_file in sorted(entry.rglob("*.md")):
                articles.append(md_file)

        return articles

    # ------------------------------------------------------------------ #
    # Per-article pipeline
    # ------------------------------------------------------------------ #

    def _process_article(
        self,
        path: Path,
        mode: str,
        force: bool,
        dry_run: bool,
    ) -> ArticleAction:
        """Run the full pipeline for a single article."""
        t0 = time.monotonic()
        str_path = str(path)
        dry_prefix = "[DRY RUN] " if dry_run else ""

        try:
            # 1. Parse front-matter
            metadata, body = self.parser.parse(str_path)

            # 2. Audience filter
            aud_ok, aud_reason = self.audience_filter.is_eligible(metadata)
            if not aud_ok:
                return ArticleAction(
                    file_path=str_path,
                    action=f"{dry_prefix}skipped_filtered",
                    mode=mode,
                    error=aud_reason,
                    duration=time.monotonic() - t0,
                )

            # 3. Status filter
            stat_ok, stat_reason = self.status_filter.is_eligible(metadata)
            if not stat_ok:
                return ArticleAction(
                    file_path=str_path,
                    action=f"{dry_prefix}skipped_filtered",
                    mode=mode,
                    error=stat_reason,
                    duration=time.monotonic() - t0,
                )

            # 4. SHA-256 hash of full file content
            content_hash = self._hash_file(path)

            # 5. Check manifest
            entry = self.manifest.get_entry(str_path, mode)

            # 6. Hash match → skip
            if entry and entry["content_hash"] == content_hash:
                return ArticleAction(
                    file_path=str_path,
                    action=f"{dry_prefix}skipped_unchanged",
                    mode=mode,
                    sp_url=entry.get("sp_url"),
                    duration=time.monotonic() - t0,
                )

            # 7. Existing entry with different hash → conflict check
            if entry:
                sp_meta = self.sp_client.get_site_page_metadata(entry["sp_item_id"]) if mode == "site" else self.sp_client.get_file_metadata(entry["sp_item_id"])
                local_changed = content_hash != entry["content_hash"]
                conflict = self.conflict_resolver.check(entry, sp_meta, local_changed)

                # 8. Conflict and not force → skip
                if conflict.is_conflict and not force:
                    return ArticleAction(
                        file_path=str_path,
                        action=f"{dry_prefix}conflicted",
                        mode=mode,
                        sp_url=entry.get("sp_url"),
                        error=conflict.details,
                        duration=time.monotonic() - t0,
                    )

            # --- dry-run: stop before writes ---
            if dry_run:
                action_name = "updated" if entry else "created"
                return ArticleAction(
                    file_path=str_path,
                    action=f"{dry_prefix}{action_name}",
                    mode=mode,
                    sp_url=entry.get("sp_url") if entry else None,
                    duration=time.monotonic() - t0,
                )

            # 9. Convert content
            properties = self._build_metadata_fields(metadata)
            category = path.parent.name

            if mode == "site":
                html = self.converter.to_html(body)
                # 10. Upload
                if entry:
                    result = self.sp_client.update_site_page(
                        item_id=entry["sp_item_id"],
                        title=metadata.get("title", path.stem),
                        html=html,
                        properties=properties,
                    )
                else:
                    result = self.sp_client.create_site_page(
                        title=metadata.get("title", path.stem),
                        html=html,
                        category=category,
                        properties=properties,
                    )
            else:
                # directory mode
                docx_bytes = self.converter.to_docx(body, metadata)
                content_b64 = base64.b64encode(docx_bytes).decode("ascii")
                slug = metadata.get("slug", path.stem)
                filename = f"{slug}.docx"
                folder_path = f"{category}/"

                if entry:
                    result = self.sp_client.upload_file(
                        folder_path=folder_path,
                        filename=filename,
                        content_base64=content_b64,
                        properties=properties,
                    )
                else:
                    self.sp_client.ensure_folder(folder_path)
                    result = self.sp_client.upload_file(
                        folder_path=folder_path,
                        filename=filename,
                        content_base64=content_b64,
                        properties=properties,
                    )

            # 11. Update manifest
            now = datetime.now(timezone.utc).isoformat()
            if entry:
                self.manifest.update_entry(str_path, mode, content_hash, now)
                action_name = "updated"
            else:
                self.manifest.add_entry(
                    str_path, mode, content_hash,
                    result.get("item_id", ""),
                    result.get("url", ""),
                )
                action_name = "created"

            return ArticleAction(
                file_path=str_path,
                action=action_name,
                mode=mode,
                sp_url=result.get("url"),
                duration=time.monotonic() - t0,
            )

        except FrontMatterError as exc:
            logger.error("Front-matter error for %s: %s", str_path, exc)
            return ArticleAction(
                file_path=str_path,
                action=f"{dry_prefix}failed",
                mode=mode,
                error=str(exc),
                duration=time.monotonic() - t0,
            )
        except ConversionError as exc:
            logger.error("Conversion error for %s: %s", str_path, exc)
            return ArticleAction(
                file_path=str_path,
                action=f"{dry_prefix}failed",
                mode=mode,
                error=str(exc),
                duration=time.monotonic() - t0,
            )
        except GraphAPIError as exc:
            logger.error("SharePoint API error for %s: %s", str_path, exc)
            return ArticleAction(
                file_path=str_path,
                action=f"{dry_prefix}failed",
                mode=mode,
                error=str(exc),
                duration=time.monotonic() - t0,
            )

    # ------------------------------------------------------------------ #
    # Orphan handling
    # ------------------------------------------------------------------ #

    def _handle_orphans(
        self,
        mode: str,
        eligible_paths: set[str],
        dry_run: bool,
    ) -> list[ArticleAction]:
        """Remove SP items for manifest entries with no eligible article."""
        actions: list[ArticleAction] = []
        dry_prefix = "[DRY RUN] " if dry_run else ""

        for entry in self.manifest.all_entries(mode=mode):
            if entry["file_path"] not in eligible_paths:
                t0 = time.monotonic()
                try:
                    if not dry_run:
                        if mode == "site":
                            self.sp_client.delete_site_page(entry["sp_item_id"])
                        else:
                            self.sp_client.delete_file(entry["sp_item_id"])
                        self.manifest.remove_entry(entry["file_path"], mode)

                    actions.append(ArticleAction(
                        file_path=entry["file_path"],
                        action=f"{dry_prefix}removed",
                        mode=mode,
                        sp_url=entry.get("sp_url"),
                        duration=time.monotonic() - t0,
                    ))
                except GraphAPIError as exc:
                    logger.error(
                        "Failed to remove orphan %s [%s]: %s",
                        entry["file_path"], mode, exc,
                    )
                    actions.append(ArticleAction(
                        file_path=entry["file_path"],
                        action=f"{dry_prefix}failed",
                        mode=mode,
                        error=str(exc),
                        duration=time.monotonic() - t0,
                    ))

        return actions

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_metadata_fields(metadata: dict) -> dict:
        """Map front-matter fields to SharePoint properties."""
        return {
            "title": metadata.get("title", ""),
            "status": metadata.get("status", ""),
            "owner": metadata.get("owner", ""),
            "updated": metadata.get("updated", ""),
            "level": str(metadata.get("level", "")),
            "tags": metadata.get("tags", []),
        }

    @staticmethod
    def _hash_file(path: Path) -> str:
        """Return ``sha256:<hex>`` digest of the full file content."""
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return f"sha256:{h.hexdigest()}"

    @staticmethod
    def _categorise(report: SyncReport, action: ArticleAction) -> None:
        """Append *action* to the correct category list on *report*."""
        # Strip dry-run prefix for categorisation
        raw = action.action.replace("[DRY RUN] ", "")
        bucket = {
            "created": report.created,
            "updated": report.updated,
            "skipped_unchanged": report.skipped_unchanged,
            "skipped_filtered": report.skipped_filtered,
            "conflicted": report.conflicted,
            "removed": report.removed,
            "failed": report.failed,
        }.get(raw, report.failed)
        bucket.append(action)
