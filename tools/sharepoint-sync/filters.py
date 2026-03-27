"""Audience and status filters for Wiki-SharePoint Sync."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class AudienceFilter:
    """Filter articles by audience field — only 'amazon-internal' is eligible."""

    ELIGIBLE = {"amazon-internal"}

    def is_eligible(self, metadata: dict) -> tuple[bool, str]:
        """Return ``(eligible, reason)`` based on the audience value.

        Missing audience field returns ``(False, ...)`` with a logged warning.
        """
        audience = metadata.get("audience")

        if audience is None:
            msg = f"Missing audience field — excluding article"
            logger.warning(msg)
            return False, msg

        if audience in self.ELIGIBLE:
            return True, f"Audience '{audience}' is eligible"

        return False, f"Audience '{audience}' is not eligible for SharePoint sync"


class StatusFilter:
    """Filter articles by status field — configurable eligible statuses."""

    DEFAULT_STATUSES = ["REVIEW", "FINAL"]

    def __init__(self, eligible_statuses: list[str] | None = None):
        raw = eligible_statuses if eligible_statuses is not None else self.DEFAULT_STATUSES
        self._eligible = {s.upper() for s in raw}

    def is_eligible(self, metadata: dict) -> tuple[bool, str]:
        """Return ``(eligible, reason)`` via case-insensitive membership check."""
        status = metadata.get("status")

        if status is None:
            return False, "Missing status field — excluding article"

        if status.upper() in self._eligible:
            return True, f"Status '{status}' is eligible"

        return False, f"Status '{status}' is not in eligible statuses: {sorted(self._eligible)}"
