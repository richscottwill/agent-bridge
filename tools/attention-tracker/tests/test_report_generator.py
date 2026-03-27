"""Unit tests for the Report Generator.

Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

import pytest

from paid_search_audit.kpi_comparator import KPIFinding
from paid_search_audit.models import (
    ActionItem,
    AnomalyFinding,
    AuditReport,
    AuditSummary,
    MarketSection,
    MultiHorizonProjection,
    PacingResult,
    PeriodProjection,
    WoWComparison,
)
from paid_search_audit.report_generator import ReportGenerator


# ------------------------------------------------------------------ #
# Fixtures / helpers
# ------------------------------------------------------------------ #

def _make_period(
    label: str = "March 2026",
    period_type: str = "MONTHLY",
    days_elapsed: int = 15,
    days_remaining: int = 16,
    actual_spend: Decimal = Decimal("5000"),
    projected_spend: Decimal = Decimal("10000"),
    target_spend: Decimal = Decimal("9000"),
    actual_regs: int = 50,
    projected_regs: int = 100,
    target_regs: int = 90,
) -> PeriodProjection:
    days_total = days_elapsed + days_remaining
    spend_vs = (
        ((projected_spend - target_spend) / target_spend) * 100
        if target_spend
        else Decimal("0")
    )
    regs_vs = (
        ((Decimal(projected_regs) - Decimal(target_regs)) / Decimal(target_regs)) * 100
        if target_regs
        else Decimal("0")
    )
    return PeriodProjection(
        period_label=label,
        period_type=period_type,
        days_elapsed=days_elapsed,
        days_remaining=days_remaining,
        days_total=days_total,
        actual_spend=actual_spend,
        projected_spend=projected_spend,
        target_spend=target_spend,
        spend_vs_op2_pct=spend_vs,
        spend_pacing_pct=Decimal("100"),
        actual_regs=actual_regs,
        projected_regs=projected_regs,
        target_regs=target_regs,
        regs_vs_op2_pct=regs_vs,
        regs_pacing_pct=Decimal("100"),
        daily_spend_run_rate=Decimal("300"),
        daily_regs_run_rate=Decimal("3"),
        status="ON_TRACK",
    )


def _make_pacing(
    market: str = "AU",
    status: str = "ON_TRACK",
    pacing_pct: Decimal = Decimal("95"),
) -> PacingResult:
    return PacingResult(
        market=market,
        period="March 2026",
        budget_target=Decimal("10000"),
        actual_spend=Decimal("5000"),
        pacing_pct=pacing_pct,
        projected_eom_spend=Decimal("9500"),
        projected_variance_pct=Decimal("-5"),
        status=status,
        days_elapsed=15,
        days_remaining=16,
    )


def _make_anomaly(
    market: str = "AU",
    severity: str = "WARNING",
    metric: str = "CPA",
) -> AnomalyFinding:
    return AnomalyFinding(
        market=market,
        metric_name=metric,
        current_value=Decimal("50"),
        baseline_value=Decimal("30"),
        deviation_pct=Decimal("66.67"),
        z_score=Decimal("2.5"),
        direction="UP",
        severity=severity,
        campaign_scope="All",
        context=f"{market} {metric} is 66.67% above baseline",
    )


def _make_kpi(
    market: str = "AU",
    metric: str = "registrations",
    status: str = "ON_TRACK",
) -> KPIFinding:
    return KPIFinding(
        market=market,
        metric_name=metric,
        actual=Decimal("45"),
        target=Decimal("100"),
        prorated_target=Decimal("50"),
        pacing_pct=Decimal("90"),
        status=status,
        is_kingpin_goal=False,
    )


def _make_wow() -> WoWComparison:
    return WoWComparison(
        spend_change_pct=Decimal("10"),
        clicks_change_pct=Decimal("-5"),
        conversions_change_pct=Decimal("15"),
        cpa_change_pct=Decimal("-3"),
        ctr_change_pct=Decimal("2"),
    )


def _make_action_item(
    priority: int = 1,
    market: str = "AU",
    urgency: str = "TODAY",
    category: str = "BUDGET",
) -> ActionItem:
    return ActionItem(
        priority=priority,
        market=market,
        category=category,
        description=f"{market} spend is underpacing",
        suggested_action=f"Review {market} budget allocation",
        urgency=urgency,
    )


def _make_report(
    markets: list[str] | None = None,
    action_items: list[ActionItem] | None = None,
    anomalies: list[AnomalyFinding] | None = None,
) -> AuditReport:
    if markets is None:
        markets = ["AU", "MX"]

    sections = []
    for m in markets:
        sections.append(
            MarketSection(
                market=m,
                pacing=_make_pacing(market=m),
                projections=MultiHorizonProjection(
                    market=m,
                    audit_date=date(2026, 3, 15),
                    monthly=_make_period("March 2026", "MONTHLY"),
                    quarterly=_make_period("Q3 FY26", "QUARTERLY"),
                    yearly=_make_period("FY26", "YEARLY"),
                ),
                anomalies=anomalies or [_make_anomaly(market=m)],
                kpi_status=[_make_kpi(market=m)],
                wow_changes=_make_wow(),
            )
        )

    return AuditReport(
        date=date(2026, 3, 15),
        generated_at=datetime(2026, 3, 15, 8, 0, 0, tzinfo=timezone.utc),
        markets_audited=markets,
        summary=AuditSummary(
            total_spend_usd=Decimal("10000"),
            total_registrations=100,
            blended_cpa_usd=Decimal("100"),
            critical_findings_count=1,
            warning_findings_count=2,
            markets_on_track=1,
            markets_at_risk=1,
        ),
        market_sections=sections,
        action_items=action_items or [_make_action_item()],
        data_quality_notes=["Test note"],
    )


# ================================================================== #
# Markdown generation tests (Req 10.1)
# ================================================================== #

class TestGenerateMarkdown:
    """Req 10.1: markdown report grouped by market."""

    def test_contains_title_with_date(self) -> None:
        gen = ReportGenerator()
        report = _make_report()
        md = gen.generate_markdown(report, date(2026, 3, 15))
        assert "# Paid Search Daily Audit — 2026-03-15" in md

    def test_contains_summary_section(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "## Summary" in md
        assert "Total Spend (USD)" in md
        assert "Total Registrations" in md

    def test_contains_action_items_section(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "## Action Items" in md
        assert "**TODAY**" in md

    def test_contains_market_sections(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "## AU" in md
        assert "## MX" in md

    def test_contains_pacing_section(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "### Budget Pacing" in md
        assert "ON_TRACK" in md

    def test_contains_anomalies_section(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "### Anomalies" in md
        assert "CPA" in md

    def test_contains_kpi_status_section(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "### KPI Status" in md
        assert "registrations" in md

    def test_contains_wow_section(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "### Week-over-Week Changes" in md
        assert "Spend" in md

    def test_contains_data_quality_notes(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "## Data Quality Notes" in md
        assert "Test note" in md

    def test_empty_report_no_crash(self) -> None:
        gen = ReportGenerator()
        report = AuditReport(
            date=date(2026, 3, 15),
            generated_at=datetime.now(timezone.utc),
        )
        md = gen.generate_markdown(report, date(2026, 3, 15))
        assert "# Paid Search Daily Audit" in md


# ================================================================== #
# WBR callout format tests (Req 10.4)
# ================================================================== #

class TestWBRCalloutFormat:
    """Req 10.4: WBR callout style projections."""

    def test_monthly_callout_format(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        # Should contain the WBR callout pattern
        assert "March 2026" in md
        assert "is projected to end at" in md
        assert "spend and" in md
        assert "registrations" in md
        assert "vs. OP2:" in md

    def test_all_three_horizons_present(self) -> None:
        gen = ReportGenerator()
        md = gen.generate_markdown(_make_report(), date(2026, 3, 15))
        assert "March 2026" in md
        assert "Q3 FY26" in md
        assert "FY26" in md

    def test_callout_includes_spend_and_regs_pct(self) -> None:
        gen = ReportGenerator()
        period = _make_period(
            projected_spend=Decimal("10000"),
            target_spend=Decimal("9000"),
            projected_regs=100,
            target_regs=90,
        )
        callout = gen._format_wbr_callout(period)
        assert "% spend" in callout
        assert "% registrations" in callout

    def test_callout_signed_percentages(self) -> None:
        gen = ReportGenerator()
        # Positive variance
        period = _make_period(
            projected_spend=Decimal("10000"),
            target_spend=Decimal("9000"),
        )
        callout = gen._format_wbr_callout(period)
        assert "+" in callout  # Positive variance should have +


# ================================================================== #
# Action item constraints (Req 10.5, 10.6, 10.7)
# ================================================================== #

class TestActionItemsInMarkdown:
    """Req 10.5: max 10 action items. Req 10.6: urgency. Req 10.7: suggested action."""

    def test_max_10_action_items_in_markdown(self) -> None:
        gen = ReportGenerator()
        items = [_make_action_item(priority=i + 1) for i in range(15)]
        report = _make_report(action_items=items)
        md = gen.generate_markdown(report, date(2026, 3, 15))
        # Count numbered items in action items section
        action_lines = [
            line for line in md.split("\n")
            if line.strip() and line[0].isdigit() and "." in line[:4]
        ]
        assert len(action_lines) <= 10

    def test_urgency_displayed(self) -> None:
        gen = ReportGenerator()
        items = [
            _make_action_item(priority=1, urgency="TODAY"),
            _make_action_item(priority=2, urgency="THIS_WEEK"),
            _make_action_item(priority=3, urgency="MONITOR"),
        ]
        report = _make_report(action_items=items)
        md = gen.generate_markdown(report, date(2026, 3, 15))
        assert "TODAY" in md
        assert "THIS_WEEK" in md
        assert "MONITOR" in md

    def test_suggested_action_included(self) -> None:
        gen = ReportGenerator()
        report = _make_report()
        md = gen.generate_markdown(report, date(2026, 3, 15))
        assert "Review AU budget allocation" in md


# ================================================================== #
# Email brief tests (Req 10.2)
# ================================================================== #

class TestGenerateEmailBrief:
    """Req 10.2: scannable email brief for morning routine."""

    def test_contains_title(self) -> None:
        gen = ReportGenerator()
        brief = gen.generate_email_brief(_make_report(), date(2026, 3, 15))
        assert "PAID SEARCH DAILY AUDIT" in brief
        assert "2026-03-15" in brief

    def test_contains_summary(self) -> None:
        gen = ReportGenerator()
        brief = gen.generate_email_brief(_make_report(), date(2026, 3, 15))
        assert "SUMMARY" in brief
        assert "Spend:" in brief
        assert "Registrations:" in brief

    def test_critical_items_highlighted(self) -> None:
        gen = ReportGenerator()
        items = [_make_action_item(urgency="TODAY")]
        report = _make_report(action_items=items)
        brief = gen.generate_email_brief(report, date(2026, 3, 15))
        assert "ACTION REQUIRED TODAY" in brief

    def test_market_sections_present(self) -> None:
        gen = ReportGenerator()
        brief = gen.generate_email_brief(_make_report(), date(2026, 3, 15))
        assert "AU" in brief
        assert "MX" in brief

    def test_pacing_in_market_brief(self) -> None:
        gen = ReportGenerator()
        brief = gen.generate_email_brief(_make_report(), date(2026, 3, 15))
        assert "Pacing:" in brief
        assert "ON_TRACK" in brief

    def test_projections_in_market_brief(self) -> None:
        gen = ReportGenerator()
        brief = gen.generate_email_brief(_make_report(), date(2026, 3, 15))
        assert "March 2026:" in brief
        assert "vs OP2:" in brief

    def test_other_items_section(self) -> None:
        gen = ReportGenerator()
        items = [
            _make_action_item(priority=1, urgency="TODAY"),
            _make_action_item(priority=2, urgency="THIS_WEEK"),
        ]
        report = _make_report(action_items=items)
        brief = gen.generate_email_brief(report, date(2026, 3, 15))
        assert "OTHER ITEMS" in brief

    def test_empty_report_no_crash(self) -> None:
        gen = ReportGenerator()
        report = AuditReport(
            date=date(2026, 3, 15),
            generated_at=datetime.now(timezone.utc),
        )
        brief = gen.generate_email_brief(report, date(2026, 3, 15))
        assert "PAID SEARCH DAILY AUDIT" in brief


# ================================================================== #
# JSON generation tests (Req 10.3)
# ================================================================== #

class TestGenerateJSON:
    """Req 10.3: structured JSON for programmatic consumption."""

    def test_top_level_keys(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        assert "date" in result
        assert "generated_at" in result
        assert "markets_audited" in result
        assert "summary" in result
        assert "market_sections" in result
        assert "action_items" in result
        assert "data_quality_notes" in result

    def test_date_is_iso_string(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        assert result["date"] == "2026-03-15"

    def test_markets_audited_list(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        assert result["markets_audited"] == ["AU", "MX"]

    def test_summary_structure(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        s = result["summary"]
        assert "total_spend_usd" in s
        assert "total_registrations" in s
        assert "blended_cpa_usd" in s
        assert "critical_findings_count" in s
        assert "warning_findings_count" in s

    def test_market_section_structure(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        section = result["market_sections"][0]
        assert "market" in section
        assert "pacing" in section
        assert "projections" in section
        assert "anomalies" in section
        assert "kpi_status" in section
        assert "wow_changes" in section

    def test_pacing_in_json(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        pacing = result["market_sections"][0]["pacing"]
        assert pacing["status"] == "ON_TRACK"
        assert pacing["market"] == "AU"

    def test_projections_in_json(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        proj = result["market_sections"][0]["projections"]
        assert proj["monthly"] is not None
        assert proj["quarterly"] is not None
        assert proj["yearly"] is not None
        assert proj["monthly"]["period_label"] == "March 2026"

    def test_anomalies_in_json(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        anomalies = result["market_sections"][0]["anomalies"]
        assert len(anomalies) >= 1
        assert anomalies[0]["metric_name"] == "CPA"
        assert anomalies[0]["severity"] == "WARNING"

    def test_action_items_in_json(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        items = result["action_items"]
        assert len(items) >= 1
        item = items[0]
        assert "priority" in item
        assert "market" in item
        assert "category" in item
        assert "description" in item
        assert "suggested_action" in item
        assert "urgency" in item

    def test_wow_in_json(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        wow = result["market_sections"][0]["wow_changes"]
        assert "spend_change_pct" in wow
        assert "clicks_change_pct" in wow

    def test_data_quality_notes_in_json(self) -> None:
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        assert result["data_quality_notes"] == ["Test note"]

    def test_none_summary_returns_none(self) -> None:
        gen = ReportGenerator()
        report = AuditReport(
            date=date(2026, 3, 15),
            generated_at=datetime.now(timezone.utc),
        )
        result = gen.generate_json(report, date(2026, 3, 15))
        assert result["summary"] is None

    def test_json_serializable(self) -> None:
        """Ensure the dict can be serialized to JSON string."""
        import json
        gen = ReportGenerator()
        result = gen.generate_json(_make_report(), date(2026, 3, 15))
        json_str = json.dumps(result)
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["date"] == "2026-03-15"


# ================================================================== #
# Edge cases
# ================================================================== #

class TestEdgeCases:
    """Edge cases for report generation."""

    def test_none_wow_changes(self) -> None:
        gen = ReportGenerator()
        report = _make_report()
        report.market_sections[0].wow_changes = WoWComparison()
        md = gen.generate_markdown(report, date(2026, 3, 15))
        assert "N/A" in md

    def test_none_projections(self) -> None:
        gen = ReportGenerator()
        report = _make_report()
        report.market_sections[0].projections = None
        md = gen.generate_markdown(report, date(2026, 3, 15))
        # Should not crash, projections section just absent
        assert "## AU" in md

    def test_none_pacing(self) -> None:
        gen = ReportGenerator()
        report = _make_report()
        report.market_sections[0].pacing = None
        md = gen.generate_markdown(report, date(2026, 3, 15))
        assert "## AU" in md

    def test_empty_anomalies(self) -> None:
        gen = ReportGenerator()
        report = _make_report(anomalies=[])
        md = gen.generate_markdown(report, date(2026, 3, 15))
        # No anomalies section when empty
        assert "## AU" in md

    def test_blended_cpa_none(self) -> None:
        gen = ReportGenerator()
        report = _make_report()
        report.summary.blended_cpa_usd = None
        md = gen.generate_markdown(report, date(2026, 3, 15))
        assert "N/A" in md
