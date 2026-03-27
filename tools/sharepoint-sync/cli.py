"""CLI entry point for Wiki-SharePoint Sync.

Usage::

    python3 cli.py --mode site --dry-run
    python3 cli.py --file ~/shared/artifacts/testing/article.md --force
    python3 cli.py --json --config /path/to/config.yaml
"""

from __future__ import annotations

import argparse
import sys

from models import ConfigError
from sync import SyncEngine


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sharepoint-sync",
        description="Sync wiki articles from ~/shared/artifacts/ to SharePoint.",
    )
    parser.add_argument(
        "--mode",
        choices=["site", "directory", "both"],
        default=None,
        help="Upload mode: site pages, document library, or both (default: from config)",
    )
    parser.add_argument(
        "--file",
        default=None,
        metavar="PATH",
        help="Sync a single article by file path instead of all eligible articles",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Overwrite SharePoint content even when a conflict is detected",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Run full pipeline but skip all SharePoint write operations",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output sync report as JSON instead of human-readable text",
    )
    parser.add_argument(
        "--config",
        default=None,
        metavar="PATH",
        help="Path to config YAML file (default: ~/shared/tools/sharepoint-sync/config.yaml)",
    )
    parser.add_argument(
        "--articles-path",
        default=None,
        metavar="PATH",
        help="Path to articles directory (overrides config; e.g. ./artifacts/)",
    )
    parser.add_argument(
        "--output-path",
        default=None,
        metavar="PATH",
        help="Path to output directory (overrides config; e.g. ./output/)",
    )
    return parser


def _build_config_overrides(args: argparse.Namespace) -> dict[str, str]:
    """Build config_overrides dict from explicitly provided CLI args."""
    overrides: dict[str, str] = {}
    if args.mode is not None:
        overrides["sync.mode"] = args.mode
    if args.articles_path is not None:
        overrides["sync.articles_path"] = args.articles_path
    if args.output_path is not None:
        overrides["sharepoint.output_path"] = args.output_path
    return overrides


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, run sync, print report, return exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    config_overrides = _build_config_overrides(args)

    try:
        engine = SyncEngine(
            config_path=args.config,
            config_overrides=config_overrides or None,
        )
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    try:
        report = engine.sync(
            mode=args.mode,
            file_path=args.file,
            force=args.force,
            dry_run=args.dry_run,
            json_output=args.json,
        )
    except Exception as exc:
        print(f"Sync failed: {exc}", file=sys.stderr)
        return 1

    # Print report
    if args.json:
        print(report.to_json())
    else:
        print(report.summary())

    return 1 if report.has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
